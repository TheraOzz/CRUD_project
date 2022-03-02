from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Trainer, Moderator
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    return render(request, "trainerapp/home.html")


def login_user(request):
    myErrors = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username , password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            if not username:
                myErrors["empty_username"] = "please enter username"
            elif not password:
                myErrors["empty_password"] = "please enter password"
            elif user is None:
                myErrors["invalid"] = "Username and password do not match"
    return render (request, "trainerapp/login.html", myErrors)

def logout_user(request):
    logout(request)
    return redirect("home")


def signup_user(request):
    if request.method == "POST":
        # form validation, save new user object, authenticate and login user
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            modList = request.POST.getlist("make_moderator")
            if modList:
                moderator = Moderator(user=request.user, is_moderator=True)
                moderator.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "trainerapp/signup.html", {"form": form})


def create(request):
    myErrors = {}
    if request.method == "POST":
        trainerCreate = Trainer()
        trainerCreate.firstName = request.POST["firstName"]
        trainerCreate.lastName = request.POST["lastName"]
        trainerCreate.subject = request.POST["subject"]
        if not trainerCreate.firstName.isalpha() or not trainerCreate.firstName:
            myErrors["empty_firstName"] = "please enter valid firstName"
        elif not trainerCreate.lastName.isalpha() or not trainerCreate.lastName:
            myErrors["empty_lastName"] = "please enter valid lastName"
        elif not trainerCreate.subject:
            myErrors["empty_subject"] = "please enter valid subject"
        elif trainerCreate is not None:
            trainerCreate.save()
            return redirect("read")
    return render(request, "trainerapp/create.html", myErrors)


def read(request):
    allTrainers = Trainer.objects.order_by("id")
    context = {"allTrainers": allTrainers}
    return render(request, "trainerapp/read.html", context)


def edit(request):
    myErrors={}
    try:
        if request.user.moderator.is_moderator:
            allTrainers = Trainer.objects.order_by("id")
            context = {"allTrainers": allTrainers}
        return render(request, "trainerapp/edit.html", context)
    except ObjectDoesNotExist:
        myErrors["no_moderator"] = "only moderators can edit trainers!"
        return render(request, "trainerapp/edit.html", myErrors)
    except AttributeError:
        myErrors["no_moderator"] = "only moderators can edit trainers!"
        return render(request, "trainerapp/edit.html", myErrors)


def update(request, id):
    myErrors = {}
    trainerUpdate = Trainer.objects.get(id=id)
    context = {"trainer": trainerUpdate}
    if request.method == "POST":
        trainerUpdate.firstName = request.POST["firstName"]
        trainerUpdate.lastName = request.POST["lastName"]
        trainerUpdate.subject = request.POST["subject"]
        if not trainerUpdate.firstName.isalpha() or not trainerUpdate.firstName:
            myErrors["empty_firstName"] = "please enter valid firstName"
        elif not trainerUpdate.lastName.isalpha() or not trainerUpdate.lastName:
            myErrors["empty_lastName"] = "please enter valid lastName"
        elif not trainerUpdate.subject:
            myErrors["empty_subject"] = "please enter valid subject"
        elif trainerUpdate is not None:
            trainerUpdate.save()
            return redirect("edit")
        return render(request, "trainerapp/update.html", myErrors)
    return render(request, "trainerapp/update.html", context)


def delete(request, id):
    trainerDelete = Trainer.objects.get(id=id)
    context = {"trainer": trainerDelete}
    if request.method == "POST":
        trainerDelete.delete()
        return redirect("edit")
    return render(request, "trainerapp/delete.html", context)

