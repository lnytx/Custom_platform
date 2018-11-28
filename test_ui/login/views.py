
import json

from django.contrib import auth
from django.contrib.admin import models
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.forms.models import model_to_dict
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

from pymysql_conn import exec_sql_args, exec_sql, connect
from salt_api.Mytoolkits import DateEncoder , get_user_info, format_result
from templates.fenye.feye import Pagination


# Create your views here.
def index(request):
    '''判断用户是否登陆'''
    #.is_authenticated()通过判断session中是否有user_id 以及user_backend 来判断用户是否登陆。
#     if not  request.user.is_authenticated():
#         return HttpResponseRedirect('/login/')
    username=request.user.username
    return render_to_response('login.html',{'username':username})

def login(request):
    '''
    2.插入数据用户名密码时应该用User.objects.create_user(username=username,password=password)，这个方法会把密码生成哈希值，插进数据库，而不能用User.objects.create（。。。。），这样插进去的数据密码是明文滴~~~~

                总结：用对方法User.objects.create_user(username=username,password=password)，插对表user
    '''
    #User.objects.create_user(username='root',password='root')
    if request.method == 'POST':
        session_txt={}
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("username,password",username,password)
#         user = User.objects.get(username=username)
        #ret = User.objects.filter(username = username)
        #使用Q对象建立多个查询条件
        ret = User.objects.filter(Q(username=username) | Q(password=password))
        for x in ret:
            session_txt['userid']=x.id
            session_txt['last_login']=json.dumps(x.last_login, cls=DateEncoder)
        session_txt['username']=username
        session_txt['password']=password
        #设置session
        print("session_txt",session_txt)
        request.session.modified = True
        request.session['session_txt'] = session_txt
        #session过期时间
        
        request.session.set_expiry(6000)
#         ret=User.objects.get(id=username)
        #session
        request.session['userid'] = username
        request.session['username'] = password
        print("post",username)
        if username is not None and password is not None:
            try:
                user = auth.authenticate(username=username,password=password)
                print("get_all_permissions",user.get_all_permissions())
                print("get_group_permissions()",user.get_group_permissions())
            except Exception as e:  
                print("str(e)",str(e))
        if user is not None and user.is_active:
            auth.login(request,user)
            print("usernameaaa",username)
            #request.session['username']=username
            #return HttpResponseRedirect('index')
            return render_to_response('index.html',{'username':username})
            #return render_to_response('git_manage/git_manage.html',{"code":1})
        else:
            print("验证错误",username)
            return render_to_response('login.html',{'login_error':'用户名或密码错误!!!!!'})
    return render_to_response('login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')
#仪表盘
def login_dashboard(request):
    user_name = request.user
    ret = get_user_info(user_name)
    username = ret['user_name']
    #计算主机、salt_key、项目数量
    sql = 'select count(*) count from host'
    count_host = exec_sql(sql)[0]['count']
    sql = 'select count(minion_id) count from host'
    count_salt_key = exec_sql(sql)[0]['count']
    sql = 'select count(distinct project_name) count from project_manage'
    count_project = exec_sql(sql)[0]['count']
    sql = 'select count(*) count from auth_user'
    count_auth_user = exec_sql(sql)[0]['count']
    print("count_host",count_host)
    print("count_salt_key",count_salt_key)
    print("count_project",count_project)
    print("count_auth_user",count_auth_user)
    return render_to_response('index.html',locals())

@login_required
@permission_required('login.can_view')
def view_logs(request):
    user_name = request.user
    #每页显示数量
    ONE_PAGE_OF_DATA = int(request.GET.get('check_num',default=5))
    #如果为0的话就设置成默认值5
    if int(ONE_PAGE_OF_DATA)==0:
        ONE_PAGE_OF_DATA=5
    #当前页
    current_page = request.GET.get('p')
    print("显示数量",type(ONE_PAGE_OF_DATA),ONE_PAGE_OF_DATA)
    print("p_sql",type(user_name),user_name)
    allPostCounts=''
    print("获取权限",user_name.get_group_permissions())
    ret = get_user_info(user_name)
    #如果是超级用户就获取所有的日志记录
    if user_name.is_superuser:
        count_sql = "select count(*) from operation_record a,auth_user b \
                   where a.user_id=b.id"
        allPostCounts = exec_sql("select count(*) count from `operation_record`")
        print("allPostCounts超级用户",allPostCounts)
    else:
        count_sql= "select count(*) count from operation_record a,auth_user b \
                        where a.user_name=%s and a.user_id=b.id"
        allPostCounts = exec_sql_args(count_sql,ret['user_name'])
        print("allPostCounts非超级",allPostCounts)
    #每页多少条记录
    #ONE_PAGE_OF_DATA=3
    #current_page = request.GET.get('p')
    #allPostCounts = exec_sql("select count(*) count from `host`")
    print("allPostCounts",type(allPostCounts[0]['count']),allPostCounts[0]['count'])
    total_num = int(allPostCounts[0]['count'])
    total_page_count = int(allPostCounts[0]['count'] / ONE_PAGE_OF_DATA)
    print("allPage",total_page_count)
    #有多少页
    remainPost = allPostCounts[0]['count'] % ONE_PAGE_OF_DATA
    #总共的数量
    if remainPost > 0:  
        total_page_count += 1 
    print("allPage",total_page_count)
    '''调用工具类进行分页
    from templates.test.fenye.feye import Pagination
    '''
    page_obj = Pagination(current_page,total_num,ONE_PAGE_OF_DATA,total_page_count,page_url="log_view")
    print("page_obj.start_page_item()",page_obj.start_page_item())
    print("page_obj.end_page_item()",page_obj.end_page_item())
    #mysql这样来分页
    print("user_name.is_superuser",user_name.is_superuser)
    if user_name.is_superuser:
        p_sql = "select a.user_name,a.action,a.target_ids,a.result,a.exec_time,b.last_login,b.date_joined \
            from operation_record a,auth_user b \
            where a.user_id=b.id limit %s,%s"
        user_log = exec_sql_args(p_sql,(page_obj.start_page_item(),ONE_PAGE_OF_DATA))
    else:
        p_sql = "select a.user_name,a.action,a.target_ids,a.result,a.exec_time,b.last_login,b.date_joined \
                from operation_record a,auth_user b \
                where a.user_name=%s \
                and a.user_id=b.id limit %s,%s"
        user_log = exec_sql_args(p_sql, (ret['user_name'],page_obj.start_page_item(),ONE_PAGE_OF_DATA))
    #data_list = USER_LIST[page_obj.start_page_item():page_obj.end_page_item()]
    print("page_obj",type(page_obj),page_obj.page_str)
    return render(request,'operation_record/operation_record.html',{'user_log':user_log,'page_obj':page_obj,'total_num':total_num})


