from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import base64
import random, string
from jitly.models import Link
from string import ascii_letters

# 함수:특정 길이의 문자열 랜덤으로 생성
# len:결과 값 길이, characters:사용할 문자 리스트
def rand_str(len, characters):
    return "".join([random.choice(characters) for _ in range(len)])

# 함수:URL 입력 화면, Link 정보를 DB에 저장
def main(request):

    # POST 통신인 경우
    if request.method=='POST':
        # 1. Form 데이터 받아 옴
        # 입력된 original URL
        input_url=request.POST.get("input_url")
        # 자바스크립트에서 유효한 URL인지 검증한 결과 값
        hidden=request.POST.get("hidden_box")

        # 2. 검사
        # URL이 유효하지 않다면, HTML 페이지로 이동
        if hidden=='wrong url':
            return render(request,'main.html')

        # 3. 입력된 URL이 기존 DB에 있는 지 확인
        link=Link.objects.filter(original=input_url)
        # 있으면 새로 암호를 만들지 않아도 됨
        if link:
            # 해당하는 DB를 불러옴
            result=Link.objects.get(original=input_url).shorts
            # localhost 사용
            return render(request, 'main.html',{'result':'http://127.0.0.1:8000/'+result})

        # 4. 없으면 Short URL 새로 만들어야 함
        else :
            # 알파벳 대, 소문자, 숫자 0~9 로 구성된 리스트
            alpah_digit_list=list(ascii_letters)+list(string.digits)
            # Short URL 생성(나중에는 db에서 자리수 확인 후 지정가능할 듯)
            result='jitly/'+rand_str(3,alpah_digit_list)
            # 중복확인:성능 저하. + 10번까지 하고 계속 중복이면, 더이상 만들지 않음. UI 메세지로 보여줘야 할듯.
            i=0
            while(True):
                key=Link.objects.filter(shorts=result)
                if key:
                    # 중복 값이 있으면 반복 계속
                    result='jitly/'+rand_str(3,alpah_digit_list)
                    i=i+1
                    if i==10:
                        result=''
                        break;
                else:
                    break
            
            # 새로 만든 Short URL DB에 저장
            link=Link(
                original=request.POST.get("input_url"),
                shorts=result
            )
            link.save()
            # localhost 사용
            return render(request, 'main.html',{'result':'http://127.0.0.1:8000/'+result})
        
    # GET 통신인 경우
    else :
        # 프론트만 출력
        return render(request, 'main.html')

# Short를 Original로 리다이렉션 하는 함수
def show(request,short):
    # 1. db에서 short인 객체를 찾는다. 
    # 2. short에 해당하는 original 링크를 찾는다.
    # 3. original 링크로 리다이렉션 한다.
    link=Link.objects.get(shorts='jitly/'+short)
    return HttpResponseRedirect(link.original)
