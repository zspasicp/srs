


'''
@param TCP_SYN_scan - Perform a TCP SYN connect scan if set to True. 
This just means that the app will send a TCP SYN packet just like any normal application would do. 
If the port is open the application must reply with SYN/ACK, however to prevent half open connections 
app will send a RST to tear down the connection again. 

@param UDP_scan - Perform an UDP scan if set to True. 
Because UDP is unreliable it is not as easy to determine if ports are open as it is with TCP.
The UDP scan sends an UDP packet with an empty header to the target port. 
If the port is closed the OS should reply with an ICMP port unreachable error, 
however if the port is open it does not necessarily mean that the service will reply with anything.
If service scan (-sV) is enabled in the scan, app will send additional packets with different payloads
in order to try trigger a response from the service. 
This type of scanning can be really slow because a typical OS will only allow about 1 ICMP packet per second. 

@param timing_template is an option for timing template.
Numbers range from 0-5 where 5 is the fastest and 0 is the slowest.
0: paranoid 1: sneaky 2: polite 3: normal 4: aggressive 5: insane
Again, this translates into 1-2 being used for IDS evasion, 
3 is the default and 4-5 is really quick scans.

@param enable_OS_detection - Make app try decide what OS type it is. 
The process of OS detection can be quite complex, but also quite simple. 
A simple factor to try decide whether it is a Windows OS or Unix OS is 
to look at the TTL (Time to live) field on packets being sent from the OS. 
Windows usually defaults to 128 while Unix defaults to 64.

@param enable_version_detection
Actively probe open ports to try determine what service and version they are running. 

@param enable_traceroute - Perform a traceroute to the target.

@param verbosity_level - Increased verbosity.
This will give your extra information in the data outputted by app.
This parameter expets 1 or 2 for extra information, where higher number means more information.

@param ICMP_echo_discovery_probes - This parameter is used to decide how app discovers hosts, 
and this one decides that app should use ICMP echo requests to deciding if a host is up or not. 
This is the same as performing a ping to the target host in determining if it is up or not.

@param timestamp_discovery_probes - This defines that instead of a regular ICMP echo request 
should be used in determining if host is up or not, app should send a ICMP Timestamp request. 
This special type of ICMP request is originally used for synchronizing timestamps between communicating nodes, 
but has been replaced by the more common network time protocol. 
This type of scan was not successfull in determining if my host was up or not.

@param TCP_SYN_to_given_ports - Also used for host discovery. 
This option simply relies on a port (default 80) to reply to an empty SYN packet, 
as is with default TCP behaviour. Simple is often good.

@param TCP_ACK_to_given_ports - Much like the TCP_SYN_to_given_ports option, 
this one sends a TCP packet with the ACK flag set instead. 
This should cause the responding server to respond with a RST packet if it 
is listening on that port as it is not expecting any data to be acknowledged by an ACK packet.
Sometimes firewall administrators configure the firewall to drop incoming SYN packets to prevent any traffic, 
which would allow for ACK packets to pass through.

@param UDP_to_given_ports - This sends out a UDP packet destined to the target port (default 40125) 
in order to try elicit a an "ICMP Port unreachable" message from the server. 
Sometimes firewalls also only drop TCP packets and don't care about UDP packets, 
allowing this type of packets through. Some configurations also allow any type of packet 
through where only TCP should be allowed. 
Camoflaging your host discovery as an UDP packet on port 53 (DNS) could be a very stealthy approach.

@param SCTP_discovery_to_given_ports - Very much like a TCP SYN scan, 
this just utilizes the SCTP (Stream Control Transmission Protocol) instead.

@param source_port_number - Specify what source port you want to use. 
Note that this is different from what destination port you are scanning. 
The real use for this comes with trying to evade IDS or blending inn with other regular data.

@param script_default_or_discovery_and_safe - it will load all scripts from the default category, 
and only the scripts in discovery category that are also in the safe category.
'''
def create_scan_command(source_port_number: int = 0,
         TCP_SYN_scan: bool = False,
         UDP_scan: bool = False,
         timing_template: int = 0,
         enable_OS_detection: bool = False,
         enable_version_detection: bool = False,
         enable_traceroute: bool = False,
         verbosity_level: int = 0,
         ICMP_echo_discovery_probes: bool = False,
         timestamp_discovery_probes: bool = False,
         TCP_SYN_to_given_ports: 'touple' = (False, []),
         TCP_ACK_to_given_ports: 'touple' = (False, []),
         UDP_to_given_ports: 'touple' = (False, []),
         SCTP_discovery_to_given_ports: 'touple' = (False, []),
         script_default_or_discovery_and_safe: bool = False,
         target: str = None,) -> str:
    
    command = 'nmap'
    if(TCP_SYN_scan):
        command += ' -sS'
    if(UDP_scan):
        command += ' -sU'
    if(timing_template != 0):
        command += ' -T%d' %timing_template
    if(enable_OS_detection):
        command += ' -O'
    if(enable_version_detection):
        command += ' -sV'
    if(enable_traceroute):
        command += ' --traceroute'
    if(verbosity_level == 1):
        command += ' -v'
    elif(verbosity_level == 2):
        command += ' -vv'
    if(ICMP_echo_discovery_probes):
        command += ' -PE'
    if(timestamp_discovery_probes):
        command += ' -PP'
    if(TCP_SYN_to_given_ports[0]):
        command += ' -PS'
        for port in TCP_SYN_to_given_ports[1]:
            command += '%s,' %port
        if(len(TCP_SYN_to_given_ports[1]) != 0):
            command = command[:-1]
    if(TCP_ACK_to_given_ports[0]):
        command += ' -PA'
        for port in TCP_ACK_to_given_ports[1]:
            command += '%s,' %port
        if(len(TCP_ACK_to_given_ports[1]) != 0):
            command = command[:-1]
    if(UDP_to_given_ports[0]):
        command += ' -PU'
        for port in UDP_to_given_ports[1]:
            command += '%s,' %port
        if(len(UDP_to_given_ports[1]) != 0):
            command = command[:-1]
    if(SCTP_discovery_to_given_ports[0]):
        command += ' -PY'
        for port in SCTP_discovery_to_given_ports[1]:
            command += '%s,' %port
        if(len(SCTP_discovery_to_given_ports[1]) != 0):
            command = command[:-1]
    if(source_port_number):
        command += ' -g %d' %source_port_number
    if(script_default_or_discovery_and_safe):
        command += ' --script \"default or (discovery and safe)\"'
    if(target is not None):
        command += ' -oX %s %s' %(target, target)
    return command


if __name__ == '__main__':
    print(create_scan_command(source_port_number = 53,
        TCP_SYN_scan = True,
        UDP_scan = True,
        timing_template = 4,
        enable_OS_detection = True,
        enable_version_detection = True,
        enable_traceroute = True,
        verbosity_level = 1,
        ICMP_echo_discovery_probes = True,
        timestamp_discovery_probes = True,
        TCP_SYN_to_given_ports = (True, []),
        TCP_ACK_to_given_ports = (True, []),
        UDP_to_given_ports = (True, []),
        SCTP_discovery_to_given_ports = (True, []),
        script_default_or_discovery_and_safe = True,
        target = 'www.test.com'))
    print(create_scan_command(target = 'www.test2.com'))