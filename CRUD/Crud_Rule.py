
def Process_Priority(rule, processed_rule):

    if(rule["priority"] == "special"):
        processed_rule += " -I"

    else:
        processed_rule += " -A"
    return processed_rule

def Process_Traffic(rule, processed_rule):
    if(rule["traffic_type"]=="input"):
        processed_rule+=" INPUT"

    elif(rule["traffic_type"]=="forward"):
        processed_rule+=" FORWARD"

    else:
        processed_rule+=" OUTPUT"
    return processed_rule

def Process_Protocol(rule, processed_rule):
    if(rule["protocol"]!=""):
        processed_rule=" -p "+rule["protocol"]
    return processed_rule

def Process_Ip(rule, processed_rule):
    if(rule["src_ip"]!=""):
            processed_rule+=" -s " + rule["src_ip"]
    if(rule["dst_ip"]!=""):
            processed_rule+=" -d " + rule["dst_ip"]
    return processed_rule


def Process_Port(rule,  processed_rule):
    if(rule["src_port"]!=""):
        processed_rule+= " --sport " + rule["src_port"]
    if(rule["dst_port"]!=""):
        processed_rule+= " --dport " + rule["dst_port"]
    return processed_rule

'''
def Process_Interface(rule):
    if(rule["in_interface"]!=""):
            rule+=" -i " + rule["in_interface"]
    if(rule["out_interface"]!=""):
            rule+=" -o " + rule["out_interface"]
    if((rule["out_interface"]!="") and (rule["in_interface"]!="")):
            rule+=" -i " + rule["in_interface"] + rule+=" -o " + rule["out_interface"]

    return rule
'''

def Process_Action(rule, processed_rule):
    if(rule["action"]=="block"):
        processed_rule += " -j DROP"
    else:
        processed_rule += " -j ACCEPT"
    return processed_rule

def Process_Rule(rule):
    
    processed_rule=""

    processed_rule1 = Process_Priority(rule, processed_rule)
    processed_rule2 = Process_Traffic(rule, processed_rule)
    processed_rule3 = Process_Protocol(rule, processed_rule)
    processed_rule4 = Process_Ip(rule, processed_rule)
    processed_rule5 = Process_Port(rule, processed_rule)
    processed_rule6 = Process_Action(rule, processed_rule)

    processed_rule = processed_rule1 + processed_rule2 + processed_rule3 + processed_rule4 +processed_rule5 + processed_rule6
    print("모듈에서 생성한 rule: ", processed_rule)
    return processed_rule

    
    


    
