from config import logger


def log_my_name():
    try:
        logger.info("Eustero Mwai on feb 21")

    except Exception as e:
        logger.error(e)
        raise


if __name__ == '__main__':
    log_my_name()