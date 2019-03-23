from cfgtemplater.extensions import ip_tests

def test_is_ip():
    assert ip_tests.is_ip('192.0.2.0/24') == True
    assert ip_tests.is_ip('192.0.2.0') == True
    assert ip_tests.is_ip('2001::1/128') == True
    assert ip_tests.is_ip('blah') == False

def test_is_ipv4():
    assert ip_tests.is_ipv4('192.0.2.0/24') == True
    assert ip_tests.is_ipv4('192.0.2.0') == True
    assert ip_tests.is_ipv4('2001::1/128') == False
    assert ip_tests.is_ipv4('blah') == False

def test_is_ipv4_net():
    assert ip_tests.is_ipv4_net('192.0.2.0/24') == True
    assert ip_tests.is_ipv4_net('192.0.2.1/24') == False
    assert ip_tests.is_ipv6('2001::1/128') == False 
    assert ip_tests.is_ipv6('blah') == False

def test_is_ipv6():
    assert ip_tests.is_ipv6('192.0.2.0/24') == False
    assert ip_tests.is_ipv6('192.0.2.0') == False
    assert ip_tests.is_ipv6('2001::1/128') == True
    assert ip_tests.is_ipv6('blah') == False

def test_is_ip_net():
    # /32 (IPv4) & /128 (IPv6) are considered valid networks
    assert ip_tests.is_ip_net('192.0.2.0/24') == True
    assert ip_tests.is_ip_net('192.0.2.1/24') == False
    assert ip_tests.is_ip_net('2001::1/128') ==True 
    assert ip_tests.is_ip_net('2001::/127') == True
    assert ip_tests.is_ip_net('blah') == False

def test_is_ipv4_net():
    assert ip_tests.is_ipv4_net('192.0.2.0/24') == True
    assert ip_tests.is_ipv4_net('192.0.2.1/24') == False
    assert ip_tests.is_ipv4_net('2001::1/128') == False 
    assert ip_tests.is_ipv4_net('blah') == False

def test_is_ipv6_net():
    assert ip_tests.is_ipv6_net('192.0.2.0/24') == False
    assert ip_tests.is_ipv6_net('192.0.2.1/24') == False
    assert ip_tests.is_ipv6_net('2001::/127') == True
    assert ip_tests.is_ipv6_net('blah') == False
