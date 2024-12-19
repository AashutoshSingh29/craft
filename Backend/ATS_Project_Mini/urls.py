from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('',views.landing,name='landing'),
    path('login/', views.login,name='login'),
    path('signup/', views.signup, name='signup'),
    path("templates/", views.resume_templates, name="resume_templates"),
    path("beginResume/",views.beginResume, name='beginResume'),
    path("editTemplates/", views.editableTemplates, name="editableTemplates")
]