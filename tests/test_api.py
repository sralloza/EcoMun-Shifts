import datetime
import os
import platform

import pytest
from freezegun import freeze_time

from .conftest import read_email, SMTP_PATH


from shifts import gen_subject, gen_message, main
from api import send_email, ADMIN_EMAIL, from_google_spreadsheets, get_daycode, DAYS_TO_CELL, \
    ALIAS_TO_MAIL, \
    CREDENTIALS_PATH, GS_CREDENTIALS_PATH, LOG_PATH, JOKES_PATH, gen_joke, split_daycode, \
    is_labourable, is_weekend, gen_weekly_report, is_class, FROM_EMAIL


# STARTING TESTS API
def tests_paths():
    if platform.system() == 'Windows':
        assert 'D:/.scripts/ecomun-shifts/' in LOG_PATH
        assert 'D:/.scripts/ecomun-shifts/' in GS_CREDENTIALS_PATH
        assert 'D:/.scripts/ecomun-shifts/' in CREDENTIALS_PATH
        assert 'D:/.scripts/ecomun-shifts/' in JOKES_PATH
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

    data = read_email()
    assert data['to'] == ['peterpan@peter.com']
    assert 'mensaje' in data['data']
    assert 'Subject: asunto' in data['data']


def test_from_google_spreadsheets():
    data = from_google_spreadsheets()

    for key in data.keys():
        assert key in DAYS_TO_CELL.keys()
        assert data[key]

    assert data.keys() == DAYS_TO_CELL.keys()
    assert len(data.keys())
    assert isinstance(data, dict)


class TestGetDaycode:
    @freeze_time('2019-04-08')
    def test_get_daycode_1(self):
        assert get_daycode() == 408
        assert get_daycode(True) == 409

    @freeze_time('2019-04-09')
    def test_get_daycode_2(self):
        assert get_daycode() == 409
        assert get_daycode(True) == 410

    @freeze_time('2019-04-10')
    def test_get_daycode_3(self):
        assert get_daycode() == 410
        assert get_daycode(True) == 411

    @freeze_time('2019-04-30')
    def test_get_daycode_4(self):
        assert get_daycode() == 430
        assert get_daycode(True) == 501

    @freeze_time('2019-05-31')
    def test_get_daycode_5(self):
        assert get_daycode() == 531
        assert get_daycode(True) == 601

    @freeze_time('2019-06-30')
    def test_get_daycode_6(self):
        assert get_daycode() == 630
        assert get_daycode(True) == 701


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

    data = read_email()
    assert data['to'] == list((ADMIN_EMAIL,))
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

    data = read_email()
    assert data['to'] == [ADMIN_EMAIL, ]
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


