from p0f import P0f, P0fException
from lib.utils import *
import logging
import yaml

logger = logging.getLogger('pstf2_logger')

with open("lib/servers/servers_config.yml", "r") as ymlfile:
    servers_config = yaml.load(ymlfile, Loader=yaml.FullLoader)


def start_p0f(p0f_bin_path, p0f_fp_path, p0f_iface):
    """
    Starts p0f's binary
    :return: ref to the process for closing it later on
    """
    return run(f'{p0f_bin_path} '
               f'-i {p0f_iface} '
               f'-s {servers_config["p0f_config"]["p0f_named_socket"]} '
               f'-f {p0f_fp_path}')


def get_p0f_data(ip):
    """
    Wraps p0f's named socket API
    Wrapper module in use is https://pypi.org/project/p0f/

    :param ip: key to query p0f by it
    :return: p0f's aggregated info for the specific ip
    """
    data = None
    p0f_named_socket = servers_config['p0f_config']['p0f_named_socket']

    p0f = P0f(p0f_named_socket)
    try:
        data = p0f.get_info(ip)
    except P0fException:
        logger.info('P0fException - Invalid query was sent to p0f. Maybe the API has changed?')
    except KeyError:
        logger.info('KeyError - No data is available for this IP address yet')
    except ValueError:
        logger.info('ValueError - p0f returned invalid constant values. Maybe the API has changed?')

    return data
