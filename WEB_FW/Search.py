def web_search(user_input, log_info):
    searched_log_info = []
    
    for log in log_info:
        if str(user_input) in str(log['time']):
            searched_log_info.append(log)
            continue
        elif str(user_input) in str(log['src_ip']):
            searched_log_info.append(log)
        elif str(user_input) in str(log['dst_ip']):
            searched_log_info.append(log)
        elif str(user_input) in str(log['src_port']):
            searched_log_info.append(log)   
        elif str(user_input) in str(log['dst_port']):
            searched_log_info.append(log)

    return searched_log_info
