from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Comments
from django.conf import settings
from django.http import HttpResponseRedirect
from django.apps import apps as django_app

# Create your views here.
@login_required
def post_comment(request):
    if request.method=='POST':
        url = request.POST.get('url')
        comment_text = request.POST.get('comment')
        user = request.user
        post_id = request.POST.get('post_id')
        Post = django_app.get_model(settings.POST_MODEL)
        post = Post.objects.get(id=post_id)
        if request.POST.get('parent'):
            comment_id = request.POST.get('parent')
            parent = Comments.objects.get(sno = comment_id)
            comment = Comments(comment_text=comment_text,user=user,post=post,parent=parent)
            comment.save()
        else:
            comment = Comments(comment_text=comment_text,user=user,post=post)
            comment.save()
    return redirect(url)