from django.shortcuts import render, HttpResponse, Http404
from studentCRM import forms
from studentCRM import models
from django.forms.models import ModelFormMetaclass
from django.db.models.base import ModelBase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json
# Create your views here.


def get_model_form(table_name):
    """通过model表名获取model form对象
    """
    for obj in dir(forms):
        form_obj = getattr(forms, obj)
        if isinstance(form_obj, ModelFormMetaclass):  # 判断是不是一个modelform实例
            model_obj = form_obj._meta.model
            model_object_name = model_obj._meta.object_name  # 获取model对应的类名
            model_model_name = model_obj._meta.model_name  # 获取model对应的表名
            if (model_object_name or model_model_name) == table_name:
                return form_obj


def get_model(model):
    """通过字符串反射获取model对象"""
    model_obj = model
    if isinstance(model, str):
        if hasattr(models, model):
            model_obj = getattr(models, model)
    return model_obj


@login_required
def admin_add_list(request, table_name):
    """添加数据页面
    request: 封装的请求对象
    table_name: 操作的表名
    """
    context = {}
    model_form = get_model_form(table_name)  # 尝试获取model form对象
    if model_form is None:  # 如果获取不到form对象,请求可能非法,直接返回404错误页面
        raise Http404
    form_data = model_form()  # 实例化form表单
    if request.method == 'POST':
        form_data = model_form(request.POST)  # 如果是POST请求,则进行校验数据
        if form_data.is_valid():
            form_data.save()
            context["message"] = "添加成功"
        else:
            context["error_message"] = "添加失败"

    context["model_form"] = form_data  # 返回model form 对象
    context["table_name"] = table_name  # 返回表名
    return render(request, 'studensCRM/add_list.html', context)


def admin_search_list(request):
    context = {}
    if request.method == 'POST':
        qq = str(request.POST.get('qq')).strip()
        context['qq'] = qq
        try:
            user_info = models.Customer.objects.get(qq=qq)
            context['user_info'] = user_info
        except Exception as e:
            print(e)

    return render(request, 'studensCRM/search_list.html', context)


def admin_update_list(request, table_name, data):
    print(data)
    ret = {"status": True, "error": ""}  # 定义返回状态信息
    model_obj = get_model(table_name)
    get_data = data.get('data', False)
    if get_data and type(get_data) is list:
        for each_data_dic in get_data:
            get_id = each_data_dic.get("id")
            if get_id:
                each_data_dic.pop('id')
                try:
                    model_obj.objects.filter(id=get_id).update(**each_data_dic)
                except (TypeError or ValueError or ValidationError) as e:
                    ret["status"] = False
                    ret["error"] = str(e)

    return HttpResponse(json.dumps(ret))


def admin_delete_list(request, table_name, data):
    """
    request: 该请求默认为POST请求
    table_name:表名
    del_list: 删除的数据列表
    """
    ret = {"status": True, "error": ""}  # 定义返回状态信息
    model_obj = get_model(table_name)
    del_list = data.get("del")  # 获取删除对象列表
    try:
        for pk in del_list:
            model_obj.objects.filter(id=pk).delete()
    except Exception as e:
        ret['status'] = False
        ret["error"] = e
    return HttpResponse(json.dumps(ret))


# get请求操作处理,定义指定的修改,和添加操作
get_actions = {
    'add': admin_add_list,
}
# post操作请求处理,主要是AJAX
post_actions = {
    "update": admin_update_list,
    "delete": admin_delete_list,
}


def resolve_url(request):
    """
    request:分解URL为列表形式
    """
    url = request.path.strip('/').split('/')
    return url


def gel_all_field_names(model):
    """
    model :model对象
    return: model的字段名
    """
    names = []
    model_obj = get_model(model)
    try:
        get_fields = model_obj._meta.get_fields()
        for field in get_fields:
            names.append(field.name)
    except AttributeError:
        pass
    return names


