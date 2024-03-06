import logging
import random
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
import requests
import time
import sqlite3
import translators as ts


def get_base_information(handle):
    link = f'https://codeforces.com/api/user.info?handles={handle}'
    response = requests.get(link)
    if response:
        return response.json()
    else:
        print("Ошибка выполнения запроса:")
        print(link)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return None


def get_statics() -> list:
    global user_handle
    link = f'https://codeforces.com/api/user.status?handle={user_handle}&from=1&count=100'
    info = requests.get(link).json()
    tasks = info["result"]
    tasks_set = set()
    verdicts = dict()
    rating = dict()
    for task in tasks:
        tasks_set.add(task['problem']['name'])
        if task['verdict'] not in verdicts:
            verdicts[task['verdict']] = 1
        else:
            verdicts[task['verdict']] += 1
        try:
            if task['problem']['rating'] not in rating:
                rating[task['problem']['rating']] = 1
            else:
                rating[task['problem']['rating']] += 1
        except:
            continue
    return [tasks_set, verdicts, rating]


conn = sqlite3.connect('data/users.db', check_same_thread=False)
cursor = conn.cursor()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

success_registration_keyboard = [['/ready']]
success_registration_markup = ReplyKeyboardMarkup(success_registration_keyboard, one_time_keyboard=False)
ready_function_keyboard = [['/statics', '/random_task'],
                           ['/get_user_info', '/events']]
ready_function_markup = ReplyKeyboardMarkup(ready_function_keyboard, one_time_keyboard=False)


async def start_first(update, context):
    await update.message.reply_text(
        f"Привет! Введи свой хендл Codeforces и я выдам тебе уникальный id для работы со мной далее: ")
    return 1


async def start_second(update, context):
    await update.message.reply_text(f'Создаю ваш id...')
    cursor.execute('INSERT INTO users (handle) VALUES (?)',
                   (update.message.text,))
    conn.commit()
    time.sleep(3)
    id_info = cursor.execute('SELECT * FROM users WHERE handle = ?', (update.message.text,))
    id_info = id_info.fetchall()
    id_info = id_info[0][0]
    await update.message.reply_text(f"Ваш id: {id_info}. Он пригодится для дальнейшей работы")
    await update.message.reply_text(f"Если Вы готовы меня использовать, нажмите /ready⬇",
                                    reply_markup=success_registration_markup)
    return ConversationHandler.END


async def menu_get_info(update, context):
    await update.message.reply_text(f'Введите id: ')
    return 1


async def menu(update, context):
    id = int(update.message.text)
    handle_info = cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
    handle_info = handle_info.fetchall()
    user_handle = handle_info[0][1]
    info_json = get_base_information(user_handle)
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=info_json['result'][0]['titlePhoto'])
    await update.message.reply_text(
        f"Пользователь: {info_json['result'][0]["lastName"]} {info_json['result'][0]["firstName"]}\n"
        f"Местоположение: {ts.translate_text(info_json['result'][0]['country'], to_language='ru')} "
        f"{ts.translate_text(info_json['result'][0]['city'], to_language='ru')} \n"
        f"Организация: {ts.translate_text(info_json['result'][0]['organization'], to_language='ru')}\n"
        f"Вклад: {info_json['result'][0]['contribution']}\n"
        f"Количество друзей: {info_json['result'][0]['friendOfCount']}\n"
        f"Ранг: {ts.translate_text(info_json['result'][0]['rank'], to_language='ru')}\n"
        f"Рейтинг: {info_json['result'][0]['rating']}\n"
        f"Максимальный рейтинг: {info_json['result'][0]['maxRating']}\n")
    print("OK")
    await update.message.reply_html(f'Выберите функцию для продолжения работы (при различных возможных сбоях в работе, забаньте бота, а потом начните работу с ним снова): ',
                                    reply_markup=ready_function_markup)
    return ConversationHandler.END


async def statics_get_info(update, context):
    await update.message.reply_text(f'Введите id: ')
    return 1


async def statics(update, context):
    await update.message.reply_text("Готовлю Вашу статистику, "
                                    "Постараюсь как можно быстрее...")
    handle_info = cursor.execute('SELECT * FROM users WHERE id = ?', (update.message.text,))
    handle_info = handle_info.fetchall()
    user_handle = handle_info[0][1]
    link = f'https://codeforces.com/api/user.status?handle={user_handle}&from=1&count=100'
    info = requests.get(link).json()
    tasks = info["result"]
    tasks_set = set()
    verdicts = dict()
    rating = dict()
    for task in tasks:
        tasks_set.add(task['problem']['name'])
        if task['verdict'] not in verdicts:
            verdicts[task['verdict']] = 1
        else:
            verdicts[task['verdict']] += 1
        try:
            if task['problem']['rating'] not in rating:
                rating[task['problem']['rating']] = 1
            else:
                rating[task['problem']['rating']] += 1
        except:
            continue
    info = [tasks_set, verdicts, rating]

    res = ""
    for el in info[0]:
        res += el
        res += "\n"
    ress = ""
    for el in info[1]:
        ress += f'{el}: {info[1][el]}\n'
    resss = ""
    for el in info[2]:
        resss += f'{el}: {info[2][el]}\n'
    await update.message.reply_text(f'Из последних 100 ваших посылок, вам удалось решить следующие задачи: \n'
                                    f'{ts.translate_text(res, to_language='ru')}')
    await update.message.reply_text(f'Статистика Ваших посылок: \n{ress}')
    await update.message.reply_text(f'Сложность решаемых Вами задач: : \n{resss}')
    await update.message.reply_html(f'Выберите функцию для продолжения работы: ',
                                    reply_markup=ready_function_markup)
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Работа бота приостановлена. Для восстановления работы введите команду /start")
    return ConversationHandler.END


