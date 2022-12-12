from .models import HealthRecordFolder, HealthRecord, HealthRecordMedia
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import HealthRecordFolderForm, HealthRecordForm, ShareHealthRecordForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from doctor.models import ShareRecordDoctor, Patients
from internalAuth.models import HealthUser

from django.contrib.auth.decorators import user_passes_test
from doctor.views import is_doctor, send_400

# Folder
class IndexViewFolder(LoginRequiredMixin, generic.ListView):
    template_name = 'folder/index.html'
    context_object_name = 'folders'

    def get_queryset(self):
        """Return all health record folders."""
        return HealthRecordFolder.objects.filter(owner=self.request.user.id).filter(parent=None)

def CreateViewFolder(request):
    if request.method == 'POST':
        form = HealthRecordFolderForm(request.POST)
        if form.is_valid():                       
            folder = HealthRecordFolder(title = form.cleaned_data['title'], description = form.cleaned_data['description'], owner = request.user)
            folder.save()
            return HttpResponseRedirect(reverse('health:indexRecord', args=[folder.pk]))
    else:
        form = HealthRecordFolderForm()
    return render(request, 'folder/create.html', {'form': form})

def CreateViewSubFolder(request, pk):
    folder = get_object_or_404(HealthRecordFolder, pk=pk)
    if folder.owner != request.user:
        return send_400()
    if request.method == 'POST':
        form = HealthRecordFolderForm(request.POST)
        if form.is_valid():                       
            folder = HealthRecordFolder(title = form.cleaned_data['title'], description = form.cleaned_data['description'], owner = request.user, parent = folder)
            folder.save()
            return HttpResponseRedirect(reverse('health:indexRecord', args=[folder.pk]))
    else:
        form = HealthRecordFolderForm()
    return render(request, 'folder/createSub.html', {'form': form, 'folder': folder, 'breadcrumb': getBreadCrumb('create subfolder', folder)})

def UpdateViewFolder(request, pk):
    folder = get_object_or_404(HealthRecordFolder, pk=pk)
    if folder.owner != request.user:
        return send_400()
    if request.method == 'POST':
        form = HealthRecordFolderForm(request.POST)
        if form.is_valid():                       
            folder.title = form.cleaned_data['title']
            folder.description = form.cleaned_data['description']
            folder.save()
            return HttpResponseRedirect(reverse('health:indexRecord', args=[folder.pk]))
    else:        
        form = HealthRecordFolderForm(instance=folder)
    return render(request, 'folder/update.html', {'form': form, 'folder': folder})

def DeleteViewFolder(request, pk):
    folder = get_object_or_404(HealthRecordFolder, pk=pk)
    if folder.owner == request.user:
        folder.delete()
        return HttpResponseRedirect(reverse('health:index'))          
    return send_400()

# Record
def IndexViewRecord(request, pkFolder):
    folder = get_object_or_404(HealthRecordFolder, pk=pkFolder)
    if folder.owner != request.user:
        return send_400()
    subfolders = HealthRecordFolder.objects.filter(owner = request.user).filter(parent = folder)
    records = HealthRecord.objects.filter(folder=folder.id)
    return render(request, 'record/index.html', {'folder': folder, 'records': records, 'subfolders': subfolders, 'breadcrumb': getBreadCrumb(folder, folder.parent)})

def CreateViewRecord(request, pkFolder):
    folder = get_object_or_404(HealthRecordFolder, pk=pkFolder)
    if folder.owner != request.user:
        return send_400() 
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        if form.is_valid():                   
            record = HealthRecord(title = form.cleaned_data['title'], description = form.cleaned_data['description'], folder = folder)
            record.save()
            for file in files:
                media = HealthRecordMedia(record=record, media=file)
                media.save()
            return HttpResponseRedirect(reverse('health:updateRecord', args=[record.pk]))
    else:
        form = HealthRecordForm()
    return render(request, 'record/create.html', {'form': form, 'folder': folder, 'breadcrumb': getBreadCrumb({"title": 'create'}, folder)})

def UpdateViewRecord(request, pkRecord):
    record = get_object_or_404(HealthRecord, pk=pkRecord)
    if record.folder.owner != request.user:
        return send_400()    
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        if form.is_valid():               
            record.title = form.cleaned_data['title']
            record.description = form.cleaned_data['description']
            record.save()
            for file in files:
                media = HealthRecordMedia(record=record, media=file)
                media.save()
            return HttpResponseRedirect(reverse('health:updateRecord', args=[record.pk]))
    else:
        form = HealthRecordForm(instance=record)
        files = HealthRecordMedia.objects.filter(record=record)
    return render(request, 'record/update.html', {'form': form, 'record': record, 'folder': record.folder, 'files': files, 'breadcrumb': getBreadCrumb(record, record.folder)})

