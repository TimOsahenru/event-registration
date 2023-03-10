from django.shortcuts import render, redirect
from .models import User, Event, Submission
from .forms import SubmissionForm, CustomUserForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from PIL import Image
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from datetime import datetime


def logout_page(request):
    logout(request)
    return redirect("login")


def login_page(request):
    page = "login"

    if request.method == "POST":
        user = authenticate(
            email=request.POST["email"], password=request.POST["password"]
        )

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Email or Password is incorrect")
            return redirect("login")

    context = {"page": page}
    return render(request, "login_register.html", context)


def register_page(request):
    form = CustomUserForm()

    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    context = {"form": form}
    return render(request, "login_register.html", context)


def home_page(request):
    users = User.objects.filter(hackathon_participant=True)
    count = users.count()

    page = request.GET.get("page")
    paginator = Paginator(users, 5)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        users = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        users = paginator.page(page)

    pages = list(range(1, (paginator.num_pages + 1)))
    users = users[0:20]
    events = Event.objects.all()
    context = {"users": users, "events": events, "count": count, "paginator": paginator}
    return render(request, "home.html", context)


@login_required(login_url="login")
def edit_account(request):
    form = UserForm(instance=request.user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("account")
    context = {"form": form}
    return render(request, "user_form.html", context)


@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            new_password = make_password(password1)
            request.user.password = new_password
            request.user.save()
            return redirect("account")
    context = {}
    return render(request, "account_password.html", context)


@login_required(login_url="login")
def event_page(request, pk):
    event = Event.objects.get(id=pk)

    present = datetime.now().timestamp()
    deadline = event.end_date.timestamp()
    past_deadline = present > deadline

    registered = request.user.events.filter(id=event.id).exists()
    submitted = Submission.objects.filter(
        participant=request.user, event=event
    ).exists()

    context = {
        "event": event,
        "registered": registered,
        "submitted": submitted,
        "past_deadline": past_deadline,
    }
    return render(request, "event.html", context)


@login_required(login_url="login")
def registration_confirmation(request, pk):
    event = Event.objects.get(id=pk)

    if request.method == "POST":
        event.participation.add(request.user)
        return redirect("event", pk=event.id)
    context = {"event": event}
    return render(request, "event_confirmation.html", context)


def user_page(request, pk):
    user = User.objects.get(id=pk)
    context = {"user": user}
    return render(request, "profile.html", context)


@login_required(login_url="login")
def account_page(request):
    user = request.user
    context = {"user": user}
    return render(request, "account.html", context)


@login_required(login_url="login")
def project_submission(request, pk):
    event = Event.objects.get(id=pk)
    form = SubmissionForm()

    if request.method == "POST":
        form = SubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()
            return redirect("account")

    context = {"event": event, "form": form}
    return render(request, "submit-project.html", context)


@login_required(login_url="login")
def update_submission(request, pk):
    submission = Submission.objects.get(id=pk)

    if request.user != submission.participant:
        return HttpResponse("You can't be here!!!")
    event = submission.event
    form = SubmissionForm(instance=submission)

    if request.method == "POST":
        form = SubmissionForm(request.POST, instance=submission)

        if form.is_valid():
            form.save()
            return redirect("account")

    context = {"form": form, "event": event}
    return render(request, "submit-project.html", context)
