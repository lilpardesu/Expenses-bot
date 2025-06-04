import logging
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


TOKEN: Final = '7746997083:AAHOqvozGY-8uGGvIGmoL0o3RYKYP00Wtig'
BOT_USERNAME: Final = '@par_expenses_bot'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text('Hello! I am your bot. How can I assist you today?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message when the /help command is issued."""
    await update.message.reply_text('Here is a list of commands you can use:\n/start - Start the bot\n/help - Get help')

# Main function to start the bot
def main():
    """Start the bot."""
    # Replace 'YOUR_TOKEN_HERE' with your bot's API token
    application = ApplicationBuilder().token('7746997083:AAHOqvozGY-8uGGvIGmoL0o3RYKYP00Wtig').build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()