from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users_authentication.models import UserSubscription, User


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        'id', 'username', 'first_name', 'last_name',
        'email', 'avatar', 'is_staff', 'is_superuser'
    )
    list_editable = ('first_name', 'last_name', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')


class UserSubscriptionAdmin(admin.ModelAdmin):
    model = UserSubscription
    list_display = ('user', 'subscribed')


admin.site.register(User, UserAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
