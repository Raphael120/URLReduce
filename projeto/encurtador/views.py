import string
from random import sample

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import redirect, render
from projeto.encurtador.models import Urllog, UrlRedirect


def home(requisicao):
    if requisicao.method == 'POST':
        link = requisicao.POST['link']
        slug = ''.join(sample(string.ascii_letters + string.digits, 5))

        url = UrlRedirect.objects.create(
            destino=link,
            slug=slug
        )
        url.save()
        return redirect(f'/relatorios/{slug}')

    return render(requisicao, 'encurtador/index.html')


def relatorios(requisicao, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    url_reduzida = requisicao.build_absolute_uri(f'/{slug}')
    redirecionamentos_por_data = list(
        UrlRedirect.objects.filter(
            slug=slug
        ).annotate(
            data=TruncDate('logs__criado_em')
        ).annotate(
            cliques=Count('data')
        ).order_by('data')
    )
    contexto = {
        'reduce': url_redirect,
        'url_reduzida': url_reduzida,
        'redirecionamentos_por_data': redirecionamentos_por_data,
        'total_de_cliques': sum(r.cliques for r in redirecionamentos_por_data)
    }
    return render(requisicao, 'encurtador/relatorio.html', contexto)


def redirecionar(requisicao, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    Urllog.objects.create(
        origem=requisicao.META.get('HTTP_REFERER'),
        user_agent=requisicao.META.get('HTTP_USER_AGENT'),
        host=requisicao.META.get('HTTP_HOST'),
        ip=requisicao.META.get('REMOTE_ADDR'),
        url_redirect=url_redirect
    )
    return redirect(url_redirect.destino)
