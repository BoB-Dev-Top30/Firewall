import re

# 상태정보 파싱에서 자료구조에 insert
def conntrack_parser(state_info):
    network_states = []

    # 각 줄을 순회하며 파싱
    for line in state_info.strip().split('\n'):
        parts = line.split()
        print("this is parts", parts)
        if(len(parts)==0):
            network_state = {
            'protocol':"",
            'connection_state': "",
            'timeout': "",
            'src1': "",
            'dst1': "",
            'sport1': "",
            'dport1': "",
            'src2': "",
            'dst2': "",
            'sport2': "",
            'dport2': "",
            'additional_info': "",
        }
        else:
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
    # 정규 표현식을 사용하지 않고 문자열 메서드로 정보를 추출하는 함수
    def extract_info_without_regex(line):
        parts = line.split()
        date_time = f"{parts[0]} {parts[1]} {parts[2]}"
        chain_activity = line.split("network_log_")[1].split(":")[0].split("_")
        chain = chain_activity[0].upper()  # 체인 (INPUT, FORWARD, OUTPUT)
        activity = chain_activity[1]  # 활동 (block, allow 등)

        src_ip = dst_ip = protocol = ""
        packet_length = 0
        for part in parts:
            if part.startswith("SRC="):
                src_ip = part.split("=")[1]
            elif part.startswith("DST="):
                dst_ip = part.split("=")[1]
            elif part.startswith("LEN="):
                packet_length = int(part.split("=")[1])
            elif part.startswith("PROTO="):
                protocol = part.split("=")[1]

        return {
            "date_time": date_time,
            "chain": chain,
            "activity": activity,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "packet_length": str(packet_length),  # 문자열로 변환
            "protocol": protocol,
        }

    parsed_data_list = []

    for line in log_info.strip().split('\n'):
        # 정규 표현식 대신 문자열 메서드를 사용해 로그 라인에서 정보 추출
        parsed_data = extract_info_without_regex(line)
        parsed_data_list.append(parsed_data)

    return parsed_data_list
