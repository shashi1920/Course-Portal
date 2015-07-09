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
from django.contrib import messages
from .models import ActivityLog
from django.db.models import Q
from django.http import Http404
def index(request):
    return render(request, 'collection/index.html')

def programme_list(request, br):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    pr=programme.objects.filter(branch=br)
    dr=dept.objects.get(dept_code=br)
    activity_log=ActivityLog.objects.filter(USER=profile).order_by('-date_time')[:5]
    context={'programme_li' : pr,'deptm': dr,'activity_log':activity_log,'profile':profile}
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
def pro_course_list_print(request, kr, pro,sem):
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
    return  render(request,'collection/print.html',context)

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
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != kr:
        return render(request,'registration/denied.html')
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
                p=ApprovedCourseTeaching(course_code=cr,prof_id1=cn,prof_id2=p1_id,prof_id3=p2_id,prof_id4=p3_id,semester=sem,programme=pr)


                p.save()
                log_message="Successfully Added Faculty Details of "+success
                log_query=ActivityLog(USER=profile,log=log_message)
                log_query.save()
                success=cr.course_code +" "+cr.course_name
                course_success.append(success)
            elif(p2_name and p1_name and (not er)):
                p1_id=Professor.objects.get(prof_id=p1_name)
                p2_id=Professor.objects.get(prof_id=p2_name)
                p=ApprovedCourseTeaching(course_code=cr,prof_id1=cn,prof_id2=p1_id,prof_id3=p2_id,semester=sem,programme=pr)
                p.save()
                success=cr.course_code +" "+cr.course_name
                log_message="Successfully Added Faculty Details of "+success
                log_query=ActivityLog(USER=profile,log=log_message)
                log_query.save()

                course_success.append(success)
            elif(p1_name and not(er)):
                p1_id=Professor.objects.get(prof_id=p1_name)

                p=ApprovedCourseTeaching(course_code=cr,prof_id1=cn,prof_id2=p1_id,semester=sem,programme=pr)
                p.save()
                success=cr.course_code +" "+cr.course_name
                log_message="Successfully Added Faculty Details of "+success
                log_query=ActivityLog(USER=profile,log=log_message)
                log_query.save()
                course_success.append(success)
            elif((not er)):
                p=ApprovedCourseTeaching(course_code=cr,prof_id1=cn,semester=sem,programme=pr)
                p.save()
                success=cr.course_code +" "+cr.course_name
                log_message="Successfully Added Faculty Details of "+success
                log_query=ActivityLog(USER=profile,log=log_message)
                log_query.save()
                course_success.append(success)

    error_list=zip(errors,course_error)
    er=False
    url="/programme/"+kr+"/"+pro+"/"+sem+"/"
    context={'errors': error_list,'course_success':course_success,'back_url':url}
    return render(request,'collection/submit.html',context)

def delete_teacher(request,br, pro,sem,entry):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    pr=programme.objects.get(branch=br,programme_code=pro)
    entry1=ApprovedCourseTeaching.objects.get(pk=entry)
    log_message="Successfully Deleted Faculty Details of "+entry1.course_code.course_code+" " + entry1.course_code.course_name

    p=ActivityLog(USER=profile,log=log_message)

    entry1.delete()
    messages.success(request,log_message)
    p.save()
    url="/programme/"+br+"/"+pro+"/"+sem

    return HttpResponseRedirect(url)
def activity_log_details(request,br):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    activity_log=ActivityLog.objects.filter(USER=profile)
    context={'activity_log' : activity_log}
    return render(request,'collection/activity_log.html',context)
def custom404(request):
    return render(request,'collection/404.html')

def fr_course_list_print(request,br, pro,sem):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')

    prog=programme.objects.filter(~Q(branch = br))
    pr=programme.objects.get(branch=br,programme_code=pro)
    courses=ApprovedCourseList.objects.filter(programme=pr,semester=sem)
    course_offered_from=ForeignCourseList.objects.filter(course=courses)
    context={'programme':prog,'courses':courses,'course_offered_from':course_offered_from,'semester':sem}
    return render(request,'collection/foreign_print.html',context)

def fr_course_list(request,br, pro,sem):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')

    prog=programme.objects.filter(~Q(branch = br))
    pr=programme.objects.get(branch=br,programme_code=pro)
    courses=ApprovedCourseList.objects.filter(programme=pr,semester=sem)
    course_offered_from=ForeignCourseList.objects.filter(course=courses)
    context={'programme':prog,'courses':courses,'course_offered_from':course_offered_from,'semester':sem}
    return render(request,'collection/404.html',context)

def fr_submit(request,br,pro,sem):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    for i in "54321":
        fr_pr='fr_program'+i
        frpr=request.POST.get(fr_pr)
        fr_cr='fr_course'+i
        frcr=request.POST.get(fr_cr)
        seme='sem'+i
        SEM=request.POST.get(seme)
        if frpr and frcr:
            pr=programme.objects.get(pk=frpr)
            cr=ApprovedCourseList.objects.get(pk=frcr)
            COURSE_CODE=cr.course_code+"A"

            if(int(SEM)>(2*pr.duration)):
                msg="Sorry, Semester count can't be greater than maximum duration for  "+cr.course_code
                messages.error(request,msg)
            else:
                ins=ForeignCourseList(programme=pr,course_code=COURSE_CODE,course=cr,semester=SEM)
                ins.save()
                msg="Successfully Offered " + cr.course_code + " " + cr.course_name +" to "+pr.programme_name+"("+pr.programme_code+") "+pr.branch.dept_name
                messages.success(request,msg)
                p=ActivityLog(USER=profile,log=msg)
                p.save()

    url="/programme/"+br+"/"+pro+"/"+sem+'/fr'
    return HttpResponseRedirect(url)
def fr_delete(request,br, pro,sem,entry):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    pr=programme.objects.get(branch=br,programme_code=pro)
    entry1=ForeignCourseList.objects.get(pk=entry)
    log_message="Successfully Deleted "+entry1.course_code+" "+entry1.course.course_name+" Offered Course"

    p=ActivityLog(USER=profile,log=log_message)

    entry1.delete()
    messages.warning(request,log_message)
    p.save()
    url="/programme/"+br+"/"+pro+"/"+sem+"/fr"
    return HttpResponseRedirect(url)

# Create your views here.
