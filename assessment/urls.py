from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('sentences/', views.sentence_list, name='sentence_list'),

    path('add-sentence/', views.add_sentence, name='add_sentence'),

    path('sentence/edit/<int:pk>/', views.update_sentence, name='update_sentence'),

    path('sentence/delete/<int:pk>/', views.delete_sentence, name='delete_sentence'),

    path('upload-audio/', views.upload_audio, name='upload_audio'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

]