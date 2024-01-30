import re

# 상태정보 파싱에서 자료구조에 insert
def conntrack_parser(state_info):
    network_states = []

    # 각 줄을 순회하며 파싱
    for line in state_info.strip().split('\n'):
        parts = line.split()

        # 각 줄에 대한 정보를 파싱하여 사전으로 저장
        network_state = {
            'protocol': parts[0],
            'connection_state': parts[3],
            'timeout': parts[2],
            'src1': parts[4].split('=')[1],
            'dst1': parts[5].split('=')[1],
            'sport1': parts[6].split('=')[1],
            'dport1': parts[7].split('=')[1],
            'src2': parts[8].split('=')[1],
            'dst2': parts[9].split('=')[1],
            'sport2': parts[10].split('=')[1],
            'dport2': parts[11].split('=')[1],
            'additional_info': ' '.join(parts[12:]),
        }

        network_states.append(network_state)

    return network_states


def log_parser(log_info):
    pattern = r'(\w{3} \d{2} \d{2}:\d{2}:\d{2}).*network_log_(\w+)_(\w+):.*SRC=(\d{1,3}(?:\.\d{1,3}){3}).*DST=(\d{1,3}(?:\.\d{1,3}){3}).*LEN=(\d+).*PROTO=(\w+)'
    
    parsed_data_list=[]

    for line in log_info.strip().split('\n'):
        match = re.search(pattern, line)
        if match:
            date_time = match.group(1)
            chain = match.group(2).upper()  # 체인 (INPUT, FORWARD, OUTPUT)
            activity = match.group(3)  # 활동 (block, allow 등)
            src_ip = match.group(4)
            dst_ip = match.group(5)
            packet_length = match.group(6)
            protocol = match.group(7)

            parsed_data = {
                "date_time": date_time,
                "chain": chain,
                "activity": activity,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "packet_length": packet_length,
                "protocol": protocol,
            }
            parsed_data_list.append(parsed_data)

    return parsed_data_list
