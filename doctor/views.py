from .models import Patients, InvitesDoctor
from .forms import ShareHealthRecordForm
from internalAuth.models import HealthUser
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test


def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()

# Create your views here.
class IndexViewPatients(UserPassesTestMixin, generic.ListView):
    template_name = 'doctor/index.html'
    context_object_name = 'patients'

    def get_queryset(self):
        """Return all patients of doctor."""
        patients_list = Patients.objects.values_list('user_id', flat=True).filter(doctor=self.request.user)
        return HealthUser.objects.filter(pk__in=patients_list)
    def test_func(self):
        return is_doctor(self.request.user)

class IndexViewAddPatients(UserPassesTestMixin, generic.ListView):
    template_name = 'doctor/add.html'
    context_object_name = 'patients'

    def get_queryset(self):
        """Return all patients of doctor."""
        patients_list = InvitesDoctor.objects.values_list('user_id', flat=True).filter(doctor=self.request.user)
        return HealthUser.objects.filter(pk__in=patients_list)
    def test_func(self):
        return is_doctor(self.request.user)

@user_passes_test(is_doctor)
def AddViewPatient(request, pk):
    if (not Patients.objects.filter(doctor=request.user, patient=pk).exists()):
        user = get_object_or_404(HealthUser, pk=pk)
        relation = Patients(doctor = request.user, user=user)
        relation.save()
        invite = InvitesDoctor.objects.filter(doctor = request.user, user = user)
        invite.delete()
    return HttpResponseRedirect(reverse('doctor:index'))

@user_passes_test(is_doctor)
def DeleteViewPatient(request, pk):
    relation = Patients.objects.filter(doctor=request.user.id, user=pk)
    relation.delete()
    return HttpResponseRedirect(reverse('doctor:index'))

def InviteViewPatient(request, uuidDoctor):
    user = HealthUser.objects.get(uuid = uuidDoctor)
    if not is_doctor(user) or InvitesDoctor.objects.filter(doctor = user, user = request.user).exists():
        return send_400()
    if request.method == 'POST':
        form = ShareHealthRecordForm(request.POST)
        if form.is_valid() and form.cleaned_data['accept_invite']:
            invite = InvitesDoctor(doctor = user, user = request.user)
            invite.save()
            return HttpResponseRedirect(reverse('home'))
    form = ShareHealthRecordForm()
    return render(request, 'share/invite.html', {'form': form, 'uuid': uuidDoctor, 'doctor': user})

# Helper function
def send_400(code = 400):
    response = HttpResponse()
    response.status_code = code              
    return response