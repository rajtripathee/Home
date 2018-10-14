#
# TO DO: Detect Different RaspberryPi Platform
#

import re

UNKNOWN     = 0
PI          = 1

def version():
    with open("/proc/cpuinfo", "r") as infile:
        cpuinfo = infile.read()
    
    match = re.search("^Hardware\s+:\s+(\w+)$", cpuinfo, flags=re.MULTILINE | re.IGNORECASE)

    if not match:
        return None
    if match.group(1) == "BCM2835":
        return 1
    if match.group(1) == "BCM2836":
        return 2
    if match.group(1) == "BCM2837":
        return 3
    else:
        return None
 
def revision():
    with open("/proc/cpuinfo", "r") as infile:
        for line in infile:
            match = re.match('Revision\s+:\s+.*(\w{4})$', line, flags=re.IGNORECASE)
            if match and match.group(1) in ['0002', '0003', '0010', '0011', '0014', '1040', '20a0']:
                return 1.0
            if match and match.group(1) in ['0012', '0015', '1041', '0021', '00c1']:
                return 1.1
            if match and match.group(1) in ['0013', '2042', '0032','0092', '2082']:
                return 1.2
            if match and match.group(1) in ['0093', '20d3']:
                return 1.3
            elif match:
                return 2.0
    raise RuntimeError("PI revision could not be determined.")


def detect_platform():
    pi = version()
    if pi is not None:
        return PI
    
    # Returns UNKNOWN if platform could not be determined.
    return UNKNOWN
    