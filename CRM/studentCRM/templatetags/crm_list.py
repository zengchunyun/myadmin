#!/usr/bin/env python
# encoding:utf8

from django.template import Library
from django.utils.html import format_html

register = Library()


@register.simple_tag
def render_data(model_data, fields):
    """model_data: 数据查询对象
    fields : 表字段
    """
    html_td = ''
    for field in fields:
        if hasattr(model_data, field):
            field_data = getattr(model_data, field)  # 获取字段数据
            field_obj = model_data._meta.get_field(field)  # 获取字段对象
            edit_type = "text"
            if field_obj.is_relation:  # 如果字段存在关系映射
                if field_obj.one_to_many:
                    pass
                elif field_obj.many_to_one:  # 多对一外键关系
                    pass
                elif field_obj.many_to_many:  # 如果字段是多对多关系
                    field_many = field_data.select_related()
                    many_field_data = []
                    for field_many_obj in field_many:
                        many_field_data.append(str(field_many_obj))
                    field_data = ",".join(many_field_data)
                if not field_obj.concrete:  # 如果字段不是在model定义时创建的,即那些Django自己映射生成的字段反向查找字段
                    remote_name = field_obj.related_model._meta.model_name  # 获取关联的外键model名字
                    local_name = model_data._meta.model_name  # 获取本地的model名字
                    if remote_name == local_name:  # 如果外键关联的是本地字段,则不进行操作
                        continue
            try:
                if field_obj.choices:  # 如果是选择字段,则尝试获取字段描述名
                    field_data = getattr(model_data, "get_%s_display" % field)
                    field_data = field_data()
            except AttributeError:
                continue

            html_td += '<td edit="true" edit-type="%s" name="%s" >%s</td>' % (edit_type, field_obj.name, field_data)
    return format_html(html_td)
