from django.urls import path
from . import views
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required

app_name = "ftp"

urlpatterns = [
    path('', views.Home, name='home'),
    path("reg/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginRequestView.as_view(),name="login-page"),
    path("logout/", views.LogoutRequestView.as_view(), name="logout-page"),
    path("dashboard/<str:pk>", views.Dashboard.as_view(), name="dashboard"),
    path("upload/<str:pk>", views.UploadView.as_view(), name="upload"),
    path("create_dir/",views.CreateFolder.as_view(), name="create-dir" ),
    path("create_sub_dir/<slug:pk>",views.CreateSubFolder.as_view(), name="create-sub-dir" ),
    path("display_folder/<slug:pk>",views.FolderView.as_view(), name="display_folder-page" ),
    path("profile/",views.ProfileView.as_view(), name="profile" ),
    path('about/', views.about_us, name='about'),
    path("del_folder/<slug:pk>",views.DeleteFolder.as_view(), name="delete-folder"),
    path("del_file/<slug:pk>/",views.DeleteFile.as_view(), name="delete-file"),
    path("all_files/<str:pk>/",views.ViewAllFiles.as_view(), name="view-all-files"),
    path("update_folder/<str:pk>/",views.FolderRenameView.as_view(), name="folder-rename"),
    path("update_file/<str:pk>/",views.FileRenameView.as_view(), name="file-rename"),
    path("change_password/",views.ChangePasswordView.as_view(), name="change-password"),
    path("search/<str:pk>",views.SearchView.as_view(), name="search"),
    path("trash/",views.TrashView.as_view(), name="trash"),
]