import socket
import time

# Fix Formatting Errors
HOST = "10.0.0.1"  # The server's IP address
PORT = 1024  # Choose a port number within the range of 1024 - 49151
NUMBER_OF_PINGS = 10  # Number of pings to send to the server
CURRENT_PING_NUMBER = 1  # The current ping value
LOST_PACKETS = 0  # The number of packets lost from the simulation
TIMEOUT = 1  # Timeout for receiving a response (1 sec)
min_rtt = float(1.000)
max_rtt = float()
total_rtt = float()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.settimeout(TIMEOUT)

    for CURRENT_PING_NUMBER in range(1, NUMBER_OF_PINGS + 1):
        STRING_PING_NUMBER = str(CURRENT_PING_NUMBER)
        MESSAGE = "Ping ".encode("utf-8")
        client_socket.sendto(MESSAGE, (HOST, PORT))
        TIMER_START = time.time()  # Saves the current time | Will be the starting point

        try:
            data, addr = client_socket.recvfrom(1024)
            TIMER_END = time.time()  # Saves the current time | Will be the ending point
            rtt = round(((TIMER_END - TIMER_START) * 1000), 3)
            STRING_RTT = str(rtt)
            print("Ping " + STRING_PING_NUMBER + ": rtt = " + STRING_RTT + " ms")
            CURRENT_PING_NUMBER += 1

            min_rtt = min(min_rtt, rtt)
            max_rtt = max(max_rtt, rtt)
            total_rtt += rtt

        except socket.timeout:
            print("Ping " + STRING_PING_NUMBER + ": Request timed out")
            LOST_PACKETS += 1
            CURRENT_PING_NUMBER += 1

    min_rtt = round(min_rtt, 3)
    max_rtt = round(max_rtt, 3)
    avg_rtt = round(total_rtt / (NUMBER_OF_PINGS - LOST_PACKETS), 3)
    PACKET_LOSS = round((LOST_PACKETS / NUMBER_OF_PINGS) * 100, 2)
    STRING_MIN_RTT = str(min_rtt)
    STRING_MAX_RTT = str(max_rtt)
    STRING_AVG_RTT = str(avg_rtt)
    STRING_PACKET_LOSS = str(PACKET_LOSS)

    print("\nSummary values:")
    print("min_rtt = " + STRING_MIN_RTT + " ms")
    print("max_rtt = " + STRING_MAX_RTT + " ms")
    print("avg_rtt = " + STRING_AVG_RTT + " ms")
    print("Packet loss: " + STRING_PACKET_LOSS + "%")
