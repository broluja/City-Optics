from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from .forms import CustomerCreationForm, CustomerUpdateForm
from .models import Customer


def register(request):
    if request.method != 'POST':
        form = CustomerCreationForm()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)
    form = CustomerCreationForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'You successfully Registered. Discount code is sent to your email. Log IN')
        return redirect('login')
    else:
        form = CustomerCreationForm(request.POST)
        context = {'form': form}
        return render(request, 'accounts/register.html', context)


class CustomerLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True


class CustomerLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


@login_required
def profile(request, slug):
    if request.method == "POST":
        form = CustomerUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated')
            context = {
                'object': 'Profile',
                'form': CustomerUpdateForm(instance=request.user),
                'customer': request.user.customer
            }
            return render(request, 'accounts/profile.html', context)
        else:
            return redirect('city-optics')

    else:
        try:
            customer = Customer.objects.get(slug=slug)
            form = CustomerUpdateForm(instance=request.user)
            context = {
                'customer': customer,
                'object': 'Profile',
                'form': form
            }
            return render(request, 'accounts/profile.html', context)
        except ObjectDoesNotExist:
            raise Http404


# TODO make API view for GETTING Coupons and Customers, possible for POSTING new Coupons
