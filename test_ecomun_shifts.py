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
os.environ['SMTP_SERVER_PORT'] = '2626'
os.environ['TESTING'] = 'True'

from shifts import gen_subject, gen_message, main
from api import send_email, ADMIN, from_google_spreadsheets, get_today, DAYS_TO_CELL, ALIAS_TO_MAIL, \
    CREDENTIALS_PATH, GS_CREDENTIALS_PATH, LOG_PATH, JOKES_PATH, gen_joke, split_daycode, \
    is_labourable, is_weekend, gen_weekly_report

SMTP_PATH = 'smtp.json'


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        with open(SMTP_PATH, 'wt') as fh:
            data = {'peer': peer, 'from': mailfrom, 'to': rcpttos, 'data': str(data),
                    'kwargs': kwargs}
            json.dump(data, fh, ensure_ascii=False, indent=4)


server = CustomSMTPServer(('127.0.0.1', 2626), None)

threading.Thread(target=asyncore.loop, name='smtpd', daemon=True).start()


# STARTING TESTS API
def tests_paths():
    if platform.system() == 'Windows':
        assert 'D:/Sistema/Desktop/turnos-ecomun/' in LOG_PATH
        assert 'D:/Sistema/Desktop/turnos-ecomun/' in GS_CREDENTIALS_PATH
        assert 'D:/Sistema/Desktop/turnos-ecomun/' in CREDENTIALS_PATH
        assert 'D:/Sistema/Desktop/turnos-ecomun/' in JOKES_PATH
    else:
        assert '/home/sralloza/ecomun-shifts/' in LOG_PATH
        assert '/home/sralloza/ecomun-shifts/' in GS_CREDENTIALS_PATH
        assert '/home/sralloza/ecomun-shifts/' in CREDENTIALS_PATH
        assert '/home/sralloza/ecomun-shifts/' in JOKES_PATH

    assert LOG_PATH.endswith('.log')
    assert GS_CREDENTIALS_PATH.endswith('.json')
    assert CREDENTIALS_PATH.endswith('.json')
    assert JOKES_PATH.endswith('.json')

    assert os.path.isfile(GS_CREDENTIALS_PATH)
    assert os.path.isfile(CREDENTIALS_PATH)
    assert os.path.isfile(JOKES_PATH)


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


# noinspection PyTypeChecker
def test_split_daycode():
    assert split_daycode(101) == (1, 1)
    assert split_daycode(202) == (2, 2)
    assert split_daycode(303) == (3, 3)
    assert split_daycode(404) == (4, 4)
    assert split_daycode(505) == (5, 5)
    assert split_daycode(606) == (6, 6)
    assert split_daycode(707) == (7, 7)
    assert split_daycode(808) == (8, 8)
    assert split_daycode(909) == (9, 9)
    assert split_daycode(1010) == (10, 10)
    assert split_daycode(1111) == (11, 11)
    assert split_daycode(1212) == (12, 12)

    assert split_daycode(516) == (5, 16)
    assert split_daycode(630) == (6, 30)
    assert split_daycode(420) == (4, 20)

    with pytest.raises(ValueError, match='Invalid daycode'):
        split_daycode(4)
    with pytest.raises(ValueError, match='Invalid daycode'):
        split_daycode(40)
    with pytest.raises(ValueError, match='Invalid daycode'):
        split_daycode(40000)
    with pytest.raises(ValueError, match='Invalid daycode'):
        split_daycode(44164)
    with pytest.raises(ValueError, match='Invalid daycode'):
        split_daycode(41659)
    with pytest.raises(ValueError, match='Invalid daycode'):
        split_daycode('hola')
    with pytest.raises(ValueError, match='Invalid daycode'):
        split_daycode('adios')
    with pytest.raises(ValueError, match='Invalid daycode'):
        split_daycode(True)
    with pytest.raises(ValueError, match='Invalid daycode'):
        split_daycode(5.26)
    with pytest.raises(ValueError, match='Invalid daycode'):
        split_daycode(4 + 2j)


def test_gen_subject():
    assert gen_subject('D', False) == 'Examen hoy'
    assert gen_subject('P', False) == 'Práctica hoy'
    assert gen_subject('T', False) == 'Test hoy'
    assert gen_subject('C', False) == 'Clase Teórica hoy'

    assert gen_subject('D', True) == 'Examen mañana'
    assert gen_subject('P', True) == 'Práctica mañana'
    assert gen_subject('T', True) == 'Test mañana'
    assert gen_subject('C', True) == 'Clase Teórica mañana'

    assert gen_subject('D', None) == 'Examen'
    assert gen_subject('P', None) == 'Práctica'
    assert gen_subject('T', None) == 'Test'
    assert gen_subject('C', None) == 'Clase Teórica'

    with pytest.raises(SystemExit):
        gen_subject('UNKOWN', False)

    with open(SMTP_PATH) as fh:
        data = json.load(fh)
        assert data['to'] == list((ADMIN,))
        assert 'is not a valid motive' in data['data']


def test_gen_message():
    assert 'Examen hoy, hay que ir todos.' in gen_message('D', False)
    assert 'Práctica hoy, hay que ir todos.' in gen_message('P', False)
    assert 'Test hoy, hay que ir todos.' in gen_message('T', False)
    assert 'Clase Teórica hoy, te toca ir.' in gen_message('C', False)

    assert 'Examen mañana, hay que ir todos.' in gen_message('D', True)
    assert 'Práctica mañana, hay que ir todos.' in gen_message('P', True)
    assert 'Test mañana, hay que ir todos.' in gen_message('T', True)
    assert 'Clase Teórica mañana, te toca ir.' in gen_message('C', True)

    with pytest.raises(SystemExit):
        gen_subject('UNKOWN', False)

    with open(SMTP_PATH) as fh:
        data = json.load(fh)
        assert data['to'] == list((ADMIN,))
        assert 'is not a valid motive' in data['data']


