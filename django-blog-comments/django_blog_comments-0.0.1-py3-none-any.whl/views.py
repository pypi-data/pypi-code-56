from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Post,Comment
from django.http import HttpResponseRedirect

# Create your views here.
@login_required
def post_comment(request):
    if request.method=='POST':
        url = request.POST.get('url')
        comment_text = request.POST.get('comment')
        user = request.user
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        if request.POST.get('parent'):
            comment_id = request.POST.get('parent')
            parent = Comment.objects.get(sno = comment_id)
            comment = Comment(comment_text=comment_text,user=user,post=post,parent=parent)
            comment.save()
        else:
            comment = Comment(comment_text=comment_text,user=user,post=post)
            comment.save()
    return redirect(url)