from django.contrib import admin

from .models import CustomUser

# Register your models here.





class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nickname', 'burakku')
    search_fields = ('id', 'email', 'nickname', 'burakku')#検索機能で検索できる中身

admin.site.register(CustomUser, PostAdmin)