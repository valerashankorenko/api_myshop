from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = (
        'is_staff',
        'is_superuser',
        'groups',
        'user_permissions'
    )
    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'date_joined_format',
        'is_active'
    )
    list_display_links = (
        'id',
        'first_name',
        'last_name',
        'email',
        'date_joined_format'
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
    )
    ordering = ('id',)
    empty_value_display = '-пусто-'

    def date_joined_format(self, obj):
        return obj.date_joined.strftime(
            '%d-%m-%Y %H:%M'
        )

    date_joined_format.short_description = 'Дата регистрации'
