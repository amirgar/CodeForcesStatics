import logging
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
import sqlite3

conn = sqlite3.connect('data/users.db', check_same_thread=False)
cursor = conn.cursor()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

entrance_keyboard = [['/SignIn', '/Registration']]
entrance_markup = ReplyKeyboardMarkup(entrance_keyboard, one_time_keyboard=False)
user_info = []


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я могу вести удобно статистику твоего аккаунта Codeforces. Если впервые здесь "
        rf"нажми на кнопку 'Регистрация', а если уже есть аккаунт то войди в него ⬇",
        reply_markup=entrance_markup
    )


async def sign_in_first(update, context):
    # question login
    global user_info
    user_info = []
    await update.message.reply_text(
        f"Введите логин от телеграмм бота:")
    return 1


async def sign_in_second(update, context):
    login = update.message.text
    global user_info
    user_info.append(login)
    await update.message.reply_text("Введите пароль: ")
    return 2


async def sign_in_third(update, context):
    password = update.message.text
    global user_info
    user_info.append(password)
    print(f'!!!!!!!!!!!!!!!!!!!!!!!!! {user_info} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return ConversationHandler.END


async def registration_first(update, context):
    global user_info
    user_info = []
    await update.message.reply_text(
        f"Введите ваше имя: ")
    return 1


async def registration_second(update, context):
    name = update.message.text
    global user_info
    user_info.append(name)
    await update.message.reply_text(
        f"Введите вашу фамилию: ")
    return 2


async def registration_third(update, context):
    surname = update.message.text
    global user_info
    user_info.append(surname)
    await update.message.reply_text(
        f"Введите ваш хендл(Codeforces): ")
    return 3


async def registration_forth(update, context):
    handle = update.message.text
    global user_info
    user_info.append(handle)
    await update.message.reply_text(
        f"Придумайте логин: ")
    return 4


async def registration_fifth(update, context):
    login = update.message.text
    global user_info
    user_info.append(login)
    await update.message.reply_text(
        f"Придумайте пароль: ")
    return 5


async def registration_sixth(update, context):
    password = update.message.text
    global user_info
    user_info.append(password)
    print(f'!!!!!!!!!!!!!!!!!!!!!!!!! {user_info} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return ConversationHandler.END

async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    sign_in = ConversationHandler(
        entry_points=[CommandHandler('SignIn', sign_in_first)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, sign_in_second)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, sign_in_third)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    registration = ConversationHandler(
        entry_points=[CommandHandler('Registration', registration_first)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_second)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_third)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_forth)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_fifth)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_sixth)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(sign_in)
    application.add_handler(registration)
    application.add_handler(CommandHandler('start', start))
    application.run_polling()


if __name__ == '__main__':
    main()
