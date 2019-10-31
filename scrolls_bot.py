
import telebot
import google_sheets_connection
import pickle
import random

types = telebot.types
bot = telebot.TeleBot('403672798:AAGhc7iqynRdjb7ddKwt8La79H8V3hgab8Q')

bot.send_message(197216910, 'старт')


@bot.inline_handler(func=lambda query:  len(query.query) < 1)
def query_text(query):
    try:
        characters_dict = pickle.load(open('passwords.pkl', 'rb'))
        connection_dicts = {value['chat_id']: key for key, value in characters_dict.items()}
        stats_data = google_sheets_connection.get_character_data(connection_dicts[query.from_user.id])
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
        traits = types.InlineQueryResultArticle(
            id='traits', title="Трейты и умения",
            description='Доступные заклинания',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('traits', stats_data)))
        additional = types.InlineQueryResultArticle(
            id='additional', title="Дополнительно",
            description='Здоровье, броня и пр.',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('additional', stats_data)))
        bot.answer_inline_query(query.id, [stats, spells, skills, traits, inventory, additional])
    except Exception as e:
        print(e)
        error = types.InlineQueryResultArticle(
            id='error', title="Ошибка",
            description='Персонаж не найден.',
            input_message_content=types.InputTextMessageContent(
                message_text='Ошибка!'))
        bot.answer_inline_query(query.id, [error])


@bot.inline_handler(func=lambda query:  len(query.query) > 1
                                        and query.query in [value['password'] for key, value
                                                            in pickle.load(open('passwords.pkl')).items()])
def query_text(query):
    try:
        characters_dict = pickle.load(open('passwords.pkl', 'rb'))
        connection_dicts = {value['password']: key for key, value in characters_dict.items()}
        stats_data = google_sheets_connection.get_character_data(connection_dicts[query.query])
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
        traits = types.InlineQueryResultArticle(
            id='traits', title="Трейты",
            description='Трейты и умения',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('spells', stats_data)))
        additional = types.InlineQueryResultArticle(
            id='additional', title="Дополнительно",
            description='Здоровье, броня и пр.',
            input_message_content=types.InputTextMessageContent(
                message_text=get_info('additional', stats_data)))
        bot.answer_inline_query(query.id, [stats, spells, skills, traits, inventory, additional])
    except:
        error = types.InlineQueryResultArticle(
            id='error', title="Ошибка",
            description='Персонаж не найден.',
            input_message_content=types.InputTextMessageContent(
                message_text='Ошибка!'))
        bot.answer_inline_query(query.id, [error])


@bot.message_handler(commands=["get_passwords"])
def switch(message):
    characters_dict = pickle.load(open('passwords.pkl', 'rb'))
    message = ''
    for key, value in characters_dict.items():
        message += '{}: {}'.format(key, value['password'])
    bot.send_message(197216910, message)


@bot.message_handler(commands=["new_character"])
def switch(message):
    character_name = message.text.split(' ', 1)[1]
    google_sheets_connection.new_character(character_name)
    characters_dict = pickle.load(open('passwords.pkl', 'rb'))
    characters_dict[character_name] = {'password': str(random.randint(0, 10000)), 'chat_id': 0}
    pickle.dump(characters_dict, open('passwords.pkl', 'wb'))
    bot.send_message(message.from_user.id, 'Персонаж успешно создан. Пароль: {}'.format(characters_dict[character_name]['password']))



@bot.message_handler(commands=["connect"])
def switch(message):
    if len(message.text.split()) > 1:
        password = message.text.split(' ', 1)[1]
        characters_dict = pickle.load(open('passwords.pkl', 'rb'))
        for key, value in characters_dict.items():
            if value['chat_id'] == message.from_user.id:
                characters_dict[key]['chat_id'] = 0
                break
        for key, value in characters_dict.items():
            if value['password'] == password:
                characters_dict[key]['chat_id'] = message.from_user.id
                pickle.dump(characters_dict, open('passwords.pkl', 'wb'))
                bot.send_message(message.from_user.id, 'Профиль подсоединен к персонажу {}'.format(key))
                return


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
    elif text == 'traits':
        stats_dict = stats_data['traits']
        text = ''
        for item in stats_dict:
            text += '\n{}'.format(item)
        return text
    elif text == 'additional':
        stats_dict = stats_data['additional']
        text = ''
        for key in stats_dict.keys():
            text += '\n{} {}'.format(key, stats_dict[key])
        return text


bot.skip_pending = True

if __name__ == '__main__':
    bot.polling(none_stop=True)
