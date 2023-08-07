from .models import FacilityFeedback
from .models import InstructorFeedback
from django.contrib.auth.forms import UserCreationForm
from django.forms import RadioSelect
from django.contrib.auth.models import User
from django import forms
from .models import InstructorFeedback
from .models import StudentDetails
from .models import CourseFeedback


class SignUpForm(UserCreationForm):

    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')



    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    










from django import forms
from django.forms import RadioSelect

class InstructorForm(forms.ModelForm):
    class Meta:
        model = InstructorFeedback
        fields = ['instructorName', 'department', 'courseUnit', 'knowledge', 'communication', 'teachingStyle',
                  'responsiveness', 'additional_comments']
        widgets = {
            'instructorName': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'courseUnit': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'knowledge': forms.RadioSelect(attrs={'class': 'rating d-flex', 'required': True}, choices=[
                (5, 'Excellent'),
                (4, 'Very Good'),
                (3, 'Good'),
                (2, 'Fair'),
                (1, 'Poor'),
            ]),
            'communication': forms.RadioSelect(attrs={'class': 'rating d-flex', 'required': True}, choices=[
                (5, 'Excellent'),
                (4, 'Very Good'),
                (3, 'Good'),
                (2, 'Fair'),
                (1, 'Poor'),
            ]),
            'teachingStyle': forms.RadioSelect(attrs={'class': 'rating d-flex', 'required': True}, choices=[
                (5, 'Excellent'),
                (4, 'Very Good'),
                (3, 'Good'),
                (2, 'Fair'),
                (1, 'Poor'),
            ]),
            'responsiveness': forms.RadioSelect(attrs={'class': 'rating d-flex', 'required': True}, choices=[
                (5, 'Excellent'),
                (4, 'Very Good'),
                (3, 'Good'),
                (2, 'Fair'),
                (1, 'Poor'),
            ]),
            'additional_comments': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
        }




class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = StudentDetails
        fields = ['name', 'studentId', 'emailAddress', 'year_of_study']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'studentId': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'emailAddress': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'year_of_study': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }



class FacilityForm(forms.Form):
    FACILITY_ACCESSIBILITY_CHOICES = [
        (5, 'Fully accessible'),
        (3, 'Partially accessible'),
        (1, 'Not accessible'),
    ]

    RATING_CHOICES = [
        (5, ''),
        (4, ''),
        (3, ''),
        (2, ''),
        (1, ''),
    ]

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Facility name', 'required': True}))
    facility_college = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'College of facility', 'required': True}))
    facility_accessibility = forms.ChoiceField(choices=FACILITY_ACCESSIBILITY_CHOICES, widget=forms.Select(attrs={'required': True}))
    cleanliness = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect())
    maintenance = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect())
    safety = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect())
    resource_availability = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect())
    facility_rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect())
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Please provide any additional comments or suggestions about our college facilities.', 'rows': 5}))





class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ['courseName', 'courseCode', 'effectiveness', 'interest', 'qualitative_feedback']
        widgets = {
            'courseName': forms.TextInput(attrs={'class': 'form-control m-3', 'required': True}),
            'courseCode': forms.TextInput(attrs={'class': 'form-control m-3', 'required': True}),
            'effectiveness': forms.RadioSelect(attrs={'class': 'rating d-flex m-3'}, choices=[
                (5, 'Excellent'),
                (4, 'Very Good'),
                (3, 'Good'),
                (2, 'Fair'),
                (1, 'Poor'),
            ]),
            'interest': forms.RadioSelect(attrs={'class': 'rating d-flex m-3'}, choices=[
                (5, 'Excellent'),
                (4, 'Very Good'),
                (3, 'Good'),
                (2, 'Fair'),
                (1, 'Poor'),
            ]),
            'qualitative_feedback': forms.Textarea(attrs={'class': 'form-control m-3', 'required': True}),
        }
