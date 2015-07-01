from django.shortcuts import render
from django.http import HttpResponse
from .models import Professor
from .models import Profile
from .models import dept
from .models import programme
from .models import ProposedCourseList
from .models import ProposedCourseTeaching
from .models import ApprovedCourseList
from .models import ApprovedCourseTeaching
from .models import ForeignCourseList
def index(request):
    return render(request, 'collection/index.html')

def programme_list(request, br):
    pr=programme.objects.filter(branch=br)
    dr=dept.objects.get(dept_code=br)
    context={'programme_li' : pr,'deptm': dr}
    #return HttpResponse(br)
    return  render(request,'collection/programme.html',context)

def pro_course_list(request, kr, pro):
    pr=programme.objects.get(branch=kr,programme_code=pro)
    #msg=br+PR
    #return HttpResponse(pro)
    courses=ApprovedCourseList.objects.filter(programme=pr)
    context={'programme_li' : pr ,'course_li' : courses}
    return  render(request,'collection/course_list.html',context)

# Create your views here.


from collection.forms import proposecourselistForm
def proposecourse(request):
    if request.method == 'GET':
        form = proposecourselistForm()    # creating a empty form.
    else:
        form = proposecourselistForm(request.POST) # Bind data from request.POST into a proposecourselistForm instance form
        if form.is_valid():
            propose_course = form.save()
            return HttpResponseRedirect('/thanks/')
    return render(request, 'collection/proposecourse.html', {'form': form,})
