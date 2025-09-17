# main_app/views.py

from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Mood
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required



# Define the home view function
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


# views.py

class MoodData:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

# Create a list of MoodData instances (for fallback data)
moods_data = [
    MoodData('Lolo', 'tabby', 'Kinda rude.', 3),
    MoodData('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
    MoodData('Fancy', 'bombay', 'Happy fluff ball.', 4),
    MoodData('Bonk', 'selkirk rex', 'Meows loudly.', 6)
]

# views.py
@login_required
def moods_index(request):
    moods = Mood.objects.filter(user=request.user)
    return render(request, 'moods/index.html', { 'moods': moods })


@login_required
def mood_calendar(request):
    # Get the current month and year from URL parameters or use current date
    year = request.GET.get('year', timezone.now().year)
    month = request.GET.get('month', timezone.now().month)
    
    try:
        year = int(year)
        month = int(month)
    except (ValueError, TypeError):
        year = timezone.now().year
        month = timezone.now().month
    
    # Get all moods for the current user in the specified month
    start_date = datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1).date()
    else:
        end_date = datetime(year, month + 1, 1).date()
    
    moods = Mood.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lt=end_date
    ).order_by('date')
    
    # Create a dictionary of moods by date
    moods_by_date = {}
    for mood in moods:
        date_key = mood.date.strftime('%Y-%m-%d')
        if date_key not in moods_by_date:
            moods_by_date[date_key] = []
        moods_by_date[date_key].append(mood)
    
    # Generate calendar data
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # Calculate previous and next month
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    context = {
        'calendar': cal,
        'month_name': month_name,
        'year': year,
        'month': month,
        'moods_by_date': moods_by_date,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    
    return render(request, 'moods/calendar.html', context)


def mood_detail(request, mood_id):
    try:
        mood = Mood.objects.get(id=mood_id)
    except Mood.DoesNotExist:
        # If mood doesn't exist in database, create a fallback
        mood = moods_data[mood_id - 1] if mood_id <= len(moods_data) else None
    return render(request, 'moods/detail.html', {'mood': mood})

class MoodCreate(LoginRequiredMixin, CreateView):
    model = Mood
    fields = ['description', 'date', 'mood_type']
    template_name = 'sanguine/mood_form.html'
    success_url = '/moods/calendar/'

    def get_initial(self):
        """Set today's date as the default date for new moods"""
        initial = super().get_initial()
        initial['date'] = timezone.now().date()
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MoodUpdate(LoginRequiredMixin, UpdateView):
    model = Mood
    fields = ['description', 'date', 'mood_type']
    template_name = 'sanguine/mood_form.html'
    success_url = '/moods/calendar/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MoodDelete(LoginRequiredMixin, DeleteView):
    model = Mood
    success_url = '/moods/calendar/'


class Home(LoginView):
    template_name = 'home.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('moods-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)