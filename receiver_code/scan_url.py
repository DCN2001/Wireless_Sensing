from bluepy.btle import Scanner

def decode_url(encoded_url):
    # Eddystone URL schemes
    schemes = ["http://www.", "https://www.", "http://", "https://"]
    # Eddystone URL extensions
    extensions = [".com/", ".org/", ".edu/", ".net/", ".info/", ".biz/", ".gov/",
                  ".com", ".org", ".edu", ".net", ".info", ".biz", ".gov"]

    # Convert the hexadecimal value to bytes
    url_bytes = bytes.fromhex(encoded_url[6:])  # Skipping the first 6 characters (aafe10)

    # Decode the scheme
    scheme_index = url_bytes[1]
    if scheme_index >= len(schemes):
        raise ValueError("Invalid URL scheme index")
    decoded_url = schemes[scheme_index]
   
    # Decode the rest of the URL
    for byte in url_bytes[2:]:
        if byte <= 0x20:  # Extension indicator
            if byte < len(extensions):
                # Check if we are not adding the same extension twice
                if not decoded_url.endswith(tuple(extensions)):
                    decoded_url += extensions[byte]
            else:
                raise ValueError("Invalid URL extension")
        else:
            decoded_url += chr(byte)

    return decoded_url

def scanning():
    scanner = Scanner()
    print("Scanning....")
    while True:
        devices = scanner.scan(10.0)  # Scans for 10 seconds
        for dev in devices:
            for (adtype, desc, value) in dev.getScanData():
                if adtype == 0X16 and value.startswith('aafe10'):
                    MAC = dev.addr.upper()
                    url = decode_url(value)
                    return  MAC, url


#--------------------------------------------------------------------
if __name__ == "__main__":
    MAC, url = scanning()
    print(f"Find URL Beacon from MAC: {MAC} {url}")
