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

from django.contrib.auth import authenticate, login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            #redirect to success page
            login(request, user)
            return render(request,'collection/index.html')

        else:
            #redirect to this page again
            return HttpResponse("Invalid login details supplied.")

    else:
        return render('registration/mylogin.html'}
    return render(request, 'registration/mylogin.html', {'form': form,})

from django.contrib.auth import logout
def logout(request):
     logout(request)
     return HttpResponseRedirect('registration/logged_out.html')

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
