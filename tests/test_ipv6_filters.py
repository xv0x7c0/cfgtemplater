from cfgtemplater.extensions import ip_filters

def test_ipv6_first_address():
    assert ip_filters.first_address('2001:db8::/127') == "2001:db8::/127"
    assert ip_filters.first_address('2001:db8::100/120') == "2001:db8::101/120" # wrong?
    assert ip_filters.first_address('2001:db8::1/128') == "2001:db8::1/128"

def test_ipv6_last_address():
    assert ip_filters.last_address('2001:db8::/127') == "2001:db8::1/127"
    assert ip_filters.last_address('2001:db8::100/120') == "2001:db8::1ff/120"
    assert ip_filters.last_address('2001:db8::1/128') == "2001:db8::1/128"

def test_ipv6_network():
    assert ip_filters.network('2001:db8::1/127') == "2001:db8::/127"
    assert ip_filters.network('2001:db8::110/120') == "2001:db8::100/120"
    assert ip_filters.network('2001:db8::1/128') == "2001:db8::1/128"

def test_ipv6_broadcast():
    assert ip_filters.broadcast('2001:db8::/127') == "2001:db8::1/127"
    assert ip_filters.broadcast('2001:db8::110/120') == "2001:db8::1ff/120"
    assert ip_filters.broadcast('2001:db8::1/128') == "2001:db8::1/128"

def test_ipv6_prefixlen():
    assert ip_filters.prefixlen('2001:db8::/127') == "127"
    assert ip_filters.prefixlen('2001:db8::110/120') == "120"

def test_ipv6_netmask():
    assert ip_filters.prefixlen('2001:db8::/127') == "127"
    assert ip_filters.prefixlen('2001:db8::110/120') == "120"

def test_ipv6_hostmask():
    assert ip_filters.hostmask('2001:db8::/127') == "::1"
    assert ip_filters.hostmask('2001:db8::110/120') == "::ff"

def test_ipv6_compress():
    assert ip_filters.compress('2001:0db8:0000:0000:0000:0000:0000:0001/127') == "2001:db8::1"

def test_ipv6_uncompress():
    assert ip_filters.uncompress('2001:db8::1') == "2001:0db8:0000:0000:0000:0000:0000:0001"

def test_ipv6_hextets():
    assert ip_filters.hextets('2001:db8::1') == ["2001", "0db8", "0000", "0000", "0000", "0000", "0000" , "0001"]

def test_ipv6_address():
    assert ip_filters.address('2001:db8::110/120') == "2001:db8::110"
    assert ip_filters.address('2001:db8::110') == "2001:db8::110"
