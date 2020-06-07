import cv2
from django.shortcuts import render,HttpResponse,redirect
from .myobj import order_msg
import json
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import tensorflow as tf
from .yzm.test import crack_captcha
from .yzm import demo
import numpy as np
# Create your views here.

graph=tf.get_default_graph()
model = demo.Discuz()

output = model.crack_captcha_cnn()
saver = tf.train.Saver()


def index(request):
    username = request.session.get('username', 'false')
    kw = order_msg( username=json.dumps(username), username2=username)
    return render(request,'app1/index.html',kw)

def login(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        passwd = request.POST.get('passwd')
        p = User.objects.filter(isdelete=False, rootid=account, passwd=passwd)
        if len(p) == 0:
            return render(request, 'app1/registered_ok.html', {'msg': '账号或密码错误'})
        elif len(p) == 1:
            request.session['username'] = account
            return redirect('/req')

        else:
            return render(request, 'app1/registered_ok.html', {'msg': '系统错误'})

def registered(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        passwd = request.POST.get('passwd')
        passwd2 = request.POST.get('passwd2')
        if passwd==passwd2:
            p = User.objects.filter(isdelete=False, rootid=account)
            if len(p) == 0:
                user = User()
                user.rootid = account
                user.passwd = passwd
                user.money = 0
                user.save()

                return render(request, 'app1/registered_ok.html', {'msg': '注册成功'})
            elif len(p) == 1:
                return render(request, 'app1/registered_ok.html', {'msg': '账号已存在'})
            else:
                return render(request, 'app1/registered_ok.html', {'msg': '系统错误'})
        else:
            return render(request, 'app1/registered_ok.html', {'msg': '系统错误'})

@csrf_exempt
def request_yzm(request):
    # return HttpResponse(12)
    width = 30
    heigth = 100
    if request.method == 'POST':
        account = request.POST.get('account')
        passwd = request.POST.get('passwd')
        p = User.objects.filter(isdelete=False, rootid=account, passwd=passwd)
        if len(p)==0:
            resp = {'status': 100, 'detail': 'Response success', 'content': '账号或者密码错误!', 'url': '/req/'}
            return JsonResponse(resp, safe=True)
        else:
            file=request.FILES.get('img')
            filename = file.name.split('.')[-1]
            print(filename)
            if filename in ['png', 'jpg', 'jpeg']:
                name = str(account) + '.png'
                path1 = 'static/imgs/' + name
                with open(path1, 'wb') as f:
                    f.write(file.read())
                batch_x = np.zeros([1, heigth * width])
                img = np.mean(cv2.imread(path1), -1)
                # 将多维降维1维
                batch_x[0, :] = img.flatten() / 255
                with graph.as_default():   #  调用默认图
                    with tf.Session() as sess:  # 更改
                        saver.restore(sess, tf.train.latest_checkpoint('app1/model/'))
                        img = batch_x[0].flatten()
                        predict = tf.argmax(tf.reshape(output, [-1, model.max_captcha, model.char_set_len]), 2)
                        text_list = sess.run(predict, feed_dict={model.X: [img], model.keep_prob: 1})
                        print(text_list)
                        text = text_list[0].tolist()
                        vector = np.zeros(model.max_captcha * model.char_set_len)
                        i = 0
                        for n in text:
                            vector[i * model.char_set_len + n] = 1
                            i += 1
                        prediction_text = model.vec2text(vector)
                        print("预测: {}".format(prediction_text))
                resp = {'status': 200, 'detail': 'Get success','content':prediction_text}
                return JsonResponse(resp, safe=True)
            else:
                resp = {'status': 404, 'detail': 'Get success'}
                return JsonResponse(resp, safe=True)
    else:
        return render(request,'app1/1.html')
