from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session, Response
import subprocess
import json
import os
####### 자체 제작 패키지&모듈 ###############
from CRUD.Crud_Rule import *
from CRUD.Parse_Table import *

from MONITOR.Parse_Monitor import *
from MONITOR.Search import *
from MONITOR.Process_Log import *

from DETAIL.Parse_Detail import *
from DETAIL.Match_Algo import *

from WEB_FW.Command import *
from WEB_FW.Process_Log import *
from WEB_FW.Search import *
###############################################

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def home():
    return redirect(url_for('index'))

@app.route("/create", methods=["GET", "POST"])
def create():
    if(request.method=="POST"):
        rule = {"traffic_type":"","action":"", "src_ip":"", "dst_ip":"", "protocol":"", "src_port":"", "dst_port":"", "in_interface":"", "out_interface":""}
        rule["traffic_type"] = request.form.get("traffic_type")
        rule["priority"] = request.form.get("priority")
        rule["action"] = request.form.get("action")
        rule["src_ip"] = request.form.get("src_ip")
        rule["dst_ip"] = request.form.get("dst_ip")
        rule["protocol"] = request.form.get("protocol")
        rule["src_port"] = request.form.get("src_port")
        rule["dst_port"] = request.form.get("dst_port")
        # rule["in_interface"] = request.form.get("in_interface")
        # rule["out_interface"] = request.form.get("out_interface")
        rule["application"] = request.form.get("application")
        
        processed_rule = Process_Create_Rule(rule)
        processed_rule2 = Process_Create_Rule(rule, log=1)

        print("가공된 rule : ", processed_rule)
        

        command = "sudo " + "iptables" + processed_rule
        command2 = "sudo " + "iptables" + processed_rule2 + " --log-prefix " + "network_log" + "_" + str(rule["traffic_type"])+"_"+str(rule["action"])+": "
        
        success = False
        try:
            subprocess.run(command2.split(), check=True)
            subprocess.run(command.split(), check=True)
            
            # 웹 방화벽을 위한 큐로 넘기는 설정 명령어
            web_command(rule["application"], rule["priority"], rule["traffic_type"])
            success = True
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

        return render_template("create.html", success=success)

    return render_template("create.html")

@app.route('/index')
def index():
    success = request.args.get('success', False)
    iptables_output = subprocess.check_output(['sudo', 'iptables', '-nvL', '--line-numbers']).decode('utf-8')
    chains = parse_iptables(iptables_output)
    print("chain입니다.", chains)
    return render_template('index.html', chains=chains, success=success)


@app.route('/delete_rule/<chain_name>', methods=['POST'])
def delete_rule(chain_name):
    selected_rules = request.form.getlist('rule_to_change')

    success = False
    for rule_number in selected_rules:
        try:
            subprocess.run(['sudo', 'iptables', '-D', chain_name, rule_number], check=True)
            success = "delete"
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            # success = False
            break
            # 오류 처리

    return redirect(url_for('index', success=success))

@app.route('/update_rule/<chain_name>', methods=['POST'])
def update_rule(chain_name):
    selected_rules = request.form.getlist('rule_to_change')
    rule_number = selected_rules[0] # 1개만 가능
    return redirect(url_for('update', rule_number =rule_number, chain_name=chain_name))

# 체인이름 전달
@app.route('/unused_rule/<chain_name>', methods=['POST'])
def unused_rule(chain_name):
    
    success=False
    print(chain_name)
    try:
        chain_name = chain_name.upper()
        iptables_output = subprocess.check_output(['sudo', 'iptables', '-nvL', '--line-numbers']).decode('utf-8')
        chains = parse_iptables(iptables_output)
        print(chains)
        
        unused_policy = parse_unused(chains, chain_name)
        success="unused"
        if(len(unused_policy[chain_name])==0):
            success="no-unused"
    except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

    return render_template('index.html', chains=unused_policy, success=success)


