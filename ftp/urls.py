from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "ftp"

urlpatterns = [
    path('', views.Home, name='home'),
    path("reg/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginRequestView.as_view(), name="login-page"),
    #path('login/',views.login_request, name='login-page'),
    path("logout/", views.LogoutRequestView.as_view(), name="logout-page"),
    #path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/<str:pk>", views.Dashboard.as_view(), name="dashboard"),
    #path("upload/<str:pk>", views.upload, name="upload"),
    path("upload/<str:pk>", views.UploadView.as_view(), name="upload"),
    #path("create_dir/",views.create_dir, name="create-dir" ),
    path("create_dir/",views.CreateFolder.as_view(), name="create-dir" ),
    path("display_folder/<str:pk>",views.FolderView.as_view(), name="display_folder-page" ),
    path("profile/",views.ProfileView.as_view(), name="profile" ),
    path('about/', views.about_us, name='about'),
    path("del_folder/<str:pk>",views.DeleteFolder.as_view(), name="delete-folder"),
    path("del_file/<int:pk>",views.DeleteFile.as_view(), name="delete-file"),
]