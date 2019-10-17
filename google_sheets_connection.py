import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import OrderedDict


def get_character_data(chat_id):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Characters.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(str(chat_id)).sheet1
    main_stats = OrderedDict(zip(sheet.col_values(1), sheet.col_values(2)))
    skills = OrderedDict(zip(sheet.col_values(3), sheet.col_values(4)))
    inventory = OrderedDict(zip(sheet.col_values(5), sheet.col_values(6)))
    spells = sheet.col_values(7)
    print(main_stats)
    character_data = {'main_stats': main_stats, 'name': main_stats['Имя:'], 'skills': skills,
                      'inventory': inventory, 'spells': spells}
    return character_data
