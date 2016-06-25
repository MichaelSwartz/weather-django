from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import SubscriberForm


def subscribe(request):
    form = SubscriberForm(request.POST or None)
    if form.is_valid():
        subscriber = form.save(commit=False)
        subscriber.save()
        return HttpResponseRedirect(reverse('emails:subscribe'))

    return render(request, 'emails/subscribe.html', {'form': form})
