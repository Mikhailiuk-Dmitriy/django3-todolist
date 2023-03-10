from django.urls import include
from django.urls import path
from django.urls import re_path

from todo import views

urlpatterns = [
    path("", views.home, name="home"),
    path("addtodo/", views.AddTodoView.as_view(), name="add_todo"),
    path("api/v1/todolist/", views.TodoAPIList.as_view(), name="api"),
    path("api/v1/todolist/<int:pk>/", views.TodoAPIDetailView.as_view()),
    path("api/v1/drf-auth/", include("rest_framework.urls"), name="auth"),
    path("api/v1/auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("complete/<int:pk>/", views.complete_todo, name="complete_todo"),
    path(
        "completedtodos/",
        views.CompletedTodoList.as_view(),
        name="completed_todos",
    ),
    path(
        "control_tags/", views.ControlTagsList.as_view(), name="control_tags"
    ),
    path("create_tag/", views.CreateTagView.as_view(), name="create_tag"),
    path("current/", views.CurrentTodosList.as_view(), name="current_todos"),
    path(
        "delete/<int:pk>/", views.DeleteTodoView.as_view(), name="delete_todo"
    ),
    path(
        "delete_tag/<int:pk>/",
        views.DeleteTagView.as_view(),
        name="delete_tag",
    ),
    path("detail_tag/<int:pk>/", views.detail_tag, name="detail_tag"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.log_out_user, name="log_out_user"),
    path("signup/", views.sign_up_user, name="sign_up_user"),
    path(
        "search_current/",
        views.TodoCurrentSearchView.as_view(),
        name="search_current",
    ),
    path(
        "search_completed/",
        views.TodoCompletedSearchView.as_view(),
        name="search_completed",
    ),
    path(
        "updatetodo/<int:pk>/",
        views.UpDateTodoView.as_view(),
        name="up_date_todo",
    ),
    path(
        "updat_tag/<int:pk>/",
        views.UpDateTagView.as_view(),
        name="up_date_tag",
    ),
]
