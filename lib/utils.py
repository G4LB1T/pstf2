import socket
import subprocess
import logging

logger = logging.getLogger('pstf2_logger')


def start_logger(lvl=logging.INFO):
    # create logger with 'spam_application'
    logger = logging.getLogger('pstf2_logger')
    logger.setLevel(lvl)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(lvl)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)


def run(cmd):
    """
    Wrapper for popen
    :param cmd: cmd to run as a different process
    :return: ref to the popened subprocess
    """
    logger.info(f'Running command:\n\t{cmd}')
    return subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def get_ptr_record(ip):
    """
    :param ip: ipv4 as string
    :return: reversed in-addr-arpa part of the record
    e.g.: for '203.208.60.1' it will return 'crawl-203-208-60-1.googlebot.com'
    where full record is # ('crawl-203-208-60-1.googlebot.com', ['1.60.208.203.in-addr.arpa'], ['203.208.60.1'])
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        # return an empty string representing the fact there's no PTR record
        return ''


def get_os_string(s):
    """
    :param s: user agent or p0f OS fingerprint
    :return: assumed OS parsed out of the input string
    """
    s = s.lower()
    if 'windows' in s:
        return 'windows'
    elif 'mac' in s:
        return 'mac'
    elif 'android' in s:
        return 'android'
    elif 'linux' in s:
        return 'linux'
    elif 'bsd' in s:
        return 'bsd'
    elif 'ios' in s:
        return 'ios'
    else:
        return 'unknown'


def print_banner():
    """
    Prints an ASCII art pstf^2 banner
    :return: None
    """
    pstf_ascii_banner = '                __  ____//|___ \n    ____  _____/ /_/ __//||__ \\\n   / __ \\/ ___/ __/ /_    __/ /\n  / /_/ (__  ) /_/ __/   / __/ \n / .___/____/\\__/_/     /____/ \n/_/                            \n'
    print('=================================')
    print('=================================')
    print(pstf_ascii_banner)
    print('=================================')
    print('=================================\n')
