from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from user.models import User, UserMsg


@csrf_exempt
def home(request):
    try:
        username = request.session['user']
        print(">>",username)
        udata = User.objects.get(username=username)
        friends = User.objects.filter().exclude(username=username)
    except Exception as e:
        print(">>>",e)
        return redirect('login')
    data = {
        "fullname": udata.first_name + " " + udata.last_name,
        "friends": friends
    }
    return render(request, "home.html",data)


@csrf_exempt
def login(request):
    try:
        username = request.session['user']
        print(">>",username)
        data = User.objects.filter(username=username)
        return redirect('home')
    except Exception as e:
        print(">>>",e)
    if request.method == 'POST':
        if User.objects.filter(username = request.POST["username"],password=request.POST["password"]).exists():
            request.session['user'] = request.POST["username"]
            return redirect('home')
    return render(request, "login.html")


@csrf_exempt
def signup(request):
    if request.method == "POST":
        if request.POST["psw"] == request.POST["psw-repeat"]:
            User(
                username=request.POST["uname"],
                first_name=request.POST["fname"],
                last_name=request.POST["lname"],
                phone=request.POST["phone"],
                email=request.POST["email"],
                password=request.POST["psw"]
            ).save()
            return redirect('login')
        else:
            return redirect('signup')
    return render(request, "signup.html")


@csrf_exempt
def logout(request):
    del request.session['user']
    return redirect('login')


@csrf_exempt
def chat(request, username):
    if request.method == 'POST':
        try:
            pmsg = []
            select_user = request.session['select_user']
            uname = request.session['user']
            msg = request.POST["msg"]
            udata = User.objects.get(username=uname)
            pmsg = UserMsg.objects.filter(Q(sender__in=[uname,select_user]) & Q(reciver__in=[uname,select_user]))
            if pmsg.exists():
                print("here",pmsg[0].message)
                pmsg = pmsg[0].message
                pmsg.append({
                    "msg": msg,
                    "sender": udata.first_name+ " "+udata.last_name
                })
                print(pmsg)
                UserMsg.objects.filter(Q(sender__in=[uname,select_user]) & Q(reciver__in=[uname,select_user])).update(
                    message=pmsg
                )
            else:
                pmsg = []
                pmsg.append({
                    "msg": msg,
                    "sender": udata.first_name+ " "+udata.last_name
                })
                UserMsg(
                    sender=uname,
                    reciver=select_user,
                    message=pmsg
                ).save()
        except Exception as e:
            print(">>>", e)
            return redirect('login')
    try:
        request.session['select_user'] = username
        select_user = username
        uname = request.session['user']
        print(">>",uname)
        udata = User.objects.get(username=uname)
        friends = User.objects.filter().exclude(username=uname)
        msg = UserMsg.objects.filter(Q(sender__in = [uname,username]) & Q(reciver__in=[username,uname]))
        if msg.exists():
            msg = msg[0]
            message =  msg.message
        else:
            message = []
    except Exception as e:
        print(">>>",e)
        return redirect('login')
    # print(message)
    message.reverse()
    data = {
        "fullname": udata.first_name + " " + udata.last_name,
        "friends": friends,
        "message": message,
        "select_user": select_user
    }
    return render(request, "chat.html", data)