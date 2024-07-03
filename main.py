import re

def parse_config(config):
    parsed_data = []

    # Split the config into lines
    lines = config.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        data = line.split(" ")
        if "allow" in data:
            users = data[1].split(",")
            entry = {"users": users}
            proxy_data = lines[i+1].split(" ")
            entry["type"] = proxy_data[0]
            entry["port"] = int(proxy_data[1].split("-p")[1])
            entry["endpoint"] = proxy_data[2].split("-e")[1]
            if "-D" in proxy_data[3]:
                entry["interface"] = proxy_data[3].split("-D")[1]
            parsed_data.append(entry)
        else:
            continue
    return parsed_data

def is_port_in_use(parsed_data, port):
    for entry in parsed_data:
        if entry.get('port') == port:
            return True
    return False

def create_config(proxy_entry):
    connection_type = proxy_entry.get('type', '')
    port = proxy_entry.get('port', '')
    endpoint = proxy_entry.get('endpoint', '')
    interface = proxy_entry.get('interface', None)
    users = proxy_entry.get('users', [])
    
    config_lines = []
    

    
    # Create the allow line
    if users:
        allow_line = f"allow {','.join(users)}"
        config_lines.append(allow_line)
    
    # Create the proxy/socks line
    proxy_line = f"{connection_type} -p{port} -e{endpoint}"
    if interface:
        proxy_line += f" -D{interface}"
    config_lines.append(proxy_line)
    
    # Add the flush line
    config_lines.append("flush")
    
    return '\n'.join(config_lines)

def list_proxies_on_interface(parsed_data, interface):
    proxies = []
    for entry in parsed_data:
        if entry.get('interface') == interface:
            proxies.append(entry)
    return proxies

def list_proxies_for_user(parsed_data, user):
    proxies = []
    for entry in parsed_data:
        if user in entry.get('users', []):
            proxies.append(entry)
    return proxies

def remove_proxy_entry(parsed_data, port):
    updated_data = [entry for entry in parsed_data if entry.get('port') != port]
    return updated_data

def remove_user_from_proxy(parsed_data, user, port):
    for entry in parsed_data:
        if entry.get('port') == port and user in entry.get('users', []):
            entry['users'].remove(user)
    return parsed_data

def generate_all_configurations(parsed_data):
    configurations = []
    for entry in parsed_data:
        try:
            config = create_config(entry)
            configurations.append(config)
        except ValueError as e:
            print(f"Error generating configuration for port {entry['port']}: {str(e)}")
    configurations = ["#Auth\nauth strong\n#auth file \nusers $/etc/3proxy/.proxyauth"] + configurations 
    return configurations

def write_to_file(filename, configurations):
    with open(filename, 'w') as f:
        for config in configurations:
            f.write(config)
            f.write('\n\n')  # Separate configurations with blank lines

def create_proxy(parsed_data, connection_type, port, endpoint, interface=None, users=None):
    if is_port_in_use(parsed_data, port):
        raise ValueError(f"Port {port} is already in use.")
    
    if users is None:
        users = []
    
    new_proxy = {
        'type': connection_type,
        'port': port,
        'endpoint': endpoint,
        'interface': interface,
        'users': users
    }
    
    parsed_data.append(new_proxy)
    return parsed_data


def readfile(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except IOError as e:
        print(f"Error reading file '{filename}': {e}")
        return None
    

def edit_proxy(parsed_data, port, new_connection_type=None, new_endpoint=None, new_interface=None, new_users=None):
    updated = False
    for entry in parsed_data:
        if entry.get('port') == port:
            if new_connection_type:
                entry['type'] = new_connection_type
            if new_endpoint:
                entry['endpoint'] = new_endpoint
            if new_interface is not None:
                entry['interface'] = new_interface
            if new_users is not None:
                entry['users'] = new_users
            updated = True
            break
    
    if not updated:
        raise ValueError(f"Proxy with port {port} not found.")
    
    return parsed_data

test_data = """#Auth
auth strong
#auth file 
users $/etc/3proxy/.proxyauth

allow user1,user2
socks -p1080 -e1.1.1.1 -Deth0
flush

allow user3,user5
proxy -p111231 -e1.1.1.1 -Deth0
flush
"""

parsed_data = parse_config(test_data)
print(parsed_data)
create_proxy(parsed_data, 'proxy', 1081, '1.1.1.1', 'eth1', ['user1', 'user2'])
write_to_file('output.txt', generate_all_configurations(parsed_data))