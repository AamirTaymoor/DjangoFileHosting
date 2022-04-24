from contextlib import nullcontext
from re import U
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from requests import request
from .forms import RegisterForm, CreateDirForm, UserLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from ftp.models import Profile, Directory, MyFiles
from django.core.files import File
# Create your views here.
#"<a href="https://www.flaticon.com/free-icons/folder" title="folder icons">Folder icons created by Kiranshastry - Flaticon</a>"

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
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            obj = Directory()
            obj.user = request.user
            obj.name = 'Home'+str(request.user)
            obj.save()
            # Directory.objects.create()
            return redirect("ftp:login-page")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
        form = RegisterForm()
        return render(request, "ftp/register_new.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("ftp:dashboard")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, template_name="ftp/login_new.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("ftp:home")


@login_required(login_url='login-page')
def dashboard(request):
    directories = Directory.objects.all().filter(user=request.user)
    print(directories)
    files = MyFiles.objects.all().filter(user=request.user)
    print(files)
    dirs = []
    my_files = []
    for f in files:
        my_files.append(f.file_path)
    for d in directories:
        dirs.append(d)
        files = MyFiles.objects.all().filter(directory=d)
        try:
            #my_files = []
            for f in files:
                my_files.append(f.file_path)
        except MyFiles.DoesNotExist:
            pass
    
        context = {'dir': dirs, 'fil':my_files}
    return render(request, "ftp/dashboard.html", context)


"""@login_required(login_url='login-page')
def upload_file(request):
    return render(request, 'ftp/upload_file.html', )"""


@login_required(login_url='login-page')
def upload(request, pk):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        obj = MyFiles()
        obj.file_path = uploaded_file_url
        obj.user = request.user
        data = Directory.objects.filter(name=pk)[0]
        obj.directory = Directory.objects.filter(name=pk)[0]
        obj.save()
        f = MyFiles.objects.filter(user=request.user)
        myfiles = []
        for i in f:
            myfiles.append(i.file_path)
        return render(request, 'ftp/dashboard.html', {'myfiles': myfiles})
    return render(request, 'ftp/upload_file.html' ,{'pk':pk})


"""@login_required(login_url='login-page')
def create_dir(request):
    if request.method == 'POST':
        d_name = request.POST['dname']
        obj = Directory()
        obj.user = request.user.username
        #d = Directory.objects.get()
        #obj.parent = 
        obj.name = d_name
        obj.save()
    else:
        return render(request, 'ftp/create_dir.html')
    return render(request,'ftp/dashboard.html' )"""


@login_required(login_url='login-page')
def create_dir(request):
    if request.method == "POST":
        # Get the posted form
        my_user_form = CreateDirForm(request.POST)
        #dname=''
        if my_user_form.is_valid():
            # do anything here
            dname = my_user_form.cleaned_data['d_name']
            print(dname)
            obj = Directory()
            #u = str(request.user.username)
            obj.user = request.user
            print(request.user)
            # d = Directory.objects.get()
            obj.parent = None
            obj.name = dname
            obj.save()
    else:
        my_user_form = CreateDirForm()
        return render(request, 'ftp/create_dir.html', {'form':my_user_form})

    return render(request, 'ftp/dashboard.html')

@login_required(login_url='login-page')
def folder_view(request, pk):
    data = Directory.objects.filter(name=pk)
    fil = MyFiles.objects.filter(directory=data[0])
    return render(request, 'ftp/display_folder.html', {'d':fil,'pk':pk})


