from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters ,Application
import os, asyncio, sqlite3

TOKEN = os.getenv("TOKEN")
user_ages = {}

# START FUNCTION
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Notify the admin
    msg = f"📢 New user started the bot:\n"
    msg += f"👤 Name: {user.full_name}\n"
    msg += f"🆔 ID: {user.id}\n"
    if user.username:
        msg += f"🔗 Username: @{user.username}"

    await context.bot.send_message(chat_id=6424248902, text=msg)

    # Simulate loading animation
    loading_msg: Message = await update.message.reply_text("Loading...")
    for dots in ["..", "...", "...."]:
        await loading_msg.edit_text(f"Loading{dots}")
        await asyncio.sleep(1)

    await loading_msg.edit_text("🔞")
    await asyncio.sleep(1)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text(f"👋 Hello, {user.first_name}.", parse_mode='Markdown')
    await update.message.reply_text(f"Your ID: {user.id}")

    await update.message.reply_text("HOW OLD ARE YOU?")
    return "AGE"

# AGE VALIDATION FUNCTION
async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age_text = update.message.text  # <-- You forgot this line

    if not age_text.isdigit():
        await update.message.reply_text("Please enter a valid number for your age.")
        return "AGE"

    age = int(age_text)
    context.user_data["age"] = age  # <-- Move this after validation

    # If age is out of realistic bounds
    if age <= 16 or age >= 50:
        await update.message.reply_text("Please enter a realistic age.")
        return "AGE"

    # If the user is under 18, restrict access
    if age < 18:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")      
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='wack')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Sorry, you must be 18 or older to use this bot.\nPlease come back when you're 18.", reply_markup=reply_markup)
    else:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        await asyncio.sleep(0.5)
        await update.message.reply_text("Welcome to Sayeb Zeby Bot!", parse_mode='Markdown')
        await asyncio.sleep(0.5)
        await update.message.reply_text("Try using /help", parse_mode='Markdown')

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
    age = update.effective_user.id

    # Check if the user is under 18
    age = context.user_data.get("age")
    if age is None or age < 18:
        await update.message.reply_text("Sorry, you must be 18 or older to use this menu.")
        return
    else :
        keyboard = [
        [InlineKeyboardButton("ℹ️ About", callback_data='about'),
         InlineKeyboardButton("📜 Terms", callback_data='terms')]
        ]
        await update.message.reply_text(
        "*Welcome to the menu*\nChoose below:",
        reply_markup = InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
        )


# Handle button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌐 𝐅𝐀𝐂𝐂𝐎𝐎𝐊", url="https://www.facebook.com/AlouiAhmed.5721")],
        [InlineKeyboardButton("📸 𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌", url="https://www.instagram.com/aloui_v1.0/")],
        [InlineKeyboardButton("💻 𝐆𝐈𝐓𝐇𝐔𝐁", url="https://github.com/xin-go")]
    ]
    
    query = update.callback_query
    await query.answer()

    if query.data == 'about':
        await query.edit_message_text(
            text="👨‍💻 I'm a bot created by the Sayeb Zeby team.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data='back')]])
        )
    elif query.data == 'terms':
        await query.edit_message_text(
            text="📜 Terms of use:\nDon't be rude and sayeb zeby 😎",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data='back')]])
        )
    elif query.data == 'back':
        await query.edit_message_text(
            text="*Welcome to the menu*\nChoose a platform below:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    elif query.data == 'wack':
        await query.edit_message_text(
            text="You're under the legal age to access certain features, please come back when you're 18.",
            parse_mode='Markdown'
        )

# Build the bot
app = ApplicationBuilder().token(TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_age))
app.add_handler(CallbackQueryHandler(button_handler))

# Start bot
app.run_polling()

