import socket
import struct

def format_mac(mac_bytes):
    return ":".join(f"{b:02x}" for b in mac_bytes)

def decode_addr(addr):
    return {
        "interface": addr[0],
        "ethertype": hex(addr[1]),
        "packet_type": addr[2],
        "hardware_type": addr[3],
        "mac": ":".join(f"{b:02x}" for b in addr[4])
    }
    
def decode_ip_addr(ip_bytes):
    return socket.inet_ntoa(ip_bytes)

def decode_ethernet(frame):
    eth_header = frame[:14]
    dest_mac, src_mac, eth_type = struct.unpack("!6s6sH", eth_header)

    return {
        "dest_mac": format_mac(dest_mac),
        "src_mac": format_mac(src_mac),
        "eth_type": eth_type
    }

def decode_ip(frame):
    ip_start = 14
    version_ihl = frame[ip_start]
    ihl = (version_ihl & 0x0F) * 4

    ip_header = frame[ip_start:ip_start + ihl]
    iph = struct.unpack("!BBHHHBBH4s4s", ip_header)

    return {
        "ihl": ihl,
        "ttl": iph[5],
        "protocol": iph[6],
        "src_ip": decode_ip_addr(iph[8]),
        "dst_ip": decode_ip_addr(iph[9]),
        "payload_start": ip_start + ihl
    }

def decode_icmp(frame, start):
    icmp_header = frame[start:start + 4]
    icmp_type, code, checksum = struct.unpack("!BBH", icmp_header)
    data = frame[start + 4:]

    return {
        "type": icmp_type,
        "code": code,
        "data": data
    }

def decode_udp(frame, start):
    udp_header = frame[start:start + 8]
    src_port, dst_port, length, checksum = struct.unpack("!HHHH", udp_header)
    data = frame[start + 8:]

    return {
        "src_port": src_port,
        "dst_port": dst_port,
        "data": data
    }

def decode_tcp(frame, start):
    tcp_header = frame[start:start + 20]
    tcph = struct.unpack("!HHLLBBHHH", tcp_header)

    data_offset = (tcph[4] >> 4) * 4
    data = frame[start + data_offset:]

    return {
        "src_port": tcph[0],
        "dst_port": tcph[1],
        "flags": tcph[5],
        "data": data
    }

def decode_packet(frame,prot):
    eth = decode_ethernet(frame)

    print("\n[ Ethernet ]")
    print(" Dest MAC :", eth["dest_mac"])
    print(" Src MAC  :", eth["src_mac"])
    print(" Type     :", hex(eth["eth_type"]))

    if eth["eth_type"] != 0x0800:
        print(" Not IPv4 packet")
        return

    ip = decode_ip(frame)
    filter_packets(ip,prot,frame)

def print_icmp(ip,prot,frame):
    icmp = decode_icmp(frame, ip["payload_start"])
    print("\n[ ICMP ]")
    print(" Type :", icmp["type"])
    print(" Code :", icmp["code"])
    
def print_udp(ip,prot,frame):
    udp = decode_udp(frame, ip["payload_start"])
    print("\n[ UDP ]")
    print(" Src Port :", udp["src_port"])
    print(" Dst Port :", udp["dst_port"])
    print(" Payload  :", udp["data"].hex())
    
def print_tcp(ip,prot,frame):
    tcp = decode_tcp(frame, ip["payload_start"])
    flages = str(tcp["flags"])
    print("\n[ TCP ]")
    print(" Src Port :", tcp["src_port"])
    print(" Dst Port :", tcp["dst_port"])
    print(" Flags    :", bin(tcp["flags"]))
    
    if (flages & 0x08) and (flages & 0x10) and tcp["data"]:
        data = tcp["data"]
        if len(data) >= 3 and data[0] == 0x16 and data[1] == 0x03:
            return "[ ENCRYPTED (TLS) ]"

        printable = sum(1 for b in data if 32 <= b <= 126)
        ratio = printable / len(data)

        if ratio > 0.7:
            return data.decode("ascii", errors="ignore")
        else:
            return "[ ENCRYPTED ]"

def filter_packets(ip,prot,frame):
    if ip["protocol"] != prot:
        return
    print("\n[ IP ]")
    print(" Src IP   :", ip["src_ip"])
    print(" Dst IP   :", ip["dst_ip"])
    print(" Protocol :", ip["protocol"])
    print(" TTL      :", ip["ttl"])
    
    if prot == 1:
        print_icmp(ip,prot,frame)
    elif prot == 6:
        print_tcp(ip,prot,frame)
    elif prot == 17:
        print_udp(ip,prot,frame)
    else:
        print(" Unknown protocol")
    
def main():
    sniffer = socket.socket(
        socket.AF_PACKET,
        socket.SOCK_RAW,
        socket.htons(0x0800)
    )
    prot_dict = {
        1:"icmp",
        17:"udmp",
        6:"tcp"
    }
    print("PACKAGE SNIFFER : ")
    # sour_ip
    # tar_ip
    print("choose an prtocol to capture : ")
    for pro in prot_dict:
        print(f"{pro} | {prot_dict[pro]}")
    prot = int(input("Enter the protocol no : "))
    
    if(prot not in prot_dict.keys()):
        print("invalid port number....")
        return
    
    sniffer.bind(("lo", 0))
    print("🦈 Sniffer running...\n")

    while True:
        frame, addr = sniffer.recvfrom(65535)
        decode_packet(frame,prot)
        print(decode_addr(addr))
main()