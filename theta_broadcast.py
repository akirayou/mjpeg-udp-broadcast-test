import cv2

cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)#hteta はmjpegじゃなかったのでソフトでmjpeg可する
cap.set(cv2.CAP_PROP_FPS, 30)
fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
fourcc = fourcc.to_bytes(4, 'little').decode('utf-8')
print("FOURCC=" + str(fourcc))
fps    = int(cap.get(cv2.CAP_PROP_FPS))
print("FPS=" + str(fps))



local_address   = '0.0.0.0' # 送信側のPCのIPアドレス
multicast_group = '239.255.0.1' # マルチキャストアドレス
port = 4000
import socket
from contextlib import closing
with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
    #sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(local_address))

    while True:
        ret, frame = cap.read()
        ret, encoded = cv2.imencode(".jpg", frame, (cv2.IMWRITE_JPEG_QUALITY, 12,cv2.IMWRITE_JPEG_OPTIMIZE,1))#とりあえずUDP一発で送れるように1フレームを64kb以下にする＝低画質にする
        print(encoded.shape)
        sock.sendto(encoded.tobytes(), (multicast_group, port))

        cv2.imshow('camera' , frame)

        key =cv2.waitKey(1)
        if key == 27:#ESC
            break

    #メモリを解放して終了するためのコマンド
    cap.release()
    cv2.destroyAllWindows()