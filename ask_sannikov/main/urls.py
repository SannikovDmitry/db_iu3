from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^(/)?(?P<page>\d+)?$',
        views.index,
        name='/'
        ),
    url(r'^index/(?P<page>\d+)?$',
        views.index,
        name='index'
        ),
    url(r'^login/$',
        views.user_login,
        name='user_login'
        ),
    url(r'^registration/$',
        views.registration,
        name='registration'
        ),
    url(r'^settings/$',
        views.settings,
        name='settings'
        ),
    url(r'^like/(?P<question_id>[0-9]+)$',
        views.like,
        name='like'
        ),
    url(r'^dislike/(?P<question_id>[0-9]+)$',
        views.dislike,
        name='dislike'
        ),
    url(r'^ask/$',
        views.ask,
        name='ask'
        ),
    url(r'^logout/',
        views.logout,
        name='logout'
        ),
    url(r'^question/(?P<question_id>[0-9]+)/(?P<page>[0-9]+)?$',
        views.question,
        name='question'
        ),
    url(r'^top/(?P<page>[0-9]+)?$',
        views.top,
        name='top'
        ),
    url(r'^tag/(?P<htag>[a-zA-Z0-9]+)/(?P<page>[0-9]+)?$',
        views.tag,
        name='tag'
        ),
    url (r'^change-password/$',
        auth_views.password_change,
        {'template_name': 'change-password.html'}
        ),
]
