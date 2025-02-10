from django.shortcuts import render, redirect
from . import models
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives
import threading
# Create your views here.

@login_required(login_url=reverse_lazy('login')) 
def home(request):
    teamList = models.Team.objects.all()
    print(teamList)

    for team in teamList:
        print(team, "[TEAM]")
        team.teamMembers = models.TeamMember.objects.filter(team=team).order_by("user__first_name")
        for teamMember in team.teamMembers:
            print(teamMember, "+++++")
            teamMemberClientWorkList = models.ClientWork.objects.filter(assign_to=teamMember.user).order_by("-id")
            print(teamMemberClientWorkList, "[teamMemberClientWorkList]")
            teamMember.teamMemberClientWorkList = teamMemberClientWorkList
            teamMember.numberOfClientWork = len(teamMember.teamMemberClientWorkList)
    clientList = models.Client.objects.all()
    context = {
        "teamList":teamList,
        "clientList":clientList
    }
    return render(request, "index.html", context)


def createClientWork(request):
    if request.method == "POST":
        workDescription = request.POST.get("workDescription", "").strip()
        team_member_email = request.POST.get("teamMemberEmail", "").strip()
        work_title = request.POST.get("workTitle", "").strip()
        client_id = request.POST.get("client", "").strip()
        proposal_start_date = request.POST.get("proposalStartDate", "").strip()
        # work_start = request.POST.get("workStart", "").strip()
        due_date = request.POST.get("dueDate", "").strip()
        status = request.POST.get("status", "").strip()
        print("post request")
        print(team_member_email,
            work_title, client_id, proposal_start_date, due_date, status)

        clientObj = models.Client.objects.filter(id=client_id).first()
        teamMemberObj = (models.TeamMember.objects.filter(user__email=team_member_email)).first()
        
        clientWorkObj = models.ClientWork(
            client=clientObj, 
            work_name=work_title,
            proposal_date=proposal_start_date,
            
            due_date = due_date,
            assign_to=teamMemberObj.user,
            work_description = workDescription
            )
        clientWorkObj.save()


        # # send mail start
        # email_subject = f"New Task {work_title} assigned by {request.user.first_name}"
        # html_message = render_to_string(
        #     "emails/task-assignment-email.html", 
        #     {
        #         "assignedBy": request.user.first_name, 
        #        "clientWorkObj":clientWorkObj,
        #        "proposal_date":proposal_start_date,
        #        "userFirstName":clientWorkObj.assign_to.first_name.capitalize()
        #     }
        #     )
        # plain_message = strip_tags(html_message)

        # messageObj = EmailMultiAlternatives(
        #     subject=email_subject,
        #     body=plain_message,
        #     from_email=None,
        #     to=[team_member_email]
        # )

        # messageObj.attach_alternative(html_message, "text/html")
        # messageObj.send()
        # # send mail end   

        def send_email_async(clientWorkObj, request, work_title, proposal_start_date, team_member_email, email_type="update"):
            email_templates = {
                "update": "emails/task-assignment-update-email.html",
                "new": "emails/task-assignment-email.html"
            }
        
            subject_prefix = "Updated" if email_type == "update" else "New"
            email_subject = f"{subject_prefix} Task {work_title} assigned by {request.user.first_name}"
            html_message = render_to_string(
                email_templates[email_type], 
                {
                    "assignedBy": request.user.first_name, 
                    "clientWorkObj": clientWorkObj,
                    "proposal_date": proposal_start_date,
                    "userFirstName": clientWorkObj.assign_to.first_name.capitalize()
                }
            )
            plain_message = strip_tags(html_message)

            messageObj = EmailMultiAlternatives(
                subject=email_subject,
                body=plain_message,
                from_email=None,
                to=[team_member_email]
            )

            messageObj.attach_alternative(html_message, "text/html")
            messageObj.send()

        def send_email_in_thread(clientWorkObj, request, work_title, proposal_start_date, team_member_email, email_type="new"):
            email_thread = threading.Thread(target=send_email_async, args=(clientWorkObj, request, work_title, proposal_start_date, team_member_email, email_type))
            email_thread.start()

        send_email_in_thread(
            clientWorkObj, 
            request, 
            clientWorkObj.work_name, 
            clientWorkObj.proposal_date, 
            team_member_email,
            )
        
        return redirect("webpages-home")
   
