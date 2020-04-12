from configs import *
from http.server import *
from utils import *
from urllib import parse
from ua_parser import user_agent_parser


# Adapted from: https://pymotw.com/3/http.server/
class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """
        Logic for serving HTTP GET requests
        :return:
        """

        # build parsed headers
        headers_to_check = {
            'client_ip_address': self.client_address[0],
            'parsed_path': parse.urlparse(self.path),  # get either path or query here
            'command': format(self.command),
            'request_version': format(self.request_version),
        }

        for name, value in sorted(self.headers.items()):
            headers_to_check[name] = value.rstrip()

        headers_to_check['parsed_ua'] = user_agent_parser.Parse(self.headers['User-Agent'])

        # request parsing is done, now do blacklist checks
        is_blacklisted = blacklist_checks.do_checks(headers_to_check)

        # if detected security service act nicely else serve EICAR as PoC
        if is_blacklisted:
            formal_print('serving benign content')
            message = 'Nothing to see here'
            self.send_response(200)
            self.send_header('Content-Type',
                             'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))
        else:
            formal_print('serving malicious content')
            message = eicar_text
            self.send_response(200)
            self.send_header('Content-Type',
                             'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))
        formal_print('content served')


def start_http_server(server_class=HTTPServer, handler_class=GetHandler):
    """
    Initialize the server, will be started in a differnt thread than p0f so it will co-exist
    :param server_class: standard python HTTP server
    :param handler_class: our custom GET handler
    :return:
    """
    server_address = ('', http_server_port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
