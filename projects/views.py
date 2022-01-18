from pickle import FALSE
from django import forms
from django.shortcuts import redirect, render
from projects.forms import ProjectForm
from .forms import ModelForm
from django.contrib.auth.decorators import login_required
from projects.models import Project, Tag

# Create your views here.

def projects(request):
    projects = Project.objects.all()
    allTags = Tag.objects.all()
    
    context = {'project':projects,'allTags':allTags}
    return render(request,"projects/projectshome.html",context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    context = {
        'project':projectObj 
    } 
    return render(request,'projects/singleproject.html',context)

@login_required(login_url='login')
def createProject(request):
    profile=request.user.profile
    forms = ProjectForm()
    if request.method == "POST":
        forms = ProjectForm(request.POST,request.FILES)
        if forms.is_valid():
            project=forms.save(commit=FALSE)
            project.owner =profile
            project.save()
            return redirect('account')

    context = {'forms':forms}
    return render(request,'projects/projectform.html',context)

@login_required(login_url='login')
def updateProject(request,pk):
    profile=request.user.profile           # we can ensure by this that only login user can edit the project or 
    project=profile.project_set.get(id=pk) #same  with deletion
    #project = Project.objects.get(id=pk)
    forms = ProjectForm(instance=project)
    if request.method == "POST":
        forms = ProjectForm(request.POST,request.FILES,instance=project)
        if forms.is_valid():
            forms.save()
            return redirect('account')

    context = {'forms':forms}
    return render(request,'projects/projectform.html',context)

@login_required(login_url='login')
def deleteProject(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)  
    #project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('account')
    context = {'object':project}
    return render(request,'delete-template.html',context)
