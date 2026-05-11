from .models import Task

class TaskService:
    
    @staticmethod
    def create_task(owner, validated_data: dict) -> Task:
        return Task.objects.create(owner=owner, **validated_data)
    
    @staticmethod
    def get_user_tasks(user):
        return Task.objects.filter(owner=user)