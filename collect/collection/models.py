from django.db import models


class Profile(models.Model):
    email = models.EmailField(null=False, blank=False, primary_key=True)
    name = models.CharField(max_length=150)
    level = models.IntegerField(max_length=1) #Level 0 is Professor, Level 1 is for HODs

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class dept(models.Model):
    dept_code = models.CharField(max_length=2, primary_key=True)
    dept_name = models.CharField(max_length=150)
    head = models.ForeignKey(Profile)  # HOD
    def __str__(self):              # __unicode__ on Python 2
        return self.dept_name

class programme(models.Model): #Btech/IDD/M.Tech/B.Pharm etc
    programme_code=models.CharField(max_length=5,primary_key=True)
    programme_name=models.CharField(max_length=200)
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
    designation = models.CharField(max_length=3, choices=des)  # Currently I have added only three desnignations

    def __str__(self):              # __unicode__ on Python 2
        return self.prof_name

class ApprovedCourseList(models.Model):
    course_code = models.CharField(max_length=10)#as IDD and B.Tech have same code so id is used
    course_name = models.CharField(max_length=150)
    syllabus = models.CharField(max_length=2500)
    credit = models.IntegerField(max_length=2)
    programme = models.ForeignKey(programme)
    level_0 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_0_list')
    level_1 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_1_list')
    level_2 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_2_list')
    def __str__(self):              # __unicode__ on Python 2
        return self.course_code


class ForeignCourseList(models.Model):
    course_code = models.CharField(max_length=10)
    course=models.ForeignKey(ApprovedCourseList)
    credit = models.IntegerField()
    programme = models.ForeignKey(programme)
    level_0 = models.ForeignKey(Profile, null=True, blank=True, related_name='for_level_0_list')
    level_1 = models.ForeignKey(Profile, null=True, blank=True, related_name='for_level_1_list')
    level_2 = models.ForeignKey(Profile, null=True, blank=True, related_name='for_level_2_list')
    def __str__(self):              # __unicode__ on Python 2
        return self.course_code

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
    course = models.CharField(max_length=10)
    date_added=models.DateTimeField(auto_now=True)
    prof_id2 = models.ForeignKey(Professor, null=True, blank=True, related_name='prof_id2')
    prof_id3 = models.ForeignKey(Professor, null=True, blank=True, related_name='prof_id3')
    prof_id4 = models.ForeignKey(Professor, null=True, blank=True, related_name='prof_id4')
    elect_or_comp = models.IntegerField(max_length=1)
    level_0 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_0_teaching')
    level_1 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_1_teaching')
    level_2 = models.ForeignKey(Profile, null=True, blank=True, related_name='app_level_2_teaching')
    def __str__(self):              # __unicode__ on Python 2
        return self.course_code

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