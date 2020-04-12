# p0f config
p0f_path = '/Users/gbitensk/work/web_fp/p0f-3.09b'
p0f_bin_path = f'{p0f_path}/p0f'
p0f_fp_path = f'{p0f_path}/p0f.fp'
iface = 'lo0'
p0f_named_socket = '/tmp/p0f_socket'

# HTTP server
http_server_port = 80
# split so won't trigger local AV/"EDR"
eicar_text = 'X5O!P%@AP[4\PZX54(P^)7CC)7}$' + 'EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

# In case a security vendor is detected, provide them with premium benign content
benign_text = 'Never gonna give you up\r\n' \
              'Never gonna let you down\r\n' \
              'Never gonna run around and desert you\r\n' \
              'Never gonna make you cry\r\n' \
              'Never gonna say goodbye\r\n' \
              'Never gonna tell a lie and hurt you\r\n'

# timeout after a service is detected
blacklist_service_observed_timeout = 60 * 5
last_time_service_observed = 0

# Semi-passive fingerprinting, DNS requests might reach to target
allow_reverse_dns = True

blacklisted_asns = [
    # add ASNs for known vendors here
    # e.g. for Google you may add 15169
    '15169',
    '16509'  # AWS etc...
]

# thresholds for browsers
min_browser_versions_allowed = {
    'Chrome': 41,
    'Firefox': 50,
    'Firefox Mobile': 54,
    'IE': 9,
    'Safari': 10,
    'Mobile Safari': 10,
    'Edge': 14

}