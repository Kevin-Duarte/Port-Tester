# Port Tester
#### Developed by In Code We Speak
 Port tester is a lightweight tool that diagnoses and confirms open ports by sending a brief message via the specified protocol. The application must be installed on two systems.
 
### Warnings and Disclaimers
- In Code We Speak is not responsible for damages caused by this software
- In Code We Speak is not responsible for maintenance of this software. However, feel free to reach us at support@incodewespeak.com for special requests or custom solutions.

### Getting the executable
- Option 1 - Direct Download: Direct download of the executable is found on www.incodewespeak.com
- Option 2 - Building From Source: Download the repo, extract it, and run `build.bat` under Port-Tester > Source. The exe file will be generated under Port-Tester > install-files (Note, if building manually, you require Python3+, Pip, and PyInstaller)

### Example Use Case - Port Testing Behind a Firewall
1. Port Tester is running on two workstations
- Workstation A is stationed behind vlan 10.0.1.x with an IP of 10.0.1.10
- Workstation B is stationed behind vlan 10.0.2.x with an IP of 10.0.2.10
- Port 80 TCP is allowed between the vlans
2. Port Tester settings on Workstation A:
- Role: Client
- Sending To: 10.0.2.10
- Port: 80
- Protocol: TCP
2. Port Tester settings on Workstation B:
- Role: Server
- Starting Server On: 10.0.2.10
- Port: 80
- Protocol TCP
3. On Workstation B, start the temporary server by clicking on `Receive Message`
4. On Workstation A, click on `Send Message`
5. Monitor Workstation B's Console to confirm the message was received
- If the message was received, communication from Workstation A -> Workstation B is working
6. Flip the roles on both workstations, update the IPs for `Sending To`/`Starting Server On` to Workstation A's IP, and Perform steps 3-4
- If the message was received, communication from Workstation B -> Workstation A is working

