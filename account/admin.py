from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User

class UserAdmin(BaseUserAdmin):
    model = User
    # list_display = [field.name for field in User._meta.fields]
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff',]
    list_filter = ['is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    filter_horizontal = ()
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'mobile', 'user_id', 'college', 'department', 'designation', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'verified_by_admin')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'username', 'mobile', 'user_id', 'college', 'department', 'designation', 'role', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin', 'verified_by_admin'),
        }),
    )


admin.site.register(User, UserAdmin)
 