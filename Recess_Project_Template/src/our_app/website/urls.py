from django.urls import path
from . import views

urlpatterns = [
    path('', views.studentDetails, name='home'),
    path('start', views.start, name='start'),
     path('thankyou', views.thankyou, name='thankyou'),
    path('course', views.course, name='course'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('recommend', views.recommend, name='recommend'),
    path('courses', views.courses, name='courses'),
    path('facilities', views.facilities, name='facilities'),
    path('instructors', views.instructors, name='instructors'),
    path('signout', views.signout, name='sign_out'),
    path('signin', views.signin, name='sign_in'),
    path('signup', views.signup, name='sign_up'),
    path('profile', views.profile, name='profile'),
    path('instructor_feedback/', views.instructor_feedback, name='instructor'),
    path('instructor_feedbacks/<int:feedback_id>/delete/',
         views.delete_instructor_feedback, name='delete_instructor_feedback'),
    path('course_feedbacks/<int:feedback_id>/delete/',
         views.delete_course_feedback, name='delete_course_feedback'),
    path('facilities/<int:feedback_id>/delete/', views.delete_facility_feedback, name='delete_facility_feedback'),
    path('facility', views.facility, name='facility'),
    # Your other URL patterns
    path('generate_course_feedback_pdf/', views.generate_course_feedback_pdf, name='generate_course_feedback_pdf'),
    path('generate_facility_feedback_pdf/', views.generate_facility_feedback_pdf, name='generate_facility_feedback_pdf'),
    path('generate_instructor_feedback_pdf/', views.generate_instructor_feedback_pdf, name='generate_instructor_feedback_pdf'),

]


