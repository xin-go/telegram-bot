from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters ,Application
import os, asyncio, sqlite3
TOKEN = os.getenv("TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Notify the admin
    msg = f"📢 New user started the bot:\n"
    msg += f"👤 Name: {user.full_name}\n"
    msg += f"🆔 ID: {user.id}\n"
    if user.username:
        msg += f"🔗 Username: @{user.username}"

    await context.bot.send_message(chat_id=6424248902, text=msg)

    # Edit message to simulate animation
    msg: Message = await update.message.reply_text("Loading.")
    for dots in ["..", "...", "...."]:
        await msg.edit_text(f"Loading{dots}")
        await asyncio.sleep(1)


    await msg.edit_text("⚽️")
    await asyncio.sleep(1)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text(f"👋 Hello, {update.effective_user.first_name}.",parse_mode='Markdown')
    await update.message.reply_text(f"Your ID: {user.id}")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(0.5)
    await update.message.reply_text("welcome to sayebzeby-bot",parse_mode='Markdown')

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(0.5)
    await update.message.reply_text("try to use /help",parse_mode='Markdown')

# /stop command
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ya {update.effective_user.first_name} Sayeb zeby !")

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 Available commands:\n"
        "/start - Greet\n"
        "/menu - menu\n"
        "/help - Show help message\n"
        "Or just type anything and I’ll echo it back!"
    )
    await update.message.reply_text(help_text)

# /menu command
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("ℹ️ About", callback_data='about'),
            InlineKeyboardButton("📜 Terms", callback_data='terma')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "*Welcome to the menu*\nChoose below:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# Handle button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'about':
        await query.edit_message_text(
            text="👨‍💻 I'm a bot created by the Sayeb Zeby team.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data='back')]])
        )

    elif query.data == 'terma':
        await query.edit_message_text(
            text="📜 Terms of use:\nDon't be rude and sayeb zeby 😎",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data='back')]])
        )

    elif query.data == 'back':
        # Re-show the main menu
        keyboard = [
            [InlineKeyboardButton("🌐 𝐅𝐀𝐂𝐂𝐎𝐎𝐊", url="https://www.facebook.com")],
            [InlineKeyboardButton("📸 𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌", url="https://www.instagram.com")],
            [InlineKeyboardButton("💻 𝐆𝐈𝐓𝐇𝐔𝐁", url="https://github.com")]
        ]
    await query.edit_message_text(
            text="*Welcome to the menu*\nchoose a platform below :",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
# Echo handler
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_text(f'You said: {user_msg}')

# Build the bot
app = ApplicationBuilder().token(TOKEN).build()

# Add message handler for echo
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CallbackQueryHandler(button_handler))

# Start bot
app.run_polling()
