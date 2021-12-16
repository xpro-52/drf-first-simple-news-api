from django.contrib import admin
from django.contrib.auth import get_user_model


USER = get_user_model()

@admin.register(USER)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',)


