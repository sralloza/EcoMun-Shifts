import datetime
import json
import logging

import gspread
from gspread.utils import a1_to_rowcol
from oauth2client.service_account import ServiceAccountCredentials as Sac

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


def send_email(destinations, subject, message, origin='Turnos EcoMun'):
    logger.debug('-' * 50)
    logger.debug('Sending mail')
    logger.debug('Destinations: %s', destinations)
    logger.debug('Subject: %s', subject)
    logger.debug('Message: %s', message)

    with open('credentials.json') as fh:
        json_data = json.load(fh)

    username = json_data['username']
    password = json_data['password']

    # msg = MIMEMultipart()
    # msg['From'] = f"{origin} <{username}>"
    # msg['To'] = destinations
    # msg['Subject'] = subject
    #
    # body = message.replace('\n', '<br>')
    # msg.attach(MIMEText(body, 'html'))
    #
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()
    # server.login(username, password)
    # server.sendmail(username, msg['To'], msg.as_string())
    # server.quit()
    # return True


def from_google_spreadsheets():
    filename = 'Turnos EcoMun'
    sheetname = 'Calendario'
    logger.debug('Getting info from google spreadsheets - %s - %s', filename, sheetname)

    # Some stuff that needs to be done to use google sheets
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = Sac.from_json_keyfile_name('googlesheets_credentials.json', scope)
    gcc = gspread.authorize(credentials)

    archivo = gcc.open(filename)
    wks = archivo.worksheet(sheetname)

    data = wks.range('G5:W9')

    output = {}
    for cell in data:
        for day, recorded_cell in DAYS_TO_CELL.items():
            row, col = a1_to_rowcol(recorded_cell)
            if cell.row == row and cell.col == col:
                output[day] = cell.value

    return output


def get_today():
    code = datetime.datetime.today().strftime('%m%d')
    return int(code)


DAYS_TO_CELL = {
    401: 'G5', 402: 'H5', 403: 'I5', 404: 'J5',
    408: 'G6', 409: 'H6', 410: 'I6', 411: 'J6',
    424: 'I8', 425: 'J8',
    429: 'G9', 430: 'H9',
    501: 'P5',
    506: 'M6', 507: 'N6', 508: 'O6', 509: 'P6',
    513: 'M7', 514: 'N7', 515: 'O7', 516: 'P7',
    520: 'M8', 521: 'N8', 522: 'O8', 523: 'P8',
    527: 'M9', 528: 'N9', 529: 'O9', 530: 'P9', 531: 'Q9',
    603: 'S6', 604: 'T6', 605: 'U6', 606: 'V6',
    610: 'S7', 611: 'T7', 612: 'U7', 613: 'V7',
    617: 'S8', 618: 'T8', 619: 'U8', 620: 'V8',
    624: 'S9', 625: 'T9', 626: 'U9', 627: 'V9',
}

ALIAS_TO_MAIL = {
    'DAG': 'sralloza@gmail.com',
    'CGC': 'carlosgandiagacalero@gmail.com',
    'VHP': 'victorherrezuelo@gmail.com',
    'CRU': 'kaluti12@gmail.com'
}

ADMIN = 'sralloza@gmail.com'
