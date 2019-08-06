import cv2
# import serial
import time
i=0



dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
cap = cv2.VideoCapture(0)
# ser = serial.Serial('/dev/ttyUSB0', 9600)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray_color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgpoints = cv2.aruco.detectMarkers(gray_color, dictionary)
    if len(corners) > 0:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        print(ids)

    # Display the resulting frame
    # if ids==[[1]]:
    #     ser.write(bytes('6', 'utf-8'))
    # if ids==[[2]]:
    #     ser.write(bytes('7', 'utf-8'))
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

