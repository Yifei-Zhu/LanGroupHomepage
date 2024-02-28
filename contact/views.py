from django.shortcuts import render,redirect
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace 'success_url' with the URL to redirect to after successful submission
    else:
        form = ContactForm()
    return render(request, 'contact/contact_us.html', {'form': form})


from django.http import HttpResponse

def submission_success(request):
    return HttpResponse("Thank you for your message. We will get back to you soon.")