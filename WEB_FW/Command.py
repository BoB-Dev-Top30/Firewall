
import subprocess
def web_command(application, priority, traffic_type):
    if(application=="yes_application"):
        if(priority=="normal"):
            priority="-A"
        elif(priority=="special"):
            priority="-I"
        try:
            subprocess.run(["sudo", "iptables", priority, traffic_type.upper(),"-p","tcp", "--dport","80","-j","NFQUEUE","--queue-num","0"], check=True)
            print("WEB Firewall start")
        except ubprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
        return 0
    return 0
