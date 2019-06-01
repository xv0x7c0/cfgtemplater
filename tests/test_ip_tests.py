import unittest

from cfgtemplater.extensions import ip_tests


class IPTests(unittest.TestCase):
    def test_is_ip(self):
        self.assertTrue(ip_tests.is_ip("192.0.2.0/24"))
        self.assertTrue(ip_tests.is_ip("192.0.2.0"))
        self.assertTrue(ip_tests.is_ip("2001:db8::1/128"))
        self.assertFalse(ip_tests.is_ip("blah"))

    def test_is_ipv4(self):
        self.assertTrue(ip_tests.is_ipv4("192.0.2.0/24"))
        self.assertTrue(ip_tests.is_ipv4("192.0.2.0"))
        self.assertFalse(ip_tests.is_ipv4("2001:db8::1/128"))
        self.assertFalse(ip_tests.is_ipv4("blah"))

    def test_is_ipv4_net(self):
        self.assertTrue(ip_tests.is_ipv4_net("192.0.2.0/24"))
        self.assertFalse(ip_tests.is_ipv4_net("192.0.2.1/24"))
        self.assertTrue(ip_tests.is_ipv6("2001:db8::1/128"))
        self.assertFalse(ip_tests.is_ipv6("blah"))

    def test_is_ipv4_net2(self):
        self.assertTrue(ip_tests.is_ipv4_net("192.0.2.0/24"))
        self.assertFalse(ip_tests.is_ipv4_net("192.0.2.1/24"))
        self.assertFalse(ip_tests.is_ipv4_net("2001:db8::1/128"))
        self.assertFalse(ip_tests.is_ipv4_net("blah"))

    def test_is_ipv6(self):
        self.assertFalse(ip_tests.is_ipv6("192.0.2.0/24"))
        self.assertFalse(ip_tests.is_ipv6("192.0.2.0"))
        self.assertTrue(ip_tests.is_ipv6("2001:db8::1/128"))
        self.assertFalse(ip_tests.is_ipv6("blah"))

    def test_is_ip_net(self):
        # /32 (IPv4) & /128 (IPv6) are considered valid networks
        self.assertTrue(ip_tests.is_ip_net("192.0.2.0/24"))
        self.assertFalse(ip_tests.is_ip_net("192.0.2.1/24"))
        self.assertTrue(ip_tests.is_ip_net("2001:db8::1/128"))
        self.assertTrue(ip_tests.is_ip_net("2001:db8::/127"))
        self.assertFalse(ip_tests.is_ip_net("blah"))

    def test_is_ipv6_net(self):
        self.assertFalse(ip_tests.is_ipv6_net("192.0.2.0/24"))
        self.assertFalse(ip_tests.is_ipv6_net("192.0.2.1/24"))
        self.assertTrue(ip_tests.is_ipv6_net("2001:db8::/127"))
        self.assertFalse(ip_tests.is_ipv6_net("2001:db8::1/127"))
        self.assertFalse(ip_tests.is_ipv6_net("blah"))

    def test_is_ipv4_host(self):
        self.assertTrue(ip_tests.is_ipv4_host("192.0.2.1/24"))
        self.assertFalse(ip_tests.is_ipv4_host("192.0.2.0/24"))
        self.assertFalse(ip_tests.is_ipv4_host("192.0.2.255/24"))
        self.assertFalse(ip_tests.is_ipv4_host("blah"))