def DeleteViewMedia(request, pkRecord, pkMedia):
    record = get_object_or_404(HealthRecord, pk=pkRecord)
    if record.folder.owner == request.user:
                
        media = HealthRecordMedia.objects.filter(pk=pkMedia, record=record)
        media.delete()
        return HttpResponseRedirect(reverse('health:updateRecord', args=[pkRecord]))          
    return send_400()

def DeleteViewRecord(request, pkRecord):
    record = get_object_or_404(HealthRecord, pk=pkRecord)
    if record.folder.owner == request.user:
        record.delete()
        return HttpResponseRedirect(reverse('health:indexRecord', args=[record.folder.pk]))          
    return send_400()

# Share
def ShareViewRecord(request, pkRecord):
    record = get_object_or_404(HealthRecord, pk=pkRecord)
    if record.folder.owner != request.user:
        return send_400()    
    if request.method == 'POST':
        form = ShareHealthRecordForm(request.POST)
        if form.data['doctor']:    
            patient = Patients.objects.get(user = request.user, doctor = form.data['doctor'])     
            if not ShareRecordDoctor.objects.filter(patient = patient, record = record).exists():
                share = ShareRecordDoctor(patient = patient, record = record)
                share.save()
            return HttpResponseRedirect(reverse('health:indexRecord', args=[record.folder.pk]))
        form.is_valid()
    else:
        form = ShareHealthRecordForm()
        reference = Patients.objects.values_list('doctor_id', flat=True).filter(user = request.user)
        form.fields['doctor'].choices = HealthUser.objects.values_list('id', 'username').filter(pk__in=reference)
    return render(request, 'share/add.html', {'form': form, 'record': record, 'folder': record.folder, 'breadcrumb': getBreadCrumb(record, record.folder), 'id': record.pk})

# Doctor
@user_passes_test(is_doctor)
def IndexViewPatient(request, pkUser):
    patient = Patients.objects.get(user=pkUser, doctor=request.user)
    shared_list = ShareRecordDoctor.objects.values_list('record_id').filter(patient=patient)
    records = HealthRecord.objects.filter(pk__in = shared_list)
    return render(request, 'share/index.html', {'records': records, 'id': pkUser})

@user_passes_test(is_doctor)
def IndexViewPatientRecord(request, pkUser, pkRecord):
    patient = Patients.objects.get(user=pkUser, doctor=request.user)
    shared = ShareRecordDoctor.objects.get(patient=patient, record=pkRecord)
    record = HealthRecord.objects.get(pk = shared.record.pk)    
    files = HealthRecordMedia.objects.filter(record=record)
    return render(request, 'share/detail.html', {'record': record, 'files': files})

@user_passes_test(is_doctor)
def CreateViewPatientRecord(request, pkUser):
    patient = Patients.objects.get(user=pkUser, doctor=request.user)
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            title = "Doctor Records: " + request.user.username
            folder = HealthRecordFolder.objects.filter(owner = patient.user, title = title)
            if len(folder) == 0:
                folder = HealthRecordFolder(title = title, description = "Records created by your doctor: " + request.user.username, owner = patient.user)
                folder.save()  
            else:
                folder = folder[0] 
            record = HealthRecord(title = form.cleaned_data['title'], description = form.cleaned_data['description'], folder = folder)
            record.save()
            for file in files:
                media = HealthRecordMedia(record=record, media=file)
                media.save()
                
            if not ShareRecordDoctor.objects.filter(patient = patient, record = record).exists():
                share = ShareRecordDoctor(patient = patient, record = record)
                share.save()

            return HttpResponseRedirect(reverse('health:indexPatient', args=[pkUser]))
    else:
        form = HealthRecordForm()
    return render(request, 'share/create.html', {'form': form, 'id': pkUser})



# Helper Function
def getBreadCrumb(item, parent=None):
    breadcrumb = list()
    breadcrumb.append(item)
    while (parent is not None):
        breadcrumb.append(parent)
        parent = parent.parent
    breadcrumb.reverse()
    return breadcrumb