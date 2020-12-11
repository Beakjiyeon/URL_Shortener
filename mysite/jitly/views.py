from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import base64
import random, string
from jitly.models import Link
from string import ascii_letters

# 특정 길이의 문자열 랜덤으로 생성해주는 함수
def rand_str(len, characters):
    # len : 결과 값 길이 / characters : 사용할 문자 리스트
    return "".join([random.choice(characters) for _ in range(len)])
    
def main(request):
    # POST 통신인 경우
    if request.method=='POST':
        input_url=request.POST.get("input_url")
        hidden=request.POST.get("hidden_box")

        if hidden=='wrong url':
            return render(request,'main.html')
        
        # original url이 기존에 있었는지 확인
        link=Link.objects.filter(original=input_url)
        
        if link:
            # 있으면 새로 암호를 만들지 않아도 됨
            result=Link.objects.get(original=input_url).shorts
            print('있습니당')
            print("뭐냐",Link.objects.filter(original=input_url))
            print("뭐냐2",result)
            return render(request, 'main.html',{'a':'http://127.0.0.1:8000/'+result})

        else :
            # 없으면 새로 만들어야 함
            # shortener 함수 호출
            # 기본값 3로 설정해둠. 나중에는 db에서 자리수 확인 후 지정가능할 듯
            alpah_digit_list=list(ascii_letters)+list(string.digits)
            print(alpah_digit_list)
            result='jitly/'+rand_str(3,alpah_digit_list)

            # 중복확인
            i=0
            while(True):

                key=Link.objects.filter(shorts=result)
                if key:
                    # 있으면 반복 계속
                    i=i+1
                    print(i+"번 만들었습니다.")
                    result='jitly/'+rand_str(3,alpah_digit_list)
                else:
                    break
            # DB에 저장 : 객체 생성
            link=Link(
                original=request.POST.get("input_url"),
                shorts=result
            )
            # DB에 반영
            link.save()
            return render(request, 'main.html',{'a':'http://127.0.0.1:8000/'+result})
        
    # GET 통신인 경우
    else :
        # 프론트만 출력
        return render(request, 'main.html')

def show(request,short):
    # db에서 short를 찾는다. 
    # short에 해당하는 original 링크를 찾는다.
    # original 링크로 리다이렉션 한다.

    # db에서 데이터 받아오기
    print('쇼트는',short)
    link=Link.objects.get(shorts='jitly/'+short)
    print('제발',link.original)
    #original='https://www.naver.com'
    return HttpResponseRedirect(link.original)
