from django.contrib import admin
from .import models

# Register your models here.
admin.site.register(models.Client)
admin.site.register(models.ClientWork)
admin.site.register(models.ClientWorkAssignTo)
admin.site.register(models.Team)
admin.site.register(models.TeamMember)
admin.site.register(models.UserTeamViewPermission)
admin.site.register(models.UserCanManageOtherTeamMemberTask)
admin.site.register(models.UserCanViewOtherTeamMemberTask)
