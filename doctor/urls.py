from django.urls import path, include
from . import views

app_name = "doctor"
urlpatterns = [
    path('patients', views.IndexViewPatients.as_view(), name='index'),
    path('patients/add', views.IndexViewAddPatients.as_view(), name='addIndex'),
    path('patients/add/<int:pk>', views.AddViewPatient, name='add'),
    path('patients/delete/<int:pk>', views.DeleteViewPatient, name='delete'),

    path('invite/<uuid:uuidDoctor>', views.InviteViewPatient, name='invite'),
]