def get_all_field_obj(model, fields):
    """
    model: model对象
    fields: model字段列表,可以通过get_all_field_names获取
    """
    field_obj_list = []
    model_obj = get_model(model)
    try:
        for field in fields:
            field_obj = model_obj._meta.get_field(field)  # 获取字段对象
            field_obj_list.append(field_obj)
    except AttributeError:
        pass
    return field_obj_list


def get_model_data(model):
    """
    model: model 对象
    """
    model_obj = get_model(model)
    try:
        get_all_data = model_obj.objects.all()
        return get_all_data
    except AttributeError:
        pass
    return []  # 如果没有数据,则返回空列表,注意!这里返回对象的必须是可迭代对象,防止页面渲染异常!


def home(request):
    """首页"""
    context = {}
    register_model = []  # 存放展示在前端的model对象,如果想排除不想展示的对象,可以尝试遍历该列表,然后获取指定不希望展示的model名,remove
    app_name = models.__package__  # 获取当前app的名字
    for obj in dir(models):  # 遍历models文件,获取对应的model对象,用来页面展示
        model_obj = getattr(models, obj)
        if isinstance(model_obj, ModelBase):  # 判断是不是一个model实例
            if model_obj._meta.app_label == app_name:  # 当对象的app名字属于当前APP则展示在前端
                register_model.append(model_obj)
    context['app_name'] = app_name  # 设置页面显示APP名字
    context['tables_obj'] = [model._meta for model in register_model]  # 获取每个model对象的_meta方法
    return render(request, 'studensCRM/home.html', context)


@login_required
def admin_controller(request):
    """
    数据展示页面
    """
    context = {}
    ret = {"status": True, "error": ""}  # 定义ajax返回信息
    get_url = resolve_url(request)
    if len(get_url) >= 4:  # 所有请求的URL长度必须大于等于4位,否则请求非法,返回错误页面
        table_name = get_url[2]
        action = get_url[3]  # 获取URL对应的操作
        if action in get_actions:  # 判断GET请求操作是否在actions内,是则反射操作
            return get_actions.get(action)(request, table_name)
        if request.method == "POST":
            data = request.POST.get("data")
            if data:  # 如果能获取到,可能是ajax请求
                data = json.loads(data)
                action = data.get('action', False)  # 尝试获取操作
                if action in post_actions:
                    return post_actions.get(action)(request, table_name, data)
                return HttpResponse(json.dumps(ret))  # 如果是ajax请求,前面没有匹配的操作,则返回ret
        if hasattr(models, table_name):  # 尝试通过表名获取model对象
            fields = gel_all_field_names(table_name)  # 获取表字段
            if 'id' in fields:  # 如果存在ID值,则删除,该值不直接显示,通过手动绑定对应的元素即可
                fields.remove('id')
            field_obj_list = get_all_field_obj(table_name, fields)  # 获取字段对象
            model_data = get_model_data(table_name)  # 获取该表所有数据
            context['fields'] = fields  # 返回表内所有字段
            context['field_obj_list'] = field_obj_list  # 返回表内字段对象
            context['model_data'] = model_data  # 返回已入库的数据
            context["table_name"] = table_name  # 返回表名
            return render(request, 'studensCRM/show_list.html', context)
    else:
        if request.method == "POST":  # 如果是POST请求,暂时用于ajax测试请求
            return HttpResponse(json.dumps(ret))
    raise Http404


def account_login(request):
    """登陆页面"""
    context = {}
    login_form = forms.LoginForm()
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)  # 验证身份
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                context['login_err'] = "该账号被禁用"
        elif username and password:
            context['login_err'] = "用户名或密码错误"
    context['login_obj'] = login_form
    return render(request, 'account/login.html', context)


def account_logout(request):
    """退出操作"""
    logout(request)
    return redirect('/')


def register(request):
    """注册页面,暂时无法通过注册添加用户,只能后台添加用户"""
    context = {}
    register_obj = forms.RegisterForm()
    if request.method == 'POST':
        register_obj = forms.RegisterForm(request.POST)
    context['register_obj'] = register_obj
    return render(request, 'account/register.html', context)
