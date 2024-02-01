from datetime import datetime
from collections import Counter

def get_time_data(processed_log):

    # 각 로그 항목에서 월을 추출
    month_list = [datetime.strptime(log['date_time'], '%b %d %H:%M:%S').strftime('%B') for log in processed_log]

    # Counter 객체를 이용해 각 월의 로그 개수를 계산
    month_counter = Counter(month_list)

    # 월과 로그 개수를 각각의 리스트로 분리
    months = list(month_counter.keys())
    counts = list(month_counter.values())

    # 결과를 반환
    return months, counts

def get_action_data(processed_log):
    allow=0
    deny=0

    for log in processed_log:
        if(log["activity"] == "block"):
            deny+=1
            continue
        elif(log["activity"] == "allow"):
            allow+=1

    return allow, deny

def get_chaining_data(processed_log):

    Input = 0
    Forward = 0
    Output = 0

    for log in processed_log:
        if(log["chain"] == "INPUT"):
            Input+=1
            continue
        elif(log["chain"] == "FORWARD"):
            Forward+=1
            continue

        elif(log["chain"]=="OUTPUT"):
            Output+=1

    return Input, Forward, Output

def get_protocol_data(processed_log):
    Tcp = 0
    Udp = 0
    Icmp = 0

    for log in processed_log:
        if(log["protocol"] == "TCP"):
            Tcp+=1
            continue
        elif(log["protocol"] == "UDP"):
            Udp+=1
            continue
        elif(log["protocol"]=="ICMP"):
            Icmp+=1
    return Tcp, Udp, Icmp

def get_ip_data(processed_log):

    ip_list = []

    # 각 로그 항목에서 IP 주소를 추출
    for log in processed_log:
        ip_list.append(log['src_ip'])
        ip_list.append(log['dst_ip'])

    # Counter 객체를 이용해 각 IP 주소의 등장 횟수를 계산
    ip_counter = Counter(ip_list)

    # 가장 많이 등장한 5개의 IP 주소 추출
    top5_ip = ip_counter.most_common(5)

    # IP 주소와 등장 횟수를 각각의 리스트로 분리
    ip_list = [ip[0] for ip in top5_ip]
    count_list = [ip[1] for ip in top5_ip]

    # 결과를 반환
    return ip_list, count_list