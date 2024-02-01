import re
from datetime import datetime
from collections import Counter


def web_parse_logs(filename):
    xss_log = []
    sql_injection_log = []
    xss_log_count = 0
    sql_injection_log_count = 0
    time_counter = Counter()

    with open(filename, 'r') as file:
        for line in file:
            if 'XSS' in line or 'SQL Injection' in line:
                time_search = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
                time = datetime.strptime(time_search.group(), '%Y-%m-%d %H:%M:%S') if time_search else None

                if time:
                    month_key = time.strftime('%Y-%m')
                    time_counter[month_key] += 1

                src_ip_search = re.search(r'소스 IP: ([\d\.]+)', line)
                src_ip = src_ip_search.group(1) if src_ip_search else None

                dst_ip_search = re.search(r'목적지 IP: ([\d\.]+)', line)
                dst_ip = dst_ip_search.group(1) if dst_ip_search else None

                src_port_search = re.search(r'소스 포트: (\d+)', line)
                src_port = int(src_port_search.group(1)) if src_port_search else None

                dst_port_search = re.search(r'목적지 포트: (\d+)', line)
                dst_port = int(dst_port_search.group(1)) if dst_port_search else None

                log_entry = {'time': time, 'src_ip': src_ip, 'dst_ip': dst_ip, 'src_port': src_port, 'dst_port': dst_port}

                if 'XSS' in line:
                    xss_log.append(log_entry)
                    xss_log_count += 1
                elif 'SQL Injection' in line:
                    sql_injection_log.append(log_entry)
                    sql_injection_log_count += 1

    time_list = sorted(time_counter.keys())
    time_count_list = [time_counter[month] for month in time_list]

    return xss_log, sql_injection_log, xss_log_count, sql_injection_log_count, time_list, time_count_list