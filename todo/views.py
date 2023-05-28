from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
#importing models
from django.contrib.auth.models import User
from .models import Todo
from .forms import NewTodoForm

#for normal USERS
def signup(request):
    # Check if the user is already authenticated, redirect to admin:index
    if request.user.is_authenticated:
        return render(request,'todo/home.html')
    # Handle POST request
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the form data and create a new user
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            #form = AuthenticationForm()
            return render(request,'todo/registered.html')  # Render to registred page after successful signup
        else:
            # If the form is not valid, render the signup page with the form and error messages
            return render(request, 'todo/signup.html', {'form': form})
    else:
        # Handle GET request
        form = UserCreationForm()
        # Render the signup page with an empty form
        return render(request, 'todo/signup.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return render(request,'todo/home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request,'todo/home.html') #home
        else:
            msg = 'Wrong Password or Username, Please try again'
            form = AuthenticationForm(request.POST)
            return render(request, 'todo/login.html', {'form': form, 'msg': msg, 'user': user})
    else:
        form = AuthenticationForm()
        return render(request, 'todo/login.html', {'form': form})
    
def signout(request):
    logout(request)
    return redirect('signin')

#ADMINS
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
    todo.complete = False 
    todo.save() #update the object in the database
    return redirect('app')

def edit_item(request, todo_id=None):
    #getting the todo item frim the database using get_object_or_404 
    #which returns the todo item if it exists, or raises a 404 error if it does not exist in the database
    todo = get_object_or_404(Todo, pk=todo_id)
 
    if request.method == 'POST':
        form = NewTodoForm(request.POST, instance=todo)
        if form.is_valid():
            #Save the updated todo item
            form.save()
            #after saving redirect to the app
            return redirect('app')
    else:
        form = NewTodoForm(instance=todo)

    return render(request, 'todo/edit_item.html', {'form': form, 'todo': todo})


#User management Model
def user_list(request):
    users = User.objects.all()
    return render(request, 'todo/users.html', {'users': users})

def deleteUser(request, user_id):
    user = User.objects.filter(pk=user_id)
    user.delete()
    return redirect('user_list')

def makeAdmin(request,user_id) :
    user = User.objects.get(pk=user_id)
    user.is_staff = True
    user.is_superuser = True
    user.save() #update the object in the database
    return redirect('user_list')

#request, HTTP request object that contains the user's input and other information

