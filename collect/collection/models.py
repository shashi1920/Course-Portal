from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    level = models.IntegerField(max_length=1) #Level 0 is Professor, Level 1 is for HODs

    def __str__(self):              # __unicode__ on Python 2
        return self.user.username

class dept(models.Model):
    dept_code = models.CharField(max_length=2, primary_key=True)
    dept_name = models.CharField(max_length=150)
    head = models.ForeignKey(Profile,unique=True)  # HOD
    def __str__(self):              # __unicode__ on Python 2
        return self.dept_name

class programme(models.Model): #Btech/IDD/M.Tech/B.Pharm etc
    programme_code=models.CharField(max_length=25)
    programme_name=models.CharField(max_length=250)
    duration=models.IntegerField(max_length=2)
    branch=models.ForeignKey(dept,blank=False,null=False)
    def __str__(self):              # __unicode__ on Python 2
        return self.programme_code

class Professor(models.Model):
    des = (
        ('P', 'Professor'),
        ('ASP', 'Assistant Professor'),
        ('APT', 'Associate Professor'),
    )
    prof_id = models.IntegerField(primary_key=True)  # This is employee id, as sir said it is unique for a prof.
    prof_name = models.CharField(max_length=150)
    email = models.EmailField(blank=False, null=False)
    dept = models.ForeignKey(dept)
    designation = models.CharField(max_length=3, choices=des,null=True,blank=True)  # Currently I have added only three desnignations

    def __str__(self):              # __unicode__ on Python 2
        return self.prof_name

class ApprovedCourseList(models.Model):
    course_code = models.CharField(max_length=10)#as IDD and B.Tech have same code so id is used
    course_name = models.CharField(max_length=150)
    syllabus = models.CharField(max_length=2500,blank=True,null=True)
    credit = models.IntegerField(max_length=2)
    ELECT=models.CharField(max_length=5,blank=True,null=True)
    programme = models.ForeignKey(programme)
    l=models.IntegerField(blank=True,null=True)
    t=models.IntegerField(blank=True,null=True)
    elect_or_comp = models.IntegerField(default=1) #1 for compulsory, 0 for elective,
    p=models.IntegerField(blank=True,null=True)
    level_0 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_0_list')
    level_1 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_1_list')
    level_2 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_2_list')
    semester=models.IntegerField(max_length=2)
    def __str__(self):              # __unicode__ on Python 2
        return self.course_code


class ForeignCourseList(models.Model):
    course_code = models.CharField(max_length=10)
    course=models.ForeignKey(ApprovedCourseList)
    credit = models.IntegerField(blank=True,null=True)
    programme = models.ForeignKey(programme)
    semester=models.IntegerField()
    l=models.IntegerField(blank=True,null=True)
    t=models.IntegerField(blank=True,null=True)
    p=models.IntegerField(blank=True,null=True)
    elect_or_comp = models.IntegerField(max_length=1,blank=True,default=1)
    prof_id1 = models.ForeignKey(Professor,blank=True,null=True)
    date_added=models.DateTimeField(auto_now=True)
    prof_id2 = models.ForeignKey(Professor, null=True, blank=True, related_name='fr_prof_id2')
    prof_id3 = models.ForeignKey(Professor, null=True, blank=True, related_name='fr_prof_id3')
    prof_id4 = models.ForeignKey(Professor, null=True, blank=True, related_name='fr_prof_id4')
    def __str__(self):              # __unicode__ on Python 2
        return self.course_code
class CheckList(models.Model):
    programme=models.ForeignKey(programme)
    semester=models.IntegerField()
    course=models.BooleanField(default=False)
    minimum_elective=models.IntegerField()
    allot=models.BooleanField(default=False)
    def __str__(self):              # __unicode__ on Python 2
        return str(self.programme)
class ProposedCourseList(models.Model):
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=150)
    syllabus = models.CharField(max_length=2500)
    programme = models.ForeignKey(programme)
    level_0 = models.ForeignKey(Profile, null=True, blank=True, related_name='pro_level_0_list')
    level_1 = models.ForeignKey(Profile, null=True, blank=True, related_name='pro_level_1_list')
    level_2 = models.ForeignKey(Profile, null=True, blank=True, related_name='pro_level_2_list')
    level_0_sign = models.IntegerField(max_length=1)
    level_1_sign = models.IntegerField(max_length=1)
    level_2_sign = models.IntegerField(max_length=1)
    date_proposed= models.DateTimeField(auto_now=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.course_code

class ApprovedCourseTeaching(models.Model):
    application_no = models.AutoField(primary_key=True)
    course_code = models.ForeignKey(ApprovedCourseList)
    prof_id1 = models.ForeignKey(Professor)
    semester = models.IntegerField(max_length=2)
    programme = models.ForeignKey(programme)
    date_added=models.DateTimeField(auto_now=True)
    prof_id2 = models.ForeignKey(Professor, null=True, blank=True, related_name='prof_id2')
    prof_id3 = models.ForeignKey(Professor, null=True, blank=True, related_name='prof_id3')
    prof_id4 = models.ForeignKey(Professor, null=True, blank=True, related_name='prof_id4')

    level_0 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_0_teaching')
    level_1 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_1_teaching')
    level_2 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_2_teaching')
    def __str__(self):              # __unicode__ on Python 2
        return str(self.application_no)


class ProposedCourseTeaching(models.Model):
    application_no = models.AutoField(primary_key=True)
    course_code = models.ForeignKey(ApprovedCourseList)
    prof_id = models.ForeignKey(Professor)
    semester = models.IntegerField(max_length=2)
    programme = models.ForeignKey(programme)
    course = models.CharField(max_length=10)
    level_0 = models.ForeignKey(Profile, null=True, blank=True, related_name='pro_level_0_teaching')
    level_1 = models.ForeignKey(Profile, null=True, blank=True, related_name='pro_level_1_teaching')
    level_2 = models.ForeignKey(Profile, null=True, blank=True, related_name='pro_level_2_teaching')
    level_0_sign = models.IntegerField(max_length=1)
    level_1_sign = models.IntegerField(max_length=1)
    level_2_sign = models.IntegerField(max_length=1)
    def __str__(self):              # __unicode__ on Python 2
        return self.course_code
class ActivityLog(models.Model):
    USER=models.ForeignKey(Profile)
    log=models.CharField(max_length=1500)
    date_time= models.DateTimeField(auto_now=True)
    def __unicode__(self):              # __unicode__ on Python 2
        return self.log