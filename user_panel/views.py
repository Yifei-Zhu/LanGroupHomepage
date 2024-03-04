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
from django.db.models import Q

@login_required
def events(request):
    events = Event.objects.all()
    events = Event.objects.filter(
        Q(is_public=True) | (Q(is_public=False) & Q(created_by=request.user))
    ).distinct()
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
            'is_public':event.is_public,
            'is_completed': event.is_completed,
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
        TodoItem.objects.filter(event=event).delete()

        event.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

from .forms import EventForm
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

            todo_description = f"From {start_time_formatted} to {end_time_formatted}, Location: {event.location}, Participants: {participants_names}"
            TodoItem.objects.create(title=f"Event: {event.title}", description=todo_description,event=event)

            subject = 'You are invited to an event'
            message = f"Hi, you have been invited by {event.created_by.first_name} {event.created_by.last_name} to participate in the event: {event.title} from {start_time_formatted} to {end_time_formatted} with {participants_names} at {event.location}."

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email for user in event.participants.all() if user.email]


            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('user_panel')

    else:
        form = EventForm()
    return render(request, 'registration/add_event.html', {'form': form})

from django.views.decorators.http import require_POST

@require_POST
def update_event_status(request, event_id):
    # 假设你已经有了验证和权限检查
    event = Event.objects.get(id=event_id)
    event.is_completed = not event.is_completed  # 切换状态
    event.save()
    return JsonResponse({"success": True, "is_completed": event.is_completed})


from .models import TodoItem, Event

from django.views.decorators.http import require_http_methods
import json
@require_http_methods(["GET"])
def load_todos(request):
    todos = TodoItem.objects.all().values('id', 'title', 'description', 'created_at')
    todos_list = list(todos)
    return JsonResponse(todos_list, safe=False)

@require_http_methods(["POST"])
def add_todo(request):
    try:
        data = json.loads(request.body)
        todo = TodoItem.objects.create(title=data['title'], description=data['description'])
        return JsonResponse({'id': todo.id, 'title': todo.title, 'description': todo.description, 'created_at': todo.created_at}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


from .models import TodoItem

@login_required
@require_http_methods(["DELETE"])
def delete_todo(request, todo_id):
    try:
        todo = TodoItem.objects.get(id=todo_id)
        # 检查这个TodoItem是否关联了一个Event，并且当前用户是否有权限删除这个Event
        if todo.event and (request.user.is_superuser or todo.event.created_by == request.user):
            todo.event.delete()  # 如果有权限，删除这个Event
        elif todo.event:
            # 如果没有权限删除Event，仅删除TodoItem，可以在这里记录日志或通知用户
            pass
        todo.delete()  # 删除TodoItem
        return JsonResponse({'message': 'Todo deleted successfully'}, status=204)
    except TodoItem.DoesNotExist:
        return JsonResponse({'error': 'Todo not found'}, status=404)
