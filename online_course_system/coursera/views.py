import random
import string
import paypalrestsdk

from .forms import *
from .models import *

from django.views import View
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate , login,logout,get_user_model

from online_course_system import settings
from online_course_system.settings import EMAIL_HOST_USER

User = get_user_model()

def main(request):
    return render(request, 'main.html')

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')  

class VerifyOTPView(View):
    def get(self, request):
        otp = request.session.get('otp')
        context = {'otp': otp}
        print(otp)
        return render(request, 'verify_otp.html', context)

    @csrf_exempt
    def post(self, request):
        userotp = request.POST.get('otp')
        print(userotp)
        registration_data = request.session.get('registration_data')
        is_teacher = request.session.get('is_teacher')
        is_student = request.session.get('is_student')
        print(userotp)
        if userotp and registration_data and (is_teacher or is_student):
            # Verify the OTP
            stored_otp = request.session.get('otp')
            if userotp == str(stored_otp):
                # Create the user and associated model objects
                username = registration_data['email'].split('@')[0]
                user = User.objects.create_user(
                    username=username,
                    password=registration_data['password'],
                    email=registration_data['email'],
                    first_name=registration_data['first_name'],
                    last_name=registration_data['last_name']
                )
                if is_teacher:
                    teacher = Teacher.objects.create(
                        user=user,
                        email=registration_data['email'],
                        first_name=registration_data['first_name'],
                        last_name=registration_data['last_name'],
                    )
                    if teacher:
                        user.is_teacher = True
                        user.save()
                        teacher.save()
                elif is_student:
                    student = Student.objects.create(
                        user=user,
                        email=registration_data['email'],
                        first_name=registration_data['first_name'],
                        last_name=registration_data['last_name'],
                        student_id=registration_data['student_id']
                    )
                    if student:
                        user.is_student = True
                        user.save()
                        student.save()

                # Clear the session data
                if 'otp' in request.session:
                    del request.session['otp']
                if 'registration_data' in request.session:
                    del request.session['registration_data']
                if 'is_teacher' in request.session:
                    del request.session['is_teacher']
                if 'is_student' in request.session:
                    del request.session['is_student']

                messages.success(request, 'User saved successfully.')
                return redirect('login')

            else:
                messages.error(request, 'Invalid OTP. Please try again.')

        return JsonResponse({'data': 'Hello'}, status=200)

class TeacherRegistrationView(View):
    def get(self, request):
        form = TeacherRegistrationForm()
        return render(request, 'teacher_registration.html', {'form': form})

    def post(self, request):
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Save the user registration information in session
            request.session['registration_data'] = cleaned_data
            request.session['is_teacher'] = True
            # Generate OTP
            otp = random.randint(1000, 9999)

            # Save OTP in session
            request.session['otp'] = otp

            # Send OTP via email
            send_mail("User Data: ", f"Verify Your Mail by the OPT: /n {otp}", EMAIL_HOST_USER,
                      [cleaned_data['email']])

            messages.success(request, 'User saved successfully.')
            return redirect('verify_otp')

        else:
            messages.error(request, form.errors)

        return render(request, 'teacher_registration.html', {'form': form})

class StudentRegistrationView(View):
    def get(self, request):
        form = StudentRegistrationForm()
        return render(request, 'student_registration.html', {'form': form})

    def post(self, request):
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Save the user registration information in session
            request.session['registration_data'] = cleaned_data
            request.session['is_student'] = True

            # Generate OTP
            otp = random.randint(1000, 9999)

            # Save OTP in session
            request.session['otp'] = otp

            # Send OTP via email
            send_mail("User Data: ", f"Verify Your Mail by the OPT: /n {otp}", EMAIL_HOST_USER,
                      [cleaned_data['email']])

            messages.success(request, 'User saved successfully.')
            return redirect('verify_otp')

        else:
            messages.error(request, form.errors)

        return render(request, 'student_registration.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password']
            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_teacher:
                    return redirect('teacher_dashboard')
                elif user.is_student:
                    return redirect('student-dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
                # return redirect('home')

        return render(request, 'login.html', {'form': form})

class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        # Add your custom filtering logic here
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, 'Email address is not registered.')
            return self.form_invalid(form)
        return super().form_valid(form)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):        
        logout(request)
        return redirect('login') 
    
class TeacherDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            instructor = Teacher.objects.get(user=request.user)
            courses = Course.objects.filter(Instructor=instructor)
            form = CourseForm()
            content = None 

            for course in courses:
                students_purchased = Payment.objects.filter(course=course).values_list('student__user__first_name', 'student__user__last_name')
                course.students_purchased = students_purchased

            if courses.exists():
                first_course = courses.first()
                coursecontents = CourseContent.objects.filter(course=first_course)
            else:
                coursecontents = []

            return render(request, 'teacher_dashboard.html', {'courses': courses, 'form': form,'purchased': True, 'coursecontents': coursecontents})
        except Teacher.DoesNotExist:
            # Redirect non-teacher users to the student dashboard
            return redirect('student-dashboard')
    
    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            instructor= request.user.teacher
            course.Instructor = instructor
            course.save()
            form.save_m2m()

            # Send email notification to students who purchased the author's other courses
            # students = Student.objects.filter(purchased_courses__instructor=instructor)
            students = Student.objects.filter(payment__course=course)
            for student in students:
                send_mail(
                    'New Course by Author',
                    f'A new course has been designed by the author of one of your purchased courses.',
                    'sender@example.com',  # Replace with your sender email address
                    [student.user.email],
                    fail_silently=True,
                )

            return redirect('teacher_dashboard')
        else:
            return render(request, 'teacher_dashboard.html', {'form': form})

