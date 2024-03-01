import logging
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import BOT_TOKEN
import sqlite3

conn = sqlite3.connect('data/users.db', check_same_thread=False)
cursor = conn.cursor()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


""" В этом разделе написаны подробно все кнопки """
entrance_keyboard = [['Sign In', 'Sign Up']]
entrance_markup = ReplyKeyboardMarkup(entrance_keyboard, one_time_keyboard=False)


""" В этом разделе написаны подробно все функции """
def database_values(user_id: int, name: str, surname: str, handle: str, login: str, password: str):
    """Функция для работы с базой данных"""
    cursor.execute('INSERT INTO users_info (user_id, name, surname, handle, login, password) VALUES (?, ?, ?, ?, ?, ?)',
                   (user_id, name, surname, handle, login, password))

async def close_keyboard(update, context):
    # Закрывает клавиатуру
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


async def get_name(update, context):
    """ Получает имя при регистрации """
    await update.message.reply_text(
        "Введите имя: ")


async def random_text(update, context):
    """ Будет выводить в случае фразы, непонятной боту """
    if update.message.text == 'Sign In':
        name, surname,
        await get_name(update, context)
    else:
        await update.message.reply_text("Простите я Вас не понимаю. Советую проверить правильность написания"
                                    "названия команды. Если остались вопросы вызовить команду /help")


async def start(update, context):
    """ Отправляет сообщение когда получена команда /start """
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я могу вести удобно статистику твоего аккаунта Codeforces. Если впервые здесь "
        rf"нажми на кнопку 'Регистрация', а если уже есть аккаунт то войди в него ⬇",
        reply_markup=entrance_markup
    )


async def help(update, context):
    """ Отправляет сообщение когда получена команда /start """
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Здесь скоро будет добавлена информация",
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, random_text)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("get_name", get_name))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(text_handler)
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()