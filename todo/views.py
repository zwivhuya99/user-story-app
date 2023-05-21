from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
#from django.contrib.auth.views import LoginView
#from django.contrib.auth import login as auth_login
#from django.urls import reverse_lazy
#from .templates import admin
#from django.http import HttpResponseRedirect
from .models import Todo
from .forms import NewTodoForm

'''def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login.html')  # Redirect to the home page after successful login
    else:
        form = AuthenticationForm() 
    return render(request, 'todo/login.html', {'form': form})'''

def app(request): #render the template and pass the required data
    todo_list = Todo.objects.order_by('id')
    newtodoform = NewTodoForm()
    context = {'todo_list' : todo_list, 'form' : newtodoform} #dict with data required in the ui
    return render(request, 'todo/app.html', context)

@require_POST
def addTodo(request): #Post. posting a form/save to the data base 
    newtodoform = NewTodoForm(request.POST)
    if newtodoform.is_valid():
        newtodoform.save()
    return redirect('app')

def completeTodo(request, todo_id): #get
    todo = Todo.objects.get(pk=todo_id)
    todo.complete = True
    todo.save()
    return redirect('app')

def deleteCompleted(request): #delete
    Todo.objects.filter(complete__exact=True).delete()
    return redirect('app')

def deleteAll(request): #delete
    Todo.objects.all().delete()
    return redirect('app')

def deleleteItem(request, todo_id): #delete
    Todo.objects.filter(pk=todo_id).delete()
    return redirect('app')

def reAddItem(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.complete = False #is now back to not completed
    todo.save() #update the object in the database
    return redirect('app')

