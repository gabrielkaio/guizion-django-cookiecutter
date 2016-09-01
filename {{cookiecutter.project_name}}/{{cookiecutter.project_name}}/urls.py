"""project_name URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import \
    password_reset_done, password_reset_confirm, password_reset_complete, password_reset

from {{cookiecutter.project_name}}.apps.upload.api import PhotoUploadAPI
from {{cookiecutter.project_name}}.config.routes import router


apipatterns = [
    url(r'^', include(router.urls)),
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^v1/photo/', PhotoUploadAPI.as_view(), name='photo_upload')
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(apipatterns)),

    url(
        regex=r'^registration/password_reset/$',
        view=password_reset,
        kwargs={'html_email_template_name': 'registration/password_reset_email.html'},
        name='password_reset',
    ),
    url(
        regex=r'^registration/password_reset/done/$',
        view=password_reset_done,
        name='password_reset_done',
        kwargs={'template_name': 'registration/reset_pass_done.html'},
    ),
    url(
        regex=r'^registration/reset/(?P<uidb64>[0-9A-Za-z_\-]+)'
              r'/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        view=password_reset_confirm,
        kwargs={'template_name': 'registration/reset_pass_form.html'},
        name='password_reset_confirm'
    ),
    url(
        regex=r'^registration/reset/done/$',
        view=password_reset_complete,
        name='password_reset_complete',
        kwargs={'template_name': 'registration/reset_pass_done.html'},
    ),
]
