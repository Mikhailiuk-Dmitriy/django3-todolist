import os
from typing import Any

import requests
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from dotenv import load_dotenv
from rest_framework import generics  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore

from .models import Tag
from .models import Todo
from .serializers import TodoSerializer

User = get_user_model()

load_dotenv()


def home(request: HttpRequest) -> HttpResponse:
    key_api: Any = os.getenv("key_api")
    url: str = (
        "https://api.openweathermap.org/data/2.5/weather?q={},"
        "by&units=metric&appid={}"
    )
    city: str = "Минск"
    res: Any = requests.get(url.format(city, key_api)).json()

    city_info = {
        "city": city,
        "temp": res["main"]["temp"],
        "icon": res["weather"][0]["icon"],
    }

    context = {"info_weather": city_info}
    return render(request, "todo/home.html", context)


def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(
            request, "todo/login-user.html", {"form": AuthenticationForm}
        )
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "todo/login-user.html",
                {
                    "form": AuthenticationForm(),
                    "error": "Логин и пароль не совпадают",
                },
            )
        else:
            login(request, user)
            return redirect("current_todos")


def sign_up_user(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(
            request, "todo/sign-up-user.html", {"form": UserCreationForm}
        )
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(  # type: ignore
                    request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("current_todos")
            except IntegrityError:
                return render(
                    request,
                    "todo/sign-up-user.html",
                    {
                        "form": UserCreationForm(),
                        "error": "Это имя пользователя уже занято. "
                        "Пожалуйста, выберите новое имя пользователя",
                    },
                )
        else:
            return render(
                request,
                "todo/sign-up-user.html",
                {"form": UserCreationForm(), "error": "Пароли не совпадают"},
            )


def log_out_user(request: HttpRequest) -> Any:
    if request.method == "POST":
        logout(request)
        return redirect("home")


class CurrentTodosList(LoginRequiredMixin, generic.ListView):
    template_name = "todo/current-todos.html"
    model = Todo
    context_object_name = "todos"

    def get_queryset(self) -> Any:
        qs: Any = super().get_queryset()
        qs = qs.filter(
            user=self.request.user, datecompleted__isnull=True
        ).order_by("-important")
        qs = search_todo(self, qs)
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data()
        search = self.request.session.get("search_current")
        context["search_current"] = search if search else ""
        context["tags"] = Tag.objects.filter(user=self.request.user)
        return context


def search_todo(self: Any, qs: Any) -> Any:
    search_text: Any = None
    list_todo: list = []
    if self.template_name == "todo/current-todos.html":
        search_text = self.request.session.get("search_current")
    elif self.template_name == "todo/completed-todos.html":
        search_text = self.request.session.get("search_completed")
    if search_text is not None:
        try:
            for item in qs:
                text: Any = str(item.title) + str(item.memo)
                if search_text in text:
                    list_todo.append(item)
            return list_todo
        except KeyError:
            return qs
    else:
        return qs


class AddTodoView(LoginRequiredMixin, generic.CreateView):
    template_name = "todo/add-todo.html"
    model = Todo
    fields = ["title", "memo", "important", "tag"]
    success_url = "/current"

    def form_valid(self, form: forms.ModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self) -> Any:
        qs: Any = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def get_context_data(self) -> dict[str, Any]:  # type: ignore
        context = super().get_context_data()
        context["tags"] = Tag.objects.filter(user=self.request.user)
        return context


class UpDateTodoView(LoginRequiredMixin, generic.UpdateView):
    template_name = "todo/up-date-todo.html"
    model = Todo
    fields = ["title", "memo", "important", "tag"]
    success_url = "/current"

    def get_queryset(self) -> Any:
        qs: Any = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def get_context_data(self) -> dict[str, Any]:  # type: ignore
        context = super().get_context_data()
        context["tags"] = Tag.objects.filter(user=self.request.user)
        return context


class CompletedTodoList(LoginRequiredMixin, generic.ListView):
    template_name = "todo/completed-todos.html"
    model = Todo
    context_object_name = "todos"

    def get_queryset(self) -> Any:
        qs: Any = super().get_queryset()
        qs = qs.filter(
            user=self.request.user, datecompleted__isnull=False
        ).order_by("-datecompleted")
        qs = search_todo(self, qs)
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data()
        search = self.request.session.get("search_completed")
        context["search_completed"] = search if search else ""
        return context


@login_required
def complete_todo(request: HttpRequest, pk: int) -> Any:
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect("current_todos")


class DeleteTodoView(LoginRequiredMixin, generic.DeleteView):  # type: ignore
    model = Todo
    success_url = "/completedtodos"


class TodoAPIList(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> Any:
        user = self.request.user
        return Todo.objects.filter(user=user)


class TodoAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> Any:
        user = self.request.user
        return Todo.objects.filter(user=user)


class TodoCurrentSearchView(LoginRequiredMixin, generic.FormView):
    form_class = forms.Form
    success_url = "/current"

    def form_valid(self, form: forms.Form) -> HttpResponse:
        search_text = self.request.POST["search_current"].lower()
        self.request.session["search_current"] = search_text
        return super().form_valid(form)


class TodoCompletedSearchView(LoginRequiredMixin, generic.FormView):
    form_class = forms.Form
    success_url = "/completedtodos"

    def form_valid(self, form: forms.Form) -> HttpResponse:
        search_text = self.request.POST["search_completed"].lower()
        self.request.session["search_completed"] = search_text
        return super().form_valid(form)


class ControlTagsList(LoginRequiredMixin, generic.ListView):
    template_name = "todo/control_tags.html"
    model = Tag
    context_object_name = "tags"

    def get_queryset(self) -> Any:
        qs: Any = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class CreateTagView(LoginRequiredMixin, generic.CreateView):
    template_name = "todo/create_tag.html"
    model = Tag
    fields = ["title"]
    success_url = "/control_tags"

    def form_valid(self, form: forms.ModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteTagView(LoginRequiredMixin, generic.DeleteView):  # type: ignore
    template_name = "todo/delete_tag.html"
    model = Tag
    success_url = "/control_tags"


class UpDateTagView(LoginRequiredMixin, generic.UpdateView):
    template_name = "todo/update_tag.html"
    model = Tag
    fields = ["title"]
    success_url = "/control_tags"


@login_required
def detail_tag(request: HttpRequest, pk: int) -> Any:
    tag = Tag.objects.get(pk=pk)
    todos = Todo.objects.filter(tag=pk, user=request.user)
    return render(
        request, "todo/detail_tag.html", {"tag": tag, "todos": todos}
    )
