from django.shortcuts import render


def home(request):
    return render(request, 'redisScan.html')


def redisScan(request):
    return render(request, 'redisScan.html')
