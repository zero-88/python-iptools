#!/usr/bin/python

import argparse
import logging
from iptools import IpRange, IpRangeList


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--command", action="store", default="info", choices=["info", "in"], help="Command")
parser.add_argument("-i", "--ip", action="store", required=True, nargs='+', type=str, help="IP/CIDR address")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose log")
args = parser.parse_args()
logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, handlers=[logging.StreamHandler()],
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("ip_tool")

logger.debug("-" * 50)
logger.debug(args.command)
logger.debug(args.ip)
logger.debug("-" * 50)


def __convert(ips):
    for ip in ips:
        yield IpRange(ip)


def __check(source: IpRange, dest: IpRange)->bool:
    logger.debug(source)
    logger.debug(dest)
    return dest[0] in source and dest[1] in source if len(dest) > 1 else True


try:
    if args.command == "info":
        ip_range = IpRange(args.ip[0], args.ip[1] if len(args.ip) > 1 else None)
        logger.info("IP range:  %s", ip_range)
        logger.info("Size:      %s", len(ip_range))
    else:
        if len(args.ip) < 2:
            raise AttributeError("At least 2 IPs")
        gen = __convert(args.ip)
        first_one = next(gen)
        for i, n in enumerate(gen, 1):
            logger.info("%s in %s: %s", args.ip[i], args.ip[0], __check(first_one, n))
    exit(0)
except Exception:
    logger.error("Error when executing", exc_info=1)
    exit(1)
