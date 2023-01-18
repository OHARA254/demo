from django.urls import path

from . import views
from django.contrib import admin
from django.contrib.auth.models import Group

app_name='app'

urlpatterns = [
    path('',views.IndexView.as_view(),name="index"),
    path('question',views.QuestionView.as_view(),name='question'),
    path('mypage',views.MypageView.as_view(),name='mypage'),
    path('bookingdelete/',views.BookingDeleteView.as_view(),name="bookingdelete"),
    path('search/',views.Search1View.as_view(),name='search_a'),
    path('newsupdate/',views.NewsUpdateView.as_view(),name='newsupdate'),
    path('nicknameupdate/',views.NicknameUpdateView.as_view(),name="nicknameupdate"),
    path('search_kekka/',views.Search_bView.as_view(),name='search_b'),
    path('done',views.DoneView.as_view(),name="done"),
    path('error',views.ErrorView.as_view(),name="error"),
    path('zaseki/',views.ZasekiView.as_view(),name='zaseki'),
    path('calendar/<int:pk>/', views.CalendarView.as_view(), name='calendar'), # 追加
    path('calendar/<int:pk>/<int:year>/<int:month>/<int:day>/', views.CalendarView.as_view(), name='calendar'), # 追加
    path('booking/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/', views.BookingView.as_view(), name='booking'), # 追加
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('bikou/', views.BikouView.as_view(), name='bikou'),
    path('riyou/', views.RiyouView.as_view(), name='riyou'),
    path('kinku', views.NicknameUpdateView.as_view(), name="kinku"),
    ]



admin.site.site_title = '大原図書館 内部管理サイト'
admin.site.site_header = '大原図書館 内部管理サイト'
admin.site.index_title = 'メニュー'
admin.site.unregister(Group) #指定したファイルを非表示にする

admin.site.disable_action('delete_selected') #削除機能を消す