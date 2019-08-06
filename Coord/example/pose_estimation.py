import numpy as np
import cv2
import cv2.aruco as aruco
import sys, time, math

# --- Define Tag
id_to_find = 3
marker_size = 10  # - [cm]


# ------------------------------------------------------------------------------
# ------- ROTATIONS https://www.learnopencv.com/rotation-matrix-to-euler-angles/
# ------------------------------------------------------------------------------
# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R):
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


# --- Get the camera calibration path
# savedir = r"D:\Robotics\ICCET2019\hta0-horizontal-robot-arm\camera_data\\"
# camera_matrix = np.load(savedir+'cam_mtx.npy')
# camera_distortion = np.load(savedir+'dist.npy')[0]

calib_path  = "../OpenFirst/"
camera_matrix   = np.loadtxt(calib_path+'cameraMatrix_webcam.txt', delimiter=',')
camera_distortion   = np.loadtxt(calib_path+'cameraDistortion_webcam.txt', delimiter=',')

print(camera_matrix, "\n", camera_distortion)

# --- 180 deg rotation matrix around the x axis
R_flip = np.zeros((3, 3), dtype=np.float32)
R_flip[0, 0] = 1.0
R_flip[1, 1] = -1.0
R_flip[2, 2] = -1.0

# --- Define the aruco dictionary
# aruco_dict  = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
#aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
#parameters = aruco.DetectorParameters_create()

# --- Capture the videocamera (this may also be a video or a picture)
cap = cv2.VideoCapture(0)
# -- Set the camera size as the one it was calibrated with
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# -- Font for the text in the image
font = cv2.FONT_HERSHEY_PLAIN



while True:

    # -- Read the camera frame
    ret, frame = cap.read()
    frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))

    # -- Convert in gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # -- remember, OpenCV stores color images in Blue, Green, Red
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 241, 2)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        cnt = sorted(contours, key=cv2.contourArea, reverse=True)
        x, y, w, h = cv2.boundingRect(cnt[0])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cor_list = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]
        corners = np.array(cor_list, dtype=np.float32)
        #print(corners)

        ret = aruco.estimatePoseSingleMarkers(corners,
                                              marker_size,
                                              camera_matrix,
                                              camera_distortion)
        # print("|||", ret)
        #
        # # -- Unpack the output, get only the first
        # rvec, tvec = ret[0][0, 0, :], ret[1][0, 0, :]
        #
        # # -- Draw the detected marker and put a reference frame over it
        # aruco.drawDetectedMarkers(frame, corners)
        # aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec, tvec, 10)
        #
        # # -- Print the tag position in camera frame
        # str_position = "MARKER Position x=%4.0f  y=%4.0f  z=%4.0f" % (tvec[0], tvec[1], tvec[2])
        # cv2.putText(frame, str_position, (0, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)


    # --- Display the frame
    cv2.imshow('frame', frame)
    cv2.imshow('thresh', thresh)

    # --- use 'q' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
