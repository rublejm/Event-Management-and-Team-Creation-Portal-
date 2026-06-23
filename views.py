
from .models import Event,Registration,Team
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import  render,redirect
from django.contrib.auth.decorators import login_required
from .models import TeamApplication,TeamMember


def home(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    return render(request, 'home.html')


def event_list(request):
    events = Event.objects.all()

    return render(
        request,
        'event_list.html',
        {'events': events}
    )

def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)

    return render(
        request,
        'event_detail.html',
        {'event': event}
    )
@login_required
def register_event(request, event_id):

    event = Event.objects.get(id=event_id)

    Registration.objects.get_or_create(
        student=request.user,
        event=event
    )

    return redirect('/events/')
def signup_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect('/')

    return render(request, 'signup.html')


def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def create_team(request):

    if request.method == "POST":

        team_name = request.POST['team_name']
        description = request.POST['description']
        max_members = request.POST['max_members']

        event_id = request.POST['event']

        event = Event.objects.get(id=event_id)

        team = Team.objects.create(
            team_name=team_name,
            leader=request.user,
            event=event,
            description=description,
            max_members=max_members
        )

        TeamMember.objects.create(
            team=team,
            member=request.user
        )

        return redirect('/events/')

    events = Event.objects.filter(
        event_type='Team'
    )

    return render(
        request,
        'create_team.html',
        {'events': events}
    )
def team_list(request):

    teams = Team.objects.all()

    return render(
        request,
        'team_list.html',
        {'teams': teams}
    )
@login_required
def apply_team(request, team_id):

    team = Team.objects.get(id=team_id)

    if team.leader == request.user:

        return render(
            request,
            'success.html',
            {
                'message':
                'You cannot apply to your own team.'
            }
        )

    application, created = TeamApplication.objects.get_or_create(
        applicant=request.user,
        team=team
    )

    if created:

        return render(
            request,
            'success.html',
            {
                'message':
                'Application submitted successfully.'
            }
        )

    return render(
        request,
        'success.html',
        {
            'message':
            'You have already applied to this team.'
        }
    )

    return redirect('/teams/')
@login_required
def my_applications(request):

    applications = TeamApplication.objects.filter(
        applicant=request.user
    )

    return render(
        request,
        'my_applications.html',
        {'applications': applications}
    )
@login_required
def leader_dashboard(request):

    applications = TeamApplication.objects.filter(
        team__leader=request.user,
        status='Pending'
    )

    return render(
        request,
        'leader_dashboard.html',
        {'applications': applications}
    )
@login_required
def accept_application(request, application_id):

    application = TeamApplication.objects.get(
        id=application_id
    )

    application.status = 'Accepted'
    application.save()

    TeamMember.objects.get_or_create(
    team=application.team,
    member=application.applicant)

    return redirect('/leader-dashboard/')


@login_required
def reject_application(request, application_id):

    application = TeamApplication.objects.get(
        id=application_id
    )

    application.status = 'Rejected'
    application.save()

    return redirect('/leader-dashboard/')
@login_required
def dashboard(request):

    registrations = Registration.objects.filter(
        student=request.user
    )

    teams = Team.objects.filter(
        leader=request.user
    )

    applications = TeamApplication.objects.filter(
        applicant=request.user
    )

    context = {
        'registrations': registrations,
        'teams': teams,
        'applications': applications,
    }

    return render(
        request,
        'dashboard.html',
        context
    )
@login_required
def team_members(request, team_id):

    team = Team.objects.get(id=team_id)

    members = TeamMember.objects.filter(
        team=team
    )

    return render(
        request,
        'team_members.html',
        {
            'team': team,
            'members': members
        }
    )
