from django.contrib import admin

from jobseekerapp.models import Resume, ResumeExperience, ResumeEducation


def name(obj):
    return f'{obj.user.user.first_name} {obj.user.user.last_name} {obj.user.middle_name}'


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (name, 'name', 'status')
    list_filter = ('status', )


admin.site.register(ResumeExperience)
admin.site.register(ResumeEducation)
