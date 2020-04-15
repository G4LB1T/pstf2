from lib.servers import start_servers
from lib.utils import start_logger

'''
Main entry point for starting the project
'''

# TODO: add arg parser
if __name__ == '__main__':
    start_logger()
    start_servers()
