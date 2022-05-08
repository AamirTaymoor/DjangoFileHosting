from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from requests import delete
from .forms import RegisterForm, CreateDirForm, UserLoginForm,FileUpload, RenameDirForm, RenameFileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from ftp.models import Profile, Directory, MyFiles
from django.core.files import File
from django.views.generic import DetailView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, CreateView
from django.urls import reverse_lazy, reverse
from django.utils.functional import lazy
import os

# Create your views here.

def Home(request):
    return render(request, "ftp/home.html")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        # pass
        return render(request, "ftp/register_new.html", context={"register_form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            print(uname)
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            obj = Directory()
            obj.user = request.user
            obj.name = 'Home'
            obj.save()
            # Directory.objects.create()
            return redirect("ftp:login-page")
        messages.error(
            request, "Unsuccessful registration. Invalid data or Username already exists.")
        form = RegisterForm()
        return render(request, "ftp/register_new.html", context={"register_form": form})


class LoginRequestView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, template_name="ftp/login_new.html", context={"login_form": form})
    
    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("ftp:dashboard",pk=user.username)
            else:
                messages.error(request, "Invalid username or password!!!")
                form = AuthenticationForm()
                return render (request, 'ftp/login_new.html', context={"login_form":form})
        else:
            messages.error(request, "Invalid username or password!!!")
            form = AuthenticationForm()
            return render (request, 'ftp/login_new.html', context={"login_form":form})


class LogoutRequestView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("ftp:home")


@method_decorator(login_required, name='dispatch')
class Dashboard(DetailView):
    model = Directory
    template_name = "ftp/dashboard.html"

    def get_queryset(self):
        uid = User.objects.get(username=self.request.user)
        self.queryset = Directory.objects.filter(user=uid)
        #print(self.queryset.filter(user=uid))
        return self.queryset.filter(user=uid)
    
    def get(self, request,pk):
        context = self.get_queryset()
        return render(request,"ftp/dashboard.html", {'context':context})


@method_decorator(login_required, name='dispatch')
class UploadView(FormView):
    form_class = FileUpload
    template_name = 'upload_file.html'  
    success_url = 'ftp/display_folder.html'

    def post(self, request, pk):
        if request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            obj = MyFiles()
            obj.file_name=filename
            print(filename)
            file_extension= os.path.splitext(filename)[1]
            obj.file_ext=file_extension
            obj.file_path = uploaded_file_url
            obj.user = request.user
            data = Directory.objects.filter(name=pk)[0]
            obj.directory = Directory.objects.filter(name=pk)[0]
            obj.save()
        else:
            f = MyFiles.objects.filter(directory=data)
            messages.error(request, "No file selected")
            return redirect('ftp/display_folder.html', {'pk': pk,'d':f})
        f = MyFiles.objects.filter(directory=data)
        return render(request, 'ftp/display_folder.html', {'pk': pk,'d':f})
    
    def get(self, request, pk):
        return render(request, 'ftp/upload_file.html' ,{'pk':pk})


@method_decorator(login_required, name='dispatch')
class CreateFolder(CreateView):
    model=Directory
    fields = ['name']

    def get(self, request):
        form = CreateDirForm()
        return render(request, 'ftp/create_dir.html', {'form':form})
    
    def post(self, request):
        my_form = CreateDirForm(request.POST)
        if my_form.is_valid():
            dname = my_form.cleaned_data['d_name']
            obj = Directory()
            folders = Directory.objects.filter(name=dname)
            print(len(folders))
            if len(folders) == 0:
                obj.user = request.user
                #print("@@@@@@@@@@@@@@@")
                # d = Directory.objects.get()
                obj.parent = None
                obj.name = dname
                obj.save()
            else:
                messages.error(request, "Folder already exists with this name. Try other name")
                #print("&&&&&&&&&&&&&&&&&&&")
                return redirect("ftp:dashboard",pk=request.user.username)
                
        uid = User.objects.get(username=self.request.user)
        context = Directory.objects.filter(user=uid)
        return render(request, 'ftp/dashboard.html',{'context':context})


@method_decorator(login_required, name='dispatch')
class FolderView(View):
    def get(self, request, pk):
        data = Directory.objects.filter(name=pk).filter(user=request.user)
        print('##############')
        fil = MyFiles.objects.filter(directory=data[0])
        print('****************************')
        return render(request, 'ftp/display_folder.html', {'d':fil,'pk':pk})


@method_decorator(login_required, name='dispatch')
class ProfileView(ListView):
    model = Profile

    def get(self,request):
        p = Profile.objects.filter(user=request.user)[0]
        return render(request, 'ftp/profile.html', {'p':p})

@method_decorator(login_required, name='dispatch')
class DeleteFolder(DeleteView):
    model = Directory
    success_url ="/dashboard/pk"

    # def delete(self, request, *args, **kwargs ):
    #     self.object = self.get_object()
    #     success_url = self.get_success_url()
    #     print(self.object.name)
    #     self.object.delete()
    #     return redirect(success_url)


@method_decorator(login_required, name='dispatch')
class DeleteFile(DeleteView):
    model = MyFiles

    def get_success_url(self):
        o_id = self.kwargs.get('pk')
        print(o_id,"idididididididid", self.kwargs['pk'])
        dir = MyFiles.objects.get(id = o_id).directory
        print(dir)
        folder_name = str(dir.name)
        print("folder########", folder_name)
        return reverse_lazy('ftp:display_folder-page', kwargs={'pk':folder_name})
    def delete(self, request, *args, **kwargs ):
        print('*********',kwargs['pk'])
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)

