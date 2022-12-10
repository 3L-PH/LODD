from django.shortcuts import render
# from .AI import vision
from .AI_new_v3 import vision
import os, random
# Create your views here.

#from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.http import JsonResponse

from .voice import speak
from . import last_word
import numpy as np

def game_start():
    dir = os.getcwd() + "/mp3/"
    os.mkdir(dir)
        
    start_word = np.load('word.npy')

    speak('끝말잇기 시작합니다', dir)
    start = start_word[random.randrange(0, len(start_word))]
    speak(start, dir)

    result = last_word.game_play(start, dir)
    if result == 'exit':
        speak('게임을 종료합니다', dir)
    elif result == 'win_com':
        speak('컴퓨터의 승리', dir)
    elif result == 'win_com':
        speak('당신의 승리', dir)
    elif result == 'win_user_black':
        speak('치사하지만 당신의 승리', dir)

    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    os.rmdir(dir)

@api_view(['POST'])
@permission_classes([AllowAny,])
def sleep_check(request):
    if request.method == 'POST':
        try:
            img = request.data["img"]
            INIT_FLAG = int(request.data["INIT_FLAG"])
        except:
            message = {"message" : "Not Enough data", "State" : "fail"}
            return JsonResponse(message, status = HTTP_400_BAD_REQUEST)
        result = vision(img, INIT_FLAG)
        
        print(result)
        if result[-1] == 1:
            message = {"data" : result, "status":"success"}
                # 여기서 게임 시작
            game_start()
        else:
            message = {"data" : result, "state" : "success"}
        return JsonResponse(message, status = HTTP_200_OK)