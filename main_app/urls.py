from django.urls import path
from . import views 

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('moods/', views.moods_index, name='moods-index'),
    path('moods/calendar/', views.mood_calendar, name='mood-calendar'),
    path('moods/<int:mood_id>/', views.mood_detail, name='mood-detail'),
    path('moods/create/', views.MoodCreate.as_view(), name='mood-create'),
    path('moods/<int:pk>/update/', views.MoodUpdate.as_view(), name='mood-update'),
    path('moods/<int:pk>/delete/', views.MoodDelete.as_view(), name='mood-delete'),
    path('accounts/signup/', views.signup, name='signup'),
]