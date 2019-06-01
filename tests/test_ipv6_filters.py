import unittest

from cfgtemplater.extensions import ip_filters


class IPTests(unittest.TestCase):
    def test_ipv6_first_address(self):
        self.assertEqual(ip_filters.first_address("2001:db8::/127"), "2001:db8::/127")
        self.assertEqual(
            ip_filters.first_address("2001:db8::100/120"), "2001:db8::101/120"
        )  # wrong?
        self.assertEqual(ip_filters.first_address("2001:db8::1/128"), "2001:db8::1/128")

    def test_ipv6_last_address(self):
        self.assertEqual(ip_filters.last_address("2001:db8::/127"), "2001:db8::1/127")
        self.assertEqual(
            ip_filters.last_address("2001:db8::100/120"), "2001:db8::1ff/120"
        )
        self.assertEqual(ip_filters.last_address("2001:db8::1/128"), "2001:db8::1/128")

    def test_ipv6_network(self):
        self.assertEqual(ip_filters.network("2001:db8::1/127"), "2001:db8::/127")
        self.assertEqual(ip_filters.network("2001:db8::110/120"), "2001:db8::100/120")
        self.assertEqual(ip_filters.network("2001:db8::1/128"), "2001:db8::1/128")

    def test_ipv6_broadcast(self):
        self.assertEqual(ip_filters.broadcast("2001:db8::/127"), "2001:db8::1/127")
        self.assertEqual(ip_filters.broadcast("2001:db8::110/120"), "2001:db8::1ff/120")
        self.assertEqual(ip_filters.broadcast("2001:db8::1/128"), "2001:db8::1/128")

    def test_ipv6_prefixlen(self):
        self.assertEqual(ip_filters.prefixlen("2001:db8::/127"), "127")
        self.assertEqual(ip_filters.prefixlen("2001:db8::110/120"), "120")

    def test_ipv6_netmask(self):
        self.assertEqual(ip_filters.prefixlen("2001:db8::/127"), "127")
        self.assertEqual(ip_filters.prefixlen("2001:db8::110/120"), "120")

    def test_ipv6_hostmask(self):
        self.assertEqual(ip_filters.hostmask("2001:db8::/127"), "::1")
        self.assertEqual(ip_filters.hostmask("2001:db8::110/120"), "::ff")

    def test_ipv6_compress(self):
        self.assertEqual(
            ip_filters.compress("2001:0db8:0000:0000:0000:0000:0000:0001/127"),
            "2001:db8::1",
        )

    def test_ipv6_uncompress(self):
        self.assertEqual(
            ip_filters.uncompress("2001:db8::1"),
            "2001:0db8:0000:0000:0000:0000:0000:0001",
        )

    def test_ipv6_hextets(self):
        self.assertEqual(
            ip_filters.hextets("2001:db8::1"),
            ["2001", "0db8", "0000", "0000", "0000", "0000", "0000", "0001"],
        )

    def test_ipv6_address(self):
        self.assertEqual(ip_filters.address("2001:db8::110/120"), "2001:db8::110")
        self.assertEqual(ip_filters.address("2001:db8::110"), "2001:db8::110")
