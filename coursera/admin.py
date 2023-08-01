from django.contrib import admin
from .models import User, Student, Teacher, Course, CourseContent, Payment
# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register( Teacher)
admin.site.register(Course)
admin.site.register(Payment)
admin.site.register(CourseContent)
