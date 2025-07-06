from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TagViewSet, tasks_list, add_task, edit_task, delete_task

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"tags", TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls)),
    path("list/", tasks_list, name="tasks_list"),
    path("add/", add_task, name="add_task"),
    path("<int:task_id>/edit/", edit_task, name="edit_task"),
    path("delete/<int:task_id>/", delete_task, name="delete_task"),
]
