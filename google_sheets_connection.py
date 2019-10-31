import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import OrderedDict


def authorize():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Characters.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(str('scrolls_data'))
    return spreadsheet


def get_character_data(google_doc_name):
    spreadsheet = authorize()
    sheet = spreadsheet.worksheet(google_doc_name)
    main_stats = OrderedDict(zip(sheet.col_values(1), sheet.col_values(2)))
    skills = OrderedDict(zip(sheet.col_values(3), sheet.col_values(4)))
    traits = sheet.col_values(5)
    inventory = OrderedDict(zip(sheet.col_values(6), sheet.col_values(7)))
    spells = sheet.col_values(8)
    additional = OrderedDict(zip(sheet.col_values(9), sheet.col_values(10)))
    print(main_stats)
    character_data = {'main_stats': main_stats, 'name': main_stats['Имя:'], 'skills': skills,
                      'inventory': inventory, 'spells': spells, 'additional': additional, 'traits': traits}
    return character_data


def create_column(worksheet, column_index, column_items):
    index = 1
    for item in column_items:
        worksheet.update_cell(index, column_index, item)
        index += 1


def new_character(character_name):
    spreadsheet = authorize()
    worksheet = spreadsheet.add_worksheet(character_name, 30, 15)
    columns = [
        ['Имя:', 'Раса:', 'Сила:', 'Выносливость:', 'Ловкость:', 'Интеллект:',
         'Мудрость:', 'Харизма:', 'Рассудок:'],
        [character_name, '-', '-', '-', '-', '-', '-', '-', '-'],
        ['Навыки ({}):'.format(character_name),
         'Акробатика (Лов):',
         'Анализ (Инт):',
         'Атлетика (Сил):',
         'Внимательность (Мдр):',
         'Выживание (Мдр):',
         'Запугивание (Хар):',
         'История (Инт):',
         'Ловкость рук (Лов):',
         'Магия (Инт):',
         'Медицина (Инт):',
         'Обман (Хар):',
         'Природа (Инт):',
         'Проницательность (Мдр):',
         'Религия (Инт):',
         'Скрытность (Лов):',
         'Убеждение (Хар):',
         'Уход за животными (Мдр):',
         ],
        ['',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         '-',
         ],
        ['Трейты ({}):'.format(character_name),
         ],
        ['Инвентарь ({}):'.format(character_name),
         ],
        [''],
        ['Заклинания ({}):'.format(character_name)],
        ['Дополнительно ({}):'.format(character_name),
         'Класс брони:', 'Здоровье:'
         ],
        ['', '', '', '', '', ''],
    ]
    i = 1
    for column in columns:
        create_column(worksheet, i, column)
        i += 1
