from p0f import P0f, P0fException
from configs import *
from utils import *


def start_p0f():
    """
    Starts p0f's binary
    :return: ref to the process for closing it later on
    """
    return run(f'{p0f_bin_path} -i {iface} -s {p0f_named_socket} -f {p0f_fp_path}')


def get_p0f_data(ip):
    """
    Wraps p0f's named socket API
    Wrapper module in use is https://pypi.org/project/p0f/

    :param ip: key to query p0f by it
    :return: p0f's aggregated info for the specific ip
    """
    data = None
    p0f = P0f(p0f_named_socket)
    try:
        data = p0f.get_info(ip)
    except P0fException:
        formal_print('P0fException - Invalid query was sent to p0f. Maybe the API has changed?')
    except KeyError:
        formal_print('KeyError - No data is available for this IP address yet')
    except ValueError:
        formal_print('ValueError - p0f returned invalid constant values. Maybe the API has changed?')

    return data
