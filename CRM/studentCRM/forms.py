#!/usr/bin/env python
# encoding:utf8

from django import forms
from studentCRM import models
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=45,
        error_messages={
            'required': u'用户名不能为空',
            'invalid': u'用户名格式错误'},
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": u"用户名/邮箱",
                "autofocus": True,
            },
        )
    )

    password = forms.CharField(
        error_messages={
            'required': u'密码不能为空',
            'invalid': u'密码格式错误'},
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": u"输入密码",
            },
        )
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        exclude = ()


class SchoolForm(forms.ModelForm):
    class Meta:
        model = models.School
        exclude = ()


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        exclude = ()


class ClassListForm(forms.ModelForm):
    class Meta:
        model = models.ClassList
        exclude = ()


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        exclude = ()


class ConsultRecordForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        exclude = ()


class CourseRecordForm(forms.ModelForm):
    class Meta:
        model = models.CourseRecord
        exclude = ()


class StudyRecordForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        exclude = ()


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=45,
        error_messages={'required': u'用户名不能为空', 'invalid': u'用户名格式错误'},
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": u"用户名", "autofocus": True},)
    )

    email = forms.EmailField(
        max_length=100,
        error_messages={'required': u'邮箱不能为空', 'invalid': u'邮箱格式错误'},
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": u"邮箱地址", },)
    )

    phone = forms.CharField(
        max_length=11,
        error_messages={'required': u'手机号不能为空', 'invalid': u'手机号格式错误'},
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": u"手机号码"},)
    )

    password = forms.CharField(
        error_messages={'required': u'密码不能为空', 'invalid': u'密码格式错误'},
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": u"输入密码"},)
    )

    confirm_password = forms.CharField(
        error_messages={'required': u'密码不能为空', 'invalid': u'密码格式错误'},
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": u"确认密码"},)
    )
