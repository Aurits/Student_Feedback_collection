from django.db import models


class InstructorFeedback(models.Model):
    
    instructorName = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    courseUnit = models.CharField(max_length=100)
    knowledge = models.IntegerField(choices=[
        (5, 'Excellent'),
        (4, 'Very Good'),
        (3, 'Good'),
        (2, 'Fair'),
        (1, 'Poor'),
    ])
    communication = models.IntegerField(choices=[
        (5, 'Excellent'),
        (4, 'Very Good'),
        (3, 'Good'),
        (2, 'Fair'),
        (1, 'Poor'),
    ])
    teachingStyle = models.IntegerField(choices=[
        (5, 'Excellent'),
        (4, 'Very Good'),
        (3, 'Good'),
        (2, 'Fair'),
        (1, 'Poor'),
    ])
    responsiveness = models.IntegerField(choices=[
        (5, 'Excellent'),
        (4, 'Very Good'),
        (3, 'Good'),
        (2, 'Fair'),
        (1, 'Poor'),
    ])
    additional_comments = models.TextField()

    def __str__(self):
        return self.instructorName


    def get_average_rating(self):
        # Calculate the average rating for instructors
        ratings = [self.knowledge, self.communication, self.teachingStyle, self.responsiveness]
        return sum(ratings) / len(ratings)



class CourseFeedback(models.Model):

    courseName = models.CharField(max_length=100)
    courseCode = models.CharField(max_length=20)
    effectiveness = models.IntegerField(choices=[
        (5, 'Excellent'),
        (4, 'Very Good'),
        (3, 'Good'),
        (2, 'Fair'),
        (1, 'Poor'),
    ])
    interest = models.IntegerField(choices=[
        (5, 'Excellent'),
        (4, 'Very Good'),
        (3, 'Good'),
        (2, 'Fair'),
        (1, 'Poor'),
    ])
    qualitative_feedback = models.TextField()

    def __str__(self):
        return self.courseName



class FacilityFeedback(models.Model):
    name = models.CharField(max_length=100)
    facility_college = models.CharField(max_length=100)
    facility_accessibility = models.IntegerField()
    cleanliness = models.IntegerField()
    maintenance = models.IntegerField()
    safety = models.IntegerField()
    resource_availability = models.IntegerField()
    facility_rating = models.IntegerField()
    comment = models.TextField()


    def __str__(self):
        return self.name



class StudentDetails(models.Model):
    name = models.CharField(max_length=100)
    studentId = models.CharField(max_length=20)
    emailAddress = models.EmailField()
    year_of_study = models.CharField(max_length=10)

    def __str__(self):
        return self.name
