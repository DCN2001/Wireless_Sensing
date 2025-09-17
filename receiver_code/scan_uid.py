from bluepy.btle import Scanner

def decode_uid(encoded_uid):
    # Convert the hexadecimal value to bytes
    uid_bytes = bytes.fromhex(encoded_uid[6:])  # Skipping the first 6 characters (aafe00)
    
    # Extract the Namespace (10 bytes) and Instance (6 bytes)
    
    namespace = uid_bytes[1:11].hex().lower()
    instance = uid_bytes[11:17].hex().lower()

    return namespace, instance

def scanning():
    scanner = Scanner()
    print("Scanning for Eddystone-UID...")
    while True:
        devices = scanner.scan(10.0)  # Scans for 10 seconds
        for dev in devices:
            for (adtype, desc, value) in dev.getScanData():
                if adtype == 0X16 and value.startswith('aafe00'):  # Eddystone-UID starts with 'aafe00'
                    MAC = dev.addr.upper()
                    namespace, instance = decode_uid(value)
                    return MAC, namespace, instance

#--------------------------------------------------------------------
if __name__ == "__main__":
    MAC, namespace, instance = scanning()
    print(f"Find Eddystone-UID Beacon from MAC: {MAC}")
    print(f"Namespace: {namespace}")
    print(f"Instance: {instance}")
