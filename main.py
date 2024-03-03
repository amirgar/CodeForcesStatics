import logging
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from functions.user_info import get_base_information
import sqlite3
import translators as ts

conn = sqlite3.connect('data/users.db', check_same_thread=False)
cursor = conn.cursor()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

login = ""
password = ""
user_handle = ""
logger = logging.getLogger(__name__)

entrance_keyboard = [['/SignIn', '/Registration']]
entrance_markup = ReplyKeyboardMarkup(entrance_keyboard, one_time_keyboard=False)
success_registration_keyboard = [['/ready']]
success_registration_markup = ReplyKeyboardMarkup(success_registration_keyboard, one_time_keyboard=False)
user_info = []


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я могу вести удобно статистику твоего аккаунта Codeforces. Если впервые здесь "
        rf"нажми на кнопку '/Registration', а если уже есть аккаунт то войди в него ⬇",
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
    global login
    login = update.message.text
    global user_info
    user_info.append(login)
    await update.message.reply_text("Введите пароль: ")
    return 2


async def sign_in_third(update, context):
    global password
    password = update.message.text
    global user_info
    user_info.append(password)
    print(f'!!!!!!!!!!!!!!!!!!!!!!!!! {user_info} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    info = cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (user_info[0], user_info[1],))
    if info.fetchone():
        await update.message.reply_html("Вход прошел успешно! Если готов использовать меня нажми кнопку начать ⬇",
                                        reply_markup=success_registration_markup
                                        )
    else:
        await update.message.reply_text("Неправильно введен логин или пароль, введите команду /SignIn "
                                        "заново для повторного прохождения регистрации")
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
    global login
    login = update.message.text
    global user_info
    user_info.append(login)
    await update.message.reply_text(
        f"Придумайте пароль: ")
    return 5


async def registration_sixth(update, context):
    global password
    password = update.message.text
    global user_info
    user_info.append(password)
    print(f'!!!!!!!!!!!!!!!!!!!!!!!!! {user_info} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    cursor.execute('INSERT INTO users (surname, name, handle, login, password) VALUES (?, ?, ?, ?, ?)',
                   (user_info[1], user_info[0], user_info[2], user_info[3], user_info[4]))
    conn.commit()
    await update.message.reply_html(f"Регистрация прошла успешна! Если готов использовать меня нажми кнопку начать ⬇",
                                    reply_markup=success_registration_markup
                                    )
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def ready_first(update, context):
    global user_handle
    handle_info = cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password,))
    handle_info = handle_info.fetchall()
    user_handle = handle_info[0][5]
    info_json = get_base_information(user_handle)
    await update.message.reply_text(
        f"Пользователь: {info_json['result'][0]["lastName"]} {info_json['result'][0]["firstName"]}\n"
        f"Местоположение: {info_json['result'][0]['country']} {info_json['result'][0]['city']} {info_json['result'][0]['organization']}\n"
        f"Вклад: {info_json['result'][0]['contribution']}\n"
        f"Количество друзей: {info_json['result'][0]['friendOfCount']}\n"
        f"Ранг: {ts.translate_text(info_json['result'][0]['rank'], to_language='ru')}\n"
        f"Рейтинг: {info_json['result'][0]['rating']}\n"
        f"Максимальный рейтинг: {info_json['result'][0]['maxRating']}\n")
    return 1


async def ready_second(update, context):
    await update.message.reply_text(f"Пока что нет новых уведомлений от Codeforces")
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

    ready = ConversationHandler(
        entry_points=[CommandHandler('ready', ready_first)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, ready_second)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(sign_in)
    application.add_handler(registration)
    application.add_handler(ready)
    application.add_handler(CommandHandler('start', start))
    application.run_polling()


if __name__ == '__main__':
    main()
