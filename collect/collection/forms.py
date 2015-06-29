from django.forms.models import modelform_factory
from .models import ProposedCourseList 
#ProposedCourseListForm = modelform_factory(ProposedCourseList, fields=("course_code", "course_name"))

from django.forms import ModelForm

class proposecourselistForm(ModelForm):
    class Meta:
        model=ProposedCourseList
        fields= ('course_code','course_name','syllabus',)
