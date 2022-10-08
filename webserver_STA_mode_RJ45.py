import network
import machine as  m

#	pin configuration for the component wt32-eth01
nl=network.LAN(mdc=m.Pin(23),mdio=m.Pin(18),power=m.Pin(16),id=0,phy_addr=1,phy_type=network.PHY_LAN8720)
#	network, set fixed IP (address, netmask, gateway, dns)
nl.ifconfig(('192.168.88.200', '255.255.255.0', '192.168.88.1', '8.8.8.8'))

#	trying to active the state of LAN network 
while nl.active() == False:
            try:
                nl.active(True)
            except(e):
                print("Trying to active the network LAN error")

print("LAN config: ",nl.ifconfig())
print("LAN connection active: ", nl.active())

#	trying to connect to the network/or internet access
while nl.isconnected() == False:
            try:
                nl.connect()
            except(e):
                print("Connection failed")
print("Connection state: ",nl.isconnected())

pins = [m.Pin(i, m.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)] #initialize the pin
 
 #	initialise the head of main web page
html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 wt32-eth01 Hello world</title> </head>
    <body> <h1>ESP32 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""
 
#	make a socket communication 
import socket
#	initialize the address. getaddrinfo() return a list of tuples containing information about socket(s) that can be created with the service.
#	getaddrinfo("<host>","<port>") it can be getaddrinfo('192.168.88.200', 80)[0][-1]
#	'0.0.0.0' mean "all IPv4 addresses on the local machine" [https://en.wikipedia.org/wiki/0.0.0.0]
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
print("information address : ",addr)
 
s = socket.socket()
s.bind(addr)
s.listen(1)
 
print('listening on', addr)
 
while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
