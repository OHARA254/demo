from django import forms

from accounts.models import CustomUser


class BookingForm(forms.Form):
    tel = forms.CharField(max_length=30, label='電話番号')
    remarks = forms.CharField(label='備考')


class NewsUpdateForm(forms.Form):
    
    news = forms.CharField(max_length=1000,label='お知らせ', widget=forms.Textarea())

class NicknameUpadateForm(forms.Form):
    nickname =forms.CharField(max_length=20,label="ニックネーム")


#class BookingDeleteForm(fomrs.Form):
