def parse_iptables(output):
    lines = output.split('\n')
    chains = {'INPUT': [], 'FORWARD': [], 'OUTPUT': []}
    current_chain = None

    for line in lines:
        if line.startswith('Chain'):
            parts = line.split()
            current_chain = parts[1] if len(parts) > 1 else None
        elif line and current_chain in chains and not line.startswith('pkts') and "target" not in line:
            rule_parts = line.split()
            if len(rule_parts) > 4:  # 기본적인 규칙 형식 확인 (번호 포함)
                parsed_rule = {
                    'num': rule_parts[0],  # 규칙 번호 추가
                    'packets': rule_parts[1],
                    'bytes': rule_parts[2],
                    'target': rule_parts[3],
                    'protocol': rule_parts[4],
                    'opt': rule_parts[5],
                    'in': rule_parts[6],
                    'out': rule_parts[7],
                    'source': rule_parts[8],
                    'destination': rule_parts[9],
                    'details': ' '.join(rule_parts[10:])
                }
                chains[current_chain].append(parsed_rule)

    return chains

