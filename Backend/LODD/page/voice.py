import speech_recognition as sr
import sys #-- 텍스트 저장시 사용

from gtts import gTTS
import os
import random, string
import playsound

def speak(text, dir):
     tts = gTTS(text=text, lang='ko')
     filename = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=6)) + '.mp3'
     tts.save(dir + filename)
     playsound.playsound(dir + filename)

def recognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speech = r.listen(source)

    try:
        audio = r.recognize_google(speech, language="ko-KR")
        print("Your speech thinks like\n " + audio)
        return audio
    except sr.UnknownValueError:
        print("Your speech can not understand unknown")
        return 'unknown'
    except sr.RequestError as e:
        print("Request Error!; {0}".format(e))


if __name__ == '__main__':
    dir = os.getcwd() + "/mp3/"
    os.mkdir(dir)

    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say Something")
            speech = r.listen(source)

        try:
            audio = r.recognize_google(speech, language="ko-KR")
            print("Your speech thinks like\n " + audio)
            speak(audio[-1]+"로 끝나는 말", dir)

            if audio == '끝' or audio == '종료':
                break
        except sr.UnknownValueError:
            print("Your speech can not understand")
        except sr.RequestError as e:
            print("Request Error!; {0}".format(e))

    speak("게임 오버", dir)

    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    os.rmdir(dir)