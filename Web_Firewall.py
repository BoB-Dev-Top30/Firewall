from netfilterqueue import NetfilterQueue
import scapy.all as scapy
import re
from collections import defaultdict


######자체제작 패키지와 모듈########
from WEB_FW.DP_Sql_Injection import *
from WEB_FW.DP_Xss import *
##################################

import logging
logging.basicConfig(filename="http_traffic.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def process_packet(packet):
    attack_counter = defaultdict(int)
    scapy_packet = scapy.IP(packet.get_payload())


    src_ip = scapy_packet[scapy.IP].src
    dst_ip = scapy_packet[scapy.IP].dst
    src_port = scapy_packet[scapy.TCP].sport
    dst_port = scapy_packet[scapy.TCP].dport

    # 프로토콜 정보 추출
    protocol = scapy_packet[scapy.IP].proto
    protocol_name = scapy_packet[scapy.IP].sprintf("%IP.proto%")

    if scapy_packet.haslayer(scapy.TCP) and scapy_packet.haslayer(scapy.Raw):
        payload = scapy_packet[scapy.Raw].load.decode(errors="ignore")
        if "HTTP" in payload:
            print("I GOT HTTP")
            if "GET" in payload:
                print("I GOT GET")

            if "POST" in payload:
                print("I GOT POST")

            # XSS 공격 패턴
            payload, xss_detected = DP_Xss(payload)

            # SQL 인젝션 공격 패턴
            payload, sql_detected = DP_Sql_Injection(payload)
            print(xss_detected)
            if xss_detected or sql_detected:
                print("I GOT ATTACK")
                # 공격 카운터 증가
                attack_key = (src_ip, dst_ip, src_port, dst_port, protocol_name, "XSS" if xss_detected else "SQL Injection")
                attack_counter[attack_key] += 1

                print("전달여부", xss_detected)
                # 로그에 공격 정보 기록
                try:
                    logging.info(f"공격 타입: {'XSS' if xss_detected else 'SQL Injection'}, 소스 IP: {src_ip}, 목적지 IP: {dst_ip}, 소스 포트: {src_port}, 목적지 포트: {dst_port}, 프로토콜: {protocol_name}, 공격 횟수: {attack_counter[attack_key]}")
                except Exception as e:
                    logging.error(f"Error processing packet: {e}")
            
            # 바뀐 안전한 패킷으로 수정
            scapy_packet[scapy.Raw].load = payload.encode()
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.TCP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(99, process_packet)

try:
    nfqueue.run()
except KeyboardInterrupt:
    nfqueue.unbind()

