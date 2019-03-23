import ipaddress

def is_ip(addr):
    try:
        ipaddress.ip_interface(addr)
        return True
    except:
        return False

def is_ipv4(addr):
    try:
        ipaddress.IPv4Interface(addr)
        return True
    except:
        return False

def is_ipv6(addr):
    try:
        ipaddress.IPv6Interface(addr)
        return True
    except:
        return False

def is_ip_net(addr):
    try:
        ipaddress.ip_network(addr)
        return True
    except:
        return False

def is_ipv4_net(addr):
    try:
        ipaddress.IPv4Network(addr)
        return True
    except:
        return False

def is_ipv6_net(addr):
    try:
        ipaddress.IPv6Network(addr)
        return True
    except:
        return False
