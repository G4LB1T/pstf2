import yaml
import argparse
from lib.servers import start_servers
from lib.utils import start_logger, print_banner

with open("lib/servers/servers_config.yml", "r") as ymlfile:
    servers_config = yaml.load(ymlfile, Loader=yaml.FullLoader)

'''
Main entry point for starting the project
'''

if __name__ == '__main__':
    print_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('--p0f_bin_path', default=servers_config["p0f_config"]["p0f_bin_path"])
    parser.add_argument('--p0f_fp_path', default=servers_config["p0f_config"]["p0f_fp_path"])
    parser.add_argument('--p0f_iface', default=servers_config["p0f_config"]["iface"])

    args = parser.parse_args()

    start_logger()
    start_servers(args.p0f_bin_path, args.p0f_fp_path, args.p0f_iface)
