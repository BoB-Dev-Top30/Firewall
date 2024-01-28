def parse_iptables(output):
    lines = output.split('\n')
    chains = {'INPUT': [], 'FORWARD': [], 'OUTPUT': []}
    current_chain = None

    for line in lines:
        if line.startswith('Chain'):
            parts = line.split()
            current_chain = parts[1] if len(parts) > 1 else None
        elif line and current_chain in chains and not line.startswith('pkts'):
            rule_parts = line.split()
            if len(rule_parts) > 3:  # 기본적인 규칙 형식 확인
                parsed_rule = {
                    'packets': rule_parts[0],
                    'bytes': rule_parts[1],
                    'target': rule_parts[2],
                    'protocol': rule_parts[3],
                    'details': ' '.join(rule_parts[4:])
                }
                chains[current_chain].append(parsed_rule)

    return chains