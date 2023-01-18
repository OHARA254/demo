from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from datetime import datetime, date, timedelta, time
from django.views.generic import View, TemplateView
from .models import Zaseki, Booking, News, Siyouritu
from django.views import generic
from django.utils.timezone import localtime, make_aware
from django.db.models import Q
import qrcode
import base64
from io import BytesIO
from PIL import Image
from accounts.models import CustomUser
# -*- coding: utf-8 -*-
import hashlib
from .forms import BookingForm, NewsUpdateForm, NicknameUpadateForm
from .mixin import SuperuserRequiredMixin, StaffRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseBadRequest
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from allauth.account.models  import EmailAddress 
from allauth.account.adapter import DefaultAccountAdapter
from django.db import models
from . import models
from . import graph


# Create your views her
# from io import BytesIOe.

class IndexView(View):

    def get(self, request, *args, **kwargs):
        news = News.objects.filter().order_by('-day')[:5]
        return render(request,'Index.html',{
        'news' : news,
        })

    





class QuestionView(TemplateView):
    template_name="question.html"


class ZasekiView(View):

    def get(self, request, *args, **kwargs):
        zaseki_data = Zaseki.objects.all()

        return render(request, 'booking/zaseki.html',{
            'zaseki_data': zaseki_data,
        })


class CalendarView(View):


    def get(self, request, *args, **kwargs):
        zaseki = Zaseki.objects.get(id=self.kwargs['pk'])
        today = date.today()
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            # 週始め
            start_date = date(year=year, month=month, day=day)
        else:
            start_date = today
        # 1週間
        days = [start_date + timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        calendar = {}
        # 10時～20時
        for hour in range(10, 18):
            row = {}
            for day in days:
                row[day] = True
            calendar[hour] = row
        start_time = make_aware(datetime.combine(start_day, time(hour=10, minute=0, second=0)))
        end_time = make_aware(datetime.combine(end_day, time(hour=20, minute=0, second=0)))
        booking_data = Booking.objects.filter(zaseki=self.kwargs['pk']).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] = False
            
        return render(request, 'booking/calendar.html', {
            'zaseki_data': zaseki,
            'calendar': calendar,
            'days': days,
            'start_day': start_day,
            'end_day': end_day,
            'before': days[0] - timedelta(days=7),
            'next': days[-1] + timedelta(days=1),
            'today': today,
        })


