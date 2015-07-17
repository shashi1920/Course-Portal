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
from .models import CheckList
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
    for PR in pr:
        global i
        i=1
        while i<((PR.duration)*2):
            CHECK_CHECK=CheckList.objects.filter(programme=PR,semester=i).count()
            if not CHECK_CHECK:

                p=CheckList(programme=PR,semester=i,allot=0,course=0,minimum_elective=0)
                p.save()
            i+=2

    check=CheckList.objects.filter(programme=pr).order_by('semester')
    dr=dept.objects.get(dept_code=br)
    activity_log=ActivityLog.objects.filter(USER=profile).order_by('-date_time')[:2]

    context={'programme_li' : pr,'deptm': dr,'activity_log':activity_log,'profile':profile,'check':check}
    #return HttpResponse(br)
    return render(request,'collection/programme.html',context)

def pro_course_list(request, kr, pro,sem):

    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.filter(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != kr:
        return render(request,'registration/denied.html')

    pr=programme.objects.get(branch=kr,programme_code=pro)
    CHECK_CHECK=CheckList.objects.filter(programme=pr,semester=sem).count()

    if not CHECK_CHECK:
        p=CheckList(programme=pr,semester=sem,allot=0,course=0,minimum_elective=0)
        p.save()
    CHECK=CheckList.objects.get(programme=pr,semester=sem)
    if CHECK.course==False:
        messages.warning(request,"First verify and lock the list of courses then only you can assign the faculty")
        context={'CHECK':CHECK.course}
        return render(request,'collection/course_list.html',context)
    #msg=br+PR
    #return HttpResponse(pro)
    teaching=ApprovedCourseTeaching.objects.filter(programme=pr,semester=sem)
    courses=ApprovedCourseList.objects.filter(programme=pr,semester=sem)
    count=0
    for cr in courses:
        if(cr.elect_or_comp == 1):
            count+=1

    fr_courses1=ForeignCourseList.objects.filter(programme=pr,semester=sem)
    for cr in fr_courses1:
        if(cr.elect_or_comp == 1):
            count+=1
    global flag
    flag=1
    course_li=[]
    global  NOT_COURSE
    NOT_COURSE=[]
    if courses:
        for cr in courses:
            NOT_COURSE.append(cr)
    if courses:
        for cr in courses:
            if teaching:
                for teach in teaching:
                    if teach.course_code.course_code==cr.course_code:
                        flag=0
                        if cr in NOT_COURSE: NOT_COURSE.remove(cr)
            if(flag==1):
                course_li.append(cr)

            flag=1

    fr_courses=ForeignCourseList.objects.filter(programme=pr,semester=sem)
    CHECK=CheckList.objects.get(programme=pr,semester=sem)
    fr_courses_li=ForeignCourseList.objects.filter(programme=pr,semester=sem,prof_id1__isnull=True)
    prof=Professor.objects.all().order_by('dept')
    url="/programme/"+kr+"/"+pro+"/"+sem+"/"
    context={'programme_li' : pr ,'course_li' : course_li,'professors':prof,'semester':sem,'teaching' : teaching,'url':url,'fr_courses':fr_courses,'fr_courses_li':fr_courses_li,'NOT_COURSE':NOT_COURSE,'CHECK':CHECK,'count':count}
    return  render(request,'collection/course_list.html',context)



def pro_course_list_print(request, kr, pro):

    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.filter(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != kr:
        return render(request,'registration/denied.html')
    pr=programme.objects.get(branch=kr,programme_code=pro)
    global flag
    flag=1
    global pr_list
    check=CheckList.objects.filter(programme=pr)
    for CH in check:
        if not CH.allot or not CH.course:
            flag=0
    if flag==1:
        i=range(1,pr.duration*2,2)
        j=['I','III','V','VII','IX','XI','XI']
        IN=zip(i,j)
        course_list=ApprovedCourseTeaching.objects.filter(programme=pr)
        fr_course_list=ForeignCourseList.objects.filter(programme=pr)

        context= {'course_list':course_list,'sem':IN,'fr_course_list':fr_course_list,'check':check,'pr':pr}
        return render(request,'collection/print_page.html',context)
    msg_log="You need to lock all the courses, courses-faculty data before you can print/export data of <b>"+pr.programme_name+"</b>"
    messages.error(request,msg_log)
    url='/programme/'+kr+'/'
    return HttpResponseRedirect(url)
def login_user(request):
    state = ""
    username = password = ''
    if request.user.is_authenticated():
        #state="Already logged in, "+request.user.username
        profile = Profile.objects.get(user=request.user)
        return HttpResponseRedirect(reverse('programme_list', args=(str(dept.objects.filter(head=profile)[0].dept_code),)))
    if request.POST:
        username = request.POST['username']
        password = request.POST['pass']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                profile = Profile.objects.get(user=request.user)
                return HttpResponseRedirect(reverse('programme_list', args=(str(dept.objects.filter(head=profile)[0].dept_code),)))
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
            messages.error(request,state)

    return render(request, 'registration/login.html')

def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
        state="You have been successfully logged out."
        messages.success(request,state)
    else:
        state="Oops ! You are already logged out ! Try logging in again"
        messages.error(request,state)
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
    fr_courses_li=ForeignCourseList.objects.filter(programme=pr,semester=sem,prof_id1__isnull=True)
    for cr in fr_courses_li:
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
                er1="You have selected same Convener name as other faculty in "
                errors.append(er1)
                er1=cr.course_code +" "+cr.course.course_name
                course_error.append(er1)
                er=True
            if((not p2_name) and (p3_name)):
                er1="Select 2nd Faculty First Then 3rd Faculty "
                errors.append(er1)
                er1=cr.course_code +" "+cr.course.course_name
                course_error.append(er1)
                er=True
            if((not p1_name) and (p2_name)):
                er1="Select 1st Faculty First Then Select 2nd Faculty "
                errors.append(er1)
                er1=cr.course_code +" "+cr.course.course_name
                course_error.append(er1)
                er=True
            if((not p1_name) and (p3_name)):
                er1="Select 1st Faculty First Then Select 3rd Faculty "
                errors.append(er1)
                er1=cr.course_code +" "+cr.course.course_name
                course_error.append(er1)
                er=True
            if((p1_name==p2_name and p1_name) or (p3_name==p1_name and p3_name)) or (p2_name==p3_name and p3_name):
                er1="You have selected same faculty "
                errors.append(er1)
                er1=cr.course_code +" "+cr.course.course_name
                course_error.append(er1)
                er=True
            #Succesful COurses Now
            if(p3_name and p2_name and p1_name and (not er)):
                p1_id=Professor.objects.get(prof_id=p1_name)
                p2_id=Professor.objects.get(prof_id=p2_name)
                p3_id=Professor.objects.get(prof_id=p3_name)
                p=ForeignCourseList.objects.get(course_code=cr,semester=sem,programme=pr)
                p.prof_id1=cn
                p.prof_id2=p1_id
                p.prof_id3=p2_id
                p.prof_id4=p3_id,

                p.save()
                success=cr.course_code +" "+cr.course.course_name
                log_message="Successfully Added Faculty Details of "+success
                log_query=ActivityLog(USER=profile,log=log_message)
                log_query.save()

                course_success.append(success)
            elif(p2_name and p1_name and (not er)):
                p1_id=Professor.objects.get(prof_id=p1_name)
                p2_id=Professor.objects.get(prof_id=p2_name)
                p=ForeignCourseList.objects.get(course_code=cr,semester=sem,programme=pr)

                p.prof_id1=cn
                p.prof_id2=p1_id
                p.prof_id3=p2_id

                p.save()
                success=cr.course_code +" "+cr.course.course_name
                log_message="Successfully Added Faculty Details of "+success
                log_query=ActivityLog(USER=profile,log=log_message)
                log_query.save()

                course_success.append(success)
            elif(p1_name and not(er)):
                p1_id=Professor.objects.get(prof_id=p1_name)
                p=ForeignCourseList.objects.get(course_code=cr,semester=sem,programme=pr)
                p.prof_id1=cn
                p.prof_id2=p1_id
                p.save()
                success=cr.course_code +" "+cr.course.course_name
                log_message="Successfully Added Faculty Details of "+success
                log_query=ActivityLog(USER=profile,log=log_message)
                log_query.save()
                course_success.append(success)
            elif((not er)):
                p=ForeignCourseList.objects.get(course_code=cr,semester=sem,programme=pr)
                p.prof_id1=cn
                p.save()
                success=cr.course_code +" "+cr.course.course_name
                log_message="Successfully Added Faculty Details of "+success
                log_query=ActivityLog(USER=profile,log=log_message)
                log_query.save()
                course_success.append(success)
    error_list=zip(errors,course_error)
    for err in error_list:
        messages.error(request,err[0]+' in '+err[1])
    er=False
    for suc in course_success:
        suc="You have successfully updated Convener and Other Faculty For <b>"+suc+"</b>"
        messages.success(request,suc)
    url="/programme/"+kr+"/"+pro+"/"+sem+"/"

    return HttpResponseRedirect(url)

def delete_teacher(request,br, pro,sem,entry):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    pr=programme.objects.get(branch=br,programme_code=pro)
    entry1=ApprovedCourseTeaching.objects.get(pk=entry)
    log_message="Successfully Deleted Faculty Details of <b>"+entry1.course_code.course_code+" : " + entry1.course_code.course_name +"</b>"

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
            global pr
            global cr
            pr=programme.objects.get(pk=frpr)
            cr=ApprovedCourseList.objects.get(pk=frcr)
            COURSE_CODE=cr.course_code+"A"

            if(int(SEM)>(2*pr.duration)):
                msg="Sorry, Semester count can't be greater than maximum duration for  "+cr.course_code
                messages.error(request,msg)
            else:
                check=ForeignCourseList.objects.filter(programme=pr,course_code=COURSE_CODE,course=cr,semester=SEM)
                if not check:
                    ins=ForeignCourseList(programme=pr,course_code=COURSE_CODE,course=cr,semester=SEM)
                    ins.save()
                    msg="Successfully Offered " + cr.course_code + " " + cr.course_name +" to "+pr.programme_name+"("+pr.programme_code+") "+pr.branch.dept_name
                    messages.success(request,msg)
                    p=ActivityLog(USER=profile,log=msg)
                    p.save()
                else:
                    msg="Sorry this course is already offered - " + cr.course_code + " " + cr.course_name +" to "+pr.programme_name+"("+pr.programme_code+") "+pr.branch.dept_name
                    messages.error(request,msg)
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
def fr_course_delete(request,br, pro,sem,entry):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    entry1=ForeignCourseList.objects.get(pk=entry)
    log_message="Successfully Deleted Faculty Details of "+entry1.course_code+" " + entry1.course.course_name
    entry1.prof_id1=None
    entry1.prof_id2=None
    entry1.prof_id3=None
    entry1.prof_id4=None
    entry1.save()
    p=ActivityLog(USER=profile,log=log_message)

    messages.success(request,log_message)
    p.save()
    url="/programme/"+br+"/"+pro+"/"+sem

    return HttpResponseRedirect(url)

def COURSES(request, br, pro,sem):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    pr=programme.objects.get(branch=br,programme_code=pro)
    CHECK=CheckList.objects.get(programme=pr,semester=sem)
    courses=ApprovedCourseList.objects.filter(programme=pr,semester=sem).order_by('-elect_or_comp')
    count=0
    for cr in courses:
        if(cr.elect_or_comp == 1):
            count+=1

    fr_courses=ForeignCourseList.objects.filter(programme=pr,semester=sem).order_by('-elect_or_comp')
    for cr in fr_courses:
        if(cr.elect_or_comp == 1):
            count+=1

    url="/programme/"+br+"/"+pro+"/"+sem+"/"
    context={'courses':courses,'semester':sem,'programme':pr,'CHECK':CHECK,'url':url,'fr_courses':fr_courses,'count':count}
    return  render(request,'collection/all_courses.html',context)

def LOCK_COURSES(request, br, pro,sem):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    pr=programme.objects.get(branch=br,programme_code=pro)
    CHECK=CheckList.objects.get(programme=pr,semester=sem)
    CHECK.course=True
    CHECK.save()
    log_message="Succesfully Locked Courses of Semester "+sem
    messages.success(request,log_message)
    url="/programme/"+br+"/"+pro+"/"+sem+"/"+"courses"
    return HttpResponseRedirect(url)

def LOCK(request, br, pro,sem):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    pr=programme.objects.get(branch=br,programme_code=pro)
    CHECK=CheckList.objects.get(programme=pr,semester=sem)
    CHECK.allot=True
    CHECK.save()
    log_message="Succesfully Locked Course-Faculty Details of Semester "+sem
    messages.success(request,log_message)
    url="/programme/"+br+"/"+pro+"/"+sem
    return HttpResponseRedirect(url)




def add_course(request, br, pro,sem):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    pr=programme.objects.get(branch=br,programme_code=pro)
    courses=ApprovedCourseList.objects.filter(programme=pr,semester=sem)
    url="/programme/"+br+"/"+pro+"/"+sem+"/"
    context={'courses':courses,'semester':sem,'programme':pr}
    url="/programme/"+br+"/"+pro+"/"+sem+"/courses"
    course_name=request.POST.get('course_name')
    course_code=request.POST.get('course_code')
    credit=request.POST.get('credit')
    type=request.POST.get('elect_or_comp')
    syllabus=request.POST.get('syllabus')
    l=request.POST.get('l')
    t=request.POST.get('t')
    p=request.POST.get('p')
    CHECK=CheckList.objects.get(programme=pr,semester=sem)
    if CHECK.course:
        messages.error(request,"Sorry Courses are locked you can't edit now!")
        return HttpResponseRedirect(url)
    if (course_name and course_code) and (credit or (l+t+p)):
        check_course=ApprovedCourseList.objects.filter(semester=sem,programme=pr,course_code=course_code)
        if not check_course:
            new_course=ApprovedCourseList(semester=sem,programme=pr,course_code=course_code,course_name=course_name,elect_or_comp=type,syllabus=syllabus,l=l,t=t,p=p,credit=credit)
            new_course.save()
            log_message="Successfully added 1 course named "+course_code + course_name

            messages.success(request,log_message)
        else: messages.error(request,"Sorry this course already exists,Try Editing the course if you want to update it.")
    return HttpResponseRedirect(url)




def DELETE_COURSES(request,br, pro,sem,entry):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    entry1=ApprovedCourseList.objects.get(pk=entry)
    url="/programme/"+br+"/"+pro+"/"+sem+"/"
    pr=programme.objects.get(branch=br,programme_code=pro)
    CHECK=CheckList.objects.get(programme=pr,semester=sem)

    if CHECK.course:
        messages.error(request,"Sorry Courses are locked you can't delete now!")
        return HttpResponseRedirect(url)
    log_message="Successfully Deleted "+entry1.course_code+" " + entry1.course_name+" course"+"offered in semester "+sem

    entry1.delete()
    p=ActivityLog(USER=profile,log=log_message)

    messages.success(request,log_message)
    p.save()
    url="/programme/"+br+"/"+pro+"/"+sem+"/courses"

    return HttpResponseRedirect(url)

def EDIT_COURSES(request,br, pro,sem,entry):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    entry1=ApprovedCourseList.objects.get(pk=entry)
    pr=programme.objects.get(branch=br,programme_code=pro)
    url="/programme/"+br+"/"+pro+"/"+sem+"/"
    CHECK=CheckList.objects.get(programme=pr,semester=sem)
    check_flag=0
    if CHECK.course:
        messages.error(request,"Sorry Courses are locked you can't delete now!")
        return HttpResponseRedirect(url)
    log_message="Successfully updated "+entry1.course_code+" " + entry1.course_name+" course"+"offered in semester "+sem

    if request.POST.get('course_code'):
        entry1.course_code=request.POST.get('course_code')

    if request.POST.get('course_name'):
        entry1.course_name=request.POST.get('course_name')

    if request.POST.get('elect_or_comp'):
        entry1.elect_or_comp=request.POST.get('elect_or_comp')

    if request.POST.get('syllabus'):
        entry1.syllabus=request.POST.get('syllabus')
    if request.POST.get('l'):
        entry1.l=request.POST.get('l')
    if request.POST.get('t'):
        entry1.t=request.POST.get('t')
    if request.POST.get('p'):
        entry1.p=request.POST.get('p')
    if request.POST.get('credit'):
        entry1.credit=request.POST.get('credit')



    entry1.save()

    p=ActivityLog(USER=profile,log=log_message)

    messages.success(request,log_message)
    p.save()
    url="/programme/"+br+"/"+pro+"/"+sem+"/courses"

    return HttpResponseRedirect(url)


def EDIT_ELECTIVE(request,br, pro,sem):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')

    pr=programme.objects.get(branch=br,programme_code=pro)
    url="/programme/"+br+"/"+pro+"/"+sem+"/courses/"
    CHECK=CheckList.objects.get(programme=pr,semester=sem)

    if CHECK.course:
        messages.error(request,"Sorry Courses are locked you can't edit it now...!!")
        return HttpResponseRedirect(url)





    if request.POST.get('minimum_elective'):
        CHECK.minimum_elective=request.POST.get('minimum_elective')

    CHECK.save()


    log_message="Minimum number of electives for semester " +sem +"of "+pr.programme_name+pr.branch.dept_name+"successfully updated"
    p=ActivityLog(USER=profile,log=log_message)

    messages.success(request,log_message)
    p.save()
    url="/programme/"+br+"/"+pro+"/"+sem+"/courses"

    return HttpResponseRedirect(url)


def EDIT_FR_COURSES(request,br, pro,sem,entry):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    entry1=ForeignCourseList.objects.get(pk=entry)
    pr=programme.objects.get(branch=br,programme_code=pro)
    url="/programme/"+br+"/"+pro+"/"+sem+"/"
    CHECK=CheckList.objects.get(programme=pr,semester=sem)

    if CHECK.course:
        messages.error(request,"Sorry Courses are locked you can't delete now!")
        return HttpResponseRedirect(url)
    log_message="Successfully updated "+entry1.course_code+" " + entry1.course.course_name+" course"+"offered in semester "+sem

    if request.POST.get('course_code'):
        entry1.course_code=request.POST.get('course_code')

#    if request.POST.get('course_name'):
 #       entry1.course_name=request.POST.get('course_name')

    if request.POST.get('elect_or_comp'):
        entry1.elect_or_comp=request.POST.get('elect_or_comp')

    if request.POST.get('syllabus'):
        entry1.syllabus=request.POST.get('syllabus')
    if request.POST.get('l'):
        entry1.l=request.POST.get('l')
    if request.POST.get('t'):
        entry1.t=request.POST.get('t')
    if request.POST.get('p'):
        entry1.p=request.POST.get('p')
    if request.POST.get('credit'):
        entry1.credit=request.POST.get('credit')

    entry1.save()

    p=ActivityLog(USER=profile,log=log_message)

    messages.success(request,log_message)
    p.save()
    url="/programme/"+br+"/"+pro+"/"+sem+"/courses"

    return HttpResponseRedirect(url)

def DELETE_FR_COURSES(request,br, pro,sem,entry):
    if not request.user.is_authenticated():
        return render(request,'registration/denied.html')
    profile = Profile.objects.get(user=request.user)
    if len(dept.objects.filter(head=profile))==0 or str(dept.objects.filter(head=profile)[0].dept_code) != br:
        return render(request,'registration/denied.html')
    entry1=ForeignCourseList.objects.get(pk=entry)
    pr=programme.objects.get(branch=br,programme_code=pro)
    url="/programme/"+br+"/"+pro+"/"+sem+"/"
    CHECK=CheckList.objects.get(programme=pr,semester=sem)

    if CHECK.course:
        messages.error(request,"Sorry Courses are locked you can't delete now!")
        return HttpResponseRedirect(url)
    log_message="Successfully deleted "+entry1.course_code+" " + entry1.course.course_name+" course"+"offered in semester "+sem


    entry1.delete()

    p=ActivityLog(USER=profile,log=log_message)

    messages.success(request,log_message)
    p.save()
    url="/programme/"+br+"/"+pro+"/"+sem+"/courses"

    return HttpResponseRedirect(url)