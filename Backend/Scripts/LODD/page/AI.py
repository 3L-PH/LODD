import numpy as np
import imutils
import time
import dlib
import cv2
from scipy.spatial import distance as dist
from imutils import face_utils
import base64

import io
import PIL.Image as Image

#from threading import Thread
#from threading import Timer
#from .check_cam_fps import check_fps

from PIL import Image

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

landmarks_list = []
both_ear_list = []

OPEN_EAR = 0 #For init_open_ear()
EAR_THRESH = 100 #Threashold value

def eye_aspect_ratio(eye) :
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

#캠 인식하고 5초 동안 눈 ear 값과 코 길이 측정
def init_open_ear(landmarks_list, both_ear_list) :
    ear_list = []
    nose_list = []
    face_list = []
    print("눈과 코 인식을 시작합니다")
    for i in range(len(landmarks_list)) :
        face = landmarks_list[i].part(8).y - landmarks_list[i].part(27).y
        nose = landmarks_list[i].part(30).y - landmarks_list[i].part(27).y
        ear_list.append(both_ear_list[i])
        face_list.append(face)
        nose_list.append(nose)
    OPEN_EAR = 0
    CLOSE_EAR = 0
    ear_list.sort(reverse=True)
    face_list.sort(reverse=True)
    nose_list.sort(reverse=True)
    for i in range(10):
        OPEN_EAR += ear_list[i]
        face_length += face_list[i]
        nose_length += nose_list[i]
    for i in range(7):
        CLOSE_EAR += ear_list[99 - i]
    OPEN_EAR /= 10
    CLOSE_EAR /= 10
    face_length /= 10
    nose_length /= 10
    EAR_THRESH = (((OPEN_EAR - CLOSE_EAR) * 0.6) + CLOSE_EAR) #EAR_THRESH means 50% of the being opened eyes state
    print("OPEN_EAR : ", OPEN_EAR, "\nCLOSE_EAR : ", CLOSE_EAR, "\nEAR_THRESH : ", EAR_THRESH, "\nNOSE_LENGTH : ", nose_length, "\nFACE_LENGTH : ", face_length)

def light_removing(frame) :
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    L = lab[:,:,0]
    med_L = cv2.medianBlur(L,99) #median filter
    invert_L = cv2.bitwise_not(med_L) #invert lightness
    composed = cv2.addWeighted(gray, 0.75, invert_L, 0.25, 0)
    return L, composed

def vision(img, INIT_FLAG, close_first, closed_flag, game_flag):
    INIT_FLAG = int(INIT_FLAG)
    close_first = float(close_first)
    closed_flag = int(closed_flag)
    game_flag = int(game_flag)

    print("Before : ", end = '')
    print(INIT_FLAG, close_first, closed_flag, game_flag)
    str_img = img.split(",")[1]
    #print(str_img)
    encoding_img = base64.b64decode((str_img))

    with open('out.jpg','wb') as f:
        f.write(encoding_img)

    # img0 = image.read()
    img_enc = np.frombuffer(encoding_img , np.uint8)
    frame = cv2.imdecode(img_enc, cv2.IMREAD_UNCHANGED)
    #frame = image
    frame = imutils.resize(frame, width = 400)
    
    L, gray = light_removing(frame)
    rects = detector(gray,0)
    # 처음 웹 캠 연결된 이미지 전송받을 때
    if INIT_FLAG == 0:
        global landmarks_list
        global both_ear_list
        global nose_length
        global face_length

        landmarks_list = []
        both_ear_list = []
        nose_length = 0
        face_length = 0

    # EAR_THRESH값 설정을 위한 데이터 수집 완료
    if INIT_FLAG == 100:
        init_open_ear(landmarks_list, both_ear_list)

    print(rects)
    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        both_ear = (leftEAR + rightEAR) * 500  #I multiplied by 1000 to enlarge the scope.
        
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)

            # 처음 100개 이미지에 대해서 landmarks랑 both ear 수집
            if INIT_FLAG < 100:
                landmarks_list.append(landmarks)
                both_ear_list.append(both_ear)
                INIT_FLAG += 1
        
        # EAR_THRESH 설정 완료 후 졸음 인식 시작
        if INIT_FLAG == 100:
            #face = landmarks.part(8).y - landmarks.part(27).y
            #nose = landmarks.part(30).y - landmarks.part(27).y
            #print(nose, face, face - nose)
            #if nose - nose_length > 3 and nose_length > 0:
            #    print("고개를 숙였습니다 : ") 
            
            # 눈 감고있는 상태
            if both_ear < EAR_THRESH:
                print("now close")

                # 처음 눈을 감은 시간
                if closed_flag == 0:
                    close_first = time.time()
                    closed_flag = 1
                # 눈을 감고있는 상태에서 지금 시간
                close_now = time.time()

            # 눈 뜬 상태
            if both_ear >= EAR_THRESH:
                print("now open")

                # 눈 감고있는 시간 변수 초기화
                close_first = 0
                close_now = 0
                closed_flag = 0

            # 눈을 감고있는 시간
            closed = close_first - close_now

            # 0.5초 이상 눈 감고있으면 졸음으로 인식 -> 게임 시작
            if closed >= 0.5 and game_flag == 0:
                game_flag = 1
                print("끝말잇기 게임이 실행됩니다")
                return [game_flag]
    print("After : ",end='')
    print(INIT_FLAG, close_first, closed_flag, game_flag)
    return [INIT_FLAG, close_first, closed_flag, game_flag]