async def generate_task_get(update, context):
    await update.message.reply_text("Введите тип задания, который вы хотите порешать (апишите значние из второго столбика): \n"
                                    "-Динамическое программирование - dp\n"
                                    "-Математика и теория чисел - math\n"
                                    "-2-SAT - 2-sat\n"
                                    "-meet-in-the-middle - meet-in-the-middle\n"
                                    "-Бинарный поиск - binary search\n"
                                    "-Битмаски - bitmasks\n"
                                    "-Геометрия - geometry\n"
                                    "-Графы - graphs\n"
                                    "-Два указателя - two pointers\n"
                                    "-Деревья - trees\n"
                                    "-Игры - games\n"
                                    "-Китайская теорема об остатках - chinese remainder theorem\n"
                                    "-Комбинаторика - combinatorics\n"
                                    "-Конструктив - constructive algorithms\n"
                                    "-Кратчайшие пути - shortest paths\n"
                                    "-Жадный алгоритм - greedy\n"
                                    "-Поиск в глубину и подобное - dfs and similar\n"
                                    "-Потоки - flows\n"
                                    "-Структуры данных - data structures\n"
                                    "-Перебор - brute force\n"
                                    "-Сотировки - sorings\n"
                                    "-Строки - strings\n"
                                    "-СНМ - dsu\n"
                                    "-Любой тип - other")
    return 1


async def task_get(update, context):
    task = update.message.text
    if task == 'other':
        task = ''
    link = f'https://codeforces.com/api/problemset.problems?tags={task}'
    info = requests.get(link).json()
    if info["result"] == 'OK':
        await update.message.reply_text("Вы ввели неправильное значение")
    else:
        tasks = info["result"]["problems"]
        n = random.randint(0, len(tasks))
        res = f'https://codeforces.com/contest/{tasks[n]['contestId']}/problem/{tasks[n]['index']}'
        await update.message.reply_text(f'Ссылка на задачу: {res}.')
    await update.message.reply_html(f'Выберите функцию для продолжения работы (при различных возможных сбоях в работе, забаньте бота, а потом начните работу с ним снова): ',
                                    reply_markup=ready_function_markup)
    return ConversationHandler.END


async def user_get(update, context):
    await update.message.reply_text("Введите хендл пользователя: ")
    return 1


async def user_info(update, context):
    user_handle = update.message.text
    info_json = get_base_information(user_handle)
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=info_json['result'][0]['titlePhoto'])
    await update.message.reply_text(
        f"Пользователь: {info_json['result'][0]["lastName"]} {info_json['result'][0]["firstName"]}\n"
        f"Местоположение: {ts.translate_text(info_json['result'][0]['country'], to_language='ru')} "
        f"{ts.translate_text(info_json['result'][0]['city'], to_language='ru')} \n"
        f"Организация: {ts.translate_text(info_json['result'][0]['organization'], to_language='ru')}\n"
        f"Вклад: {info_json['result'][0]['contribution']}\n"
        f"Количество друзей: {info_json['result'][0]['friendOfCount']}\n"
        f"Ранг: {ts.translate_text(info_json['result'][0]['rank'], to_language='ru')}\n"
        f"Рейтинг: {info_json['result'][0]['rating']}\n"
        f"Максимальный рейтинг: {info_json['result'][0]['maxRating']}\n")
    await update.message.reply_html(f'Выберите функцию для продолжения работы (при различных возможных сбоях в работе, забаньте бота, а потом начните работу с ним снова): ',
                                    reply_markup=ready_function_markup)
    return ConversationHandler.END

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    start = ConversationHandler(
        entry_points=[CommandHandler('start', start_first)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_second)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    ready = ConversationHandler(
        entry_points=[CommandHandler('ready', menu_get_info)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    static = ConversationHandler(
        entry_points=[CommandHandler('statics', statics_get_info)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, statics)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    random_task = ConversationHandler(
        entry_points=[CommandHandler('random_task', generate_task_get)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_get)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    get_user_info = ConversationHandler(
        entry_points=[CommandHandler('get_user_info', user_get)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_info)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(start)
    application.add_handler(ready)
    application.add_handler(static)
    application.add_handler(random_task)
    application.add_handler(get_user_info)
    application.add_handler(CommandHandler('stop', stop))
    application.run_polling()


if __name__ == '__main__':
    main()
