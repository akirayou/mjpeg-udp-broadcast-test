import cv2
import socket
import numpy as np

multicast_if_addr='192.168.111.108'

#マルチキャストアドレスとポート(grSim参照)
multicast_group = '239.255.0.1' # マルチキャストアドレス
multicast_port=4000

my_addr='0.0.0.0' #これは変えない
server_address=(my_addr, multicast_port)

sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)

mreq=socket.inet_aton(multicast_group)+socket.inet_aton(multicast_if_addr)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:

    data, address=sock.recvfrom(1024*200) 
    data = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(data, flags=cv2.IMREAD_COLOR)
    cv2.imshow('recv' , frame)
    key =cv2.waitKey(10)
    if key == 27:#ESC
        break
