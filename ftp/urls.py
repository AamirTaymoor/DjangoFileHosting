from django.urls import path
from . import views

app_name = "ftp"

urlpatterns = [
    path('', views.Home, name='home'),
    path("reg/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginRequestView.as_view(), name="login-page"),
    #path('login/',views.login_request, name='login-page'),
    path("logout/", views.LogoutRequestView.as_view(), name="logout-page"),
    path("dashboard/", views.dashboard, name="dashboard"),
    #path("upload/<str:pk>", views.upload, name="upload"),
    path("upload/<str:pk>", views.Upload.as_view(), name="upload"),
    path("create_dir/",views.create_dir, name="create-dir" ),
    path("display_folder/<str:pk>",views.folder_view, name="display_folder-page" ),
]