def test_gen_joke():
    assert isinstance(gen_joke(), str)
    assert isinstance(gen_joke(), str)
    assert isinstance(gen_joke(), str)
    assert isinstance(gen_joke(), str)
    assert len(gen_joke())
    assert len(gen_joke())
    assert len(gen_joke())
    assert len(gen_joke())


def test_gen_weekly_report():
    report = gen_weekly_report()

    assert 'Monday' not in report
    assert 'Tuesday' not in report
    assert 'Thursday' not in report
    assert 'Friday' not in report
    assert 'Saturday' not in report
    assert 'Sunday' not in report
    assert 'day' not in report

    assert 'Informe semanal' in report
    assert 'Semana No.' in report
    assert report.count('\n') > 1


# noinspection PyTypeChecker
def test_is_labourable():
    dt = datetime.datetime
    assert is_labourable(dt(2019, 1, 1))
    assert is_labourable(dt(2019, 2, 1))
    assert is_labourable(dt(2019, 3, 1))
    assert is_labourable(dt(2019, 4, 1))
    assert is_labourable(dt(2019, 5, 1))
    assert not is_labourable(dt(2019, 6, 1))
    assert is_labourable(dt(2019, 7, 1))
    assert is_labourable(dt(2019, 8, 1))
    assert not is_labourable(dt(2019, 9, 1))
    assert is_labourable(dt(2019, 10, 1))
    assert is_labourable(dt(2019, 11, 1))
    assert not is_labourable(dt(2019, 12, 1))

    assert is_labourable(dt(2019, 4, 8))
    assert is_labourable(dt(2019, 4, 9))
    assert is_labourable(dt(2019, 4, 10))
    assert is_labourable(dt(2019, 4, 11))
    assert is_labourable(dt(2019, 4, 12))
    assert not is_labourable(dt(2019, 4, 13))
    assert not is_labourable(dt(2019, 4, 14))

    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_labourable('hello world')
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_labourable(datetime.date(2000, 5, 2))
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_labourable(5)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_labourable(True)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_labourable(None)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_labourable(5 + 2j)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_labourable(1.2)


# noinspection PyTypeChecker
def test_is_weekend():
    dt = datetime.datetime
    assert not is_weekend(dt(2019, 1, 1))
    assert not is_weekend(dt(2019, 2, 1))
    assert not is_weekend(dt(2019, 3, 1))
    assert not is_weekend(dt(2019, 4, 1))
    assert not is_weekend(dt(2019, 5, 1))
    assert is_weekend(dt(2019, 6, 1))
    assert not is_weekend(dt(2019, 7, 1))
    assert not is_weekend(dt(2019, 8, 1))
    assert is_weekend(dt(2019, 9, 1))
    assert not is_weekend(dt(2019, 10, 1))
    assert not is_weekend(dt(2019, 11, 1))
    assert is_weekend(dt(2019, 12, 1))

    assert not is_weekend(dt(2019, 4, 8))
    assert not is_weekend(dt(2019, 4, 9))
    assert not is_weekend(dt(2019, 4, 10))
    assert not is_weekend(dt(2019, 4, 11))
    assert not is_weekend(dt(2019, 4, 12))
    assert is_weekend(dt(2019, 4, 13))
    assert is_weekend(dt(2019, 4, 14))

    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_weekend('hello world')
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_weekend(datetime.date(2000, 5, 2))
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_weekend(5)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_weekend(True)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_weekend(None)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_weekend(5 + 2j)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_weekend(1.2)


# ------------------- TEST CONSTANT VARIABLES ----------------
def test_days_to_cell():
    assert len(DAYS_TO_CELL) == 46
    assert isinstance(DAYS_TO_CELL, dict)


def test_alias_to_mail():
    assert len(ALIAS_TO_MAIL) == 4
    assert isinstance(ALIAS_TO_MAIL, dict)


# -------------------- TESTS OF SHIFTS.PY -----------------------

class TestMain:
    def test_main_today(self):
        main()

        data = from_google_spreadsheets()
        today = get_today()

        if today not in data:
            month, day = split_daycode(today)

            datetime_ = datetime.datetime(2019, month, day)

            if datetime_.isoweekday() in (5, 6, 7):
                assert not os.path.isfile(SMTP_PATH)
                return

            assert os.path.isfile(SMTP_PATH)

            with open(SMTP_PATH) as fh:
                mail_data = json.load(fh)

            assert mail_data['to'] == ADMIN
            assert mail_data['from'] == "idkvnoxkdnfwodk642310@gmail.com"
            assert 'ERROR' in mail_data['data']
            assert isinstance(mail_data, dict)

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

        if today not in data:
            day = int(str(today)[:-2])
            month = int(str(today)[-2:])

            datetime_ = datetime.datetime(2019, month, day)

            if datetime_.weekday() in (4, 5, 6):
                return

            assert 0

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

    def test_weekly_report(self):
        assert main(tomorrow=False, weekly_report=True)

        assert os.path.isfile(SMTP_PATH)

        with open(SMTP_PATH) as fh:
            mail_data = json.load(fh)

        assert mail_data['to'] == list(ALIAS_TO_MAIL.values())
        assert mail_data['from'] == "idkvnoxkdnfwodk642310@gmail.com"
        assert 'Informe Semanal' in mail_data['data']
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
