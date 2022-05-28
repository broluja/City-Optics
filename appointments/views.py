from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

# Custom APPs imports
from .models import Appointment
from .serializers import AppointmentSerializer

# Third party imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes


def staff_credentials(login_url=None, *args, **kwargs):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)


def appointment(request):
    if request.method != "POST":
        hours = [hour[1] for hour in Appointment.HOURS]
        context = {
            'object': 'appointment',
            'hours': hours
        }
        return render(request, 'appointments/appointment.html', context)

    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    hour = request.POST.get('hours')
    message = request.POST.get('message')
    hours = Appointment.HOURS
    day = request.POST.get('day')
    customer = None

    if request.user.is_authenticated:
        customer = request.user.customer
        customer.phone = phone
        customer.save()

    for pair in hours:
        value, key = pair
        if key == hour:
            hour = value
            break

    new_appointment = Appointment(name=name, phone=phone, email=email, hour=hour, message=message, date=day,
                                  customer=customer)
    new_appointment.save()
    hours = [hour[1] for hour in hours]
    context = {
        'object': 'appointment',
        'name': name,
        'hours': hours
    }
    return render(request, 'appointments/appointment.html', context)


@staff_credentials(login_url='/admin/')
def schedules(request):
    try:
        my_appointments = Appointment.objects.all().order_by('date')
        context = {
            'object': 'Schedule',
            'my_appointments': my_appointments
        }
        return render(request, 'appointments/schedules.html', context)
    except ObjectDoesNotExist:
        raise Http404


@login_required
@require_http_methods(['DELETE'])
def delete_appointment(request, pk):
    my_appointment = Appointment.objects.get(pk=pk)
    my_appointment.delete()
    return render(request, 'appointments/delete_snippet.html')


# API Views

class AppointmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object():
        try:
            return Appointment.objects.filter(is_confirmed=True).order_by('date')
        except ObjectDoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    @staticmethod
    def get_relative_object(request):
        try:
            return Appointment.objects.filter(customer=request.user.customer)
        except ObjectDoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request):
        if request.user.is_superuser:
            queryset = self.get_object()
        else:
            queryset = self.get_relative_object(request)
        serializer = AppointmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAdminUser, ))
def post_appointment(request):
    if request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            new_appointment = serializer.save()
            data['response'] = 'Successfully posted appointment.'
            data['appointment'] = new_appointment.name
        else:
            data = serializer.errors
        return Response(data)


@api_view(['PUT'])
@permission_classes((IsAdminUser, ))
def edit_appointment(request):
    data = {}
    try:
        queryset = Appointment.objects.get(id=request.data['id'])
    except ObjectDoesNotExist:
        data['response'] = 'Object does not exist!'
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    serializer = AppointmentSerializer(queryset, data=request.data)

    if serializer.is_valid():
        edited_appointment = serializer.save()
        data['response'] = 'Successfully edited appointment.'
        data['appointment'] = edited_appointment.name
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
