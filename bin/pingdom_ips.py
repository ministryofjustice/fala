#!/usr/bin/env python3
import re
import requests
import sys


def get_pingdom_probe_ips():
    """
    Fetches the current list of Pingdom IPv4 probe addresses and returns them
    as a list of CIDR strings (/32).

    This list is used to allowlist Pingdom health-check traffic at the ingress
    level. The endpoint queried is public and this function is invoked during
    deployment only (not at runtime), so request volume is very low
    (typically tens of calls per hour at peak). As a result, rate limiting is
    not expected to be an issue in practice.

    Returns:
        list[str]: A list of IPv4 CIDR strings (e.g. "1.2.3.4/32").
    """
    ip_list = []
    pingdom_link = "https://my.pingdom.com/probes/ipv4"
    pingdom_ips = requests.get(pingdom_link).text.split()
    parsed_pingdom_ip_list = ["".join([ip.strip(), "/32"]) for ip in pingdom_ips]
    regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/32$"

    for ip in parsed_pingdom_ip_list:
        if re.match(regex, ip) is not None:
            ip_list.append(ip)
    return ip_list


if __name__ == "__main__":
    ips = r"\,".join(get_pingdom_probe_ips())
    sys.stdout.write(ips)
