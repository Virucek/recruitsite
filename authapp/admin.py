from django.contrib import admin

from authapp.models import Employer, Jobseeker, IndustryType

admin.site.register(Employer)
admin.site.register(Jobseeker)
admin.site.register(IndustryType)