def updateClientWork(request):
    if request.method == "POST":
        clientWorkId = request.POST.get("clientWorkId", "").strip()
        workDescription = request.POST.get("workDescription", "").strip()
        team_member_email = request.POST.get("teamMemberEmail", "").strip()
        print(team_member_email, "))))))))))))))")
        work_title = request.POST.get("workTitle", "").strip()
        client_id = request.POST.get("client", "").strip()
        proposal_start_date = request.POST.get("proposalStartDate", "").strip()
        work_start = request.POST.get("workStart", "").strip()
        due_date = request.POST.get("dueDate", "").strip()
        status = request.POST.get("status", "").strip()
        print("post request")
        print(team_member_email,
            work_title, client_id, proposal_start_date, work_start, due_date, status)


        clientWorkObj = models.ClientWork.objects.get(id=clientWorkId)
        clientWorkObj.work_name = work_title
        clientWorkObj.proposal_date = proposal_start_date
        clientWorkObj.work_started_at = work_start
        clientWorkObj.due_date = due_date
        clientWorkObj.client = models.Client.objects.get(id=client_id)
        clientWorkObj.status =status
        clientWorkObj.work_description = workDescription
        clientWorkObj.save()
        print(clientWorkObj, "+++++++++++++++++++++++")


        # # send mail start
        # email_subject = f"Updated Task {work_title} assigned by {request.user.first_name}"
        # html_message = render_to_string(
        #     "emails/task-assignment-update-email.html", 
        #     {
        #         "assignedBy": request.user.first_name, 
        #        "clientWorkObj":clientWorkObj,
        #        "proposal_date":proposal_start_date,
        #        "userFirstName":clientWorkObj.assign_to.first_name.capitalize()
        #     }
        #     )
        # plain_message = strip_tags(html_message)

        # messageObj = EmailMultiAlternatives(
        #     subject=email_subject,
        #     body=plain_message,
        #     from_email=None,
        #     to=[team_member_email]
        # )

        # messageObj.attach_alternative(html_message, "text/html")
        # messageObj.send()
        # # send mail end

        # threading
        def send_email_async(clientWorkObj, request, work_title, proposal_start_date, team_member_email, email_type="update"):
            email_templates = {
                "update": "emails/task-assignment-update-email.html",
                "new": "emails/task-assignment-email.html"
            }
        
            subject_prefix = "Updated" if email_type == "update" else "New"
            email_subject = f"{subject_prefix} Task {work_title} assigned by {request.user.first_name}"
            html_message = render_to_string(
                email_templates[email_type], 
                {
                    "assignedBy": request.user.first_name, 
                    "clientWorkObj": clientWorkObj,
                    "proposal_date": proposal_start_date,
                    "userFirstName": clientWorkObj.assign_to.first_name.capitalize()
                }
            )
            plain_message = strip_tags(html_message)

            messageObj = EmailMultiAlternatives(
                subject=email_subject,
                body=plain_message,
                from_email=None,
                to=[team_member_email]
            )

            messageObj.attach_alternative(html_message, "text/html")
            messageObj.send()

        def send_email_in_thread(clientWorkObj, request, work_title, proposal_start_date, team_member_email, email_type="update"):
            email_thread = threading.Thread(target=send_email_async, args=(clientWorkObj, request, work_title, proposal_start_date, team_member_email, email_type))
            email_thread.start()

        send_email_in_thread(
            clientWorkObj, 
            request, 
            clientWorkObj.work_name, 
            clientWorkObj.proposal_date, 
            team_member_email,
            )
        
        
    return redirect("webpages-home")



def deleteClientWork(request, client_work_id):
    clientWorkObj = models.ClientWork.objects.get(id=client_work_id)
    clientWorkObj.delete()
    
    # send mail start
    # email_subject = f"Deleted Task {clientWorkObj.work_name} assigned by {request.user.first_name}"
    # html_message = render_to_string(
    #     "emails/task-assignment-delete-email.html", {
    #     "assignedBy": request.user.first_name, 
    #     "clientWorkObj":clientWorkObj,
    #     "proposal_date":clientWorkObj.proposal_date,
    #     "userFirstName":clientWorkObj.assign_to.first_name.capitalize()
    #     }
    # )
    # plain_message = strip_tags(html_message)

    # messageObj = EmailMultiAlternatives(
    #     subject=email_subject,
    #     body=plain_message,
    #     from_email=None,
    #     to=[clientWorkObj.assign_to.email]
    # )

    # messageObj.attach_alternative(html_message, "text/html")
    # messageObj.send()
    # send mail end

    # threading
    def send_email_async(clientWorkObj, request):
        email_subject = f"Deleted Task {clientWorkObj.work_name} assigned by {request.user.first_name}"
        html_message = render_to_string(
            "emails/task-assignment-delete-email.html", {
                "assignedBy": request.user.first_name,
                "clientWorkObj": clientWorkObj,
                "proposal_date": clientWorkObj.proposal_date,
                "userFirstName": clientWorkObj.assign_to.first_name.capitalize()
            }
        )
        plain_message = strip_tags(html_message)

        messageObj = EmailMultiAlternatives(
            subject=email_subject,
            body=plain_message,
            from_email=None,
            to=[clientWorkObj.assign_to.email]
        )

        messageObj.attach_alternative(html_message, "text/html")
        messageObj.send()

    def send_email_in_thread(clientWorkObj, request):
        email_thread = threading.Thread(target=send_email_async, args=(clientWorkObj, request))
        email_thread.start()

    send_email_in_thread(clientWorkObj, request)
    
    print(clientWorkObj.work_name, "________________")
    return redirect("webpages-home")
