import logging
import sqlite3
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import time
import os
from dotenv import load_dotenv


# Configuration
load_dotenv()  # Load the .env file
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME = "@par_expenses_bot"
NAME1 = "@lilpardesu"  # Adds to balance
NAME2 = "@Marymirzaei"  # Subtracts from balance

# Database setup
DB_FILE = "balances.db"

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS balances (
        chat_id INTEGER PRIMARY KEY,
        balance REAL DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Database helper functions
def get_balance(chat_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM balances WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_balance(chat_id, amount):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO balances (chat_id, balance)
    VALUES (?, COALESCE((SELECT balance FROM balances WHERE chat_id = ?), 0) + ?)
    """, (chat_id, chat_id, amount))
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message with instructions"""
    await update.message.reply_text(
        "💰 Balance Tracker Bot\n\n"
        f"• Mention {NAME1} with amount to add\n"
        f"• Mention {NAME2} with amount to subtract\n\n"
        "Commands:\n"
        "/balance - Show current balance\n"
        "/reset - Reset balance to 0\n\n"
        "Example:\n"
        "• '100 {NAME1}' → Adds 100\n"
        "• '50 {NAME2}' → Subtracts 50"
    )

async def show_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current balance"""
    chat_id = update.message.chat.id
    balance = get_balance(chat_id)
    await update.message.reply_text(f"Current balance: {balance:.2f}")

async def reset_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset balance to zero"""
    chat_id = update.message.chat.id
    update_balance(chat_id, -get_balance(chat_id))
    await update.message.reply_text("♻️ Balance reset to 0")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process balance updates"""
    if not update.message or not update.message.text:
        return

    chat_id = update.message.chat.id
    text = update.message.text.lower()

    try:
        # Find the first number in message
        amount = next(
            (float(word) for word in text.split() 
            if word.replace('.', '', 1).isdigit())
        )

        # Determine action
        if NAME1.lower() in text:
            update_balance(chat_id, amount)
            action = f"➕ Added {amount:.2f} (via {NAME1})"
        elif NAME2.lower() in text:
            update_balance(chat_id, -amount)
            action = f"➖ Subtracted {amount:.2f} (via {NAME2})"
        else:
            return

        new_balance = get_balance(chat_id)
        await update.message.reply_text(
            f"{action}\n"
            f"New balance: {new_balance:.2f}"
        )

    except (StopIteration, ValueError):
        pass  # No valid number found

def create_application():
    """Create and configure bot application"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", show_balance))
    application.add_handler(CommandHandler("reset", reset_balance))
    
    # Message handler
    application.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS,
        handle_message
    ))
    
    return application


def run_bot():
    """Run with webhook for Render deployment"""
    init_db()
    logger.info("Initializing database...")

    app = create_application()
    logger.info("Bot started successfully")

    # Run webhook instead of polling
    port = int(os.environ.get("PORT", 10000))
    url = os.environ.get("RENDER_EXTERNAL_URL")
    if url is None:
        raise Exception("RENDER_EXTERNAL_URL not set")
    
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=f"{url}/{BOT_TOKEN}"
    )


if __name__ == "__main__":
    run_bot()