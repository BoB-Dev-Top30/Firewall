from flask import Flask, render_template, request, flash
import subprocess

# 자체 제작 모듈
from CRUD.Crud_Rule import *
from CRUD.Parse_Table import *


app = Flask(__name__)

blocked_ips = []


@app.route("/")
def home():
    return render_template("crud.html")

'''
@app.route("/block_ip", methods=["POST"])
def block_ip():
    ip_to_block = request.form.get("ip")
    print("차단할 IP: ", ip_to_block)
    blocked_ips.append(ip_to_block)
    

    subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-s", ip_to_block, "-j", "DROP"])
    return render_template("crud.html", blocked_ips=blocked_ips)
'''
@app.route("/create", methods=["POST"])
def create():

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
    
    processed_rule = Process_Rule(rule)

    print("가공된 rule : ", processed_rule)
    

    command = "sudo " + "iptables" + processed_rule

    success = False
    try:
        subprocess.run(command.split(), check=True)
        success = True
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    return render_template("crud.html", success=success, blocked_ips=blocked_ips)

@app.route('/read')
def read():
    iptables_output = subprocess.check_output(['sudo', 'iptables', '-nvL']).decode('utf-8')
    chains = parse_iptables(iptables_output)
    return render_template('read.html', chains=chains)

'''
@app.route("/unblock_ip/<ip>", methods=["POST"])
def unblock_ip(ip):
    blocked_ips.remove(ip)
    subprocess.run(["sudo", "iptables", "-D", "FORWARD", "-s", ip, "-j", "DROP"])
    return render_template("crud.html", blocked_ips=blocked_ips)
'''

if __name__ == "__main__":
    app.run(debug=True)



@app.route("/unblock_ip/<ip>", methods=["POST"])
def unblock_ip(ip):
    blocked_ips.remove(ip)
    subprocess.run(["sudo", "iptables", "-D", "FORWARD", "-s", ip, "-j", "DROP"])
    return render_template("crud.html", blocked_ips=blocked_ips)
if __name__ == "__main__":
    app.run(debug=True)