from django import forms
from .models import Student, Teacher, Course, CourseContent
from .models import User
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match("^[a-zA-Z]+$", first_name):
            raise forms.ValidationError("First name should only contain alphabets.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match("^[a-zA-Z]+$", last_name):
            raise forms.ValidationError("Last name should only contain alphabets.")
        return last_name
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*()-_=+{};:,<.>]', password):
            raise forms.ValidationError("Password must contain at least one symbol.")
        return password
    
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'student_id', 'email', 'password', 'confirm_password')

class TeacherRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match("^[a-zA-Z]+$", first_name):
            raise forms.ValidationError("First name should only contain alphabets.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match("^[a-zA-Z]+$", last_name):
            raise forms.ValidationError("Last name should only contain alphabets.")
        return last_name
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*()-_=+{};:,<.>]', password):
            raise forms.ValidationError("Password must contain at least one symbol.")
        return password
    
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title','description','duration','price')
       
    

class CourseContentForm(forms.ModelForm):
    class Meta:
        model = CourseContent
        fields = ['name','body','url']

