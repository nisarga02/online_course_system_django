from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=10)

    def __str__(self):
        return self.email

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(unique=True)
    # subject = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.email




class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    post_date =  models.DateTimeField(default=timezone.now)
    Instructor =  models.ForeignKey(Teacher, on_delete=models.CASCADE, default=None)


    def __str__(self):
        return self.title
    
    
class CourseContent(models.Model):
    name = models.CharField(max_length=200,default=None)
    body = models.TextField()
    url = models.URLField(blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, default=None)


    def __str__(self):
        return self.name
    


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='purchases_courses')
    purchased_at = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=100, default=0)

    def _str_(self):
        return f"{self.student.username} purchased {self.course.title} from {self.teacher.username} at {self.purchased_at}"


    
    


