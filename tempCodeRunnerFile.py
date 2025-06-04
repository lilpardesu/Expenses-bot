import logging
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters

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

async def handle_mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle when the bot is mentioned in a message."""
    # Check if the bot was mentioned
    if BOT_USERNAME.lower() in update.message.text.lower():
        await update.message.reply_text("Yes? You mentioned me! How can I help you?")
        
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages."""
    # You can add other message handling logic here
    pass

# Main function to start the bot
def main():
    """Start the bot."""
    application = ApplicationBuilder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(MessageHandler(filters.TEXT & filters.Entity("mention"), handle_mention))

    # Run the bot
    application.run_polling()
    print('polling...')

if __name__ == '__main__':
    main()