#查看日志
def view_details(request):
    target_ids = request.GET.get("target_ids")
    print("target_ids",type(target_ids),target_ids)
    user_name = request.user
    p_sql = "select * from opertion_minions \
                where target_ids=%s"
    user_log = exec_sql_args(p_sql,(target_ids,))
    print("user_log",user_log)
    return render(request,'operation_record/details.html',{"user_log":user_log})

#查找日志
def search_log(request):
    log_operation_name = str(request.GET.get("log_operation_name"))
    print("log_operation_name",log_operation_name)
    log_starttime = str(request.GET.get("log_starttime"))
    print("log_starttime",type(log_starttime),log_starttime)
    log_endtime = str(request.GET.get("log_endtime"))
    #每页显示数量
    ONE_PAGE_OF_DATA = int(request.GET.get('check_num',default=5))
    #如果为0的话就设置成默认值5
    if int(ONE_PAGE_OF_DATA)==0:
        ONE_PAGE_OF_DATA=5
    print("每页显示数量",type(ONE_PAGE_OF_DATA),ONE_PAGE_OF_DATA)
    #当前页
    current_page = request.GET.get('p')
    allPostCounts=''
    parmas = []
    conn=connect()
    cursor = conn.cursor()
    sql_count = "select count(*) count \
            from operation_record a,auth_user b \
            where a.user_id=b.id and 1=1 "
    sql_base = "select a.user_name,a.action,a.target_ids,a.result,a.exec_time,b.last_login,b.date_joined \
            from operation_record a,auth_user b \
            where a.user_id=b.id and 1=1 "
    if log_operation_name != 'None' and log_operation_name.rstrip()!='':
        sql_base += "and a.user_name like '%%%%%s%%%%'";
        sql_count += "and a.user_name like '%%%%%s%%%%'";
        parmas.append(log_operation_name);
    if log_starttime != 'None' and log_starttime.rstrip()!='':
        print("有空值1")
        sql_base += " and a.exec_time >= '%s'";  
        sql_count += " and a.exec_time >= '%s'";  
        parmas.append(log_starttime);
    if log_endtime != 'None' and log_endtime.rstrip()!='':
        print("有空值2")
        sql_base += " and a.exec_time <= '%s'";  
        sql_count += " and a.exec_time <= '%s'";  
        parmas.append(log_endtime);
    print("parmas",type(parmas),parmas,tuple(parmas))
    sql_count = sql_count %(tuple(parmas))
    #确定查询的总数量
    print("sql_count",sql_count)
    cursor.execute(sql_count)
    allPostCounts = cursor.fetchall()
    print("allPostCounts",type(allPostCounts),allPostCounts)
    search_total_num = int(allPostCounts[0]['count'])
    total_page_count = int(allPostCounts[0]['count'] / ONE_PAGE_OF_DATA)
    #有多少页
    remainPost = allPostCounts[0]['count'] % ONE_PAGE_OF_DATA
    #总共的数量
    if remainPost > 0:  
        total_page_count += 1 
    #分页的URL，按之前的可能就跳到默认所有的分页界面了
    page_url = "log_view/search_log/?check_num=%s&log_operation_name=%s&log_starttime=%s&log_endtime=%s" %(ONE_PAGE_OF_DATA,log_operation_name,log_starttime,log_endtime)
    #print("page_url",page_url)
    #生成page分页对象
    search_page_obj = Pagination(current_page,search_total_num,ONE_PAGE_OF_DATA,total_page_count,page_url=page_url)
    #正式加上分页limit
    sql_result = sql_base %(tuple(parmas))
    sql_result = sql_result+' limit %s,%s' % (search_page_obj.start_page_item(),ONE_PAGE_OF_DATA)
    print("sql_result",sql_result)
    cursor.execute(sql_result)
    search_user_log = cursor.fetchall()
    #获取结果
    #user_log = 
    #print("result",type(user_log),user_log)
    #msg={'code':1,'msg':'error'}
    print("search_page_obj",type(search_page_obj),search_page_obj.search_page_str)
    #return HttpResponse(json.dumps(msg), content_type='application/json')
    return render(request,'operation_record/operation_record.html',{'search_user_log':search_user_log,'search_page_obj':search_page_obj,'search_total_num':search_total_num,'ONE_PAGE_OF_DATA':ONE_PAGE_OF_DATA})