from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from requests import delete
from .forms import RegisterForm, CreateDirForm, UserLoginForm,FileUpload, RenameDirForm, RenameFileForm, ChangePasswordForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from ftp.models import  Directory, MyFiles, Profile
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
    if request.user.is_authenticated:
        return redirect("ftp:dashboard",pk=request.user.username)

    return redirect("ftp:login-page")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        # pass
        return render(request, "ftp/register_new.html", context={"register_form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("ftp:login-page")
        messages.warning(
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
                messages.warning(request, "Invalid username or password!!!")
                form = AuthenticationForm()
                return render (request, 'ftp/login_new.html', context={"login_form":form})
        else:
            messages.warning(request, "Invalid username or password!!!")
            form = UserLoginForm()
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
        self.queryset = Directory.objects.filter(user=uid).filter(is_deleted=False).filter(parent=None)
        return self.queryset

    def get(self, request,pk):
        context = self.get_queryset()
        return render(request,"ftp/dashboard.html", {'context':context,})


@method_decorator(login_required, name='dispatch')
class UploadView(FormView):
    form_class = FileUpload
    template_name = 'upload_file.html'
    success_url = 'ftp/display_folder.html'

    def post(self, request, pk):
        current_dir = Directory.objects.get(pk=pk)
        if request.FILES.get('myfile'):
            myfile = request.FILES.get('myfile')
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            obj = MyFiles()
            obj.file_name=filename
            file_extension= os.path.splitext(filename)[1]
            obj.file_ext=file_extension
            obj.file_path = uploaded_file_url
            obj.user = request.user
            obj.directory = current_dir
            obj.save()
            messages.success(request, "File uploaded successfully")
        else:
            f1 = MyFiles.objects.filter(directory=current_dir)
            messages.warning(request, "No file selected")
            return render(request, 'ftp/display_folder.html', {'pk': pk,'d':f1})
        f = MyFiles.objects.filter(directory=current_dir)
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
            if not self.if_folder_name_exists(dname):
                obj.user = request.user
                # obj.parent = pk
                obj.name = dname
                obj.save()
                messages.success(request, "Folder created successfully")
            else:
                messages.warning(request, "Folder already exists with this name. Try other name")
                # return redirect("ftp:dashboard",pk=pk)
                return redirect("ftp:dashboard",pk=request.user.username)


        uid = User.objects.get(username=self.request.user)
        context = Directory.objects.filter(user=uid).filter(is_deleted=False)
        return render(request, 'ftp/dashboard.html', {'context':context})

    def if_folder_name_exists(self, name):
        no_of_folders = Directory.objects.filter(name=name,is_deleted=False, user=self.request.user).count()
        if no_of_folders == 0:
            return False
        return True 
@method_decorator(login_required, name='dispatch')
class CreateSubFolder(CreateView):
    model=Directory
    fields = ['name']
    
    def get(self, request):
        form = CreateDirForm()
        return render(request, 'ftp/create_dir.html', {'form':form})

    def post(self, request, pk):
        my_form = CreateDirForm(request.POST)
        if my_form.is_valid():
            dname = my_form.cleaned_data['d_name']
            obj = Directory()
            if not self.if_folder_name_exists(dname):
                obj.user = request.user
                obj.parent = Directory.objects.get(pk=pk)
                obj.name = dname
                obj.save()
                messages.success(request, "Folder created successfully")
            else:
                messages.warning(request, "Folder already exists with this name. Try other name")
                # return redirect("ftp:dashboard",pk=pk)
                return redirect("ftp:display_folder-page",pk=pk)


        uid = User.objects.get(username=self.request.user)
        context = Directory.objects.filter(user=uid).filter(is_deleted=False)
        return render(request, 'ftp/dashboard.html', {'context':context})

    def if_folder_name_exists(self, name):
        no_of_folders = Directory.objects.filter(name=name,is_deleted=False, user=self.request.user).count()
        if no_of_folders == 0:
            return False
        return True
    
@method_decorator(login_required, name='dispatch')
class FolderView(View):
    def get(self, request, pk):
        directory = Directory.objects.get(pk=pk)
        # data = Directory.objects.filter(pk=pk).filter(user=request.user).filter(is_deleted='False').filter(parent=pk)
        fil = MyFiles.objects.filter(directory=directory).filter(is_deleted=False)
        sub_dirs = Directory.objects.filter(user=self.request.user, is_deleted=False, parent=pk)
        return render(request, 'ftp/display_folder.html', {'d':fil,'sub_dirs':sub_dirs, 'pk':pk})


@method_decorator(login_required, name='dispatch')
class ProfileView(ListView):
    model = Profile

    def get(self,request):
        p = Profile.objects.get(user=request.user)
        return render(request, 'ftp/profile.html', {'p':p})

@method_decorator(login_required, name='dispatch')
class DeleteFolder(DeleteView):
    model = Directory

    def get_success_url(self):
        u = self.request.user.username
        messages.info(self.request, "Folder deleted!!")
        return reverse_lazy('ftp:dashboard', kwargs={'pk':u})

    # def delete(self, request, *args, **kwargs ):
    #     self.object = self.get_object()
    #     success_url = self.get_success_url()
    #     print(self.object.name)
    #     #self.object.delete()
    #     self.object.is_deleted = True
    #     print("@@@@@@@@@@@@@@@")
    #     return redirect(success_url)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_deleted = True
        r_files = MyFiles.objects.filter(user=request.user).filter(directory= self.object)
        r_files.update(is_deleted=True)
        self.object.save()
        return redirect(success_url)

@method_decorator(login_required, name='dispatch')
class DeleteFile(DeleteView):
    model = MyFiles

    def get_success_url(self):
        o_id = self.kwargs.get('pk')
        dir = MyFiles.objects.get(id = o_id).directory
        folder_name = str(dir.name)
        messages.info(self.request, "File deleted!!")
        return reverse_lazy('ftp:display_folder-page', kwargs={'pk':folder_name})

    # def delete(self, request, *args, **kwargs ):
    #     print('*********',kwargs['pk'])
    #     self.object = self.get_object()
    #     success_url = self.get_success_url()
    #     self.object.delete()
    #     return redirect(success_url)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url= self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return redirect(success_url)

@method_decorator(login_required, name='dispatch')
class ViewAllFiles(View):
    def get(self, request, pk):
        all_files = MyFiles.objects.filter(user=request.user).filter(is_deleted=False)
        return render(request, 'ftp/all_files.html', {'d':all_files,'pk':pk})

@method_decorator(login_required, name='dispatch')
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
            related_files = MyFiles.objects.filter(user= request.user).filter(directory=obj[0])

            if len(all_dirs) == 0:
                #Directory.objects.filter(user=request.user).get(name=kwargs['pk']).update(name=new_name)
                if len(related_files) != 0:
                    new_dir = Directory(user=request.user, name=new_name, parent=None)
                    new_dir.save()
                    related_files.update(directory=new_dir)
                    for i in obj:
                        obj.delete()
                else:
                    obj.update(name=new_name)
                messages.success(request, "Folder renamed successfully")
                return redirect("ftp:dashboard",pk=request.user.username)
            else:
                messages.warning(request, "Folder name already exists. Try other name ")
                return redirect("ftp:dashboard",pk=request.user.username)

@method_decorator(login_required, name='dispatch')
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
                messages.success(request, "File renamed successfully")
                return redirect("ftp:display_folder-page",pk=dir.name)
            else:
                messages.warning(request, "Filename already exists. Try other name ")
                dir = MyFiles.objects.get(id=kwargs['pk']).directory
                return redirect("ftp:display_folder-page",pk=dir.name)

class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        my_form = ChangePasswordForm()
        return render(request, 'ftp/password_change.html',context= {"myform":my_form})
    def post(self, request,*args, **kwargs):
        my_form = ChangePasswordForm(request.POST)
        if my_form.is_valid():
            uname = my_form.cleaned_data['user_name']
            new_password = my_form.cleaned_data['pass_word']
            try:
                u = User.objects.get(username = uname)
                u.set_password(new_password)
                u.save()
                messages.success(request, "Password changed!!")
                return redirect("ftp:login-page")
            except :
                messages.warning(request, "Username does not exist!!! Enter registered Username.")
                return redirect("ftp:change-password")

@method_decorator(login_required, name='dispatch')
class SearchView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ftp/search_results.html')

    def post(self, request, *args, **kwargs):
        searched = request.POST.get('searched')
        pk = kwargs['pk']
        if len(searched) != 0:
            print('nothing to search')
            #folders = Directory.objects.filter(user=request.user).filter(name__icontains=searched)
            #print(folders)
            files = MyFiles.objects.filter(user=request.user).filter(file_name__icontains=searched)
            #print(files)
            return render (request, 'ftp/all_files.html', {'d':files,'pk':pk})
        else:
            messages.warning(request, "Enter some text to search")
            return redirect("ftp:dashboard", pk=request.user.username)

class TrashView(View):
    def get(self, request, *args, **kwargs):
        d = Directory.objects.filter(user= request.user).filter(is_deleted ='True')
        f = MyFiles.objects.filter(user=request.user).filter(is_deleted='True')
        return render(request, 'ftp/trash.html', {'d':d, 'f':f })

def about_us(request):
    return render(request, 'ftp/about_us.html')