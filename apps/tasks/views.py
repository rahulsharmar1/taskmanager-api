from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 

from .models import Task
from .pagination import TaskPagination
from .serializers import TaskSerializer
from .services import TaskService


@extend_schema_view(
    list=extend_schema(
        summary="List all tasks",
        description=(
            "Returns a paginated list of tasks belonging to the authenticated user. "
            "Supports filtering by status and due_date, and ordering by any declared field."
        ),
        parameters=[
            OpenApiParameter("status", OpenApiTypes.STR, description="Filter by status: todo | in_progress | done"),
            OpenApiParameter("due_date", OpenApiTypes.DATE, description="Filter by exact due date (YYYY-MM-DD)"),
            OpenApiParameter("ordering", OpenApiTypes.STR, description="Sort by: due_date, -due_date, created_at, -created_at, title"),
            OpenApiParameter("page", OpenApiTypes.INT, description="Page number"),
            OpenApiParameter("page_size", OpenApiTypes.INT, description="Results per page (max 100)"),
        ],
    ),
    create=extend_schema(
        summary="Create a task",
        description="Creates a new task. The owner is automatically set to the authenticated user.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a task",
        description="Returns a single task by ID. Returns 404 if the task does not belong to the authenticated user.",
    ),
    update=extend_schema(
        summary="Full update a task",
        description="Replaces all fields of a task. All required fields must be provided.",
    ),
    partial_update=extend_schema(
        summary="Partial update a task",
        description="Updates only the provided fields. All other fields remain unchanged.",
    ),
    destroy=extend_schema(
        summary="Delete a task",
        description="Permanently deletes a task. Returns 204 No Content on success.",
    ),
)

class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    filterset_fields = ["status", "due_date"]

    ordering_fields = ["due_date", "created_at", "updated_at", "title"]

    ordering = ["-created_at"]

    def get_queryset(self):
        return TaskService.get_user_tasks(self.request.user)
    
    def perform_create(self, serializer):
        TaskService.create_task(
            owner=self.request.user,
            validated_data=serializer.validated_data,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        task = TaskService.get_user_tasks(request.user).latest("created_at")
        return Response(
            self.get_serializer(task).data,
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)