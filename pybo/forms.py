from django import forms

from pybo.models import Question, Answer

class QuestioinForm(forms.ModelForm):
    class Meta:
        model = Question # # 사용할 모델
        fields = [ # QuestionForm에서 사용할 Question 모델의 속성
            'subject',
            'content'
        ]
        # 수동 폼 사용시에는 불필요
        #widgets = {
        #    'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #    'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        #}
        labels = {
            'subject': '제목',
            'content': '내용',
        }
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'content'
        ]
        lables = {
            'content': '답변내용'
        }