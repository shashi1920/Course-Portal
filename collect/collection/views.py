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
    url="/programme/"+kr+"/"+pro+"/"+sem+"/"
    context={'programme_li' : pr ,'course_li' : course_li,'professors':prof,'semester':sem,'teaching' : teaching,'url':url}
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
    course_error=[]
    course_success=[]
    pr=programme.objects.get(branch=kr,programme_code=pro)
    courses=ApprovedCourseList.objects.filter(programme=pr,semester=sem)
    prof=Professor.objects.all().order_by('prof_name')
    #if request.method=='POST':
     #   form=
    teaching=ApprovedCourseTeaching.objects.filter(programme=pr,semester=sem)
    global flag
    flag=1
    course_li=[]
    global er
    er=False
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

        p1_form="p1name"+cr.course_code
        p1_name=request.POST.get(p1_form)
        p2_form="p2name"+cr.course_code
        p2_name=request.POST.get(p2_form)
        p3_form="p3name"+cr.course_code
        p3_name=request.POST.get(p3_form)
        if con_name:
            cn=Professor.objects.get(prof_id=con_name)
            if (con_name==p1_name or con_name==p2_name or con_name==p3_name):
                er1="You have selected same Convener name as other faculty "
                errors.append(er1)
                er1=cr.course_code +" "+cr.course_name
                course_error.append(er1)
                er=True
            if((not p2_name) and (p3_name)):
                er1="Select 2nd Faculty First Then 3rd Faculty "
                errors.append(er1)
                er1=cr.course_code +" "+cr.course_name
                course_error.append(er1)
                er=True
            if((not p1_name) and (p2_name)):
                er1="Select 1st Faculty First Then Select 2nd Faculty "
                errors.append(er1)
                er1=cr.course_code +" "+cr.course_name
                course_error.append(er1)
                er=True
            if((not p1_name) and (p3_name)):
                er1="Select 1st Faculty First Then Select 3rd Faculty "
                errors.append(er1)
                er1=cr.course_code +" "+cr.course_name
                course_error.append(er1)
                er=True
            if((p1_name==p2_name and p1_name) or (p3_name==p1_name and p3_name)) or (p2_name==p3_name and p3_name):
                er1="You have selected same faculty "
                errors.append(er1)
                er1=cr.course_code +" "+cr.course_name
                course_error.append(er1)
                er=True
            #Succesful COurses Now
            if(p3_name and p2_name and p1_name and (not er)):
                p1_id=Professor.objects.get(prof_id=p1_name)
                p2_id=Professor.objects.get(prof_id=p2_name)
                p3_id=Professor.objects.get(prof_id=p3_name)
                p=ApprovedCourseTeaching(course_code=cr,prof_id1=cn,prof_id2=p1_id,prof_id3=p2_id,prof_id4=p3_id,semester=sem,programme=pr,elect_or_comp=1)

                p.save()
                success=cr.course_code +" "+cr.course_name
                course_success.append(success)
            elif(p2_name and p1_name and (not er)):
                p1_id=Professor.objects.get(prof_id=p1_name)
                p2_id=Professor.objects.get(prof_id=p2_name)
                p=ApprovedCourseTeaching(course_code=cr,prof_id1=cn,prof_id2=p1_id,prof_id3=p2_id,semester=sem,programme=pr,elect_or_comp=1)
                p.save()

                success=cr.course_code +" "+cr.course_name
                course_success.append(success)
            elif(p1_name and not(er)):
                p1_id=Professor.objects.get(prof_id=p1_name)

                p=ApprovedCourseTeaching(course_code=cr,prof_id1=cn,prof_id2=p1_id,semester=sem,programme=pr,elect_or_comp=1)
                p.save()
                success=cr.course_code +" "+cr.course_name
                course_success.append(success)
            elif((not er)):
                p=ApprovedCourseTeaching(course_code=cr,prof_id1=cn,semester=sem,programme=pr,elect_or_comp=1)
                p.save()
                success=cr.course_code +" "+cr.course_name
                course_success.append(success)
    error_list=zip(errors,course_error)
    er=False
    url="/programme/"+kr+"/"+pro+"/"+sem+"/"
    context={'errors': error_list,'course_success':course_success,'back_url':url}
    return render(request,'collection/submit.html',context)

def delete_teacher(request,br, pro,sem,entry):
    pr=programme.objects.get(branch=br,programme_code=pro)
    entry1=ApprovedCourseTeaching.objects.get(pk=entry)
    entry1.delete()
# Create your views here.
