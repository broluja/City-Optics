from django.shortcuts import render, redirect
from .forms import CustomerCreationForm


def register(request):
    if request.method != 'POST':
        form = CustomerCreationForm()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)
    form = CustomerCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('city-optics')
    else:
        form = CustomerCreationForm(request.POST)
        context = {'form': form}
        return render(request, 'accounts/register.html', context)
