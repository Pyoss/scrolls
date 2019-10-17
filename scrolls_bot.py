
import telebot
import google_sheets_connection

types = telebot.types
bot = telebot.TeleBot('403672798:AAGhc7iqynRdjb7ddKwt8La79H8V3hgab8Q')

bot.send_message(197216910, 'старт')
# Инлайн тимчата

@bot.inline_handler(func=lambda query: True)
def query_text(query):
    print(query)
    try:
        r_sum = types.InlineQueryResultArticle(
            id='stats', title="Статы",
            # Описание отображается в подсказке,
            # message_text - то, что будет отправлено в виде сообщения
            description='Тест',
            input_message_content=types.InputTextMessageContent(
                message_text='Статы персонажа...'))
        bot.answer_inline_query(query.id, [r_sum])
    except:
        r_sum = types.InlineQueryResultArticle(
            id='22', title="Ошибка!",
            description='Команда не найдена.',
            input_message_content=types.InputTextMessageContent(
                message_text='Ошибка!'))
        bot.answer_inline_query(query.id, [r_sum])


@bot.chosen_inline_handler(func=lambda chosen_inline_result: True )
def test_chosen(chosen_inline_result):
    print(chosen_inline_result)
    if chosen_inline_result.result_id == 'stats':
        stats_data = google_sheets_connection.get_character_data(chosen_inline_result.from_user.id)
        stats_dict = stats_data['main_stats']
        text = ''
        for key in stats_dict.keys():
            text += '\n{} {}'.format(key, stats_dict[key])
        bot.send_message(chosen_inline_result.chat.id, text)


bot.skip_pending = True

if __name__ == '__main__':
    bot.polling(none_stop=True)
