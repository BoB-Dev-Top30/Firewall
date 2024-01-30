
import ipaddress

def rule_matches_ip(user_ip, iptables_ip):
    # iptables 규칙이 모든 IP 주소를 의미하는 '0.0.0.0'인 경우
    if iptables_ip == '0.0.0.0/0':
        return True

    # iptables 규칙이 CIDR 표기법을 사용하는 경우
    elif '/' in iptables_ip:
        net = ipaddress.ip_network(iptables_ip)
        return ipaddress.ip_address(user_ip) in net
    # iptables 규칙이 단일 IP 주소를 지정하는 경우
    else:
        return user_ip == iptables_ip

def rule_matches_port(user_port, iptables_port):

    if iptables_port == "*":
        return True

    elif user_port == iptables_port.lower():
        return True

    else:
        return False

def rule_matches_protocol(user_protocol, iptables_protocol):
    if iptables_protocol == "all":
        return True
    elif user_protocol== iptables_protocol.lower():
        return True
    return False

def Match_Rule(packet, iptables_chains):


    matched_chain={"INPUT":[], "FORWARD":[], "OUTPUT":[]}
    matched_list = []
    unmatched_list = []

    for chain, rules in iptables_chains.items():
        for rule in rules:
            print(rule)
            if rule_matches_ip(packet["src_ip"], rule['src_ip']):
                if rule_matches_ip(packet["dst_ip"], rule['dst_ip']):
                    if rule_matches_port(packet["src_port"], rule['src_port']):
                        if rule_matches_port(packet["dst_port"], rule['dst_port']):
                            if rule_matches_protocol(packet["protocol"], rule['protocol']):
                                matched_list.append(rule)
                            else:
                                unmatched_list.append(rule)
                        else:
                            unmatched_list.append(rule)
                    else:
                        unmatched_list.append(rule)
                else:
                    unmatched_list.append(rule)
            else:
                unmatched_list.append(rule)
    print("매치된 리스트", matched_list)
    matched_chain[chain] = matched_list
    matched_chain_num = len(matched_chain["INPUT"]) + len(matched_chain["FORWARD"]) + len(matched_chain["OUTPUT"]) 
        
    unmatched_chain = matched_chain.copy()
    unmatched_chain[chain] = unmatched_list        
    unmatched_chain_num = len(unmatched_chain["INPUT"]) + len(unmatched_chain["FORWARD"]) + len(unmatched_chain["OUTPUT"]) 

    return matched_chain, unmatched_chain, matched_chain_num, unmatched_chain_num
