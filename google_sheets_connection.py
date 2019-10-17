import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_character_data(chat_id):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Characters.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(str(chat_id)).sheet1
    main_stats = dict(zip(sheet.col_values(1), sheet.col_values(2)))
    skills = dict(zip(sheet.col_values(3), sheet.col_values(4)))
    inventory = dict(zip(sheet.col_values(5), sheet.col_values(6)))
    spells = sheet.col_values(7)
    character_data = {'main_stats': main_stats, 'name': main_stats['name'], 'skills': skills,
                      'inventory': inventory, 'spells': spells}
    return character_data
