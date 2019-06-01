#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import ipaddress
import re


def first_address(addr):
    """Return the first address of a subnet, or self in case of hostaddress
       is given
    """
    ip = ipaddress.ip_interface(addr)
    prefixlen = ip.network.prefixlen
    version = re.sub("Interface", "", ip.__class__.__name__)
    if any(
        [
            (version == "IPv4" and prefixlen == 32),
            (version == "IPv6" and prefixlen == 128),
        ]
    ):
        return str(ip)
    return f"{next(ip.network.hosts())}/{prefixlen}"


def last_address(addr):
    """Return the last address of a subnet, or self in case of hostaddress
       is given
    """
    ip = ipaddress.ip_interface(addr)
    prefixlen = ip.network.prefixlen
    version = re.sub("Interface", "", ip.__class__.__name__)
    if any(
        [
            (version == "IPv4" and prefixlen == 32),
            (version == "IPv6" and prefixlen == 128),
        ]
    ):
        return str(ip)
    return f"{list(ip.network.hosts())[-1]}/{prefixlen}"


def network(addr):
    """Return the network address of an address
    """
    return str(ipaddress.ip_interface(addr).network)


def broadcast(addr):
    """Return the broadcast address of the current network
    """
    ip = ipaddress.ip_interface(addr)
    return f"{ip.network.broadcast_address}/{ip.network.prefixlen}"


def prefixlen(addr):
    """Return the prefix length of an address
    """
    return str(ipaddress.ip_interface(addr).network.prefixlen)


def netmask(addr):
    """Return the netmask of an address
    """
    return str(ipaddress.ip_interface(addr).netmask)


def hostmask(addr):
    """Return the hostmask of an address
    """
    return str(ipaddress.ip_interface(addr).hostmask)


def compress(addr):
    """Return the compressed form of address, removing leading zeroes
    """
    return str(ipaddress.ip_interface(addr).ip.compressed)


def uncompress(addr):
    """Return the uncompressed form of an address, adding leading zeroes
    """
    ip = ipaddress.ip_interface(addr)
    version = re.sub("Interface", "", ip.__class__.__name__)
    if version == "IPv4":
        return ".".join(map(lambda x: "%03d" % int(x), str(ip.ip).split(".")))
    if version == "IPv6":
        return ip.ip.exploded


def octets(addr):
    """Return a list of octets
    """
    ip = ipaddress.IPv4Interface(addr).ip
    return list(map(int, str(ip).split(".")))


def hextets(addr):
    """Return a list of hextets
    """
    ip = ipaddress.IPv6Interface(addr).ip
    return ip.exploded.split(":")


def address(addr):
    """Return an ip adddress
    """
    return str(ipaddress.ip_interface(addr).ip)
