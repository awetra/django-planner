from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



class Profession(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Worker(models.Model):

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='workers'
    )
    profession = models.ForeignKey(
        Profession,
        null=True,
        on_delete=models.SET_NULL,
        related_name='workers'
    )

    def __str__(self):
        return f'{self.user.username} - {self.profession.name}'


class Status(models.Model):

    text = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.text


class Task(models.Model):

    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    text = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now=True)
    actual_end_date = models.DateTimeField(null=True, blank=True, default=None)
    expected_end_date = models.DateTimeField(null=True, blank=True, default=None)
    status = models.ForeignKey(
        Status,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tasks'
    )
    contact = models.CharField(
        max_length=150, 
        null=True, 
        blank=True, 
        default=None
    )

    def __str__(self):
        return f'{self.text} - {self.status}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.status = Status.objects.get(text='Выполняется')
        else:
            if self.status.text == 'Выполняется':
                self.actual_end_date = None
            else:
                self.actual_end_date = timezone.now()

        super().save(*args, **kwargs)

    def clean(self):
        if self.expected_end_date:
            now = timezone.now()

            if self.expected_end_date <= now:
                raise ValidationError('Expected end date must be correct')

    @property
    def time_is_over(self):
        if self.expected_end_date:
            if self.expected_end_date <= timezone.now():
                return True
        return False
