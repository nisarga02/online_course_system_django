from django.urls import path,include
from .views import StudentRegistrationView, TeacherRegistrationView,HomeView, VerifyOTPView,LoginView, LogoutView,TeacherDashboardView,edit_course,delete_course,StudentDashboardView, add_course_content, update_course_content, delete_course_content ,CustomPasswordResetView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path('main/',views.main, name='main'),

    path('', HomeView.as_view(), name='home'),

    path('student/register/', StudentRegistrationView.as_view(), name='student_register'),
    path('teacher/register/', TeacherRegistrationView.as_view(), name='teacher_register'),
    path('student/verify/', VerifyOTPView.as_view(), name='verify_otp'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('reset_password/', CustomPasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html") ,name ="password_reset_done" ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html") ,name="password_reset_confirm"),
    path('reset_password_completed/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),name ="password_reset_complete" ),

    path('teacher/dashboard/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('teacher/dashboard/course/<int:pk>/edit/', edit_course, name='edit_course'),
    path('teacher/dashboard/course/<int:pk>/delete/', delete_course, name='delete_course'),


    path('course/<int:course_id>/add-content/', add_course_content, name='add_course_content'),   
    path('course/content/<int:content_id>/update/', update_course_content, name='update_course_content'),   
    path('course/content/<int:content_id>/delete/', delete_course_content, name='delete_course_content'),
    
    path('student/dashboard/',StudentDashboardView.as_view(), name='student-dashboard'),    
    path('student/dashboard/course/<int:pk>/course_details/',views.course_details, name='course_details'),
    path('student/dashboard/search_course/', views.search_course, name='search_course'),

    path('payment/success/', views.payment_success, name='payment_success'),

    path('payment/error/',views.payment_error,name='payment_error'),

    path('payment_cancel/',views.payment_cancel,name='payment_cancel'),

    path('payment/purchase/<int:pk>/', views.purchase_course, name='purchase_course'),
    # Other URLs in your project...
]
