from django.shortcuts import HttpResponse,render,redirect
from app01 import models
import json
import datetime
from django.utils.safestring import mark_safe
# Create your views here.



def business(request):
    v1 = models.Business.objects.all()
    v2 = models.Business.objects.all().values('id','caption')
    v3 = models.Business.objects.all().values_list('id','caption')

    return render(request, 'business.html', {'v1': v1, 'v2': v2,'v3':v3})


# def host(request):
#     v1 = models.Host.objects.filter(nid__gt=0)
#     for row in v1:
#         print(row.nid,row.hostname,row.ip,row.port,row.b_id,row.b.caption)
#         # print(row.b.fk.name)
#s
#     v2 = models.Host.objects.filter(nid__gt=0).values('nid','hostname','ip','b_id','b__caption','port')
#     for row in v2:
#         print(row['nid'],row['hostname'],row['ip'],row['b_id'],row['b__caption'],row['port'])
#
#     v3 = models.Host.objects.filter(nid__gt=0).values_list('nid','hostname','ip','b_id','b__caption','port')
#
#
#
#     return render(request,'host.html',{'v1': v1,'v2':v2,'v3':v3})
#     # return render(request,'host.html', ['v1': v1, 'v2': v2, 'v3':v3])

def host(request):
    if request.method =="GET":
        v1 = models.Host.objects.filter(nid__gt=0)
        v2 = models.Host.objects.filter(nid__gt=0).values('nid','hostname','ip','b_id','b__caption','port')
        v3 = models.Host.objects.filter(nid__gt=0).values_list('nid','hostname','ip','b_id','b__caption','port')
        b_list = models.Business.objects.all()
        return render(request,'host.html',{'v1': v1,'v2':v2,'v3':v3,'b_list': b_list})

    elif request.method == "POST":
       h = request.POST.get('hostname')
       i = request.POST.get('ip')
       p = request.POST.get('port')
       b = request.POST.get('b_id')
       models.Host.objects.create(hostname=h,
                                   ip=i,
                                   port=p,
                                   b_id=b,
                                   )
    return redirect('/host')

    # return render(request,'host.html',{'v1': v1,'v2':v2,'v3':v3,'b_list': b_list})
    # return render(request,'host.html', ['v1': v1, 'v2': v2, 'v3':v3])

def test_ajax(request):
    ret = {'status': True, 'error': None, 'data': None}
    try:
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        p = request.POST.get('port')
        b = request.POST.get('b_id')
        if h and len(h) > 5:
            models.Host.objects.create(hostname=h,
                                           ip=i,
                                           port=p,
                                           b_id=b,
                                           )
        else:
            ret['status'] = False
            ret['error'] = '太短了'
    except Exception as e:
        ret['status'] = True
        ret['error'] = '请求错误'
    return HttpResponse(json.dumps(ret))




    # # print(request.method,request.POST,sep='\t')
    #     return HttpResponse('太短了')

def app(request):
    if request.method == "GET":

        app_list = models.Application.objects.all()
        # for row in app_list:
        #     print(row.name, row.r.all)
        host_list = models.Host.objects.all()
        return render(request, 'app.html', {"app_list": app_list, "host_list": host_list})

    elif request.method == "POST":
        app_name = request.POST.get('app_name')
        host_list = request.POST.getlist('host_list')
        # print(app_name,host_list)
        obj = models.Application.objects.create(name=app_name)
        obj.r.add(*host_list)

        return redirect('/app')


def ajax_add_app(request):
    ret = {'status': True, 'error': None, 'data': None}
    app_name = request.POST.get('app_name')
    host_list = request.POST.getlist('host_list')    #拿到所有的值
    obj = models.Application.objects.create(name=app_name)
    obj.r.add(*host_list)
    return HttpResponse(json.dumps(ret))



from utils import pagination

LIST = []
for i in range(159):
    LIST.append(i)

def user_list(request):
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    val = request.COOKIES.get('per_page_count')
    val = int(val)
    page_obj = pagination.Page(current_page,len(LIST),val)

    data = LIST[page_obj.start:page_obj.end]

    page_str = page_obj.page_str("/user_list")
    return render(request,"user_list.html", {"li": data, "page_str": page_str})     ## 返回前端 信息，页面 两个变量数值


###############################
##cookie##
user_info = {
    'hou1' : {'pwd':"123"},
    'hou2' : {'pwd':"jjjjj"},
}

def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('pwd')
        dic = user_info.get(u)
        if not dic:
            return render(request,'login.html')
        if dic['pwd'] == p:
            res = redirect('/index/')
            # res.set_cookie('username111',u,max_age=10)
            current_date = datetime.datetime.utcnow()
            current_date = current_date + datetime.timedelta(seconds=5)
            res.set_cookie('username111', u, expires=current_date)
            return res
        else:
            return render(request, 'login.html')



def index(request):
    v = request.COOKIES.get('username111')
    if not v:
        return redirect('/login/')
    return render(request,'index.html',{'current_user': v})




def cookie(request):
    request.COOKIES.get('username111')
    response = render(request,'index.html')
    response = redirect('/index/')
    response.set_cookie('key','value')
    current_date = datetime.datetime.utcnow()
    response.set_cookie('username111','value',max_age=10)
    return response