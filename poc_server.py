from utils import *
import http_server
from threading import Thread
import signal
import p0f_wrapper

'''
Main entry point for starting the project
Here we start both p0f and an HTTP server in parallel
'''

if __name__ == '__main__':
    # start p0f in a different process
    formal_print('Starting p0f...')
    p0f_proc = p0f_wrapper.start_p0f()
    formal_print('p0f started!')

    # start HTTP server in a different thread to allow management of the script
    formal_print('Starting HTTP server...')
    try:
        d = Thread(target=http_server.start_http_server)
        d.setDaemon(True)
        d.start()
        formal_print('HTTP server started!')
        formal_print('If you wish to terminate the server press CTRL+C')
        signal.pause()
    except KeyboardInterrupt:
        formal_print('HTTP server stopped!')

    # kill p0f which was opened in a different process
    formal_print('Killing p0f...')
    p0f_proc.kill()
    formal_print('p0f killed!')
