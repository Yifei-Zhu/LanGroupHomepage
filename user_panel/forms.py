from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

from django import forms
from .models import Event
from django.contrib.auth.models import User

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['participants'].label_from_instance = lambda obj: "%s" % (obj.first_name+' '+obj.last_name)

    class Meta:
        model = Event
        fields = ['title', 'start_time', 'end_time', 'participants']
        widgets = {
            'participants': forms.CheckboxSelectMultiple,
        }