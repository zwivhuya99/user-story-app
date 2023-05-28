from django.urls import path
from django.contrib.auth.decorators import login_required
#from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    #The app view should only be accessed after a succesful login
    path('newUser/signup/',views.signup, name='signup'),
    path('newUser/signin/',views.signin, name='signin'),
    path('newUser/signout/',views.signout, name='signout'),
    path('admin/', login_required(views.app), name='app'),
    path('item/<todo_id>/edit/', views.edit_item, name='edit_item'),
    path('users/',views.user_list, name='user_list'),
    path('users/delete/<user_id>/', views.deleteUser, name='deleteUser'),
    path('users/makeAdmin/<user_id>/',views.makeAdmin, name='makeAdmin'),
    path('admin/add/', views.addTodo, name='add'),  
    path('admin/complete/<todo_id>/', views.completeTodo, name='complete'), 
    path('admin/deletecomplete/', views.deleteCompleted, name='deletecomplete'),  
    path('admin/deleteall/', views.deleteAll, name='deleteall'),  
    path('admin/deleteItem/<todo_id>/', views.deleleteItem, name='deleleteItem'),  
    path('admin/reAddItem/<todo_id>/', views.reAddItem, name='reAddItem'),

]
