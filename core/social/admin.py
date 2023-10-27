from django.contrib import admin

from social.models import SiteComment


class SiteCommentAdmin(admin.ModelAdmin):
    search_fields = ('user__username'),


admin.site.register(SiteComment, SiteCommentAdmin)
