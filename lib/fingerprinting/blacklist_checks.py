from lib.servers.p0f_wrapper import get_p0f_data
from lib.utils import *
from time import sleep
from lib.fingerprinting.asn_checker import get_asn
import time
import calendar
import yaml
import logging

with open("lib/fingerprinting/fingerprints.yml", "r") as ymlfile:
    fingerprints_config = yaml.load(ymlfile, Loader=yaml.FullLoader)

logger = logging.getLogger('pstf2_logger')

last_time_service_observed = 0


def reset_last_time_service_observed():
    """
    Resets the timer for last time we've observed a service to evade from
    :return:
    """
    global last_time_service_observed
    last_time_service_observed = calendar.timegm(time.gmtime())


def do_checks(request):
    """
    Main routine for sending to the different checks
    :param request:
    :return: True iff request matches blacklist patterns
    """
    client_ip = request['client_ip_address']

    logger.info('Getting asn data...')
    try:
        request['asn'] = get_asn(client_ip)
        logger.info('asn data received!')

    except:
        request['asn'] = 'No ASN data is available'
        logger.info('Failed getting asn data')

    # configurable, due to the fact that it does perform somewhat active fingerprinting
    if fingerprints_config['allow_reverse_dns']:
        logger.info('Getting reverse DNS data...')
        request['ptr_record'] = get_ptr_record(client_ip)
        logger.info('Reverse DNS data received!')

    logger.info('Getting p0f data...')
    p0f_data = {}

    # polling and waiting to get p0f data
    while p0f_data == {} or p0f_data is None:
        p0f_data = get_p0f_data(client_ip)
        sleep(0.01)

    logger.info('p0f data received!')

    for key in p0f_data:
        if p0f_data[key]:
            val = p0f_data[key]
            if type(val) == bytes:
                val = val.decode("utf-8").rstrip('\x00')
            p0f_data[key] = str(val).lower()

    request['p0f_data'] = p0f_data

    if any([
        # vendor specific tests
        check_virus_total_ua(request),
        # check_vendor_a(request)
        # check_vendor_b(request)

        # generic tests
        check_link_is_ethernet(request),
        check_last_sec_service_observed_timeout(),
        check_obsolete_browser_version(request),
        check_os_mismatches(request),
        check_blacklist_asn(request)
    ]):
        # reset timer and return True
        reset_last_time_service_observed()
        return True
    else:
        return False


'''
Specific fingerprint detection
'''


def check_virus_total_ua(request):
    """

    :param request:
    :return: true iff VirusTotal request is received
    """
    if 'user_agent' in request and 'virustotalcloud' in request['user_agent'].lower():
        logger.info('Got Request from VirusTotal!')
        return True
    else:
        return False

# can be extended, left as "an exercise for the reader"...
# def check_vendor_a(request):
#     return 'vendor_a_name' in request['ptr_record'].lower() and check_os_mismatches(request)
#
#
# def check_vendor_b(request):
#     return 'vendor_b_name' in request['user_agent'].lower() and check_os_mismatches(request)




'''
Generic fingerprint detection
'''


def check_blacklist_asn(request):
    """
    Is the ASN suspicious?
    :param request:
    :return: True iff ASN hints it is a security tool
    """
    if request['asn'] in fingerprints_config['blacklisted_asns']:
        asn = request['asn']
        logger.info(f'ASN {asn} is in blacklist!')
        return True
    else:
        return False


def check_link_is_ethernet(request):
    """
    Checks if the MTU value is atypical
    :param request: the HTTP GET headers
    :return: True iff MTU value is suspicious
    """
    if 'link_type' in request['p0f_data'] and request['p0f_data']['link_type'] not in ['ethernet or modem', 'dsl']:
        mtu_val = request['p0f_data']['link_type']
        logger.info(f'Unusual MTU detected, value was typical to {mtu_val} connection!')
        return True
    else:
        return False


def check_os_mismatches(request):
    """
    Compare the declared OS and TCP metadata OS
    Uses get_os_string to transform to a canonical form
    :param request: the HTTP GET headers
    :return: True iff UA and TCP disagree on the client's OS
    """
    p0f_os = get_os_string(request['p0f_data']['os_name'])
    ua_os = get_os_string(request['parsed_ua']['os']['family'])

    # some tolerance is allowed to allow inaccurate mobile useragent to match p0f's signature
    if p0f_os == ua_os or (p0f_os  == 'android' and ua_os == 'linux') or (p0f_os  == 'ios' and ua_os == 'mac'):
        return False
    else:
        logger.info(f'p0f OS string was typical to {p0f_os} while ua header was typical to {ua_os}!')
        return True


def check_obsolete_browser_version(request):
    """
    Detect implementations where developers neglected to update their code to reflect contemporary browser versions
    :param request:
    :return: True iff the version in the request is less than the one defined in the configuration
    """
    try:
        browser_type = request['parsed_ua']['user_agent']['family']
        request_version = int(request['parsed_ua']['user_agent']['major'])
        min_allowed_version = fingerprints_config['browser_versions_thresholds'][browser_type]

        if request_version < min_allowed_version:
            logger.info(f'Browser version was too low! Type: {browser_type}, request version: {request_version}, '
                        f'minimal version allowed: {min_allowed_version}')
            return True
        else:
            return False
    except:
        # catch errors on UA parsing or illegal major versions
        return False


def check_last_sec_service_observed_timeout():
    """

    :return: True iff we've recently seen a service checking our server
    """
    current_time = calendar.timegm(time.gmtime())
    timeout = fingerprints_config['blacklist_service_observed_timeout']
    if current_time < last_time_service_observed + int(timeout):
        logger.info(f'Server is currently under cooldown period, saw a scanner less than {timeout} seconds ago.')
        logger.info(f'Normal operations will resume in {str(current_time - last_time_service_observed)} seconds.')
        return True
    else:
        return False