class TestGenWeeklyReport:
    def test_gen_weekly_report(self):
        try:
            report = gen_weekly_report()
        except RuntimeError as ex:
            assert 'Empty processed data' in str(ex)
            return

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

        assert 'Chiste del día' in report

    @freeze_time('2019-03-31')
    def test_week_14(self):
        assert main(weekly_report=True)

        mail = read_email()
        assert mail['to'] == list(ALIAS_TO_MAIL.values())
        assert mail['from'] == FROM_EMAIL

        report = gen_weekly_report()

        assert 'Informe Semanal' in mail['data']
        assert 'Informe semanal' in report
        assert 'Chiste del día' in report

        assert 'Lunes' in report
        assert 'Martes' in report
        assert 'Miércoles' in report
        assert 'Jueves' in report
        assert 'Viernes' not in report
        assert 'Sábado' not in report
        assert 'Domingo' not in report

    @freeze_time('2019-04-07')
    def test_week_15(self, data):
        assert main(weekly_report=True)

        mail = read_email()
        assert mail['to'] == list(ALIAS_TO_MAIL.values())
        assert mail['from'] == FROM_EMAIL

        report = gen_weekly_report(data)

        assert 'Informe Semanal' in mail['data']
        assert 'Informe semanal' in report
        assert 'Chiste del día' in report

        assert 'Lunes' in report
        assert 'Martes' in report
        assert 'Miércoles' in report
        assert 'Jueves' in report
        assert 'Viernes' not in report
        assert 'Sábado' not in report
        assert 'Domingo' not in report

    @freeze_time('2019-04-14')
    def test_week_16(self, data):
        assert not main(weekly_report=True)
        assert not os.path.isfile(SMTP_PATH)

        with pytest.raises(RuntimeError, match='Empty processed data'):
            gen_weekly_report(data)

    @freeze_time('2019-04-21')
    def test_week_17(self, data):
        assert main(weekly_report=True)

        mail = read_email()
        assert mail['to'] == list(ALIAS_TO_MAIL.values())
        assert mail['from'] == FROM_EMAIL

        report = gen_weekly_report(data)

        assert 'Informe Semanal' in mail['data']
        assert 'Informe semanal' in report
        assert 'Chiste del día' in report

        assert 'Lunes' not in report
        assert 'Martes' not in report
        assert 'Miércoles' in report
        assert 'Jueves' in report
        assert 'Viernes' not in report
        assert 'Sábado' not in report
        assert 'Domingo' not in report

    @freeze_time('2019-04-28')
    def test_week_18(self, data):
        assert main(weekly_report=True)

        mail = read_email()
        assert mail['to'] == list(ALIAS_TO_MAIL.values())
        assert mail['from'] == FROM_EMAIL

        report = gen_weekly_report(data)

        assert 'Informe Semanal' in mail['data']
        assert 'Informe semanal' in report
        assert 'Chiste del día' in report

        assert 'Lunes' in report
        assert 'Martes' in report
        assert 'Miércoles' not in report
        assert 'Jueves' in report
        assert 'Viernes' not in report
        assert 'Sábado' not in report
        assert 'Domingo' not in report

    @freeze_time('2019-05-01')
    def test_week_19(self, data):
        assert main(weekly_report=True)

        mail = read_email()
        assert mail['to'] == list(ALIAS_TO_MAIL.values())
        assert mail['from'] == FROM_EMAIL

        report = gen_weekly_report(data)

        assert 'Informe Semanal' in mail['data']
        assert 'Informe semanal' in report
        assert 'Chiste del día' in report

        assert 'Lunes' in report
        assert 'Martes' in report
        assert 'Miércoles' not in report
        assert 'Jueves' in report
        assert 'Viernes' not in report
        assert 'Sábado' not in report
        assert 'Domingo' not in report

    @freeze_time('2019-05-12')
    def test_week_20(self, data):
        assert main(weekly_report=True)

        mail = read_email()
        assert mail['to'] == list(ALIAS_TO_MAIL.values())
        assert mail['from'] == FROM_EMAIL

        report = gen_weekly_report(data)

        assert 'Informe Semanal' in mail['data']
        assert 'Informe semanal' in report
        assert 'Chiste del día' in report

        assert 'Lunes' not in report
        assert 'Martes' in report
        assert 'Miércoles' in report
        assert 'Jueves' in report
        assert 'Viernes' not in report
        assert 'Sábado' not in report
        assert 'Domingo' not in report

    @freeze_time('2019-05-19')
    def test_week_21(self, data):
        assert main(weekly_report=True)

        mail = read_email()
        assert mail['to'] == list(ALIAS_TO_MAIL.values())
        assert mail['from'] == FROM_EMAIL

        report = gen_weekly_report(data)

        assert 'Informe Semanal' in mail['data']
        assert 'Informe semanal' in report
        assert 'Chiste del día' in report

        assert 'Lunes' in report
        assert 'Martes' in report
        assert 'Miércoles' in report
        assert 'Jueves' in report
        assert 'Viernes' not in report
        assert 'Sábado' not in report
        assert 'Domingo' not in report

    @freeze_time('2019-05-26')
    def test_week_22(self, data):
        assert main(weekly_report=True)

        mail = read_email()
        assert mail['to'] == list(ALIAS_TO_MAIL.values())
        assert mail['from'] == FROM_EMAIL

        report = gen_weekly_report(data)

        assert 'Informe Semanal' in mail['data']
        assert 'Informe semanal' in report
        assert 'Chiste del día' in report

        assert 'Lunes' not in report
        assert 'Martes' not in report
        assert 'Miércoles' not in report
        assert 'Jueves' not in report
        assert 'Viernes' in report
        assert 'Sábado' not in report
        assert 'Domingo' not in report

    @freeze_time('2019-06-02')
    def test_week_23(self, data):
        assert not main(weekly_report=True)
        assert not os.path.isfile(SMTP_PATH)

        with pytest.raises(RuntimeError, match='Empty processed data'):
            gen_weekly_report(data)

    @freeze_time('2019-06-09')
    def test_week_24(self, data):
        assert not main(weekly_report=True)
        assert not os.path.isfile(SMTP_PATH)

        with pytest.raises(RuntimeError, match='Empty processed data'):
            gen_weekly_report(data)

    @freeze_time('2019-06-16')
    def test_week_25(self, data):
        assert main(weekly_report=True)

        mail = read_email()
        assert mail['to'] == list(ALIAS_TO_MAIL.values())
        assert mail['from'] == FROM_EMAIL

        report = gen_weekly_report(data)

        assert 'Informe Semanal' in mail['data']
        assert 'Informe semanal' in report
        assert 'Chiste del día' in report

        assert 'Lunes' not in report
        assert 'Martes' not in report
        assert 'Miércoles' not in report
        assert 'Jueves' not in report
        assert 'Viernes' in report
        assert 'Sábado' not in report
        assert 'Domingo' not in report

    @freeze_time('2019-06-23')
    def test_week_26(self, data):
        assert not main(weekly_report=True)
        assert not os.path.isfile(SMTP_PATH)

        with pytest.raises(RuntimeError, match='Empty processed data'):
            gen_weekly_report(data)


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


