from django.urls import path
from . import views

app_name = 'comment'
urlpatterns = [
    path('',views.post_comment,name='post_comment')
]
