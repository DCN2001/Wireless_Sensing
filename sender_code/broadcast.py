import subprocess
import signal
import sys
import os
import argparse


def get_bluetooth_mac():
    # Get Bluetooth MAC using hciconfig
    result = os.popen('hciconfig | grep "BD Address"').read()
    
    # Extract MAC address from the output
    mac_address = result.split()[2] if result else None
    return mac_address

def stop_advertising(signal, frame):
    """Stops the URL advertising when interrupted."""
    print("\nStopping advertising...")
    subprocess.call("sudo hcitool -i hci0 cmd 0x08 0x000a 00 > /dev/null 2>&1", shell=True)  # Stop advertising
    sys.exit(0)
    
    
def advertise_url(url):
    """Advertise a URL using Eddystone-URL format."""
    
    # URL encoding
    def encode_url(url):
        schemes = ["http://www.", "https://www.", "http://", "https://"]
        extensions = [".com/", ".org/", ".edu/", ".net/", ".info/", ".biz/", ".gov/", ".com", ".org", ".edu", ".net", ".info", ".biz", ".gov"]

        data = []
        i = 0

        # URL Scheme
        for s, scheme in enumerate(schemes):
            if url.startswith(scheme):
                data.append(s)
                i += len(scheme)
                break
        else:
            raise ValueError("Invalid URL scheme")

        # URL encoding
        while i < len(url):
            if url[i] == '.':
                for e, ext in enumerate(extensions):
                    if url.startswith(ext, i):
                        data.append(e)
                        i += len(ext)
                        break
                else:
                    data.append(0x2E)  # ASCII for '.'
                    i += 1
            else:
                data.append(ord(url[i]))  # ASCII value of the character
                i += 1

        return data

    # Encode URL
    data = encode_url(url)
    
    # Eddystone packet
    payload = [
        0x02, 0x01, 0x06,  # Flags
        0x03, 0x03, 0xAA, 0xFE,  # Eddystone UUID
        len(data) + 5,  # Service Data length
        0x16, 0xAA, 0xFE, 0x10,  # Frame type and URL frame
        0x00  # Tx power level
    ]
    payload.extend(data)

    # Complete message and pad to 32 bytes
    message = [len(payload)] + payload + [0x00] * (32 - len(payload) - 1)
    message_hex = " ".join(f"{x:02x}" for x in message)

    # Using hcitools to control Bluetooth 
    subprocess.call("sudo hciconfig hci0 up > /dev/null 2>&1", shell=True)
    subprocess.call("sudo hcitool -i hci0 cmd 0x08 0x000a 00 > /dev/null 2>&1", shell=True)  # Stop previous advertising
    subprocess.call(f"sudo hcitool -i hci0 cmd 0x08 0x0008 {message_hex} > /dev/null 2>&1", shell=True)  # Set advertising
    subprocess.call("sudo hcitool -i hci0 cmd 0x08 0x000a 01 > /dev/null 2>&1", shell=True)  # Start advertising
	
	#Showing the broadcasting info 
    MAC = get_bluetooth_mac()
    print(f"MAC address: {MAC}")
    print(f"URL: {url}")
    print("Press Ctrl+C to stop.")
    
    # Keep advertising until interrupted
    signal.signal(signal.SIGINT, stop_advertising)
    signal.pause()
    
    
#--------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, default="http://www.nut.com/", help="Type in the URL you want to broadcast")
    args = parser.parse_args()

    advertise_url(args.url)
