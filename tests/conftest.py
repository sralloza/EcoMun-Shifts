import asyncore
import json
import logging
import os
import smtpd
import threading

import pytest

os.environ['SMTP_SERVER_HOST'] = 'localhost'
os.environ['SMTP_SERVER_PORT'] = '2626'
os.environ['TESTING'] = 'True'


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        with open(SMTP_PATH, 'wt') as fh:
            data = {'peer': peer, 'from': mailfrom, 'to': rcpttos, 'data': str(data),
                    'kwargs': kwargs}
            json.dump(data, fh, ensure_ascii=False, indent=4)


server = CustomSMTPServer(('127.0.0.1', 2626), None)

threading.Thread(target=asyncore.loop, name='smtpd', daemon=True).start()


from api import from_google_spreadsheets, TESTING_LOG_PATH

SMTP_PATH = 'smtp.json'


@pytest.fixture(scope='module')
def data():
    return from_google_spreadsheets()


@pytest.fixture(autouse=True)
def autoreset():
    return safe_delete_files()


def safe_delete_files():
    try:
        os.remove(SMTP_PATH)
    except FileNotFoundError:
        pass


def pytest_sessionfinish(*args):
    logging.shutdown()

    try:
        os.remove(TESTING_LOG_PATH)
    except FileNotFoundError:
        pass
    return safe_delete_files()


def read_email():
    assert os.path.isfile(SMTP_PATH)

    with open(SMTP_PATH, encoding='utf-8') as fh:
        data = json.load(fh)

    safe_delete_files()

    return data
