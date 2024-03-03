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
        self.fields['participants'].queryset = User.objects.all().order_by('last_name')
        self.fields['participants'].label_from_instance = lambda obj: "%s" % (obj.first_name+' '+obj.last_name)
        self.fields['location'].required = False  # 确保 location 是可选的
        self.fields['is_public'] = forms.BooleanField(required=False, label='Is this event public?')

    class Meta:
        model = Event
        fields = ['title', 'location', 'start_time', 'end_time', 'participants', 'is_public']
        widgets = {
            'participants': forms.CheckboxSelectMultiple,
        }

