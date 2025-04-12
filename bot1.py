# Xin-go Telegram-Bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message, InputMediaPhoto, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import os, asyncio, sqlite3, random

TOKEN = os.getenv("TOKEN")
AGE, CAPTCHA = range(2)

# --- Utility for CAPTCHA ---
def generate_captcha():
    emojis = ["🍕", "🐱", "🐶", "🚀", "🎲", "🍔", "👻", "🐍"]
    correct = random.choice(emojis)
    choices = random.sample(emojis, 4)
    if correct not in choices:
        choices[random.randint(0, 3)] = correct
    return correct, choices

# --- Start Function ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Notify the admin
    msg = f"📢 New user started the bot:\n"
    msg += f"👤 Name: {user.full_name}\n🆔 ID: {user.id}\n"
    if user.username:
        msg += f"🔗 Username: @{user.username}"
    await context.bot.send_message(chat_id=6424248902, text=msg)

    # Loading simulation
    loading_msg: Message = await update.message.reply_text("Loading...")
    for dots in ["..", "...", "...."]:
        await loading_msg.edit_text(f"Loading{dots}")
        await asyncio.sleep(1)
    await loading_msg.edit_text("🌿")
    await asyncio.sleep(1)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text(f"👋 Hello, {user.first_name}.", parse_mode='Markdown')
    await update.message.reply_text(f"Your ID: {user.id}")
    
    return await ask_captcha(update, context)

# --- CAPTCHA Handling ---
async def ask_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    correct, choices = generate_captcha()
    context.user_data["captcha_answer"] = correct

    keyboard = [[c] for c in choices]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        f"🛡 Please click the emoji: {correct}",
        reply_markup=reply_markup
    )
    return CAPTCHA

async def verify_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text
    correct = context.user_data.get("captcha_answer")

    if user_answer == correct:
        await update.message.reply_text("HOW OLD ARE YOU?")
        return AGE
    else:
        await update.message.reply_text("❌ Wrong emoji. Fuck Your Mom!")
        return CAPTCHA

# --- Age Handling ---
async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age_text = update.message.text

    if age_text is None or not age_text.isdigit():
        await update.message.reply_text("Please enter a valid number for your age.")
        return AGE

    age = int(age_text)

    if age < 18:
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='wack')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Sorry, you must be 18 or older to use this feature.", reply_markup=reply_markup)
        return ConversationHandler.END

# --- Age Check (Reusable) ---
async def check_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age = context.user_data.get("age")
    if age is None or age < 18:
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='wack')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Sorry, you must be 18 or older to use this feature.", reply_markup=reply_markup)
        return AGE

# --- Random Image ---
async def random_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    folder_path = "image"
    files = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    if not files:
        await update.message.reply_text("No images found in the folder.")
        return

    random_file = random.choice(files)
    file_path = os.path.join(folder_path, random_file)

    with open(file_path, "rb") as img:
        await update.message.reply_photo(photo=img, caption=f"🎲 Random image: {random_file}")

# --- Static Image ---
async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open('image/terr.jpg', 'rb') as image_file:
        await update.message.reply_photo(photo=image_file)

# --- Stop Command ---
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ya {update.effective_user.first_name} Sayeb zeby!")

# --- Help ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 Available commands:\n"
        "/start - Greet\n"
        "/menu - menu\n"
        "/random - random_image\n"
        "/help - Show help message\n"
    )
    await update.message.reply_text(help_text)

# --- Menu ---
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ℹ️ About", callback_data='about'),
         InlineKeyboardButton("📜 Terms", callback_data='terms')]
    ]
    await update.message.reply_text(
        "*Welcome to the menu*\nChoose below:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# --- Button Callbacks ---
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

# --- Build App ---
app = ApplicationBuilder().token(TOKEN).build()

# --- Conversation Handler (CAPTCHA + AGE) ---
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CAPTCHA: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_captcha)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
    },
    fallbacks=[]
)

# --- Add Handlers ---
app.add_handler(conv_handler)
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("ask", ask_captcha,))
app.add_handler(CommandHandler("image", image))
app.add_handler(CommandHandler("random", random_image))

# --- Run Bot ---
app.run_polling()
