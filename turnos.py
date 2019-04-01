import argparse
import logging
import time

from api import from_google_spreadsheets, get_today, send_email, ADMIN, ALIAS_TO_MAIL

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('./EcoMun-shifts.log', 'at', 'utf-8')
handler.setFormatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')  # or whatever
root_logger.addHandler(handler)

logger = logging.getLogger(__name__)

oauth2client_logger = logging.getLogger('oauth2client')
oauth2client_logger.setLevel(logging.CRITICAL)

urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)


def gen_subject(motive: str, tomorrow: bool):
    if motive == 'D':
        subject = 'Examen'
    elif motive == 'P':
        subject = 'Práctica'
    elif motive == 'T':
        subject = 'Test'
    elif motive == 'C':
        subject = 'Clase Teórica'
    else:
        send_email(ADMIN, 'ERROR', f'{motive!r} is not a valid motive')
        return exit(-1)

    if tomorrow:
        subject += ' mañana'
    else:
        subject += ' hoy'

    return subject


def gen_message(motive: str, tomorrow: bool):
    if motive == 'D':
        message = 'Examen'
    elif motive == 'P':
        message = 'Práctica'
    elif motive == 'T':
        message = 'Test'
    elif motive == 'C':
        message = 'Clase Teórica'
    else:
        send_email(ADMIN, 'ERROR', f'{motive!r} is not a valid motive')
        return exit(-1)

    if tomorrow:
        message += ' mañana'
    else:
        message += ' hoy'

    return message


def main(tomorrow=False):
    logger.debug('Starting app, tomorrow=%r', tomorrow)
    data = from_google_spreadsheets()

    logger.debug('Data=%r', data)

    if tomorrow:
        today = get_today() + 1
    else:
        today = get_today()

    logger.debug('Today=%r', today)

    if today not in data:
        logger.critical('Today (%r) not in data', today)
        return send_email(ADMIN, 'ERROR', f'{today!r} is not defined in the database')

    if data[today] not in ALIAS_TO_MAIL:
        logger.debug('Data is not a known alias, broadcasting')
        destinations = ', '.join(ALIAS_TO_MAIL.values())
        motive = data[today]
    else:
        destinations = ALIAS_TO_MAIL[data[today]]
        logger.debug('Found alias: %r', destinations)
        motive = 'C'

    logger.debug('Motive=%r', motive)

    return send_email(destinations, gen_subject(motive, tomorrow), gen_message(motive, tomorrow))


if __name__ == '__main__':
    t0 = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-tomorrow', action='store_true')

    opt = vars(parser.parse_args())

    main(tomorrow=opt['tomorrow'])

    logger.debug(f'EcoMun Shifts executed in {time.time() - t0:.2f} s')