class ViewAllFiles(View):
    def get(self, request, pk):
        all_files = MyFiles.objects.filter(user=request.user)
        print('##############')
        #fil = MyFiles.objects.filter(directory=data[0])
        print('****************************')
        return render(request, 'ftp/all_files.html', {'d':all_files,'pk':pk})

class FolderRenameView(UpdateView):
    model = Directory
    fields = ['name']
    #template_name_suffix = '_update_form'
    # def get(self, request):
    #     form = RenameDirForm()
    #     return render(request, 'ftp/.html', {'form':form})

    def post(self,request, *args, **kwargs):
        my_form = RenameDirForm(request.POST)
        if my_form.is_valid():
            obj=Directory.objects.filter(user=request.user).filter(name=kwargs['pk'])
            new_name = my_form.cleaned_data['d_name']
            all_dirs = Directory.objects.filter(user=request.user).filter(name=new_name)
            print(new_name, all_dirs, obj)
            if len(all_dirs) == 0:
                #Directory.objects.filter(user=request.user).get(name=kwargs['pk']).update(name=new_name)
                obj.update(name=new_name)
                return redirect("ftp:dashboard",pk=request.user.username)
            else:
                messages.error(request, "Folder name already exists. Try other name ")
                return redirect("ftp:dashboard",pk=request.user.username)

class FileRenameView(UpdateView):
    model = MyFiles
    fields = ['file_name']
    #template_name_suffix = '_update_form'
    # def get(self, request):
    #     form = RenameDirForm()
    #     return render(request, 'ftp/.html', {'form':form})

    def post(self,request, *args, **kwargs):
        my_form = RenameFileForm(request.POST)
        print(kwargs['pk'])
        if my_form.is_valid():
            obj=MyFiles.objects.filter(user=request.user).filter(id=kwargs['pk'])
            new_name = my_form.cleaned_data['d_name']
            all_files = MyFiles.objects.filter(user=request.user).filter(file_name=new_name)
            print(new_name, all_files, obj)
            if len(all_files) == 0:
                #Directory.objects.filter(user=request.user).get(name=kwargs['pk']).update(name=new_name)
                obj.update(file_name=new_name)
                dir = MyFiles.objects.get(id=kwargs['pk']).directory
                return redirect("ftp:display_folder-page",pk=dir.name)
            else:
                messages.error(request, "Folder name already exists. Try other name ")
                dir = MyFiles.objects.get(id=kwargs['pk']).directory
                return redirect("ftp:display_folder-page",pk=dir.name)
def about_us(request):
    return render(request, 'ftp/about_us.html')