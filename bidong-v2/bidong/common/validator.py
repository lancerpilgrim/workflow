import re
import ipaddress


MOBILE_PATTERN = re.compile(
    r'^(?:13[0-9]|14[57]|15[0-35-9]|17[01678]|18[0-9])\d{8}$')

MAC_ADDRESS_PATTERN = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')


def check_mobile(mobile):
    return True if re.match(MOBILE_PATTERN, mobile) else False


def check_mac_address(mac):
    return True if re.match(MAC_ADDRESS_PATTERN, mac) else False


def check_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    return True
