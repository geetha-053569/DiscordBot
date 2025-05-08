import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai  # Google Gemini API

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Set up Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True  # Required for commands to work

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    """Greets the user."""
    await ctx.send(f'Hello {ctx.author.mention}! I am your AI-powered bot. 🤖')

@bot.command()
async def ping(ctx):
    """Check bot latency."""
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def helpme(ctx):
    """Displays available commands."""
    help_text = """
    *🤖 Chatbot Commands:*
    - !hello → Get a friendly greeting.
    - !ping → Check bot latency.
    - !gemini <message> → Chat with Gemini AI.
    - !helpme → Show this help menu.
    """
    await ctx.send(help_text)

@bot.command()
async def gemini(ctx, *, message: str = None):
    """Chat with Google Gemini AI."""
    if not message:
        await ctx.send("❌ Please provide a message. Example: !gemini Hello!")
        return

    if not GEMINI_API_KEY:
        await ctx.send("❌ AI feature is disabled. Set up GEMINI_API_KEY in .env to enable it.")
        return
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Use an available model
        response = model.generate_content(message)
        reply = response.text

        if not reply:
            await ctx.send("🤖 Gemini AI could not generate a response.")
            return

        # Split long responses into chunks of 2000 characters
        for chunk in [reply[i:i+2000] for i in range(0, len(reply), 2000)]:
            await ctx.send(chunk)

    except Exception as e:
        await ctx.send("❌ Error fetching AI response.")
        print(f"Error: {e}")

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use !helpme to see available commands.")
    else:
        print(f"Error: {error}")

# Run the bot
bot.run(TOKEN)
