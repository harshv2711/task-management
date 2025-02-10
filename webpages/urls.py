from django.urls import path
from .import views

urlpatterns = [
    path("", view=views.home, name="webpages-home"),
    path("create-client-work", view=views.createClientWork, name="webpages-create-client-work"),
    path("updated-client-work", view=views.updateClientWork, name="webpages-updated-client-work"),
    path("delete-client-work/<int:client_work_id>/", view=views.deleteClientWork, name="webpages-delete-client-work"),
]