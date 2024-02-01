
def state_search(state_info, user_input):


    print("state_info", state_info)
    print("user_input", user_input)
    searched_state_info = []
    for state in state_info:
        print("dict", state)
        if str(user_input) in str(state['protocol']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in str(state['connection_state']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in str(state['timeout']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in str(state['src1']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in str(state['dst1']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in str(state['sport1']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in str(state['dport1']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in str(state['src2']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in str(state['dst2']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in str(state['sport2']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in str(state['dport2']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in str(state['additional_info']):
            searched_state_info.append(state)
            continue
    return searched_state_info

def log_search(log_info, user_input):
    searched_log_info = []
    
    for log in log_info:
        if str(user_input) in str(log['date_time']):
            searched_log_info.append(log)
            continue
        elif str(user_input) in str(log['chain']):
            searched_log_info.append(log)
        elif str(user_input) in str(log['activity']):
            searched_log_info.append(log)
        elif str(user_input) in str(log['src_ip']):
            searched_log_info.append(log)
        elif str(user_input) in str(log['dst_ip']):
            searched_log_info.append(log)
        elif str(user_input) in str(log['packet_length']):
            searched_log_info.append(log)   
        elif str(user_input) in str(log['protocol']):
            searched_log_info.append(log)

    return searched_log_info
        

