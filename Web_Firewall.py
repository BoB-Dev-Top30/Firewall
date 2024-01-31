from netfilterqueue import NetfilterQueue
import scapy.all as scapy
import re


######자체제작 패키지와 모듈########
from WEB_FW.DP_Sql-Injection import *
from WEB_FW.Xss import *
##################################

import logging
logging.basicConfig(filename="http_traffic.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.TCP) and scapy_packet.haslayer(scapy.Raw):
        payload = scapy_packet[scapy.Raw].load.decode(errors="ignore")
        
        if "HTTP" in payload:
            payload가 데이터임
            # XSS 공격 패턴
            payload = DP-Xss(payload)

            # SQL 인젝션 공격 패턴
            payload = DP-Sql-Injection(payload)
            
            # 패킷 수정
            scapy_packet[scapy.Raw].load = payload.encode()
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.TCP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(0, process_packet)

try:
    nfqueue.run()
except KeyboardInterrupt:
    nfqueue.unbind()

