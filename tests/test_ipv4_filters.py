#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import unittest

from cfgtemplater.extensions import ip_filters


class IPv4FiltersTests(unittest.TestCase):

    def test_ipv4_first_address(self):
        self.assertEqual(ip_filters.first_address('192.0.2.0/24'), "192.0.2.1/24")
        self.assertEqual(ip_filters.first_address('192.0.2.100'), "192.0.2.100/32")
        self.assertEqual(ip_filters.first_address('192.0.2.1/31'), "192.0.2.0/31")

    def test_ipv4_last_address(self):
        self.assertEqual(ip_filters.last_address('192.0.2.0/24'), "192.0.2.254/24")
        self.assertEqual(ip_filters.last_address('192.0.2.100'), "192.0.2.100/32")
        self.assertEqual(ip_filters.last_address('192.0.2.0/31'), "192.0.2.1/31")

    def test_ipv4_network(self):
        self.assertEqual(ip_filters.network('192.0.2.100/24'), "192.0.2.0/24")
        self.assertEqual(ip_filters.network('192.0.2.100'), "192.0.2.100/32")
        self.assertEqual(ip_filters.network('192.0.2.1/31'), "192.0.2.0/31")

    def test_ipv4_broadcast(self):
        self.assertEqual(ip_filters.broadcast('192.0.2.100/24'), "192.0.2.255/24")
        self.assertEqual(ip_filters.broadcast('192.0.2.100'), "192.0.2.100/32")
        self.assertEqual(ip_filters.broadcast('192.0.2.0/31'), "192.0.2.1/31")

    def test_ipv4_prefixlen(self):
        self.assertEqual(ip_filters.prefixlen('192.0.2.100'), "32")
        self.assertEqual(ip_filters.prefixlen('192.0.2.0/24'), "24")

    def test_ipv4_netmask(self):
        self.assertEqual(ip_filters.netmask('192.0.2.100/32'), "255.255.255.255")
        self.assertEqual(ip_filters.netmask('192.0.2.100/24'), "255.255.255.0")
        self.assertEqual(ip_filters.netmask('192.0.2.100/22'), "255.255.252.0")

    def test_ipv4_hostmask(self):
        self.assertEqual(ip_filters.hostmask('192.0.2.100/32'), "0.0.0.0")
        self.assertEqual(ip_filters.hostmask('192.0.2.100/24'), "0.0.0.255")
        self.assertEqual(ip_filters.hostmask('192.0.2.100/22'), "0.0.3.255")

    def test_ipv4_compress(self):
        self.assertEqual(ip_filters.compress('192.000.002.100/32'), "192.0.2.100")
        self.assertEqual(ip_filters.compress('192.000.002.100/24'), "192.0.2.100")

    def test_ipv4_uncompress(self):
        self.assertEqual(ip_filters.uncompress('192.0.2.100/32'), "192.000.002.100")
        self.assertEqual(ip_filters.uncompress('192.0.002.100/24'), "192.000.002.100")

    def test_ipv4_octets(self):
        self.assertEqual(ip_filters.octets('192.0.2.100'), [192, 0, 2, 100])
        self.assertEqual(ip_filters.octets('192.0.2.100/24'), [192, 0, 2, 100])

    def test_ipv4_address(self):
        self.assertEqual(ip_filters.address('192.0.2.100'), "192.0.2.100")
        self.assertEqual(ip_filters.address('192.0.2.100/32'), "192.0.2.100")
