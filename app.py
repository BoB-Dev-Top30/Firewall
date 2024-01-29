from flask import Flask, render_template, request, flash, redirect, url_for
import subprocess

# 자체 제작 모듈
from CRUD.Crud_Rule import *
from CRUD.Parse_Table import *

from MONITOR.Parse_Monitor import *

app = Flask(__name__)


@app.route("/")
def home():
    return redirect(url_for('index'))

'''
@app.route("/block_ip", methods=["POST"])
def block_ip():
    ip_to_block = request.form.get("ip")
    print("차단할 IP: ", ip_to_block)
    blocked_ips.append(ip_to_block)
    

    subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-s", ip_to_block, "-j", "DROP"])
    return render_template("crud.html", blocked_ips=blocked_ips)
'''
@app.route("/create", methods=["GET"])
def create1():
    return render_template("create.html")


@app.route("/create", methods=["POST"])
def create2():
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
    
    processed_rule = Process_Delete_Rule(rule)

    print("가공된 rule : ", processed_rule)
    

    command = "sudo " + "iptables" + processed_rule

    success = False
    try:
        subprocess.run(command.split(), check=True)
        success = True
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    return render_template("create.html", success=success)

@app.route('/index')
def index():
    success = request.args.get('success', False)
    iptables_output = subprocess.check_output(['sudo', 'iptables', '-nvL', '--line-numbers']).decode('utf-8')
    chains = parse_iptables(iptables_output)
    return render_template('index.html', chains=chains, success=success)


@app.route('/delete_rule/<chain_name>', methods=['POST'])
def delete_rule(chain_name):
    selected_rules = request.form.getlist('rule_to_change')

    success = False
    for rule_number in selected_rules:
        try:
            subprocess.run(['sudo', 'iptables', '-D', chain_name, rule_number], check=True)
            success = True
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

        print("가공된 rule : ", processed_rule)
        

        command = "sudo " + "iptables " + "-R " + str(chain_name) + " " + str(rule_number) + " " + processed_rule

        print(command)
        success = False
        try:
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
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        
    '''
    if(methods=='POST'):
        # 검색기능해서 -> 명령어로 만들기 (grep해오는거)
        try:
            filtered_state_info = subprocess.run(["sudo", "conntrack", "-L", "|", "grep", "-E",  "'ESTABLISHED|RELATED'", "|", "grep", "-v",  "'127.0.0.1'"], check=True)
            filtered_state_info = conntrack_parser(filtered_state_info)
            success=True
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            success=False

        return render_template('network_state.html', state_info=filtered_state_info, success=success)
    '''
    print(state_info)
    return render_template('network_state.html', state_info=state_info)

if __name__ == "__main__":
    app.run(debug=True)

'''
@app.route("/unblock_ip/<ip>", methods=["POST"])
def unblock_ip(ip):
    blocked_ips.remove(ip)
    subprocess.run(["sudo", "iptables", "-D", "FORWARD", "-s", ip, "-j", "DROP"])
    return render_template("crud.html", blocked_ips=blocked_ips)
'''



'''
@app.route("/unblock_ip/<ip>", methods=["POST"])
def unblock_ip(ip):
    blocked_ips.remove(ip)
    subprocess.run(["sudo", "iptables", "-D", "FORWARD", "-s", ip, "-j", "DROP"])
    return render_template("crud.html", blocked_ips=blocked_ips)
if __name__ == "__main__":
    app.run(debug=True)
    '''