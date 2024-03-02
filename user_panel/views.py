from django.shortcuts import render,redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm

@login_required
def user_panel_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.save()
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'registration/user_panel.html', {'form': form})

'''
@login_required
def events(request):
    events = Event.objects.all()
    event_list = [{
        'id': event.id,
        'title': event.title,
        'start': event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'end': event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'location': event.location,
        'created_by': event.created_by.first_name+' '+event.created_by.last_name,  # 使用 first_name
        'participants': ', '.join([f'{user.first_name} {user.last_name}' for user in event.participants.all()]),
        'is_deletable': request.user.is_superuser or request.user == event.created_by,
    } for event in events]
    return JsonResponse(event_list, safe=False)
'''
@login_required
def events(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        participants_sorted = event.participants.all().order_by('last_name')
        participants_names = ', '.join([user.get_full_name() for user in participants_sorted])
        
        event_data = {
            'id': event.id,
            'title': event.title,
            'start': event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'location': event.location,
            'created_by':  event.created_by.first_name+' '+event.created_by.last_name,
            'participants': participants_names,
            'is_deletable': request.user.is_superuser or request.user == event.created_by,
        }
        event_list.append(event_data)
    
    return JsonResponse(event_list, safe=False)

from django.shortcuts import get_object_or_404, redirect
from .models import Event
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # 检查当前用户是否有权限删除该事件
    if not (request.user.is_superuser or event.created_by == request.user):
        return HttpResponseForbidden("You are not allowed to delete this event.")
    if request.method == 'POST':
        event.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

def get_events(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'location': event.location,
            'canDelete': request.user.is_superuser or event.created_by == request.user,  # 示例权限检查
        })
    return JsonResponse(event_list, safe=False)


from .forms import EventForm
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            form.save_m2m()

            participants_names = ', '.join([user.get_full_name() or user.username for user in event.participants.all()])

            start_time_formatted = event.start_time.strftime("%Y-%m-%d %H:%M")
            end_time_formatted = event.end_time.strftime("%Y-%m-%d %H:%M")

            subject = 'You are invited to an event'
            message = f"Hi, you have been invited by {event.created_by.first_name} {event.created_by.last_name} to participate in the event: {event.title} from {start_time_formatted} to {end_time_formatted} with {participants_names} at {event.location}."

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email for user in event.participants.all() if user.email]


            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('user_panel')

    else:
        form = EventForm()
    return render(request, 'registration/add_event.html', {'form': form})
