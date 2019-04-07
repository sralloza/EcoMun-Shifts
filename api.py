import datetime
import json
import logging
import os
import platform
import random
import smtplib
from collections import OrderedDict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union

import gspread
import httplib2
import requests
from gspread.utils import a1_to_rowcol
from oauth2client.service_account import ServiceAccountCredentials as Sac

logger = logging.getLogger(__name__)

if platform.system() == 'Windows':
    LOG_PATH = 'D:/Sistema/Desktop/turnos-ecomun/ecomun-shifts.log'
    GS_CREDENTIALS_PATH = 'D:/Sistema/Desktop/turnos-ecomun/googlesheets_credentials.json'
    CREDENTIALS_PATH = 'D:/Sistema/Desktop/turnos-ecomun/credentials.json'
    JOKES_PATH = 'D:/Sistema/Desktop/turnos-ecomun/jokes.json'
else:
    LOG_PATH = '/home/sralloza/ecomun-shifts/ecomun-shifts.log'
    GS_CREDENTIALS_PATH = '/home/sralloza/ecomun-shifts/googlesheets_credentials.json'
    CREDENTIALS_PATH = '/home/sralloza/ecomun-shifts/credentials.json'
    JOKES_PATH = '/home/sralloza/ecomun-shifts/jokes.json'


def send_email(destinations, subject, message, origin='Turnos EcoMun', retries=5):
    logger.debug('----------------')
    logger.debug('Sending mail')
    logger.debug('Destinations: %s', destinations)
    logger.debug('Subject: %s', subject)
    logger.debug('Message: %s', message)

    testing = os.environ.get('TESTING') is not None

    with open(CREDENTIALS_PATH) as fh:
        json_data = json.load(fh)

    username = json_data['username']
    password = json_data['password']

    msg = MIMEMultipart()
    msg['From'] = f"{origin} <{username}>"
    if isinstance(destinations, (tuple, list)):
        msg['To'] = ', '.join(destinations)
    else:
        msg['To'] = destinations
    msg['Subject'] = subject

    body = message.replace('\n', '<br>')
    msg.attach(MIMEText(body, 'html'))

    while retries > 0:
        try:
            server = smtplib.SMTP(
                os.environ.get('SMTP_SERVER_HOST') or "smtp.gmail.com",
                os.environ.get('SMTP_SERVER_PORT') or 587
            )
        except smtplib.SMTPConnectError:
            retries -= 1
            logger.warning('SMTP Connection Error')
            continue

        if not testing:
            server.starttls()

        if not testing:
            server.login(username, password)

        server.sendmail(username, destinations, msg.as_string())
        server.quit()
        return True

    logger.critical('Retries exceeded')
    return False


def from_google_spreadsheets(retries=5):
    filename = 'Turnos EcoMun'
    sheetname = 'Calendario'
    logger.debug('Getting info from google spreadsheets - %s - %s', filename, sheetname)

    # Some stuff that needs to be done to use google sheets
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = Sac.from_json_keyfile_name(GS_CREDENTIALS_PATH, scope)

    while retries > 0:
        try:
            gcc = gspread.authorize(credentials)
        except httplib2.ServerNotFoundError:
            logger.warning('Server not found error in authorization, retries=%r', retries)
            retries -= 1
            continue
        except TimeoutError:
            logger.warning('Timeout error in authorization, retries=%r', retries)
            retries -= 1
            continue
        except requests.exceptions.ConnectionError:
            logger.warning('Connection error in authorization, retries=%r', retries)
            retries -= 1
            continue

        try:
            archivo = gcc.open(filename)
        except requests.exceptions.ConnectionError:
            logger.warning('Connection error getting file, retries=%r', retries)
            retries -= 1
            continue

        wks = archivo.worksheet(sheetname)

        data = wks.range('G5:W9')

        output = {}
        for cell in data:
            for day, recorded_cell in DAYS_TO_CELL.items():
                row, col = a1_to_rowcol(recorded_cell)
                if cell.row == row and cell.col == col:
                    output[day] = cell.value

        return output

    logger.critical('Max retries')
    return send_email(ADMIN, 'ERROR', 'MAX RETRIES. CHECK LOG')


def get_today():
    code = datetime.datetime.today().strftime('%m%d')
    return int(code)


def split_daycode(daycode: Union[str, int]):
    daycode = str(daycode)

    if len(daycode) < 2 or len(daycode) > 4:
        raise ValueError(f'Invalid daycode: {daycode!r}')

    try:
        month = int(str(daycode)[:-2])
        day = int(str(daycode)[-2:])
    except ValueError:
        raise ValueError(f'Invalid daycode: {daycode!r}')

    return month, day


def gen_subject(motive: str, tomorrow: bool = None):
    logger.debug('Generating subject from motive %r (tomorrow=%r)', motive, tomorrow)
    if motive == 'D':
        subject = 'Examen {}'
    elif motive == 'P':
        subject = 'Práctica {}'
    elif motive == 'T':
        subject = 'Test {}'
    elif motive == 'C':
        subject = 'Clase Teórica {}'
    else:
        send_email(ADMIN, 'ERROR', f'{motive!r} is not a valid motive')
        return exit(-1)

    if tomorrow is True:
        subject = subject.format('mañana')
    elif tomorrow is False:
        subject = subject.format('hoy')
    else:
        subject = subject.format('').strip()

    return subject


def gen_message(motive: str, tomorrow: bool):
    logger.debug('Generating message from motive %r (tomorrow=%r)', motive, tomorrow)
    if motive == 'D':
        message = 'Examen {}, hay que ir todos.'
    elif motive == 'P':
        message = 'Práctica {}, hay que ir todos.'
    elif motive == 'T':
        message = 'Test {}, hay que ir todos.'
    elif motive == 'C':
        message = 'Clase Teórica {}, te toca ir.'
    else:
        send_email(ADMIN, 'ERROR', f'{motive!r} is not a valid motive')
        return exit(-1)

    if tomorrow:
        message = message.format('mañana')
    else:
        message = message.format('hoy')

    message += '\n\nChiste del día:\n' + gen_joke()

    return message


def gen_joke():
    with open(JOKES_PATH, encoding='utf-8') as fh:
        jokes = json.load(fh)

    return random.choice(jokes)


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
