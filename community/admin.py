from django.contrib import admin
from .models import Comment, JointShipping

class CommentInline(admin.TabularInline):
    model = Comment

class JointShippingAdmin(admin.ModelAdmin):
    list_display = ('context',)  # 필요한 필드들을 추가하십시오.
    inlines = [CommentInline]  # CommentInline을 JointShipping 모델에 인라인으로 추가

admin.site.register(JointShipping, JointShippingAdmin)
