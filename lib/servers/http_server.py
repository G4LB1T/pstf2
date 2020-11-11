from http.server import *
from urllib import parse
from ua_parser import user_agent_parser
import logging
import yaml
import lib.fingerprinting.blacklist_checks as fp

with open("lib/servers/servers_config.yml", "r") as ymlfile:
    servers_config = yaml.load(ymlfile, Loader=yaml.FullLoader)

logger = logging.getLogger('pstf2_logger')


# Adapted from: https://pymotw.com/3/http.server/
class GetHandler(BaseHTTPRequestHandler):
    def parse_headers(self):
        """
        build parsed headers from request
        :return: headers prepared for fingerprinting stage
        """
        #
        parsed_headers = {
            'client_ip_address': self.client_address[0],
            'parsed_path': parse.urlparse(self.path),  # get either path or query here
            'command': format(self.command),
            'request_version': format(self.request_version),
        }

        for name, value in sorted(self.headers.items()):
            parsed_headers[name] = value.rstrip()

        parsed_headers['parsed_ua'] = user_agent_parser.Parse(self.headers['User-Agent'])

        return parsed_headers

    def do_GET(self):
        """
        Logic for serving HTTP GET requests
        :return:
        """

        headers_to_check = self.parse_headers()

        # request parsing is done, now do blacklist checks
        is_blacklisted = fp.do_checks(headers_to_check)

        # if detected security service act nicely else serve EICAR as PoC
        if is_blacklisted:
            if servers_config['web_server']['rickroll_mode']:
                rickroll_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
                self.send_response(302)
                self.send_header('Location', rickroll_url)
                self.end_headers()
                pass
            else:
                logger.info('serving benign content')
                message = servers_config['web_server']['benign_text']
                self.send_response(200)
                self.send_header('Content-Type',
                                 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(message.encode('utf-8'))
        else:
            logger.info('serving malicious content')
            message = servers_config['web_server']['eicar_text_a'] + servers_config['web_server']['eicar_text_b']
            self.send_response(200)
            self.send_header('Content-Type',
                             'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))
        logger.info('content served')


def start_http_server(server_class=HTTPServer, handler_class=GetHandler):
    """
    Initialize the server, will be started in a differnt thread than p0f so it will co-exist
    :param do_rickroll:
    :param malicious_response:
    :param benign_response:
    :param server_class: standard python HTTP server
    :param handler_class: our custom GET handler
    :return:
    """
    server_address = ('', int(servers_config['web_server']['http_server_port']))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
