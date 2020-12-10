from django.db import models
class Link(models.Model): 
    # 슈퍼클래스 models의 하위클래스 Model을 상속받는다.
    # 필요한 데이터 정의
    original = models.TextField(null=False)
    shorts = models.CharField(max_length=8,primary_key=True)

    
    def __str__(self):
        return self.original

    
