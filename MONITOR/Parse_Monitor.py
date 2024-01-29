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

