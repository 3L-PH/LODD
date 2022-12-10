import numpy as np
import time
import cv2
from scipy.spatial import distance as dist
import base64
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius = 1)

#face list를 통해서 ear 측정하는 함수
def eye_aspect_ratio(face) :
    A = dist.euclidean(face[2], face[3])
    B = dist.euclidean(face[4], face[7])

    X = dist.euclidean(face[9], face[8])
    Y = dist.euclidean(face[10], face[11])

    ear_right = A / B
    ear_left = X / Y
    ear = (ear_right + ear_left) * 1000

    return ear

def vision(img, INIT_FLAG):

    str_img = img.split(",")[1]
    #print(str_img)
    encoding_img = base64.b64decode((str_img))

    # img0 = image.read()
    img_enc = np.frombuffer(encoding_img , np.uint8)
    frame = cv2.imdecode(img_enc, cv2.IMREAD_UNCHANGED)
    #frame = image
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    # 처음 웹 캠 연결된 이미지 전송받을 때
    if INIT_FLAG == 0:
        INIT_FLAG += 1
        global first
        global blink
        global n_y
        global f_length
        global nose_y
        global face_length
        global OPEN_EAR
        global CLOSE_EAR
    
        global e_list
        global n_list
        global f_list

        global close_first
        global closed_flag
        global down_first
        global down_flag
        global game_flag

        first = 1                           #안내 문구 출력 위한 flag

        blink = 0                           #눈 감겼는지 확인 위한 threshold
        n_y = 0                             #7초 동안 측정한 코의 평균 y축 좌표
        f_length = 0                        #실시간으로 측정되는 얼굴 전체 길이
        nose_y = 0                          #실시간으로 측정되는 코 y축 좌표
        face_length = 0                     #7초 동안 측정한 얼굴 전체 길이
        OPEN_EAR = 0                        #7초 동안 측정한 눈 뜨고 있을 때의 ear
        CLOSE_EAR = 0                       #7초 동안 측정한 눈 감고 있을 때의 ear
    
        e_list = []                         #7초 동안의 ear 저장 위한 리스트
        n_list = []                         #7초 동안의 코 y 좌표 저장 위한 리스트
        f_list = []                         #7초 동안의 얼굴 전체 길이 저장위한 리스트

        
        close_first = 0
        closed_flag = 0
        down_first = 0
        down_flag = 0
        game_flag = 0
    elif INIT_FLAG == 2 and closed_flag == 0 and down_flag == 0 and game_flag == 1:
        game_flag = 0
    print(len(e_list))
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            face = []
            for id, lm in enumerate(faceLms.landmark):
                ih, iw, ic = frame.shape
                #landmark의 x축과 y축 좌표 계산
                x, y = (lm.x*iw), (lm.y*ih)
                
                #10~152 : 얼굴 전체 길이 / 20~168 코 전체 / 130, 243 : 오른쪽 눈 가로 / 23, 27 : 오른쪽 눈 세로 / 359, 463 : 왼쪽 눈 가로 / 257, 253 : 왼쪽 눈 세로
                if id == 10 or id == 152 or id == 168 or id == 20 or id == 130 or id == 243 or id == 23 or id == 27 or id == 359 or id == 463 or id == 257 or id == 253:
                    face.append([x, y])
                
                #위 12개 랜드마크를 모두 측정했으면 EAR 계산
                if len(face) == 12:  
                    ear = eye_aspect_ratio(face)
                    
                if INIT_FLAG == 1 and len(face) == 12 and id <= 463:
                    if first == 1:
                        print("눈과 코 인식을 시작합니다. 카메라를 응시해주세요.")
                        first = 0
                    #7초 동안 코 Y축 좌표, EAR 등 측정
                    f_length = dist.euclidean(face[0], face[5])
                    n_y = face[6][1]
                    e_list.append(ear)
                    f_list.append(f_length)
                    n_list.append(n_y)
                    if len(e_list) == 200:
                        e_list.sort(reverse=True)
                        f_list.sort(reverse=True)
                        n_list.sort(reverse=True)
                        for i in range(20):
                            OPEN_EAR += e_list[i]
                            face_length += f_list[i]
                            nose_y += n_list[i]
                        for i in range(7):
                            CLOSE_EAR += e_list[199 - i]
                        OPEN_EAR /= 20
                        CLOSE_EAR /= 7
                        face_length /= 20
                        nose_y /= 20
                        #측정한 값 토대로 threshold 측정
                        blink = (((OPEN_EAR - CLOSE_EAR) * 0.1) + CLOSE_EAR)
                        INIT_FLAG += 1

            if INIT_FLAG  != 2: continue

            print(blink, n_y,f_length,nose_y,face_length)
            print(ear, abs(face[6][1] - n_y) * 7)
            print(down_flag, down_first)

            #얼굴 길이 대비 코 y축 좌표의 변화값을 토대로 처음 고개 떨군 시점 측정
            if abs(face[6][1] - n_y) > f_length / 7 and down_flag == 0:
                down_first = time.time()
                down_flag = 1
            if abs(face[6][1] - n_y) < f_length / 7 and down_flag == 1:
                down_flag = 0
            #고개 떨군 시간이 특정 시간 이상이면 졸음 운전으로 인식
            if abs(face[6][1] - n_y) > f_length / 7 and down_flag == 1:
                if time.time() - down_first >= 0.8 and game_flag == 0:
                    game_flag = 1
                    print("끝말잇기 게임이 실행됩니다_고개")
            #theshold 이하로 ear 떨어지면 눈 감은 것
            if ear < blink and closed_flag == 0:
                close_first = time.time()
                closed_flag = 1
            if ear > blink  and closed_flag == 1:
                closed_flag = 0
            #특정 시간 이상 눈 감고 있으면 졸음운전으로 인식
            if ear < blink and closed_flag == 1:
                if time.time() - close_first >= 0.8 and game_flag == 0:
                    game_flag = 1
                    print("끝말잇기 게임이 실행됩니다_눈")

    if game_flag == 1:
        close_first = 0
        closed_flag = 0
        down_first = 0
        down_flag = 0
    return [INIT_FLAG, game_flag]