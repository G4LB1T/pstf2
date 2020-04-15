from functools import lru_cache
from cymruwhois import Client
import yaml

with open("lib/fingerprinting/fingerprints.yml", "r") as ymlfile:
    fingerprints_config = yaml.load(ymlfile, Loader=yaml.FullLoader)


@lru_cache(maxsize=fingerprints_config['asn_cache_size'])
def get_asn(ip):
    """
    Gets asnum for ip using Cymru's API
    (https://pythonhosted.org/cymruwhois/api.html)
    Stores in cache for future use using the lru_cache decorator
    :param ip:
    :return: asnum info
    """

    client = Client()
    result = client.lookup(ip)

    return result.asn
