from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Event(models.Model):

    EVENT_TYPES = [
        ('Individual', 'Individual'),
        ('Team', 'Team'),
    ]

    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    venue = models.CharField(max_length=200)
    event_date = models.DateField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    team_size = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.event.title}"


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField()
    max_members = models.PositiveIntegerField()

    def __str__(self):
        return self.team_name


class TeamApplication(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.applicant.username} -> {self.team.team_name}"


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.username} - {self.team.team_name}"
