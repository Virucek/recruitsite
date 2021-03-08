from django.shortcuts import render
from authapp.models import Employer

def main(request):
    data_emploers = Employer.objects.all()[:4]
    return data_emploers