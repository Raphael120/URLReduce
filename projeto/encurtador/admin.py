from django.contrib import admin

# Register your models here.
from projeto.encurtador.models import UrlRedirect, Urllog


@admin.register(UrlRedirect)
class UrlRedirectAdmin(admin.ModelAdmin):
    list_display = ('destino', 'slug', 'criado_em', 'atualizado_em')


@admin.register(Urllog)
class UrllogAdmin(admin.ModelAdmin):
    list_display = ('criado_em', 'origem', 'user_agent', 'host', 'ip', 'url_redirect')
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
