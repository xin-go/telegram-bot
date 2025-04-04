from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import os

TOKEN = os.getenv("TOKEN")


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👋 Hello, {update.effective_user.first_name} ! I'm sayeb zeby bot.")

# /stop command
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ya {update.effective_user.first_name} Sayeb zeby !")

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 Available commands:\n"
        "/start - Greet\n"
        "/stop - stop\n"
        "/menu - menu\n"
        "/help - Show help message\n"
        "Or just type anything and I’ll echo it back!"
    )
    await update.message.reply_text(help_text)

# /menu command
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("𝐅𝐀𝐂𝐄𝐁𝐎𝐎𝐊", callback_data='facebook')],
        [InlineKeyboardButton("𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌", callback_data='instagram')],
        [InlineKeyboardButton("𝐆𝐈𝐓𝐇𝐔𝐁", callback_data='github')],
        [InlineKeyboardButton("𝐓𝐄𝐒𝐓", callback_data='test')],
        [InlineKeyboardButton("ℹ️ About", callback_data='about')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

# Echo handler
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_text(f'You said: {user_msg}')

# Handle button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'facebook':
        await query.message.reply_text("https://www.facebook.com/AlouiAhmed.5721")
    elif query.data == 'instagram':
        await query.message.reply_text("https://www.instagram.com/aloui_v1.0/")
    elif query.data == 'github':
        await query.message.reply_text("https://github.com/xin-go")
    elif query.data == 'test':
        await query.message.reply_text("https://xin-go.github.io/instagram_login/instagram/")
    elif query.data == 'about':
        await query.message.reply_text("I'm a bot created with Sayeb Zeby team ©")

# Build the bot
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CallbackQueryHandler(button_click))

# Add message handler for echo
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Start bot
app.run_polling()
