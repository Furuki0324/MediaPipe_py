import TrackingModule
import math
import socket
import struct
import cv2

serv_address = ("127.0.0.1", 50001)
serv_address2 = ("127.0.0.1", 50002)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

cap = cv2.VideoCapture(1)
detector = TrackingModule.HandDetector(detectionCon=0.7, trackCon=0.3)
pose = TrackingModule.PoseDetector(modelComplexity = 0, detectionCon=0.7, trackCon=0.5)

tracking = False
shoot = False

while True:
    ret, img = cap.read()
    #Flip the image.
    img = cv2.flip(img,1)

    #img, handNum = detector.findHands(img)
    #list = []

    
    img = pose.findBody(img)
    success, landmarks = pose.findPosePosition(img)
    if(success):
        print(landmarks)
        message = str(landmarks)
        sock.sendto(message.encode(), serv_address)


    """

    for num in range(handNum):
        list.append(detector.findPosition(img, handNo = num, draw = True))

        if len(list) == 2:
            tracking = True

            #w is wrist, s is sum, i is index, m is middle, c is center
            wx1, wy1 = int(list[0][0][1]), int(list[0][0][2])
            sx1, sy1 = list[0][4][1], list[0][4][2]
            ix1, iy1 = int(list[0][8][1]), int(list[0][8][2])
            mx1, my1 = int(list[0][9][1]), int(list[0][9][2])
            cx1, cy1 = (wx1 + mx1) // 2, (wy1 + my1) // 2
            cv2.line(img, (wx1, wy1), (mx1, my1), (255,0,255), 3)
            cv2.circle(img, (cx1, cy1), 5, (0,0,255), cv2.FILLED)

            wx2, wy2 = int(list[1][0][1]), int(list[1][0][2])
            sx2, sy2 = list[1][4][1], list[1][4][2]
            ix2, iy2 = int(list[1][8][1]), int(list[1][8][2])
            mx2, my2 = int(list[1][9][1]), int(list[1][9][2])
            cx2, cy2 = (wx2 + mx2) // 2, (wy2 + my2) // 2
            cv2.line(img, (wx2, wy2), (mx2, my2), (255,0,255), 3)
            cv2.circle(img, (cx2, cy2), 5, (0,0,255), cv2.FILLED)

            cv2.line(img, (cx1, cy1), (cx2, cy2), (0,255,255), 2)
            length = math.hypot(cx2 - cx1, cy2 - cy1)
            len1 = math.hypot(sx1 - ix1, sy1 - iy1)
            len2 = math.hypot(sx2 - ix2, sy2 - iy2)

            if length >= 200:
                shoot = True

            if len1 <= 40 and len2 <= 40:
                cv2.line(img,(ix1,iy1), (ix2,iy2),(255,0,0),3)

            try:
                #sock.sendto(struct.pack('i', int(length)), serv_address)
                message = "WY1:" + str(wy1) + " WY2:" + str(wy2)
                message = str(list[0])
                print(list[0])
                sock.sendto(message.encode(), serv_address);
                message = str(list[1])
                sock.sendto(message.encode(), serv_address2)
            except KeyboardInterrupt:
                sock.close()
                break


    if handNum != 2 and tracking:
        tracking = False
        if shoot:
            #sock.sendto(struct.pack('i',0), serv_address)
            #sock.sendto("Shoot".encode(), serv_address)
            shoot = False
    #print(tracking)
    """

    cv2.imshow("Img", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()

