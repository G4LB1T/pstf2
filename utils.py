import calendar
import datetime
import socket
import subprocess
import time

import configs


def reset_last_time_service_observed():
    configs.last_time_service_observed = calendar.timegm(time.gmtime())


def formal_print(string):
    """
    Just a nicer format for printing strings
    :param string:
    :return:
    """
    print(f'[+] {str(datetime.datetime.now())} {string}')


def run(cmd):
    """
    Wrapper for popen
    :param cmd: cmd to run as a different process
    :return: ref to the popened subprocess
    """
    formal_print(f'Running command:\n\t{cmd}')
    return subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def get_ptr_record(ip):
    """
    :param ip: ipv4 as string
    :return: reversed in-addr-arpa part of the record
    e.g.: for '203.208.60.1' it will return 'crawl-203-208-60-1.googlebot.com'
    where full record is # ('crawl-203-208-60-1.googlebot.com', ['1.60.208.203.in-addr.arpa'], ['203.208.60.1'])
    """
    return socket.gethostbyaddr(ip)[0]


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
