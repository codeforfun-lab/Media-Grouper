from telegram import (
    Update,
    InputMediaPhoto,
    InputMediaVideo,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = "8289236185:AAHfqqH2iOp_GEQtKWJvTXwAERKegFe54vM"

user_media = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Done", callback_data="done")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Send me up to 10 photos/videos.\nPress ✅ Done when finished.",
        reply_markup=reply_markup,
    )


async def collect_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_media:
        user_media[user_id] = []

    if len(user_media[user_id]) >= 10:
        await update.message.reply_text("Maximum 10 items per album reached.")
        return

    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        user_media[user_id].append(InputMediaPhoto(file_id))
        await update.message.reply_text("Photo added.")

    elif update.message.video:
        file_id = update.message.video.file_id
        user_media[user_id].append(InputMediaVideo(file_id))
        await update.message.reply_text("Video added.")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "done":
        if user_id not in user_media or len(user_media[user_id]) == 0:
            await query.message.reply_text("No media collected.")
            return

        await query.message.reply_media_group(user_media[user_id])
        user_media[user_id] = []


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, collect_media))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
