from django.forms.models import modelform_factory
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import ProposedCourseList 
#ProposedCourseListForm = modelform_factory(ProposedCourseList, fields=("course_code", "course_name"))

from django.forms import ModelForm

class proposecourselistForm(ModelForm):
    class Meta:
        model=ProposedCourseList
        fields= ('course_code','programme','course_name','syllabus','level_0_sign',)
