import argparse
import logging
import time

from api import from_google_spreadsheets, get_today, send_email, ADMIN, ALIAS_TO_MAIL, LOG_PATH, \
    gen_subject, gen_message

logging.basicConfig(handlers=[logging.FileHandler(LOG_PATH, 'a', 'utf-8')],
                    level=logging.DEBUG, format='[%(asctime)s] %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

oauth2client_logger = logging.getLogger('oauth2client')
oauth2client_logger.setLevel(logging.CRITICAL)

urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)


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
        destinations = list(ALIAS_TO_MAIL.values())
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
