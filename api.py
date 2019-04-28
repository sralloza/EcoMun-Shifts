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
from functools import lru_cache
from typing import Union

import gspread
import httplib2
import oauth2client.client
import requests
from gspread.utils import a1_to_rowcol
from oauth2client.service_account import ServiceAccountCredentials as Sac

logger = logging.getLogger(__name__)

if platform.system() == 'Windows':
    LOG_PATH = 'D:/.scripts/ecomun-shifts/ecomun-shifts.log'
    GS_CREDENTIALS_PATH = 'D:/.scripts/ecomun-shifts/googlesheets_credentials.json'
    CREDENTIALS_PATH = 'D:/.scripts/ecomun-shifts/credentials.json'
    JOKES_PATH = 'D:/.scripts/ecomun-shifts/jokes.json'
    TESTING_LOG_PATH = 'D:/.scripts/ecomun-shifts/testing.log'
else:
    LOG_PATH = '/home/sralloza/ecomun-shifts/ecomun-shifts.log'
    GS_CREDENTIALS_PATH = '/home/sralloza/ecomun-shifts/googlesheets_credentials.json'
    CREDENTIALS_PATH = '/home/sralloza/ecomun-shifts/credentials.json'
    JOKES_PATH = '/home/sralloza/ecomun-shifts/jokes.json'
    TESTING_LOG_PATH = '/home/sralloza/ecomun-shifts/testing.log'

TESTING = os.environ.get('TESTING') is not None


def send_email(destinations, subject, message, origin='Turnos EcoMun', retries=5):
    logger.debug('----------------')
    logger.debug('Sending mail')
    logger.debug('Destinations: %s', destinations)
    logger.debug('Subject: %s', subject)
    logger.debug('Message: %s', message)

    if not TESTING and platform.system() == 'Windows':
        raise RuntimeError('Only linux')

    with open(CREDENTIALS_PATH) as fh:
        json_data = json.load(fh)

    username = json_data['username']
    password = json_data['password']

    if isinstance(destinations, str):
        destinations = [destinations, ]

    msg = MIMEMultipart()
    msg['From'] = f"{origin} <{username}>"
    msg['To'] = ', '.join(destinations)
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

        if not TESTING:
            server.starttls()

        if not TESTING:
            server.login(username, password)

        server.sendmail(username, destinations, msg.as_string())
        server.quit()
        return True

    logger.critical('Retries exceeded')
    return False


@lru_cache()
def from_google_spreadsheets(retries=10):
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
        except oauth2client.client.HttpAccessTokenRefreshError:
            logger.warning('HttpAccessTokenRefreshError in authorization, retries=%r', retries)
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
    send_email(ADMIN_EMAIL, 'ERROR', 'MAX RETRIES. CHECK LOG')
    raise RuntimeError('Max retries')


def get_daycode(tomorrow=False):
    dt = datetime.datetime.today()

    if tomorrow:
        dt += datetime.timedelta(days=1)

    code = dt.strftime('%m%d')
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
        send_email(ADMIN_EMAIL, 'ERROR', f'{motive!r} is not a valid motive')
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
        send_email(ADMIN_EMAIL, 'ERROR', f'{motive!r} is not a valid motive')
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


def gen_weekly_report(data: dict = None, retries=10):
    # todo - make the report in order (monday, tuesday, wednesday...) and make tests.
    from googletrans import Translator

    if data is None:
        data = from_google_spreadsheets()

    today = datetime.datetime.today()
    logger.debug('Generating weekly report (today=%r)', today.ctime())
    if is_weekend(today):
        week = today.isocalendar()[1] + 1
        logger.debug('Weekend detected, week=%r', week)
    else:
        week = today.isocalendar()[1]
        logger.debug('Business day detected, week=%r', week)

    converted = OrderedDict()
    for daycode, value in data.items():
        month, day = split_daycode(daycode)
        dt = datetime.datetime(2019, month, day)

        if dt.isocalendar()[1] == week:
            if value not in ALIAS_TO_MAIL.keys():
                value = gen_subject(value, tomorrow=None)
            converted[dt] = value

    if len(converted) == 0:
        raise RuntimeError('Empty processed data')

    report = f'Informe semanal (Semana No. {week})\n'
    translator = Translator()

    for dt, value in converted.items():
        dt: datetime.datetime

        while retries:
            try:
                report += translator.translate(dt.strftime('%A: '), dest='es', src='en').text
                break
            except requests.exceptions.ConnectionError:
                logger.warning('ConnectionError in translator')
                retries -= 1
                continue

        report += ' '
        report += value
        report += '\n'

    report += '\n\nChiste del día:\n' + gen_joke()

    return report


def is_labourable(dt: datetime.datetime):
    if not isinstance(dt, datetime.datetime):
        raise TypeError(f'dt must be datetime.datetime, not {type(dt).__name__!r}')
    return dt.isoweekday() not in (6, 7)


def is_weekend(dt: datetime.datetime):
    if not isinstance(dt, datetime.datetime):
        raise TypeError(f'dt must be datetime.datetime, not {type(dt).__name__!r}')
    return dt.isoweekday() in (6, 7)


def is_class(dt: datetime.datetime):
    if not isinstance(dt, datetime.datetime):
        raise TypeError(f'dt must be datetime.datetime, not {type(dt).__name__!r}')

    if datetime.datetime(2019, 4, 15) <= dt <= datetime.datetime(2019, 4, 23):
        return False
    if datetime.datetime(2019, 5, 27) <= dt <= datetime.datetime(2019, 5, 30):
        return False
    if datetime.datetime(2019, 6, 1) <= dt <= datetime.datetime(2019, 6, 27):
        return False
    if dt == datetime.datetime(2019, 5, 1):
        return False

    return dt.isoweekday() not in (5, 6, 7)


DAYS_TO_CELL = {
    401: 'G5', 402: 'H5', 403: 'I5', 404: 'J5',
    408: 'G6', 409: 'H6', 410: 'I6', 411: 'J6',
    424: 'I8', 425: 'J8',
    429: 'G9', 430: 'H9',
    502: 'P5',
    506: 'M6', 507: 'N6', 508: 'O6', 509: 'P6',
    513: 'M7', 514: 'N7', 515: 'O7', 516: 'P7',
    520: 'M8', 521: 'N8', 522: 'O8', 523: 'P8',
    531: 'Q9',
    621: 'W8',
}

ALIAS_TO_MAIL = {
    'DAG': 'sralloza@gmail.com',
    'CGC': 'carlosgandiagacalero@gmail.com',
    'VHP': 'victorherrezuelo@gmail.com',
    'CRU': 'kaluti12@gmail.com'
}

ADMIN_EMAIL = 'sralloza@gmail.com'
FROM_EMAIL = "idkvnoxkdnfwodk642310@gmail.com"
