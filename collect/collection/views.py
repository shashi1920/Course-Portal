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

def pro_course_list(request, kr, pro,sem):
    pr=programme.objects.get(branch=kr,programme_code=pro)
    #msg=br+PR
    #return HttpResponse(pro)
    courses=ApprovedCourseList.objects.filter(programme=pr,semester=sem)
    prof=Professor.objects.all().order_by('prof_name')
    context={'programme_li' : pr ,'course_li' : courses,'professors':prof,'semester':sem}
    return  render(request,'collection/course_list.html',context)

def add_teacher(request, kr, pro,sem):
    errors=[]
    pr=programme.objects.get(branch=kr,programme_code=pro)
    courses=ApprovedCourseList.objects.filter(programme=pr,semester=sem)
    prof=Professor.objects.all().order_by('prof_name')
    #if request.method=='POST':
     #   form=
    for cr in courses:
        con_name= request.POST.get('("cname"+cr.course_code)')
        if con_name:
            p=ApprovedCourseTeaching(course_code=cr,prof_id1=con_name,semester=sem,programme=pr,elect_or_comp=1)
            p.save()
    return render(request,'collection/submit.html')




# Create your views here.
