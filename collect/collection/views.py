from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
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
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.filter(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    pr=programme.objects.filter(branch=br)
    dr=dept.objects.get(dept_code=br)
    context={'programme_li' : pr,'deptm': dr}
    #return HttpResponse(br)
    return render(request,'collection/programme.html',context)

def pro_course_list(request, kr, pro,sem):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.filter(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != kr:
        return render(request,'registration/denied.html')
    pr=programme.objects.get(branch=kr,programme_code=pro)
    #msg=br+PR
    #return HttpResponse(pro)
    teaching=ApprovedCourseTeaching.objects.filter(programme=pr,semester=sem)
    courses=ApprovedCourseList.objects.filter(programme=pr,semester=sem)
    global flag
    flag=1
    course_li=[]
    if courses:
        for cr in courses:
            if teaching:
                for teach in teaching:
                    if teach.course_code.course_code==cr.course_code:
                        flag=0
            if(flag==1):
                course_li.append(cr)
            flag=1
    prof=Professor.objects.all().order_by('prof_name')
    context={'programme_li' : pr ,'course_li' : course_li,'professors':prof,'semester':sem,'teaching' : teaching}
    return  render(request,'collection/course_list.html',context)

def login_user(request):
    state = ""
    username = password = ''
    if request.user.is_authenticated():
        #state="Already logged in, "+request.user.username
        profile = Profile.objects.filter(user=request.user)
        return HttpResponseRedirect(reverse('programme_list', args=(str(dept.objects.filter(head=profile)[0].dept_code),)))
    if request.POST:
        username = request.POST['username']
        password = request.POST['pass']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                profile = Profile.objects.filter(user=request.user)
                return HttpResponseRedirect(reverse('programme_list', args=(str(dept.objects.filter(head=profile)[0].dept_code),)))
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render(request, 'registration/login.html',{'state':state})

def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
    return render(request, 'registration/logged_out.html')


def add_teacher(request, kr, pro,sem):
    errors=[]
    pr=programme.objects.get(branch=kr,programme_code=pro)
    courses=ApprovedCourseList.objects.filter(programme=pr,semester=sem)
    prof=Professor.objects.all().order_by('prof_name')
    #if request.method=='POST':
     #   form=
    teaching=ApprovedCourseTeaching.objects.filter(programme=pr,semester=sem)
    global flag
    flag=1
    course_li=[]
    if courses:
        for cr in courses:
            if teaching:
                for teach in teaching:
                    if teach.course_code.course_code==cr.course_code:
                        flag=0
            if(flag==1):
                course_li.append(cr)
            flag=1
    for cr in course_li:
        conevner_form="cname_"+cr.course_code
        con_name= request.POST.get(conevner_form)

        p1_form="p1name_"+cr.course_code
        p1_name=request.POST.get(p1_form)
        p2_form="p1name_"+cr.course_code
        p1_name=request.POST.get(p1_form)
        if con_name:
            cn=Professor.objects.get(prof_id=con_name)

        p1_id=Professor.objects.get(prof_id=p1_name)
        p=ApprovedCourseTeaching(course_code=cr,prof_id1=cn,prof_id2=p1_name,semester=sem,programme=pr,elect_or_comp=1)
        p.save()


    return render(request,'collection/submit.html')




# Create your views here.
