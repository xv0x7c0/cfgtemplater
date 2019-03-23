from cfgtemplater.extensions import ip_filters

def test_ipv4_first_address():
    assert ip_filters.first_address('192.0.2.0/24') == "192.0.2.1/24"
    assert ip_filters.first_address('192.0.2.100') == "192.0.2.100/32"
    assert ip_filters.first_address('192.0.2.1/31') == "192.0.2.0/31"

def test_ipv4_last_address():
    assert ip_filters.last_address('192.0.2.0/24') == "192.0.2.254/24"
    assert ip_filters.last_address('192.0.2.100') == "192.0.2.100/32"
    assert ip_filters.last_address('192.0.2.0/31') == "192.0.2.1/31"

def test_ipv4_network():
    assert ip_filters.network('192.0.2.100/24') == "192.0.2.0/24"
    assert ip_filters.network('192.0.2.100') == "192.0.2.100/32"
    assert ip_filters.network('192.0.2.1/31') == "192.0.2.0/31"

def test_ipv4_broadcast():
    assert ip_filters.broadcast('192.0.2.100/24') == "192.0.2.255/24"
    assert ip_filters.broadcast('192.0.2.100') == "192.0.2.100/32"
    assert ip_filters.broadcast('192.0.2.0/31') == "192.0.2.1/31"

def test_ipv4_prefixlen():
    assert ip_filters.prefixlen('192.0.2.100') == "32"
    assert ip_filters.prefixlen('192.0.2.0/24') == "24"

def test_ipv4_netmask():
    assert ip_filters.netmask('192.0.2.100/32') == "255.255.255.255"
    assert ip_filters.netmask('192.0.2.100/24') == "255.255.255.0"
    assert ip_filters.netmask('192.0.2.100/22') == "255.255.252.0"

def test_ipv4_hostmask():
    assert ip_filters.hostmask('192.0.2.100/32') == "0.0.0.0"
    assert ip_filters.hostmask('192.0.2.100/24') == "0.0.0.255"
    assert ip_filters.hostmask('192.0.2.100/22') == "0.0.3.255"

def test_ipv4_compress():
    assert ip_filters.compress('192.000.002.100/32') == "192.0.2.100"
    assert ip_filters.compress('192.000.002.100/24') == "192.0.2.100"

def test_ipv4_uncompress():
    assert ip_filters.uncompress('192.0.2.100/32') == "192.000.002.100"
    assert ip_filters.uncompress('192.0.002.100/24') == "192.000.002.100"

def test_ipv4_octets():
    assert ip_filters.octets('192.0.2.100') == [192, 0, 2, 100]
    assert ip_filters.octets('192.0.2.100/24') == [192, 0, 2, 100]

def test_ipv4_address():
    assert ip_filters.address('192.0.2.100') == "192.0.2.100"
    assert ip_filters.address('192.0.2.100/32') == "192.0.2.100"
