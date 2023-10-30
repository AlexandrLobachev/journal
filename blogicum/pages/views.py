from django.shortcuts import render
from django.views.generic import TemplateView


class AboutPage(TemplateView):
    """Возвращает страницу 'О проекте'."""

    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    """Возвращает страницу 'Наши правила'."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Возвращает страницу 'Ошибка 404'."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Возвращает страницу 'Ошибка 500'."""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)
