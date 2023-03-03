import re
from ipaddress import IPv4Network


class CidrMaskConvert:
    def cidr_to_mask(self, cidr_value):
        if cidr_value == '0' or cidr_value == '32':  # ToDo: Check other invalid CIRD values
            return 'Invalid'

        try:
            # Let's use IPv4Network to convert from CIRD to IP mask. The `192.168.1.0/` address could be any valid IP address.
            network = IPv4Network('192.168.1.0/' + str(cidr_value), False)
            mask = str(network.netmask)  # Convert from IPv4Network class to String
        except Exception as e:
            print(f"CIDR to Mask conversion failed with error {e}.")
            return 'Invalid'

        return mask


    def mask_to_cidr(self, mask):
        if mask == '0.0.0.0' or mask == '255.255.255.255':  # ToDo: Check other invalid IP masks
            return 'Invalid'

        try:
            network = IPv4Network('192.168.1.0/' + str(mask), False)
            cird_value = str(network.prefixlen)
        except Exception as e:
            print(f"Mask to CIDR conversion failed with error {e}.")
            return 'Invalid'

        return cird_value


class IpValidate:
    def ipv4_validation(self, ip_address):
        try:
            network = IPv4Network(str(ip_address), False)
        except Exception as e:
            print(f"WARNING: IP address is not valid: {e}.")
            return False
        
        return True
