from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Custom APP imports
from .forms import CustomerCreationForm, CustomerUpdateForm, TestimonyForm
from .models import Customer, Coupon
from .serializers import CustomerSerializer, CouponSerializer, RegistrationSerializer

# Third party imports
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token


def register(request):
    if request.user.is_authenticated:
        messages.info(request, f'You are already registered and signed In as {request.user.customer}')
        return redirect('profile', slug=request.user.customer.slug)
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


@login_required
def testify(request):
    if request.method == "POST":
        form = TestimonyForm(request.POST)
        if form.is_valid() and form.cleaned_data.get('agree'):
            testimony = form.save(commit=False)
            try:
                testimony.customer = request.user.customer
                testimony.save()
            except ObjectDoesNotExist:
                messages.warning(request, 'You are not registered Customer')
                return redirect('city-optics')
            except IntegrityError:
                messages.info(request, 'You have already posted your testimony')
                return redirect('profile', slug=request.user.customer.slug)
            messages.success(request, 'Your testimony has been sent to our Admins for verification.')
            return redirect('profile', slug=request.user.customer.slug)
        else:
            return render(request, 'accounts/testimony.html', {'form': form})

    else:
        form = TestimonyForm()
        context = {'form': form}
        return render(request, 'accounts/testimony.html', context)


def edit_testimony(request, slug):
    customer = Customer.objects.get(slug=slug)
    if request.user != customer.user:
        raise Http404
    try:
        customer = Customer.objects.get(slug=slug)
        if request.method == 'POST':
            form = TestimonyForm(request.POST, request.FILES, instance=customer.testimony)
            if form.is_valid():
                testimony = form.save(commit=False)
                testimony.approved = False
                testimony.save()
                messages.success(request, 'Updated!')
                return redirect('profile', slug=request.user.customer.slug)

        else:
            form = TestimonyForm(instance=customer.testimony)
            context = {'form': form}
            return render(request, 'accounts/edit_testimony.html', context)
    except ObjectDoesNotExist:
        messages.info(request, 'Post your testimony.')
        customer = Customer.objects.get(slug=slug)
        form = CustomerUpdateForm(instance=request.user)
        context = {
            'customer': customer,
            'object': 'Profile',
            'form': form
        }
        return render(request, 'accounts/profile.html', context)


# API views

class CustomerAPIView(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object():
        try:
            return Customer.objects.all()
        except ObjectDoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request):
        queryset = self.get_object()
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CouponAPIView(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object():
        try:
            return Coupon.objects.all()
        except ObjectDoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request):
        queryset = self.get_object()
        serializer = CouponSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Successfully registered new user.'
            data['email'] = user.email
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


# HtmX views
# View for giving suggestions on register page
def hx_username(request):
    username = request.GET.get('username')
    if username:
        if User.objects.filter(username=username).exists():
            return HttpResponse(f'<p style="color:red; font-size:17px;">Username: {username} is not available!</p>')
        return HttpResponse(f'<p style="color:green;">Username: {username} is available.</p>')
    return HttpResponse('Hints')

