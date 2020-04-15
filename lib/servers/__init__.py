from threading import Thread
import signal
import logging

from lib.servers import p0f_wrapper, http_server

logger = logging.getLogger('pstf2_logger')


def start_servers():
    """
    Here we start both p0f and an HTTP server in parallel
    :return:
    """

    # start p0f in a different process
    logger.info('Starting p0f...')
    p0f_proc = p0f_wrapper.start_p0f()
    logger.info('p0f started!')

    # start HTTP server in a different thread to allow management of the script
    logger.info('Starting HTTP server...')
    try:
        d = Thread(target=http_server.start_http_server)
        d.setDaemon(True)
        d.start()
        logger.info('HTTP server started!')
        logger.info('If you wish to terminate the server press CTRL+C')
        signal.pause()
    except KeyboardInterrupt:
        logger.info('HTTP server stopped!')

    # kill p0f which was opened in a different process
    try:
        logger.info('Killing p0f...')
        p0f_proc.kill()
        logger.info('p0f killed!')
    except:
        logger.info('can\'t kill p0f!')

    logger.info('exiting...')
