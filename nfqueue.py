from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw

nfqueue = NetfilterQueue()


def packet_handler(packet):
    print("Packet processed:", packet)

    # print("RAW DATA", packet.get_payload())
    
    # ip헤더 tcp헤더 파싱
    ip_packet = IP(packet.get_payload())
    print("소스IP: ", ip_packet.src)
    print("목적지IP: ", ip_packet.dst)

    tcp_header = ip_packet[TCP]
    print("소스포트: ", tcp_header.sport)
    print("목적지포트: ", tcp_header.dport)

    if ip_packet.haslayer(Raw):
        payload = ip_packet[Raw].load
        modified_payload = payload.replace(b"bob", b"BOB")
        ip_packet[Raw].load = modified_payload
        packet.set_payload(bytes(ip_packet))

    # http_request = IP(dst=target_url) / TCP(dport=80) / Raw(load="GET / HTTP/q.q\r\nHOST: {}\r\n\r\n".format(target_url))
    # print("HTTP 요청:", http_request)

    # 이 패킷을 어떻게 할거냐??
    # packet.drop()
    packet.accept()

# 만든 큐를 커널에 등록 해야함
# 0번 큐에 nfqueue를 등록하고 패킷이 다믹면 packet_handler를 호출해주세요
nfqueue.bind(0, packet_handler)

# 이 코드 실행 후 대기...
nfqueue.run()

# 여기까지 오면 종료
print("종료중...")
nfqueue.unbind()
