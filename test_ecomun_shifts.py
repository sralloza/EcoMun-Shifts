# def main(tomorrow=False): ...

import asyncore
import datetime
import json
import os
import platform
import smtpd
import threading

import pytest

os.environ['SMTP_SERVER_HOST'] = 'localhost'
os.environ['SMTP_SERVER_PORT'] = '26'
os.environ['TESTING'] = 'True'

from turnos import gen_subject, gen_message, main
from api import send_email, ADMIN, from_google_spreadsheets, get_today, DAYS_TO_CELL, ALIAS_TO_MAIL, \
    CREDENTIALS_PATH, GS_CREDENTIALS_PATH, LOG_PATH

SMTP_PATH = 'smtp.json'


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        with open(SMTP_PATH, 'wt') as fh:
            data = {'peer': peer, 'from': mailfrom, 'to': rcpttos, 'data': str(data),
                    'kwargs': kwargs}
            json.dump(data, fh, ensure_ascii=False, indent=4)


server = CustomSMTPServer(('127.0.0.1', 26), None)

threading.Thread(target=asyncore.loop, name='smtpd', daemon=True).start()


# STARTING TESTS API
def tests_paths():
    if platform.system() == 'Windows':
        assert 'D:/Sistema/Desktop/turnos-ecomun/' in LOG_PATH
        assert 'D:/Sistema/Desktop/turnos-ecomun/' in GS_CREDENTIALS_PATH
        assert 'D:/Sistema/Desktop/turnos-ecomun/' in CREDENTIALS_PATH
    else:
        assert '/home/sralloza/ecomun-shifts/' in LOG_PATH
        assert '/home/sralloza/ecomun-shifts/' in GS_CREDENTIALS_PATH
        assert '/home/sralloza/ecomun-shifts/' in CREDENTIALS_PATH

    assert LOG_PATH.endswith('.log')
    assert GS_CREDENTIALS_PATH.endswith('.json')
    assert CREDENTIALS_PATH.endswith('.json')

    assert os.path.isfile(GS_CREDENTIALS_PATH)
    assert os.path.isfile(CREDENTIALS_PATH)


def test_send_email():
    assert send_email('peterpan@peter.com', 'asunto', 'mensaje')

    with open(SMTP_PATH) as fh:
        data = json.load(fh)
        assert data['to'] == ['peterpan@peter.com']
        assert 'mensaje' in data['data']
        assert 'Subject: asunto' in data['data']


def test_from_google_spreadsheets():
    data = from_google_spreadsheets()

    for key in data.keys():
        assert key in DAYS_TO_CELL.keys()

    assert data.keys() == DAYS_TO_CELL.keys()
    assert len(data.keys())
    assert isinstance(data, dict)


def test_get_today():
    assert get_today() == int(datetime.datetime.today().strftime('%m%d'))
    assert isinstance(get_today(), int)


def test_gen_subject():
    assert gen_subject('D', False) == 'Examen hoy'
    assert gen_subject('P', False) == 'Práctica hoy'
    assert gen_subject('T', False) == 'Test hoy'
    assert gen_subject('C', False) == 'Clase Teórica hoy'

    assert gen_subject('D', True) == 'Examen mañana'
    assert gen_subject('P', True) == 'Práctica mañana'
    assert gen_subject('T', True) == 'Test mañana'
    assert gen_subject('C', True) == 'Clase Teórica mañana'

    with pytest.raises(SystemExit):
        gen_subject('UNKOWN', False)

    with open(SMTP_PATH) as fh:
        data = json.load(fh)
        assert data['to'] == list((ADMIN,))
        assert 'is not a valid motive' in data['data']


def test_gen_message():
    assert gen_message('D', False) == 'Examen hoy'
    assert gen_message('P', False) == 'Práctica hoy'
    assert gen_message('T', False) == 'Test hoy'
    assert gen_message('C', False) == 'Clase Teórica hoy'

    assert gen_message('D', True) == 'Examen mañana'
    assert gen_message('P', True) == 'Práctica mañana'
    assert gen_message('T', True) == 'Test mañana'
    assert gen_message('C', True) == 'Clase Teórica mañana'

    with pytest.raises(SystemExit):
        gen_subject('UNKOWN', False)

    with open(SMTP_PATH) as fh:
        data = json.load(fh)
        assert data['to'] == list((ADMIN,))
        assert 'is not a valid motive' in data['data']


def test_days_to_cell():
    assert len(DAYS_TO_CELL) == 46
    assert isinstance(DAYS_TO_CELL, dict)


def test_alias_to_mail():
    assert len(ALIAS_TO_MAIL) == 4
    assert isinstance(ALIAS_TO_MAIL, dict)


# -------------------- TESTS OF TURNOS -----------------------

class TestMain:
    def test_main_today(self):
        main()

        data = from_google_spreadsheets()
        today = get_today()
        if data[today] not in ALIAS_TO_MAIL:
            destinations = list(ALIAS_TO_MAIL.values())
        else:
            destinations = [ALIAS_TO_MAIL[data[today]], ]

        with open(SMTP_PATH) as fh:
            mail_data = json.load(fh)

        assert mail_data['to'] == destinations
        assert mail_data['from'] == "idkvnoxkdnfwodk642310@gmail.com"
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    def test_main_tomorrow(self):
        main(tomorrow=True)

        data = from_google_spreadsheets()
        today = get_today() + 1
        print(data[today])
        if data[today] not in ALIAS_TO_MAIL:
            destinations = list(ALIAS_TO_MAIL.values())
        else:
            destinations = [ALIAS_TO_MAIL[data[today]], ]

        with open(SMTP_PATH) as fh:
            mail_data = json.load(fh)

        assert mail_data['to'] == destinations
        assert mail_data['from'] == "idkvnoxkdnfwodk642310@gmail.com"
        assert 'ma=C3=B1ana' in mail_data['data']
        assert isinstance(mail_data, dict)


# -------------------- FIXTURES -----------------------

@pytest.fixture(autouse=True)
def autoreset():
    return safe_delete_files()


def safe_delete_files():
    try:
        os.remove(SMTP_PATH)
    except FileNotFoundError:
        pass


def teardown_module():
    return safe_delete_files()
