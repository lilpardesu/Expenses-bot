import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Configuration
BOT_TOKEN = '7746997083:AAHOqvozGY-8uGGvIGmoL0o3RYKYP00Wtig'
BOT_USERNAME = '@par_expenses_bot'  # Must include the @ symbol

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command"""
    await update.message.reply_text(
        "🤖 I'm your expenses bot! Mention me in a group with "
        f"{BOT_USERNAME} to interact with me."
    )

async def handle_group_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for group mentions and messages"""
    if not update.message or not update.message.text:
        return
    
    # Log the incoming message for debugging
    logger.info(
        f"Message in {update.message.chat.type} (ID: {update.message.chat.id}): "
        f"{update.message.text}"
    )
    
    # Check if the bot was mentioned (using Telegram entity or text matching)
    mentioned = False
    
    # Check for proper mention entities first
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type == "mention":
                mentioned_text = update.message.text[
                    entity.offset:entity.offset+entity.length
                ].lower()
                if mentioned_text == BOT_USERNAME.lower():
                    mentioned = True
                    break
    
    # Fallback to text matching if no entities found
    if not mentioned and BOT_USERNAME.lower() in update.message.text.lower():
        mentioned = True
    
    # Respond if mentioned
    if mentioned:
        await update.message.reply_text(
            "✅ I heard my name! Here's what I can do:\n"
            "- Track expenses with /add\n"
            "- View summaries with /report\n"
            "- Get help with /help"
        )

def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    
    # Handler for group messages (only triggers when privacy mode is disabled)
    application.add_handler(MessageHandler(
        filters.TEXT & (filters.ChatType.GROUPS) & ~filters.COMMAND,
        handle_group_mention
    ))
    
    # Handler for mentions (works even in privacy mode)
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Entity("mention"),
        handle_group_mention
    ))
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == '__main__':
    main()