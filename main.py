import logging
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from config import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def random_text(update, context):
    """ Будет выводить в случае фразы, непонятной боту """
    await update.message.reply_text("Простите я Вас не понимаю. Советую проверить правильность написания"
                                    "названия команды. Если остались вопросы вызовить команду /help")


async def start(update, context):
    """ Отправляет сообщение когда получена команда /start """
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def help(update, context):
    """ Отправляет сообщение когда получена команда /start """
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Здесь скоро будет добавлена информация",
    )


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Создаём обработчик сообщений типа filters.TEXT
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, random_text)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    # Регистрируем обработчики в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()