@app.route('/update', methods=['GET', 'POST'])
def update():
    rule_number = request.args.get('rule_number')
    chain_name = request.args.get("chain_name")
    print("가지고온 룰 번호", str(rule_number))
    print("가지고온 체인", str(chain_name))
    if request.method == 'POST':
        # post일떄 가져옴
        rule_number = request.form.get('rule_number')
        chain_name = request.form.get("chain_name")
        rule = {"traffic_type":"","action":"", "src_ip":"", "dst_ip":"", "protocol":"", "src_port":"", "dst_port":"", "in_interface":"", "out_interface":""}
        
        #예외
        # rule["traffic_type"] = chain_name
        # rule["priority"] = request.form.get("priority")
        rule["action"] = request.form.get("action")
        rule["src_ip"] = request.form.get("src_ip")
        rule["dst_ip"] = request.form.get("dst_ip")
        rule["protocol"] = request.form.get("protocol")
        rule["src_port"] = request.form.get("src_port")
        rule["dst_port"] = request.form.get("dst_port")
        # rule["in_interface"] = request.form.get("in_interface")
        # rule["out_interface"] = request.form.get("out_interface")
        rule["application"] = request.form.get("application")
        
        processed_rule = Process_Update_Rule(rule)
        processed_rule2 = Process_Update_Rule(rule,log=1)

        print("가공된 rule : ", processed_rule)
        

        command = "sudo " + "iptables " + "-R " + str(chain_name) + " " + str(rule_number) + " " + processed_rule 
        command2 = "sudo " + "iptables " + "-R " + str(chain_name) + " " + str(rule_number) + " " + processed_rule2 + " --log-prefix " + "network_log" + "_" +str(chain_name)+"_"+str(rule["action"])+": "
        print(command)
        success = False
        try:
            subprocess.run(command2.split(), check=True)
            subprocess.run(command.split(), check=True)
            success = True
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

        return render_template("update.html", success=success)
    # 업데이트 로직

    # 겟일때 렌더링
    return render_template("update.html", rule_number=rule_number, chain_name=chain_name) 



@app.route('/network_state', methods=['GET', 'POST'])
def network_state():
    try:
        # allow 한 상태정보만 가지고 오기
        command = "sudo conntrack -L | grep -E 'ESTABLISHED|RELATED' | grep -v '127.0.0.1'"
        state_info = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE)
        state_info = conntrack_parser(state_info.stdout)

        print(state_info)
    except subprocess.CalledProcessError as e:
        state_info = None
        print(f"An error occurred: {e}")
        
    if(request.method=='POST'):
        # 검색기능
        try:
            user_input = request.form.get("user_input")
            print("state:",state_info)
            filtered_state_info = state_search(state_info, user_input)
            success=True
            if len(filtered_state_info)==0:
                print("결과 없음")
                success = "No Answer"
        
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            success=False

        return render_template('network_state.html', state_info=filtered_state_info, success=success)
    
    return render_template('network_state.html', state_info=state_info)


# 로그 테이블 정보
@app.route('/log_more', methods=['GET', 'POST'])
def log_more():
    try:
        # 로그 전체정보 가지고오기
        command = 'grep network_log /var/log/syslog'
        log_info = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        
        processed_log = log_parser(log_info.stdout)
        print("################processed_log###############", processed_log )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    if(request.method=='POST'):
        # 검색기능
        try:
            user_input = request.form.get("user_input")

            filtered_log_info = log_search(processed_log, user_input)
            success=True
            if len(filtered_log_info)==0:
                print("결과 없음")
                success = "No Answer"
        
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            success=False

        return render_template('log_more.html', log_info=filtered_log_info, success=success)
        
    
    return render_template('log_more.html', log_info=processed_log)

# 로그 테이블 찍는 api
@app.route('/api/log')
def api_log():
    try:
        # 로그 전체정보 가지고오기
        command = 'grep network_log /var/log/syslog'
        log_info = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        
        print("log_info\n",log_info.stdout)
        processed_log = log_parser(log_info.stdout)
        print("processed_log in api\n", processed_log)

        # 날짜별 데이터
        time_list, time_count_list = get_time_data(processed_log)

        # 허용.차단 데이터
        allow, deny = get_action_data(processed_log)

        # chaining 데이터
        Input, Forward, Output = get_chaining_data(processed_log)

        # protocol 데이터
        Tcp, Udp, Icmp = get_protocol_data(processed_log)

        # ip 데이터
        ip_list, ip_count_list = get_ip_data(processed_log)
        print(ip_list)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    data = {
    "time": {
        "labels": time_list,
        "values": time_count_list
    },

    "action": {
        "labels": ["Allow", "Deny"],
        "values": [allow, deny]
    },
    
    "chaining": {
        "labels": ["Input", "Forward", "Output"],
        "values": [Input, Forward, Output]
    },
    
    "protocol": {
        "labels": ["Tcp", "Udp", "Icmp"],
        "values": [Tcp, Udp, Icmp]
    },
    
    "ip": {
        "labels": ip_list,
        "values": ip_count_list
    },

    }
    return jsonify(data)

@app.route('/log', methods=['GET'])
def log():

    return render_template('log.html')

