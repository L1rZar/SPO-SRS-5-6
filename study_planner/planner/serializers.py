from rest_framework import serializers

from .models import Subject, Task


class SubjectSerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()

    def get_task_count(self, obj):
        count = getattr(obj, 'task_count', None)
        return count if count is not None else obj.tasks.count()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'task_count']


class TaskSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'subject', 'subject_name', 'due_date',
            'status', 'status_label',
        ]
