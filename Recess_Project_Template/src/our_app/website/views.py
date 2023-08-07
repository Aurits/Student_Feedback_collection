from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .forms import InstructorForm
from .models import StudentDetails
from .forms import FacilityForm
from .models import FacilityFeedback
from .models import InstructorFeedback
from .models import CourseFeedback
from .forms import CourseFeedbackForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.core.paginator import Paginator
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from itertools import chain




def home(request):
    return render(request, 'index.html')

def start(request):
    return render(request, 'start.html')

def thankyou(request):
    return render(request, 'thankyou.html')




def course(request):
    if request.method == 'POST':
        form = CourseFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instructor')
    else:
        form = CourseFeedbackForm()

    return render(request, 'course.html', {'courseForm': form})


def instructor(request):
    return render(request, 'instructor.html')




def dashboard(request):
    students = StudentDetails.objects.all()
    course_items = CourseFeedback.objects.all()
    facilities = FacilityFeedback.objects.all()
    instructors = InstructorFeedback.objects.all()

    # Calculate the feedback counts for each category and aspect
    knowledge_counts = [InstructorFeedback.objects.filter(knowledge=i).count() for i in range(1, 6)]
    communication_counts = [InstructorFeedback.objects.filter(communication=i).count() for i in range(1, 6)]
    teaching_style_counts = [InstructorFeedback.objects.filter(teachingStyle=i).count() for i in range(1, 6)]
    responsiveness_counts = [InstructorFeedback.objects.filter(responsiveness=i).count() for i in range(1, 6)]

        # Calculate the average ratings for each category
    avg_course_effectiveness = CourseFeedback.objects.aggregate(Avg('effectiveness'))['effectiveness__avg']
    avg_course_interest = CourseFeedback.objects.aggregate(Avg('interest'))['interest__avg']

    avg_instructor_knowledge = InstructorFeedback.objects.aggregate(Avg('knowledge'))['knowledge__avg']
    avg_instructor_communication = InstructorFeedback.objects.aggregate(Avg('communication'))['communication__avg']
    avg_instructor_teaching_style = InstructorFeedback.objects.aggregate(Avg('teachingStyle'))['teachingStyle__avg']
    avg_instructor_responsiveness = InstructorFeedback.objects.aggregate(Avg('responsiveness'))['responsiveness__avg']

    avg_facility_accessibility = FacilityFeedback.objects.aggregate(Avg('facility_accessibility'))['facility_accessibility__avg']
    avg_facility_cleanliness = FacilityFeedback.objects.aggregate(Avg('cleanliness'))['cleanliness__avg']
    avg_facility_maintenance = FacilityFeedback.objects.aggregate(Avg('maintenance'))['maintenance__avg']
    avg_facility_safety = FacilityFeedback.objects.aggregate(Avg('safety'))['safety__avg']
    avg_facility_resource_availability = FacilityFeedback.objects.aggregate(Avg('resource_availability'))['resource_availability__avg']
    avg_facility_rating = FacilityFeedback.objects.aggregate(Avg('facility_rating'))['facility_rating__avg']
    # Number of items to show per page
    items_per_page = 10

    paginator = Paginator(students, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the corresponding page from the paginator
    page_obj = paginator.get_page(page_number)

    context = {
        'course_items': course_items,
        'facilities': facilities,
        'instructors': instructors,
        'students': students,
        'poor_knowledge': knowledge_counts[0],
        'fair_knowledge': knowledge_counts[1],
        'good_knowledge': knowledge_counts[2],
        'very_good_knowledge': knowledge_counts[3],
        'excellent_knowledge': knowledge_counts[4],
        'poor_communication': communication_counts[0],
        'fair_communication': communication_counts[1],
        'good_communication': communication_counts[2],
        'very_good_communication': communication_counts[3],
        'excellent_communication': communication_counts[4],
        'poor_teaching_style': teaching_style_counts[0],
        'fair_teaching_style': teaching_style_counts[1],
        'good_teaching_style': teaching_style_counts[2],
        'very_good_teaching_style': teaching_style_counts[3],
        'excellent_teaching_style': teaching_style_counts[4],
        'poor_responsiveness': responsiveness_counts[0],
        'fair_responsiveness': responsiveness_counts[1],
        'good_responsiveness': responsiveness_counts[2],
        'very_good_responsiveness': responsiveness_counts[3],
        'excellent_responsiveness': responsiveness_counts[4],
        'avg_course_effectiveness': avg_course_effectiveness,
        'avg_course_interest': avg_course_interest,
        'avg_instructor_knowledge': avg_instructor_knowledge,
        'avg_instructor_communication': avg_instructor_communication,
        'avg_instructor_teaching_style': avg_instructor_teaching_style,
        'avg_instructor_responsiveness': avg_instructor_responsiveness,
        'avg_facility_accessibility': avg_facility_accessibility,
        'avg_facility_cleanliness': avg_facility_cleanliness,
        'avg_facility_maintenance': avg_facility_maintenance,
        'avg_facility_safety': avg_facility_safety,
        'avg_facility_resource_availability': avg_facility_resource_availability,
        'avg_facility_rating': avg_facility_rating,
        'page_obj': page_obj,
    }

    return render(request, 'dashboard/pages/dashboard.html', context)




def courses(request):
    course_items = CourseFeedback.objects.all()
    course_ratings = list(CourseFeedback.objects.values_list('effectiveness', flat=True))
    course_rating_counts = [course_ratings.count(rating) for rating in range(1, 6)]
        # Number of items to show per page
    items_per_page = 10

    paginator = Paginator(course_items, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the corresponding page from the paginator
    page_obj = paginator.get_page(page_number)

    context = {
        'course_items': course_items,
        'course_rating_counts': course_rating_counts,
        'page_obj': page_obj, }
    return render(request, 'dashboard/pages/courses.html', context)


def delete_course_feedback(request, feedback_id):
    feedback = get_object_or_404(CourseFeedback, pk=feedback_id)
    if request.method == 'POST':
        feedback.delete()
        return redirect('courses')
    return render(request, 'dashboard/pages/delete_course_feedback.html', {'feedback': feedback})


def facilities(request):
    facilities = FacilityFeedback.objects.all()
    facility_ratings = list(FacilityFeedback.objects.values_list('facility_rating', flat=True))
    facility_rating_counts = [facility_ratings.count(rating) for rating in range(1, 6)]
            # Number of items to show per page
    items_per_page = 10

    paginator = Paginator(facilities, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the corresponding page from the paginator
    page_obj = paginator.get_page(page_number)

    context = {
        'facilities': facilities,
        'facility_rating_counts': facility_rating_counts,
        'page_obj': page_obj,
    }
    return render(request, 'dashboard/pages/facilities.html', context)


def instructors(request):
    feedbacks = InstructorFeedback.objects.all()
    instructor_ratings = list(InstructorFeedback.objects.values_list('knowledge', flat=True))
    instructor_rating_counts = [instructor_ratings.count(rating) for rating in range(1, 6)]
    
    # Prepare the rating labels to be passed to the template
    rating_labels = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
            # Number of items to show per page
    items_per_page = 10

    paginator = Paginator(feedbacks, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the corresponding page from the paginator
    page_obj = paginator.get_page(page_number)

    context = {
        'feedbacks': feedbacks,
        'instructor_rating_counts': instructor_rating_counts,
        'rating_labels': rating_labels,
        'page_obj': page_obj,
    }
    return render(request, 'dashboard/pages/instructors.html', context)


def delete_instructor_feedback(request, feedback_id):
    feedback = get_object_or_404(InstructorFeedback, id=feedback_id)
    if request.method == 'POST':
        feedback.delete()
        return redirect('instructors')
    return render(request, 'dashboard/pages/delete_instructor_feedback.html', {'feedback': feedback})


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard/pages/profile.html')
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('sign_in')


def signout(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def signin(request):
    if request.user.is_authenticated:
        students = StudentDetails.objects.all()
        course_items = CourseFeedback.objects.all()
        facilities = FacilityFeedback.objects.all()
        instructors = InstructorFeedback.objects.all()

        # Calculate the feedback counts for each category and aspect
        knowledge_counts = [
            InstructorFeedback.objects.filter(knowledge=i).count() for i in range(1, 6)
        ]
        communication_counts = [
            InstructorFeedback.objects.filter(communication=i).count() for i in range(1, 6)
        ]
        teaching_style_counts = [
            InstructorFeedback.objects.filter(teachingStyle=i).count() for i in range(1, 6)
        ]
        responsiveness_counts = [
            InstructorFeedback.objects.filter(responsiveness=i).count() for i in range(1, 6)
        ]


            # Calculate the average ratings for each category
        avg_course_effectiveness = CourseFeedback.objects.aggregate(Avg('effectiveness'))['effectiveness__avg']
        avg_course_interest = CourseFeedback.objects.aggregate(Avg('interest'))['interest__avg']

        avg_instructor_knowledge = InstructorFeedback.objects.aggregate(Avg('knowledge'))['knowledge__avg']
        avg_instructor_communication = InstructorFeedback.objects.aggregate(Avg('communication'))['communication__avg']
        avg_instructor_teaching_style = InstructorFeedback.objects.aggregate(Avg('teachingStyle'))['teachingStyle__avg']
        avg_instructor_responsiveness = InstructorFeedback.objects.aggregate(Avg('responsiveness'))['responsiveness__avg']

        avg_facility_accessibility = FacilityFeedback.objects.aggregate(Avg('facility_accessibility'))['facility_accessibility__avg']
        avg_facility_cleanliness = FacilityFeedback.objects.aggregate(Avg('cleanliness'))['cleanliness__avg']
        avg_facility_maintenance = FacilityFeedback.objects.aggregate(Avg('maintenance'))['maintenance__avg']
        avg_facility_safety = FacilityFeedback.objects.aggregate(Avg('safety'))['safety__avg']
        avg_facility_resource_availability = FacilityFeedback.objects.aggregate(Avg('resource_availability'))['resource_availability__avg']
        avg_facility_rating = FacilityFeedback.objects.aggregate(Avg('facility_rating'))['facility_rating__avg']

            # Number of items to show per page
        items_per_page = 10

        paginator = Paginator(students, items_per_page)

        # Get the current page number from the request's GET parameters
        page_number = request.GET.get('page')

        # Get the corresponding page from the paginator
        page_obj = paginator.get_page(page_number)

        context = {
            'course_items': course_items,
            'facilities': facilities,
            'instructors': instructors,
            'students': students,
            'poor_knowledge': knowledge_counts[0],
            'fair_knowledge': knowledge_counts[1],
            'good_knowledge': knowledge_counts[2],
            'very_good_knowledge': knowledge_counts[3],
            'excellent_knowledge': knowledge_counts[4],
            'poor_communication': communication_counts[0],
            'fair_communication': communication_counts[1],
            'good_communication': communication_counts[2],
            'very_good_communication': communication_counts[3],
            'excellent_communication': communication_counts[4],
            'poor_teaching_style': teaching_style_counts[0],
            'fair_teaching_style': teaching_style_counts[1],
            'good_teaching_style': teaching_style_counts[2],
            'very_good_teaching_style': teaching_style_counts[3],
            'excellent_teaching_style': teaching_style_counts[4],
            'poor_responsiveness': responsiveness_counts[0],
            'fair_responsiveness': responsiveness_counts[1],
            'good_responsiveness': responsiveness_counts[2],
            'very_good_responsiveness': responsiveness_counts[3],
            'excellent_responsiveness': responsiveness_counts[4],
            'avg_course_effectiveness': avg_course_effectiveness,
            'avg_course_interest': avg_course_interest,
            'avg_instructor_knowledge': avg_instructor_knowledge,
            'avg_instructor_communication': avg_instructor_communication,
            'avg_instructor_teaching_style': avg_instructor_teaching_style,
            'avg_instructor_responsiveness': avg_instructor_responsiveness,
            'avg_facility_accessibility': avg_facility_accessibility,
            'avg_facility_cleanliness': avg_facility_cleanliness,
            'avg_facility_maintenance': avg_facility_maintenance,
            'avg_facility_safety': avg_facility_safety,
            'avg_facility_resource_availability': avg_facility_resource_availability,
            'avg_facility_rating': avg_facility_rating,
            'page_obj': page_obj,
        }

        return render(request, 'dashboard/pages/dashboard.html', context)


    else:
        # Check to see if logging in
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            # Authenticate
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You Have Been Logged In!")
                return redirect('dashboard')
            else:
                messages.success(request, "There Was An Error Logging In, Please Try Again...")

                return redirect('home')
        else:
            return render(request, 'dashboard/pages/sign_in.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")

            return redirect('dashboard')
    else:
        form = SignUpForm()
        return render(request, 'dashboard/pages/sign_up.html', {'form': form})

    return render(request, 'dashboard/pages/sign_up.html', {'form': form})


def instructor_feedback(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form_data = form.cleaned_data
            feedback = InstructorFeedback(
                instructorName=form_data['instructorName'],
                department=form_data['department'],
                courseUnit=form_data['courseUnit'],
                knowledge=form_data['knowledge'],
                communication=form_data['communication'],
                teachingStyle=form_data['teachingStyle'],
                responsiveness=form_data['responsiveness'],
                additional_comments=form_data['additional_comments']
            )
            feedback.save()

            # Redirect to a success page after successful form submission
            return redirect('facility')
    else:
        form = InstructorForm()

    return render(request, 'instructor.html', {'form': form})


def studentDetails(request):
    if request.method == 'POST':
        name = request.POST['name']
        studentId = request.POST['studentId']
        emailAddress = request.POST['emailAddress']
        year_of_study = request.POST['year_of_study']

        # Save data to the database
        StudentDetails.objects.create(name=name, studentId=studentId, emailAddress=emailAddress,
                                      year_of_study=year_of_study)

        # Set a success message to display on the index.html template
        success_message = "Thank you for signing up!"
        return redirect('start')

    else:
        success_message = None

    return render(request, 'index.html', {'success_message': success_message})





def facility(request):
    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            feedback = FacilityFeedback(
                name=form.cleaned_data['name'],
                facility_college=form.cleaned_data['facility_college'],
                facility_accessibility=form.cleaned_data['facility_accessibility'],
                cleanliness=form.cleaned_data['cleanliness'],
                maintenance=form.cleaned_data['maintenance'],
                safety=form.cleaned_data['safety'],
                resource_availability=form.cleaned_data['resource_availability'],
                facility_rating=form.cleaned_data['facility_rating'],
                comment=form.cleaned_data['comment'],
            )
            feedback.save()
            return redirect('thankyou')  
    else:
        form = FacilityForm()

    return render(request, 'facility.html', {'form': form})


def delete_facility_feedback(request, feedback_id):
    if request.method == 'POST':
        feedback = FacilityFeedback.objects.get(pk=feedback_id)
        feedback.delete()
    return redirect('facilities')





#GENERATE THE REPORTS


def generate_course_feedback_pdf(request):
    data = CourseFeedback.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="course_feedback.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Define table headers and data
    table_data = [['Course', 'Effectiveness', 'Interest', 'Feedback']]
    for item in data:
        table_data.append([item.courseName, item.get_effectiveness_display(), item.get_interest_display(), item.qualitative_feedback])

    # Create the table and set styles
    table = Table(table_data, colWidths=[150, 100, 100, 250], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(Paragraph("Course Feedback", style=None))
    elements.append(table)

    doc.build(elements)

    return response

def generate_facility_feedback_pdf(request):
    data = FacilityFeedback.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="facility_feedback.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Define table headers and data
    table_data = [['Facility', 'Rating', 'Comment']]
    for item in data:
        table_data.append([item.name, item.facility_rating, item.comment])

    # Create the table and set styles
    table = Table(table_data, colWidths=[150, 100, 250], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(Paragraph("Facility Feedback", style=None))
    elements.append(table)

    doc.build(elements)

    return response

def generate_instructor_feedback_pdf(request):
    data = InstructorFeedback.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="instructor_feedback.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Define table headers and data
    table_data = [['Instructor', 'Knowledge', 'Communication', 'Teaching Style', 'Responsiveness', 'Feedback']]
    for item in data:
        table_data.append([item.instructorName, item.get_knowledge_display(), item.get_communication_display(), item.get_teachingStyle_display(), item.get_responsiveness_display(), item.additional_comments])

    # Create the table and set styles
    table = Table(table_data, colWidths=[150, 100, 100, 100, 100, 250], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(Paragraph("Instructor Feedback", style=None))
    elements.append(table)

    doc.build(elements)

    return response






def recommend(request):
    # Query the database to get all the feedback data
    instructor_feedbacks = InstructorFeedback.objects.all()
    course_feedbacks = CourseFeedback.objects.all()
    facility_feedbacks = FacilityFeedback.objects.all()
    students = StudentDetails.objects.all()
    course_items = CourseFeedback.objects.all()
    facilities = FacilityFeedback.objects.all()
    instructors = InstructorFeedback.objects.all()


    # Calculate average ratings for instructors
    avg_instructor_knowledge = instructor_feedbacks.aggregate(Avg('knowledge'))['knowledge__avg']
    avg_instructor_communication = instructor_feedbacks.aggregate(Avg('communication'))['communication__avg']
    avg_instructor_teaching_style = instructor_feedbacks.aggregate(Avg('teachingStyle'))['teachingStyle__avg']
    avg_instructor_responsiveness = instructor_feedbacks.aggregate(Avg('responsiveness'))['responsiveness__avg']

    # Calculate average ratings for courses
    avg_course_effectiveness = course_feedbacks.aggregate(Avg('effectiveness'))['effectiveness__avg']
    avg_course_interest = course_feedbacks.aggregate(Avg('interest'))['interest__avg']

    # Calculate average ratings for facilities
    avg_facility_accessibility = facility_feedbacks.aggregate(Avg('facility_accessibility'))['facility_accessibility__avg']
    avg_facility_cleanliness = facility_feedbacks.aggregate(Avg('cleanliness'))['cleanliness__avg']
    avg_facility_maintenance = facility_feedbacks.aggregate(Avg('maintenance'))['maintenance__avg']
    avg_facility_safety = facility_feedbacks.aggregate(Avg('safety'))['safety__avg']
    avg_facility_resource_availability = facility_feedbacks.aggregate(Avg('resource_availability'))['resource_availability__avg']
    avg_facility_rating = facility_feedbacks.aggregate(Avg('facility_rating'))['facility_rating__avg']

    # Generate recommendations based on the averages
    instructor_recommendation = get_recommendation(avg_instructor_knowledge, avg_instructor_communication, avg_instructor_teaching_style, avg_instructor_responsiveness)
    course_recommendation = get_recommendation(avg_course_effectiveness, avg_course_interest)
    facility_recommendation = get_facility_recommendation(avg_facility_accessibility, avg_facility_cleanliness, avg_facility_maintenance, avg_facility_safety, avg_facility_resource_availability, avg_facility_rating)

    # Filter records with poor performance (average <= 2)
    poor_performance_instructors = instructor_feedbacks.annotate(
        avg_rating=(Avg('knowledge') + Avg('communication') + Avg('teachingStyle') + Avg('responsiveness')) / 4
    ).filter(avg_rating__lte=2)

    poor_performance_courses = course_feedbacks.annotate(
        avg_rating=(Avg('effectiveness') + Avg('interest')) / 2
    ).filter(avg_rating__lte=2)

    poor_performance_facilities = facility_feedbacks.annotate(
        avg_rating=(Avg('facility_accessibility') + Avg('cleanliness') + Avg('maintenance') + Avg('safety') + Avg('resource_availability') + Avg('facility_rating')) / 6
    ).filter(avg_rating__lte=2)

    # Filter records with very poor performance (average <= 1)
    very_poor_performance_instructors = instructor_feedbacks.annotate(
        avg_rating=(Avg('knowledge') + Avg('communication') + Avg('teachingStyle') + Avg('responsiveness')) / 4
    ).filter(avg_rating__lte=1)

    very_poor_performance_courses = course_feedbacks.annotate(
        avg_rating=(Avg('effectiveness') + Avg('interest')) / 2
    ).filter(avg_rating__lte=1)

    very_poor_performance_facilities = facility_feedbacks.annotate(
        avg_rating=(Avg('facility_accessibility') + Avg('cleanliness') + Avg('maintenance') + Avg('safety') + Avg('resource_availability') + Avg('facility_rating')) / 6
    ).filter(avg_rating__lte=1)

        # Concatenate the two querysets to remove duplicates
    combined_instructors = poor_performance_instructors | very_poor_performance_instructors
    combined_courses = poor_performance_courses | very_poor_performance_courses
    combined_facilities = poor_performance_facilities | very_poor_performance_facilities

    context = {
        'course_items': course_items,
        'facilities': facilities,
        'instructors': instructors,
        'students': students,
        'combined_instructors': combined_instructors,
        'combined_courses': combined_courses,
        'combined_facilities': combined_facilities,
        'instructor_recommendation': instructor_recommendation,
        'course_recommendation': course_recommendation,
        'facility_recommendation': facility_recommendation,
    }

    return render(request, 'dashboard/pages/recommend.html', context)

# Other functions like get_recommendation and get_facility_recommendation remain unchanged.


def get_recommendation(*args):
    overall_avg = sum(args) / len(args)
    if overall_avg <= 1:
        return ""
    else:
        return "Performance is fair but there is room for improvement."

def get_facility_recommendation(avg_accessibility, avg_cleanliness, avg_maintenance, avg_safety, avg_resource_availability, avg_rating):
    overall_avg = (avg_accessibility + avg_cleanliness + avg_maintenance + avg_safety + avg_resource_availability + avg_rating) / 6
    if overall_avg <= 1:
        return "Facilities need improvement."
    else:
        return "Facilities are doing well but there is room for improvement."
