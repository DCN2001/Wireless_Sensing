import subprocess
import signal
import sys
import argparse
import os



def get_bluetooth_mac():
    # Get Bluetooth MAC using hciconfig
    result = os.popen('hciconfig | grep "BD Address"').read()
    
    # Extract MAC address from the output
    mac_address = result.split()[2] if result else None
    return mac_address

def stop_broadcast(signal, frame):
    """Stops the Eddystone UID broadcast when interrupted."""
    print("\nStopping broadcast...")
    subprocess.call("sudo hcitool -i hci0 cmd 0x08 0x000a 00 > /dev/null 2>&1", shell=True)
    sys.exit(0)

def broadcast_uid(args):
    uid_namespace = args.namespace
    uid_instance = args.instance
    
    # Eddystone-UID payload
    payload = [
        0x02, 0x01, 0x06,  # Flags
        0x03, 0x03, 0xaa, 0xfe,  # Eddystone UUID
        0x17,  # Service Data length
        0x16, 0xaa, 0xfe,  # Frame type
        0x00,  # UID Frame type (0x00)
        0xed,  # Tx power level
    ]
    
    payload.extend(int(uid_namespace[i:i+2], 16) for i in range(0, len(uid_namespace), 2))
    payload.extend(int(uid_instance[i:i+2], 16) for i in range(0, len(uid_instance), 2))
    payload.extend([0x00] * 2)  # RFU

    message = [len(payload)] + payload
    message_hex = " ".join(f"{x:02x}" for x in message)

    # Send broadcast command
    subprocess.call("sudo hciconfig hci0 up > /dev/null 2>&1", shell=True)
    subprocess.call(f"sudo hcitool -i hci0 cmd 0x08 0x0008 {message_hex} > /dev/null 2>&1", shell=True)
    subprocess.call("sudo hcitool -i hci0 cmd 0x08 0x000a 01> /dev/null 2>&1", shell=True)

    # Handle signal to stop broadcasting
    signal.signal(signal.SIGINT, stop_broadcast)

    #Show info
    MAC = get_bluetooth_mac()
    print("Broadcasting Eddystone UID. Press Ctrl+C to stop.")
    print(f"MAC address: {MAC}")
    print(f"namespace: {args.namespace}   instance: {args.instance}")

    # Stop broadcasting
    signal.pause()


#--------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--namespace", type=str, default="aaaa456789abcdefaaaa", help="Type in the namespace")
    parser.add_argument("--instance", type=str, default="456789abcdef", help="Type in the instance")
    args = parser.parse_args()

    broadcast_uid(args)
