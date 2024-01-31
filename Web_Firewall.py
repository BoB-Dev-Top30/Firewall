from netfilterqueue import NetfilterQueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.TCP) and scapy_packet.haslayer(scapy.Raw):
        # HTTP 요청인지 확인
        if "HTTP" in scapy_packet[scapy.Raw].load.decode():
            # POST 요청인지 확인
            if "POST" in scapy_packet[scapy.Raw].load.decode():
                # POST 요청 데이터 처리
                print("POST 요청 발견:", scapy_packet[scapy.Raw].load.decode())

    packet.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(0, process_packet)  # 0번 큐에 바인딩

try:
    nfqueue.run()
except KeyboardInterrupt:
    nfqueue.unbind()
