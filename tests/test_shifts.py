import datetime
import os

from freezegun import freeze_time

from api import get_daycode, is_class, ALIAS_TO_MAIL, FROM_EMAIL
from shifts import main
from .conftest import read_email
from .test_api import SMTP_PATH


class TestWeek14:
    @freeze_time('2019-04-01')
    def test_main_2019_04_01(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CGC'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CGC'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-04-02')
    def test_main_2019_04_02(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CRU'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CRU'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-04-03')
    def test_main_2019_04_03(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'P'
        assert data[today] not in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == list(ALIAS_TO_MAIL.values())
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-04-04')
    def test_main_2019_04_04(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CGC'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CGC'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-04-05')
    def test_main_2019_04_05(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-06')
    def test_main_2019_04_06(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-07')
    def test_main_2019_04_07(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek15:
    @freeze_time('2019-04-08')
    def test_main_2019_04_08(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CGC'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CGC'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-04-09')
    def test_main_2019_04_09(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CRU'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CRU'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-04-10')
    def test_main_2019_04_10(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'VHP'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['VHP'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-04-11')
    def test_main_2019_04_11(self, data):
        assert main()

        today = get_daycode()
        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'T'
        assert data[today] not in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == list(ALIAS_TO_MAIL.values())
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-04-12')
    def test_main_2019_04_12(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-13')
    def test_main_2019_04_13(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-14')
    def test_main_2019_04_14(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek16:
    @freeze_time('2019-04-15')
    def test_main_2019_04_15(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-16')
    def test_main_2019_04_16(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-17')
    def test_main_2019_04_17(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-18')
    def test_main_2019_04_18(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-19')
    def test_main_2019_04_19(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-20')
    def test_main_2019_04_20(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-21')
    def test_main_2019_04_21(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek17:
    @freeze_time('2019-04-22')
    def test_main_2019_04_22(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-23')
    def test_main_2019_04_23(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-24')
    def test_main_2019_04_24(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'DAG'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['DAG'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-04-25')
    def test_main_2019_04_25(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'VHP'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['VHP'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-04-26')
    def test_main_2019_04_26(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-27')
    def test_main_2019_04_27(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-04-28')
    def test_main_2019_04_28(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek18:
    @freeze_time('2019-04-29')
    def test_main_2019_04_29(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'DAG'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['DAG'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-04-30')
    def test_main_2019_04_30(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CRU'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CRU'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-01')
    def test_main_2019_05_01(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-02')
    def test_main_2019_05_02(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'VHP'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['VHP'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-03')
    def test_main_2019_05_03(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-04')
    def test_main_2019_05_04(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-05')
    def test_main_2019_05_05(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek19:
    @freeze_time('2019-05-06')
    def test_main_2019_05_06(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'VHP'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['VHP'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-07')
    def test_main_2019_05_07(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CGC'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CGC'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-08')
    def test_main_2019_05_08(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CRU'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CRU'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-09')
    def test_main_2019_05_09(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'DAG'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['DAG'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-10')
    def test_main_2019_05_10(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-11')
    def test_main_2019_05_11(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-12')
    def test_main_2019_05_12(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek20:
    @freeze_time('2019-05-13')
    def test_main_2019_05_13(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'VHP'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['VHP'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-14')
    def test_main_2019_05_14(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CGC'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CGC'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-15')
    def test_main_2019_05_15(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CRU'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CRU'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-16')
    def test_main_2019_05_16(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'DAG'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['DAG'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-17')
    def test_main_2019_05_17(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-18')
    def test_main_2019_05_18(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-19')
    def test_main_2019_05_19(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek21:
    @freeze_time('2019-05-20')
    def test_main_2019_05_20(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'VHP'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['VHP'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-21')
    def test_main_2019_05_21(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CGC'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CGC'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-22')
    def test_main_2019_05_22(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'CRU'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['CRU'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-23')
    def test_main_2019_05_23(self, data):
        assert main()
        today = get_daycode()

        assert today in data
        assert is_class(datetime.datetime.today())
        assert data[today] == 'DAG'
        assert data[today] in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == [ALIAS_TO_MAIL['DAG'], ]
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-05-24')
    def test_main_2019_05_24(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-25')
    def test_main_2019_05_25(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-26')
    def test_main_2019_05_26(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek22:
    @freeze_time('2019-05-27')
    def test_main_2019_05_27(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-28')
    def test_main_2019_05_28(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-29')
    def test_main_2019_05_29(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-30')
    def test_main_2019_05_30(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-05-31')
    def test_main_2019_05_31(self, data):
        assert main()

        today = get_daycode()
        assert today in data
        assert data[today] == 'D'
        assert data[today] not in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == list(ALIAS_TO_MAIL.values())
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-06-01')
    def test_main_2019_06_01(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-02')
    def test_main_2019_06_02(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek23:
    @freeze_time('2019-06-03')
    def test_main_2019_06_03(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-04')
    def test_main_2019_06_04(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-05')
    def test_main_2019_06_05(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-06')
    def test_main_2019_06_06(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-07')
    def test_main_2019_06_07(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-08')
    def test_main_2019_06_08(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-09')
    def test_main_2019_06_09(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek24:
    @freeze_time('2019-06-10')
    def test_main_2019_06_10(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-11')
    def test_main_2019_06_11(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-12')
    def test_main_2019_06_12(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-13')
    def test_main_2019_06_13(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-14')
    def test_main_2019_06_14(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-15')
    def test_main_2019_06_15(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-16')
    def test_main_2019_06_16(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek25:
    @freeze_time('2019-06-17')
    def test_main_2019_06_17(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-18')
    def test_main_2019_06_18(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-19')
    def test_main_2019_06_19(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-20')
    def test_main_2019_06_20(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-21')
    def test_main_2019_06_21(self, data):
        assert main()

        today = get_daycode()
        assert today in data
        assert data[today] == 'D'
        assert data[today] not in ALIAS_TO_MAIL

        mail_data = read_email()
        assert mail_data['to'] == list(ALIAS_TO_MAIL.values())
        assert mail_data['from'] == FROM_EMAIL
        assert 'hoy' in mail_data['data']
        assert isinstance(mail_data, dict)

    @freeze_time('2019-06-22')
    def test_main_2019_06_22(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-23')
    def test_main_2019_06_23(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)


class TestWeek26:
    @freeze_time('2019-06-24')
    def test_main_2019_06_24(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-25')
    def test_main_2019_06_25(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-26')
    def test_main_2019_06_26(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-27')
    def test_main_2019_06_27(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-28')
    def test_main_2019_06_28(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-29')
    def test_main_2019_06_29(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)

    @freeze_time('2019-06-30')
    def test_main_2019_06_30(self, data):
        assert main()

        today = get_daycode()
        assert today not in data
        assert not is_class(datetime.datetime.today())
        assert not os.path.isfile(SMTP_PATH)
