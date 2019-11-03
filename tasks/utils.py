from django.utils import timezone


def task_is_expired(task):

    if task.expected_end_date and timezone.now() > task.expected_end_date:
        return True
    return False
