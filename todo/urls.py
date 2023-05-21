from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views #password reset viewa
from . import views

urlpatterns = [
    #The app view should only be accessed after a succesful login
    path('', login_required(views.app), name='app'),
    path('add/', views.addTodo, name='add'),  
    path('complete/<todo_id>/', views.completeTodo, name='complete'), 
    path('deletecomplete/', views.deleteCompleted, name='deletecomplete'),  
    path('deleteall/', views.deleteAll, name='deleteall'),  
    path('deleteItem/<todo_id>/', views.deleleteItem, name='deleleteItem'),  
    path('reAddItem/<todo_id>/', views.reAddItem, name='reAddItem'),

    #django Url patterns for password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