# noinspection PyTypeChecker
def test_is_class():
    dt = datetime.datetime
    assert is_class(dt(2019, 1, 1))
    assert not is_class(dt(2019, 2, 1))
    assert not is_class(dt(2019, 3, 1))
    assert is_class(dt(2019, 4, 1))
    assert not is_class(dt(2019, 5, 1))
    assert not is_class(dt(2019, 6, 1))
    assert is_class(dt(2019, 7, 1))
    assert is_class(dt(2019, 8, 1))
    assert not is_class(dt(2019, 9, 1))
    assert is_class(dt(2019, 10, 1))
    assert not is_class(dt(2019, 11, 1))
    assert not is_class(dt(2019, 12, 1))

    assert is_class(dt(2019, 4, 8))
    assert is_class(dt(2019, 4, 9))
    assert is_class(dt(2019, 4, 10))
    assert is_class(dt(2019, 4, 11))
    assert not is_class(dt(2019, 4, 12))
    assert not is_class(dt(2019, 4, 12))
    assert not is_class(dt(2019, 4, 13))
    assert not is_class(dt(2019, 4, 13))
    assert not is_class(dt(2019, 4, 14))
    assert not is_class(dt(2019, 4, 14))

    assert not is_class(dt(2019, 4, 15))
    assert not is_class(dt(2019, 4, 16))
    assert not is_class(dt(2019, 4, 17))
    assert not is_class(dt(2019, 4, 18))
    assert not is_class(dt(2019, 4, 19))
    assert not is_class(dt(2019, 4, 20))
    assert not is_class(dt(2019, 4, 21))
    assert not is_class(dt(2019, 4, 22))
    assert not is_class(dt(2019, 4, 23))

    assert not is_class(dt(2019, 6, 1))
    assert not is_class(dt(2019, 6, 2))
    assert not is_class(dt(2019, 6, 3))
    assert not is_class(dt(2019, 6, 7))
    assert not is_class(dt(2019, 6, 10))
    assert not is_class(dt(2019, 6, 13))
    assert not is_class(dt(2019, 6, 14))
    assert not is_class(dt(2019, 6, 17))
    assert not is_class(dt(2019, 6, 19))
    assert not is_class(dt(2019, 6, 21))
    assert not is_class(dt(2019, 6, 23))
    assert not is_class(dt(2019, 6, 25))
    assert not is_class(dt(2019, 6, 27))
    assert not is_class(dt(2019, 6, 30))

    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_class('hello world')
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_class(datetime.date(2000, 5, 2))
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_class(5)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_class(True)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_class(None)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_class(5 + 2j)
    with pytest.raises(TypeError, match='dt must be datetime.datetime'):
        is_class(1.2)


def test_days_to_cell():
    assert len(DAYS_TO_CELL) == 26
    assert isinstance(DAYS_TO_CELL, dict)


def test_alias_to_mail():
    assert len(ALIAS_TO_MAIL) == 4
    assert isinstance(ALIAS_TO_MAIL, dict)