# Ajax로 막대그래프 (매치된거와 안매치된거)
@app.route('/packet_simulate', methods=["GET","POST"])
def packet_simulate():

    if(request.method == "POST"):
        print(request.data)
        data = request.json  # AJAX 요청에서 JSON 데이터를 딕셔너리로 받음
        print(data)
        src_ip = str(data.get('src_ip'))
        dst_ip = str(data.get('dst_ip'))
        src_port = str(data.get('src_port'))
        dst_port = str(data.get('dst_port'))
        protocol = str(data.get('protocol'))

        print(data)
        packet = {"src_ip":"", "dst_ip":"", "src_port":"", "dst_port":"", "protocol":""}
        packet["src_ip"] = src_ip
        packet["dst_ip"] =  dst_ip
        packet["src_port"] =  src_port
        packet["dst_port"] =  dst_port
        packet["protocol"] =  protocol

        print("생성된 패킷", packet)

        iptables_output = subprocess.check_output(['sudo', 'iptables', '-nvL', '--line-numbers']).decode('utf-8')
        
        chains = parse_iptables(iptables_output)
        
        matched_chain, unmatched_chain, matched_chain_num, unmatched_chain_num = Match_Rule(packet, chains)

        print("matched", matched_chain)

        
        data = {
            "labels" : ["Matched", "Un-Matched"],
            "values" : [matched_chain_num, unmatched_chain_num],
            "original_values" : [matched_chain, unmatched_chain]
            }

        json_data = json.dumps(data, sort_keys=False)
        return Response(json_data, mimetype='application/json')
    return render_template("packet_simulate.html")

@app.route('/matched', methods=['POST'])
def matched():
    data = request.get_json()  # AJAX 요청에서 JSON 데이터를 딕셔너리로 받음
    chains = data['original_values']
    print("/matched에서의 chains", chains)
    json_data = json.dumps({'chains': chains}, sort_keys=False)
    return Response(json_data, mimetype='application/json')

@app.route('/unmatched', methods=['POST'])
def unmatched():
    data = request.get_json()  # AJAX 요청에서 JSON 데이터를 딕셔너리로 받음
    chains = data['original_values']
    print("/unmatched에서의 chains", chains)
    json_data = json.dumps({'chains': chains}, sort_keys=False)
    return Response(json_data, mimetype='application/json')

@app.route('/match_table', methods=['POST'])
def match_table():
    data = request.get_json()
    print("data", data)
    chains = data['chains']
    print("chain입니다.", chains)
    return render_template('match_table.html', chains=chains, success="detail")

# 웹 방화벽 정보주는 api
@app.route('/api/web')
def api_web():
    try:
        # 로그 전체정보 가지고오기
        xss_log, sql_injection_log, xss_log_count, sql_injection_log_count, time_list, time_count_list = web_parse_logs('http_traffic.log')

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    data = {
    "webtime": {
        "labels": time_list,
        "values": time_count_list
    },

    "firewall": {
        "labels": ["XSS", "SQL-Injection"],
        "values": [xss_log_count, sql_injection_log_count]
    },
    }
    print(xss_log)
    return jsonify(data)


@app.route('/web_firewall', methods=["GET"])
def web_firewall():
    return render_template("web_firewall.html")

@app.route('/xss_log', methods=["GET", "POST"])
def xss_log():
    # 기본 로그 데이터 GET
    xss_log, sql_injection_log, xss_log_count, sql_injection_log_count, time_list, time_count_list = web_parse_logs('http_traffic.log')

    xss_log_info = xss_log
    # 검색
    if(request.method == "POST"):
        try:
            user_input = request.form.get("user_input")

            filtered_xss_log_info = web_search(user_input, xss_log_info)
            success=True
            if len(filtered_xss_log_info)==0:
                print("결과 없음")
                success = "No Answer"
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            success=False

        return render_template("xss_log.html", xss_info = filtered_xss_log_info)

    return render_template("xss_log.html", xss_info = xss_log_info)


@app.route('/sql_injection_log', methods=["GET", "POST"])
def sql_injection_log():
    # 기본 로그 데이터 GET
    xss_log, sql_injection_log, xss_log_count, sql_injection_log_count, time_list, time_count_list = web_parse_logs('http_traffic.log')
    
    sql_log_info = sql_injection_log
    # 검색
    if(request.method == "POST"):
        try:
            user_input = request.form.get("user_input")

            filtered_sql_log_info = web_search(user_input, sql_log_info)
            success=True
            if len(filtered_log_info)==0:
                print("결과 없음")
                success = "No Answer"
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            success=False

        return render_template("sql_injection_log.html", sql_info = filtered_sql_log_info)
    return render_template("sql_injection_log.html", sql_info =sql_log_info)

if __name__ == "__main__":
    app.run(debug=True)