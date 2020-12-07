#!/usr/bin/python3

"""Command line tool for Motion Blinds."""

import argparse
import asyncio
import errno
import logging

import motion_blinds

SERVER_MULTICAST = "238.0.0.18"

# Define command line arguments
parser = argparse.ArgumentParser(
    description="Command line tool for Google Nest SDM API"
)
#parser.add_argument("--token", required=False, help="Device token")
parser.add_argument("--ip", default=SERVER_MULTICAST, required=False, help="Device ip address")
parser.add_argument("--key", required=True, help="Device key")
parser.add_argument(
    "-v", "--verbose", help="Increase output verbosity", action="store_true"
)

cmd_parser = parser.add_subparsers(dest="command", required=True)
list_devices_parser = cmd_parser.add_parser("list_devices")

async def RunTool(args):
    gateway = motion_blinds.MotionGateway(
        ip=args.ip,
        key=args.key)
    if args.command == "list_devices":
        gateway.GetDeviceList()
        gateway.Update()
        for blind in gateway.device_list.values():
            blind.Update()
            print(blind)


def main():
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(RunTool(args))
    loop.close()


if __name__ == "__main__":
    main()
