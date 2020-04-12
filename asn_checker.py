from cymruwhois import Client

# saves API calls by caching resolutions on our malicious server
cache_buff = {}


def get_asn(ip):
    """
    Gets asnum for ip using Cymru's API
    (https://pythonhosted.org/cymruwhois/api.html)
    Stores in cache for future use
    :param ip:
    :return: asnum info
    """
    if ip in cache_buff:
        return cache_buff[ip]
    else:
        c = Client()
        r = c.lookup(ip)

        res = r.asn
        cache_buff[ip] = res

        return res
