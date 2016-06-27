from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import SubscriberForm


def subscribe(request):
    form = SubscriberForm(request.POST or None)
    if form.is_valid():
        subscriber = form.save(commit=False)
        subscriber.save()
        message = "You've registered {} to get weather emails for {}!"
        message = message.format(subscriber.email, subscriber.city)
        messages.success(request, message)
        return HttpResponseRedirect(reverse('emails:subscribe'))

    return render(request, 'emails/subscribe.html', {'form': form})
