from django.contrib import admin
from .models import Professor
from .models import Profile
from .models import dept
from .models import ActivityLog
from .models import programme
from .models import ProposedCourseList
from .models import ProposedCourseTeaching
from .models import ApprovedCourseList
from .models import ApprovedCourseTeaching
from .models import ForeignCourseList

admin.site.register(Profile)
admin.site.register(ProposedCourseTeaching)
admin.site.register(ProposedCourseList)
admin.site.register(ApprovedCourseList)
admin.site.register(ApprovedCourseTeaching)
admin.site.register(ForeignCourseList)
admin.site.register(dept)
admin.site.register(programme)
admin.site.register(Professor)
admin.site.register(ActivityLog)


# Register your models here.
