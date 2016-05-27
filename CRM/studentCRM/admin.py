from django.contrib import admin
from studentCRM import models
# Register your models here.


class StudyRecordAdmin(admin.ModelAdmin):
    list_display = ('course_record', 'student', 'record', 'record_color', 'score_color', 'score', 'date', 'note')
    list_editable = ('record', 'score', 'note')  # 允许可编辑字段
    list_per_page = 20  # 设置每页最大显示20条记录
    list_filter = ('course_record', 'course_record__course',)  # 右侧显示过滤功能,以某个字段为条件过滤
    search_fields = ('student', 'score', 'course_record',)  # 设置搜索字段
    actions = ["student_check", 'student_noshow', 'student_late', 'student_leave_early']  # 设置批量操作功能

    def student_check(self, request, queryset):  # 已签到设置
        queryset.update(record='checked')

    def student_noshow(self, request, queryset):  # 缺勤
        queryset.update(record="noshow")

    def student_late(self, request, queryset):  # 迟到
        queryset.update(record="late")

    def student_leave_early(self, request, queryset):  # 早退
        queryset.update(record='leave_early')

    student_check.short_description = u'设置所选学员为--已签到'
    student_noshow.short_description = u"设置所选学员为--缺勤"
    student_late.short_description = u"设置所选学员为--迟到"
    student_leave_early.short_description = u"设置所选学员为--早退"

    def get_actions(self, request):  # 删除默认执行的删除操作
        actions = super().get_actions(request)
        if actions.get('delete_selected'):
            actions.pop('delete_selected')
        return actions


class CourseRecordAdmin(admin.ModelAdmin):
    list_display = ('course', 'day_num', 'date', 'teacher')


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'addr')


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'qq', 'name', 'phone', 'stu_id', 'source', 'course', 'customer_note', 'status', 'consultant', 'date',
    )


class ConsultRecordAdmin(admin.ModelAdmin):
    list_display = ('customer', 'note', 'status', 'consultant', 'date')


class ClassListAdmin(admin.ModelAdmin):
    list_display = ('course', 'course_type', 'semester', 'start_date', 'graduate_date')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'online_price', 'brief')


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.School, SchoolAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.ClassList, ClassListAdmin)
admin.site.register(models.ConsultRecord, ConsultRecordAdmin)
admin.site.register(models.CourseRecord, CourseRecordAdmin)
admin.site.register(models.StudyRecord, StudyRecordAdmin)
