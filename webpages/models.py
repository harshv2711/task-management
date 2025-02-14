from django.db import models
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

# Create your models here.
class Client(models.Model):
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    client_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name

class ClientWork(models.Model):
    class Meta:
        verbose_name = "Client Work"
        verbose_name_plural = "Client Works"
    

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    work_name = models.CharField(max_length=255)
    work_description = models.TextField(blank=True, null=True)
    proposal_date = models.DateField(blank=True, null=True)
    work_started_at = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    assign_to = models.ForeignKey(User, models.CASCADE, blank=True, null=True)

    STATUS_CHOICES = [
        ("in_queue", "In queue"),
        ("ongoing", "Ongoing"),
        ("waiting_for_approval", "Waiting for approval"),
        ("completed", "Completed"),
        ("on_hold", "On Hold"),
        ("cancelled", "Cancelled"),
    ]
    

    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.work_name

class ClientWorkAssignTo(models.Model):
    class Meta:
        verbose_name = "Client Work Assign To"
        verbose_name_plural = "Client Work Assign To"

    client_work = models.ForeignKey(ClientWork, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # work_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.client_work.work_name} assigned to {self.user.email}"
    

class Team(models.Model):
    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    team_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name
    

class TeamMember(models.Model):
    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} in {self.team}"


class UserTeamViewPermission(models.Model):
    class Meta:
        verbose_name = "Allow user to view team dasboard"
        verbose_name_plural = "Allow user to view team dasboard"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.user.email} can view {self.team.team_name}"


class AllowUserToViewOtherTeamMemberTask(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)

    def __str__(self):
        return f"Allowed {self.user.first_name} - {self.user.email} to view {self.team_member.user.first_name} - {self.team_member.user.email} task board"

    # UserCanManageOtherTeamMemberTask
class AllowUserToManageOtherTeamMemberTaskBoard(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)

    def __str__(self):
        return f"Allowed {self.user.first_name} - {self.user.email} to manage {self.team_member.user.first_name} - {self.team_member.user.email} task"