class BookingView(View):
    def get(self, request, *args, **kwargs):
        zaseki = Zaseki.objects.get(id=self.kwargs['pk'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        form = BookingForm(request.POST or None)

        return render(request, 'booking/booking.html', {
            'zaseki_data': zaseki,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        zaseki_data = get_object_or_404(Zaseki, id=self.kwargs['pk'])
        booking_dataxxx = get_object_or_404(CustomUser, id=self.request.user.id)
        user = CustomUser.objects.get(pk = self.request.user.id)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
        end_time = make_aware(datetime(year=year, month=month, day=day, hour=hour + 1))
        days = make_aware(datetime(year=year,month=month,day=day))
        booking_data = Booking.objects.filter(zaseki=self.kwargs['pk'], start=start_time)
        booking_data1 = CustomUser.objects.get(pk=self.request.user.id)
        #顧客の予約上限数を判定　予約
        booking_data2 = Booking.objects.filter(customer=self.request.user.id, today=days)
        #顧客が当日の予約上限に達しているか判定　
        booking_data3 = Booking.objects.filter(customer=self.request.user.id, start=start_time)
        #顧客が同じ時間帯で複数予約をしないように設定
        booking_data4 = Booking.objects.filter(customer=self.request.user.id, end=end_time)
        #顧客が同じ時間帯で複数予約をしないように設定
        booking_data5 = Siyouritu.objects.get(name=self.kwargs['pk'])

        form = BookingForm(request.POST or None)
        if booking_data.exists():    
            form.add_error(None, '既に予約があります。\n別の日時で予約をお願いします。')
        elif user.burakku == True:#ブラックリストようの判別
            form.add_error(None, 'このアカウントは現在予約できません。\n職員の指示に従ってください。')
        elif  user.is_staff == True:
            booking = Booking()
            booking_data1.booking_kazu += 1
            booking_data5.kazu += 1
            booking.zaseki = zaseki_data
            booking.start = start_time
            booking.end = end_time
            booking.tel = form.data['tel']
            booking.remarks = form.data['remarks']
            booking.customer = booking_dataxxx
            booking.today = days
            booking.save()
            booking_data1.save()
            booking_data5.save()
            return redirect('app:thanks')
        elif booking_data1.booking_kazu  >= 3:
            form.add_error(None, '予約上限に達しています。\n予約上限数は3です。')
        elif booking_data2.exists():
            form.add_error(None, '既に本日分の予約をしております。\n別の日付で予約をお願いします。')
        elif booking_data3.exists():
            form.add_error(None, '既に同じ時間帯で予約があります。\n別の時間で予約をお願いします。')
        elif booking_data4.exists(): 
            form.add_error(None, '既に同じ時間帯で予約があります。\n別の時間で予約をお願いします。')
        elif form.is_valid():
            booking = Booking()
            booking_data1.booking_kazu += 1
            booking_data5.kazu += 1
            booking.zaseki = zaseki_data
            booking.start = start_time
            booking.end = end_time
            booking.tel = form.cleaned_data['tel']
            booking.remarks = form.cleaned_data['remarks']
            booking.customer = booking_dataxxx
            booking.today = days
            booking.save()
            booking_data1.save()
            booking_data5.save()
                                    
            return redirect('app:thanks') 

        return render(request, 'booking/booking.html', {
            'zaseki_data': zaseki_data,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form,
        })

class ThanksView(TemplateView):
    template_name = 'booking/thanks.html'

class BookingDeleteView(View):
 
    def get(self, request, *args, **kwargs):
        Custom = CustomUser.objects.get(pk = self.request.user.id)
        x = Custom.booking_kazu
        days = date.today()
        booking = Booking.objects.filter(customer = self.request.user.id, today__gte = days).order_by('today')
        return render(request,"bookingdelete.html",{
            "booking_data" : booking
        })
    
    def post(self, request, *args, **kwargs):
        try:
            delete = self.request.POST['delete']
            Booking.objects.filter(pk = delete).delete()
            Custom = CustomUser.objects.get(pk = self.request.user.id)
            if Custom.is_staff == False:
                Custom.booking_kazu -= 1
                Custom.save()
            return redirect('app:mypage') 
        except:
            return redirect('app:error')



class Search1View(StaffRequiredMixin,TemplateView):
    template_name = 'search/search_a.html'

class Search_bView(StaffRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        try:
            yuubin = self.request.GET["yuubin"]
            birth1  = self.request.GET["birth"]
            last = self.request.GET["last_name"]
            first = self.request.GET["first_name"]
            cusyuu = CustomUser.objects.get(post_code = yuubin, birth = birth1, last_name = last, first_name = first)
        except:
            return redirect('app:error') 
        return render(request,"search/search_b.html",{
            "cusyuu" : cusyuu,
                    })

    def post(self, request, *args, **kwargs):
        lastn = self.request.POST["lastn"]
        firstn = self.request.POST["firstn"]
        aaddress = self.request.POST["aaddress"]
        emaila = self.request.POST["emaila"]
        postcode = self.request.POST["postcode"]
        tell1 = self.request.POST["tell1"]
        pk1 = self.request.POST["pk"]
        updateemail = EmailAddress.objects.get(user_id = pk1)
        update1 = CustomUser.objects.get(pk = pk1)
        update1.last_name = lastn
        update1.first_name = firstn
        update1.address = aaddress
        update1.email = emaila
        update1.post_code = postcode
        update1.tel = tell1
        updateemail.email = emaila
        update1.save()
        updateemail.save()
        return redirect('app:done') 

class DoneView(TemplateView):
    template_name = 'search/done.html'

class ErrorView(TemplateView):
    template_name = 'search/error.html'


class MypageView(View):

    def get(self, request, *args, **kwargs):

        user = CustomUser.objects.get(pk =self.request.user.id )
        booking = Booking.objects.filter(customer = self.request.user.id).order_by('-start')[:30]
        return render(request,"mypage.html",{
            "user" : user,
            "booking_data" : booking
                    })

class NewsUpdateView(View):

    def get(self, request, *args, **kwargs):
        form = NewsUpdateForm
        today = date.today()

        return render(request,"newsupdate.html",{
            "form" : form,
            "today" : today
                    })

    def post(self, request, *args, **kwargs):
        news = self.request.POST['news']
        newsz = News()
        newsz.news = news
        newsz.save()
        return redirect('app:done') 

class NicknameUpdateView(View):

    def get(self, request, *args, **kwargs):
        form = NicknameUpadateForm
        
        return render(request,"nicknameupdate.html",{
            "form" : form
                    })
    
    def post(self, request, *args, **kwargs):
        nickname = CustomUser.objects.get(pk = self.request.user.id)
        new = self.request.POST['nickname']
        if "いけだ" in new:
            return redirect('app:kinku')
        elif "こばやし" in new:
            return redirect('app:kinku')
        else:
            nickname.nickname = new
            nickname.save()
            return redirect('app:done') 
        



class BikouView(View):
    def get(self, request, *args, **kwargs):
        todays = date.today()
        day = timedelta(days=7)
        kijun = "あればここに記入する"
        Custom = Booking.objects.filter(Q(today__gte=todays),Q(today__lte=todays+day))
        
        
        return render(request,"bikou.html",{
            "Custom" : Custom,
            "kijun" : kijun,
        })


class RiyouView(TemplateView):
     #変数としてグラフイメージをテンプレートに渡す
    def get_context_data(self, **kwargs):

        #グラフオブジェクト
        qs    = models.Siyouritu.objects.all()  #モデルクラス(ProductAテーブル)読込
        x     = [x.name for x in qs]           #X軸データ
        y     = [y.kazu for y in qs]        #Y軸データ
        chart = graph.Plot_Graph(x,y)          #グラフ作成

        #変数を渡す
        context = super().get_context_data(**kwargs)
        context['chart'] = chart
        return context

    #get処理
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

     #テンプレートファイル連携
    template_name = "riyou.html"


