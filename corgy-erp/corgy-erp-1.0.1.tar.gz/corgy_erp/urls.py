"""corgy_erp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views import generic
from material.frontend import urls as frontend_urls
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from django.contrib.sitemaps import views as sitemapviews
from django.contrib.flatpages import views as flatviews
from .feeds import NewsFeed
from django.contrib.flatpages.sitemaps import FlatPageSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'flatpages': FlatPageSitemap,
}


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    #path('admin/', admin.site.urls),
    path('', include(frontend_urls)),
    #path('api/', include('snippets.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('i18n/', include('django.conf.urls.i18n')),
    url('avatar/', include('avatar.urls')),
    #path('license/', flatviews.flatpage, {'url': '/license/'}, name='license'),
    #path('privacy/', flatviews.flatpage, {'url': '/privacy/'}, name='privacy'),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/<int:news_id>/rss/', NewsFeed()),

    url('^$', generic.RedirectView.as_view(url='./workflow/'), name="index"),
    path('sitemap.xml', sitemapviews.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', sitemapviews.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

]

handler404 = 'corgy_erp.views.page_not_found_view'
handler500 = 'corgy_erp.views.error_view'
handler403 = 'corgy_erp.views.permission_denied_view'
handler400 = 'corgy_erp.views.bad_request_view'
