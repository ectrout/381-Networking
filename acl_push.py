from netmiko import ConnectHandler

def block_ip(router_ip, username, password, bad_ip):
    router = {
        "device_type": "vyos",
        "host": router_ip,
        "username": username,
        "password": password,
    }

    commands = [
        f"set firewall name HONEYPOT-BLOCK rule 10 source address {bad_ip}",
        f"set firewall name HONEYPOT-BLOCK rule 10 action drop",
        "commit",
        "save"
    ]

    try:
        with ConnectHandler(**router) as conn:
            output = conn.send_config_set(commands)
            print(f"Blocked {bad_ip} on {router_ip}")
            print(output)
    except Exception as e:
        print(f"Failed to connect to router: {e}")

if __name__ == "__main__":
    # Test values - replace with real IPs when lab is running
    block_ip("192.168.1.1", "vyos", "vyos", "10.0.0.99")
