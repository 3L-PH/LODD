#https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=pdj2885&logNo=221552896123

import requests, hgtk, random
from . import voice

# 지정한 두 개의 문자열 사이의 문자열을 리턴하는 함수
# string list에서 단어, 품사와 같은 요소들을 추출할때 사용됩니다
def midReturn(val, s, e):
    if s in val:
        val = val[val.find(s) + len(s):]
        if e in val: val = val[:val.find(e)]
    return val


# 지정한 두 개의 문자열 사이의 문자열 여러개를 리턴하는 함수
# string에서 XML 등의 요소를 분석할때 사용됩니다
def midReturn_all(val, s, e):
    if s in val:
        tmp = val.split(s)
        val = []
        for i in range(0, len(tmp)):
            if e in tmp[i]: val.append(tmp[i][:tmp[i].find(e)])
    else:
        val = []
    return val


def findword(query, apikey, history, blacklist):
    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&pos=1&q=' + query
    response = requests.get(url, verify = False)
    ans = []

    # 단어 목록을 불러오기
    words = midReturn_all(response.text, '<item>', '</item>')
    for w in words:
        # 이미 쓴 단어가 아닐때
        if not (w in history):
            # 한글자가 아니고 품사가 명사일때
            word = midReturn(w, '<word>', '</word>')
            pos = midReturn(w, '<pos>', '</pos>')
            if len(word) > 1 and pos == '명사' and not word in history and not word[len(word) - 1] in blacklist:
                ans.append(w)
    if len(ans) > 0:
        return random.choice(ans)
    else:
        return ''


def checkexists(query, apikey, history):
    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&sort=popular&num=100&pos=1&q=' + query
    response = requests.get(url, verify = False)
    ans = ''

    # 단어 목록을 불러오기
    words = midReturn_all(response.text, '<item>', '</item>')
    for w in words:
        # 이미 쓴 단어가 아닐때
        if not (w in history):
            # 한글자가 아니고 품사가 명사일때
            word = midReturn(w, '<word>', '</word>')
            pos = midReturn(w, '<pos>', '</pos>')
            if len(word) > 1 and pos == '명사' and word == query: ans = w

    if len(ans) > 0:
        return ans
    else:
        return ''


def game_play(st, dir):
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    # 이미 있는 단어 알기위해 단어목록 저장
    history = [st]
    playing = True
    # 키 발급은 https://krdict.korean.go.kr/openApi/openApiInfo
    apikey = '0DFD73DA7DC4702D93CE13903CE27DCC'

    # 좀 치사한 한방단어 방지 목록
    blacklist = ['즘', '틱', '늄', '슘', '퓸', '늬', '뺌', '섯', '숍', '튼', '름', '늠', '쁨']
    answord = ''
    sword = st[-1]

    while (playing):
        print("playing")
        wordOK = False

        while (not wordOK):
            query = voice.recognition()
            
            if query == 'unknown':
                continue

            wordOK = True

            if query == '종료':
                return 'exit'

            elif query == '재시작':
                history = []
                answord = ''
                voice.speak('게임 다시 시작', dir)
                wordOK = False

            else:
                if query == '':
                    wordOK = False

                    # 음성 인식된 것이 없을 때, 어떻게 할 지 생각해보자
                    if len(history) == 0:
                        voice.speak('음성을 입력하세요',dir)
                    else:
                        voice.speak(sword + '(으)로 시작하는 단어를 말해주세요', dir)
                        playing = False
                        break

                else:
                    # 첫 글자의 초성 분석하여 두음법칙 적용 -> 규칙에 아직 완벽하게 맞지 않으므로 차후 수정 필요
                    if not len(history) == 0 and not query[0] == sword and not query == '':
                        sdis = hgtk.letter.decompose(sword)
                        qdis = hgtk.letter.decompose(query[0])
                        if sdis[0] == 'ㄹ' and qdis[0] == 'ㄴ':
                            print('두음법칙 적용됨')
                        elif (sdis[0] == 'ㄹ' or sdis[0] == 'ㄴ') and qdis[0] == 'ㅇ' and qdis[1] in (
                        'ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ'):
                            print('두음법칙 적용됨')
                        else: # 끝말 안 이어지고 두음법칙 적용도 안되면 그냥 틀림
                            # wordOK = False
                            # playing = False
                            # voice.speak('컴퓨터의 승리!', dir)
                            # print(sword + '(으)로 시작하는 단어여야 합니다.')
                            return 'win_com'

                    if len(query) == 1:
                        wordOK = False
                        voice.speak('두 글자 이상의 단어를 말해주세요', dir)

                    if query in history: # 이미 말한 단어인 경우
                        return 'win_com'

                    if query[len(query) - 1] in blacklist:
                        return 'win_user_black'

                    if wordOK:
                        # 단어의 유효성을 체크
                        ans = checkexists(query, apikey, history)
                        if ans == '':
                            print('유효한 단어가 아닙니다')
                            return 'win_com'
        history.append(query)

        if playing:
            start = query[len(query) - 1]

            ans = findword(start + '*', apikey, history, blacklist)

            if ans == '':
                # ㄹ -> ㄴ 검색
                sdis = hgtk.letter.decompose(start)
                if sdis[0] == 'ㄹ':
                    newq = hgtk.letter.compose('ㄴ', sdis[1], sdis[2])
                    # print(start, '->', newq)
                    start = newq
                    ans = findword(newq + '*', apikey, history, blacklist)

            if ans == '':
                # (ㄹ->)ㄴ -> ㅇ 검색
                sdis = hgtk.letter.decompose(start)
                if sdis[0] == 'ㄴ' and sdis[1] in ('ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ'):
                    newq = hgtk.letter.compose('ㅇ', sdis[1], sdis[2])
                    # print(start, '->', newq)
                    ans = findword(newq + '*', apikey, history, blacklist)

            if ans == '':
                return 'win_user'
            else:
                answord = midReturn(ans, '<word>', '</word>')  # 단어 불러오기
                # ansdef = midReturn(ans, '<definition>', '</definition>')  # 품사 불러오기
                history.append(answord)

                # print(query, '>', answord, '\n(' + ansdef + ')\n')
                voice.speak(answord, dir)
                sword = answord[len(answord) - 1]