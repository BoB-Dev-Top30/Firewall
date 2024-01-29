
def state_search(state_info, user_input):


    print("state_info", state_info)
    print("user_input", user_input)
    searched_state_info = []
    for state in state_info:
        print("dict", state)
        if str(user_input) in str(state['protocol']):
            searched_state_info.append(state)
            continue
        elif str(user_input) in state['connection_state']:
            searched_state_info.append(state)
            continue
        elif str(user_input) in state['timeout']:
            searched_state_info.append(state)
            continue
        elif str(user_input) in state['src1']:
            searched_state_info.append(state)
            continue
        elif str(user_input) in state['dst1']:
            searched_state_info.append(state)
            continue
        elif str(user_input) in state['sport1']:
            searched_state_info.append(state)
            continue
        elif str(user_input) in state['dport1']:
            searched_state_info.append(state)
            continue
        elif str(user_input) in state['src2']:
            searched_state_info.append(state)
            continue
        elif str(user_input) in state['dst2']:
            searched_state_info.append(state)
            continue
        elif str(user_input) in state['sport2']:
            searched_state_info.append(state)
            continue
        elif str(user_input) in state['dport2']:
            searched_state_info.append(state)
            continue
        elif str(user_input) in state['additional_info']:
            searched_state_info.append(state)
            continue
    return searched_state_info
        

