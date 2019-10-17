
import telebot
import google_sheets_connection

types = telebot.types
bot = telebot.TeleBot('403672798:AAGhc7iqynRdjb7ddKwt8La79H8V3hgab8Q')
# Инлайн тимчата

x = '78.47.202.24:3128'
telebot.apihelper.proxy = {
'http': 'http://{}'.format(x),
'https': 'http://{}'.format(x)
}

players_dict = {'Тайлор': 83697884}

bot.send_message(197216910, 'старт')
@bot.inline_handler(func=lambda query:  len(query.query) < 1)
def query_text(query):
    try:
        stats_data = google_sheets_connection.get_character_data(query.from_user.id)
        stats = types.InlineQueryResultArticle(
            id='stats', title="Статы",
            # Описание отображается в подсказке,
            # message_text - то, что будет отправлено в виде сообщения
            description='Характеристики персонажа',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('stats', stats_data)))
        skills = types.InlineQueryResultArticle(
            id='skills', title="Навыки",
            description='Изученные навыки',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('skills', stats_data)))
        inventory = types.InlineQueryResultArticle(
            id='inventory', title="Инвентарь",
            description='Вещи в сумке',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('inventory', stats_data)))
        spells = types.InlineQueryResultArticle(
            id='spells', title="Магия",
            description='Доступные заклинания',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('spells', stats_data)))
        bot.answer_inline_query(query.id, [stats, spells, skills, inventory])
    except:
        error = types.InlineQueryResultArticle(
            id='error', title="Ошибка",
            description='Персонаж не найден.',
            input_message_content=types.InputTextMessageContent(
                message_text='Ошибка!'))
        bot.answer_inline_query(query.id, [error])


@bot.inline_handler(func=lambda query:  len(query.query) > 1 and query.query in players_dict)
def query_text(query):
    try:
        chat_id = players_dict[query.query]
        stats_data = google_sheets_connection.get_character_data(chat_id)
        stats = types.InlineQueryResultArticle(
            id='stats', title="Статы",
            # Описание отображается в подсказке,
            # message_text - то, что будет отправлено в виде сообщения
            description='Характеристики персонажа',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('stats', stats_data)))
        skills = types.InlineQueryResultArticle(
            id='skills', title="Навыки",
            description='Изученные навыки',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('skills', stats_data)))
        inventory = types.InlineQueryResultArticle(
            id='inventory', title="Инвентарь",
            description='Вещи в сумке',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('inventory', stats_data)))
        spells = types.InlineQueryResultArticle(
            id='spells', title="Магия",
            description='Доступные заклинания',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('spells', stats_data)))
        bot.answer_inline_query(query.id, [stats, spells, skills, inventory])
    except:
        error = types.InlineQueryResultArticle(
            id='error', title="Ошибка",
            description='Персонаж не найден.',
            input_message_content=types.InputTextMessageContent(
                message_text='Ошибка!'))
        bot.answer_inline_query(query.id, [error])


def get_info(text, stats_data):
    if text == 'stats':
        stats_dict = stats_data['main_stats']
        text = ''
        for key in stats_dict.keys():
            text += '\n{} {}'.format(key, stats_dict[key])
        return text
    elif text == 'skills':
        stats_dict = stats_data['skills']
        text = ''
        for key in stats_dict.keys():
            text += '\n{} {}'.format(key, stats_dict[key])
        return text
    elif text == 'inventory':
        stats_dict = stats_data['inventory']
        text = ''
        for key in stats_dict.keys():
            text += '\n{} {}'.format(key, stats_dict[key])
        return text
    elif text == 'spells':
        stats_dict = stats_data['spells']
        text = ''
        for item in stats_dict:
            text += '\n{}'.format(item)
        return text


bot.skip_pending = True

if __name__ == '__main__':
    bot.polling(none_stop=True)