@login_required
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid() :
            course = form.save()  # Save the course instance
    else:
        form = CourseForm(instance=course)

    return render(request, 'edit_course.html', {'form': form})

@login_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('teacher_dashboard')
    context = {'course': course}
    return render(request, 'delete_course.html', context)

@login_required
def add_course_content(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseContentForm(request.POST)
        if form.is_valid():
            content = form.save(commit=False)
            content.course = course
            content.save()

            # Send email notification to students who purchased the course
            students = Student.objects.filter(payment__course=course)
            for student in students:
                send_mail(
                    'New Course Content Added',
                    f'A new topic has been added to the course: {course.title}',
                    'sender@example.com',  # Replace with your sender email address
                    [student.user.email],
                    fail_silently=True,
                )

            return redirect('add_course_content', course_id=course.id)
    else:
        form = CourseContentForm(initial={'course': course})

    coursecontents = CourseContent.objects.filter(course=course)
    return render(request, 'add_course_content.html', {'form': form, 'course': course, 'coursecontents': coursecontents}) 

@login_required
def update_course_content(request, content_id):
    content = get_object_or_404(CourseContent, pk=content_id)
    if request.method == 'POST':
        form = CourseContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            return redirect('add_course_content', course_id=content.course.id)
    else:
        form = CourseContentForm(instance=content)
    return render(request, 'update_course_content.html', {'form': form, 'content': content})

@login_required
def delete_course_content(request, content_id):
    # Use get_object_or_404 to fetch the CourseContent object
    content = get_object_or_404(CourseContent, pk=content_id)
    course_id = content.course.id

    if request.method == 'POST':
        content.delete()
        return redirect(reverse('add_course_content', kwargs={'course_id': course_id}))

    # If the request method is not POST, render the confirmation template
    return render(request, 'delete_coures_content.html', {'content': content})


class StudentDashboardView(LoginRequiredMixin,View):
    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            # Redirect non-student users to the teacher dashboard
            return redirect('teacher_dashboard')

        # Fetch all courses
        courses = Course.objects.all()

        # Get all teachers who created the courses
        teachers = Teacher.objects.filter(course__in=courses).distinct()

        students = Student.objects.all()

        context = {
            'courses': courses,
            'teachers': teachers,
            'students': students,
        }

        return render(request, 'student_dashboard.html', context)

@login_required
def course_details(request, pk):
    course = get_object_or_404(Course, pk=pk)
    content = CourseContent.objects.filter(course=course)
    student = Student.objects.get(user=request.user)

    context = {
        'course': course,
        'content': content,
        'purchased': Payment.objects.filter(course_id=course.id, student_id=student.user.id).exists()
    }

    return render(request, 'course_details.html', context)

@login_required
def search_course(request):
    query = request.GET.get('query')
    courses = Course.objects.filter(title__icontains=query)
    context = {
        'courses': courses
    }
    return render(request, 'search_results.html', context)

def generate_invoice_number(course_pk, user_pk):
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f'{course_pk}-{user_pk}-{random_string}'

@login_required
def purchase_course(request, pk):
    # try:
        course = get_object_or_404(Course, pk=pk)
        price = course.price
        user = request.user


        # if course.is_purchased_by_user(user):
        #     return HttpResponse('Course already purchased')
            # return redirect('course_detail', pk=pk)

        paypalrestsdk.configure({
            'mode': settings.PAYPAL_MODE,
            'client_id': settings.PAYPAL_CLIENT_ID,
            'client_secret': settings.PAYPAL_CLIENT_SECRET
        })

        invoice_number = generate_invoice_number(course.pk,user.pk)

        # payer_id = f'{course.pk}-{uuid.uuid4().hex}'

        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'payer': {'payment_method': 'paypal'},
            'transactions': [{
                'amount': {'total': str(price), 'currency': 'USD'},
                'description': 'Course Payment',
                # 'invoice_number': str(user.pk),
                 'invoice_number': invoice_number,
            }],
            'redirect_urls': {
                'return_url': request.build_absolute_uri(reverse('payment_success')),
                'cancel_url': request.build_absolute_uri(reverse('payment_cancel')),
            }
        })

        if payment.create():
            # Redirect user to PayPal payment approval URL
            for link in payment.links:
                if link.method == 'REDIRECT':
                    return redirect(link.href)

        else:
        #     # Handle PayPal payment creation error
            return render(request, 'payment_cancel.html')

        return render(request, 'payment_success.html')
    

    # except Exception as e:
    #     # Handle other exceptions
    #     return render(request, 'payment_error.html')

@login_required
def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({'payer_id': payer_id}):
        invoice_number = payment.transactions[0].invoice_number
        course_pk, user_pk, _ = invoice_number.split('-')

        course = Course.objects.get(pk=course_pk)
        user = request.user
        student = get_object_or_404(Student, user=request.user) 
        teacher = course.Instructor

        payment_obj = Payment.objects.create(
                    student=student,   # Assuming the student is making the payment
                    teacher= teacher,
                    course=course,
                    purchased_at=timezone.now(),
                    transaction_id=payment_id,
                )

        return render(request, 'payment_success.html', {'course': course, 'payment': payment_obj})
    else:
        return render(request, 'payment_cancel.html')

@login_required
def payment_error(request):
    return render(request, 'payment_error.html')  
@login_required
def payment_cancel(request):
    return render(request, 'payment_cancel.html')  # Create the payment_failed.html template


