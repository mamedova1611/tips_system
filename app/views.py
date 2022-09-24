import json
import os.path

import cv2
from django.http import HttpResponseRedirect
from django.shortcuts import render

from app.forms import RegisterForm, ActivateForm, AuthForm

import requests

url = 'https://api.yii2-stage.test.wooppay.com'

"""Главная"""


def index(request):
    return render(request, 'main.html')


"""Регистрация. 1 этап"""

registation = '/v1/registration/create-account'


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            email = form.cleaned_data.get('email')
            data = {'login': login, 'email': email}
            response = requests.post(url + registation, data=data)
            response_json = response.json()
            if response_json is not None:
                if response.status_code == 201:
                    return render(request, 'activate.html')
                else:
                    form = RegisterForm()
                    return render(request, 'register.html', {'form': form, 'error': response_json[0]['message']})
            else:
                form = RegisterForm()
                return render(request, 'register.html', {'form': form, 'error': 'Попробуйте позже'})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


"""Регистрация.2 этап"""

activate = '/v1/registration/set-password'


def activate_view(request):
    if request.method == 'POST':
        form = ActivateForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            activate_code = form.cleaned_data.get('activate_code')
            password = form.cleaned_data.get('password')
            data = {'login': login, 'password': password, 'activate_code': activate_code}
            response = requests.post(url + activate, data=data)
            response_json = response.json()
            if response_json is not None:
                if response.status_code == 201:
                    response_auth = request.post(url + auth, data={'login': login, 'password': password})
                    if response_auth.status_code == '200':
                        response_balance = requests.get(url + balance,
                                                        headers={'Authorization': response_json['token']})
                        response = requests.post(url + id_status, headers={'Authorization': response_json['token']})
                        status = response.json()['status']
                        return render(request, 'profile.html',
                                      {'data': response_json, 'balance': response_balance.json()['active'],
                                       'status': status})
                    else:
                        return render(request, 'login.html')
                else:
                    form = ActivateForm()
                    return render(request, 'activate.html', {'form': form, 'error': response_json[0]['message']})
            else:
                form = ActivateForm()
                return render(request, 'activate.html', {'form': form, 'error': 'Попробуйте позже'})
    else:
        form = ActivateForm()
    return render(request, 'activate.html', {'form': form})


"""Авторизация"""

auth = '/v1/auth'
balance = '/v1/balance'
id_status = '/v1/user/id-status'


def login_view(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            data = {'login': login, 'password': password}
            response = requests.post(url + auth, data=data, headers={'Partner-name': 'tips'})
            response_json = response.json()
            if response.status_code == 200:
                response_balance = requests.get(url + balance, headers={'Authorization': response_json['token'],
                                                                        'Partner-name': 'tips'})
                response_status = requests.get(url + id_status, headers={'Authorization': response_json['token'],
                                                                         'Partner-name': 'tips'})
                status = response_status.json()['status']
                return render(request, 'profile.html',
                              {'data': response_json, 'balance': response_balance.json()['active'], 'status': status})
            else:
                form = AuthForm()
                return render(request, 'login.html', {'form': form, 'error': response_json[0]['message']})
    else:
        form = AuthForm()
    return render(request, 'login.html', {'form': form})


"""Создание услуги(чаевые) и генерирование кьюара"""
import qrcode

img_name = 'blank.png'
donate = '/v1/service/donate'
def donate_view(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        data = json.dumps({
            "fields": {
                "amount": "0"
            },
            "title": "Чаевые!",
            "name": "УРА! Чаевые!",
            "description": "Нужно больше золота..."
        })
        response = requests.post(url + donate, headers={'Content-Type': 'application/json', 'Authorization': token},
                                 data=data)
        service_name = response.json()['service_name']
        img = qrcode.make(service_name)
        img.save('app/static/img/blank%s.png' % token[5:10])
        return render(request, 'qr.html', {'qr': 'img/blank%s.png' % token[5:10]})


# чтение куара
transfer_new = '/v1/payment/transfer-new'
pay_card = '/v1/payment/pay-from-card'
def qr_reader(request):
    cam = cv2.VideoCapture(0)  # включаем камеру
    detector = cv2.QRCodeDetector()  # включаем  QRCode detector
    while True:
        _, img = cam.read()
        service_name, bbox, _ = detector.detectAndDecode(img)
        if service_name[:8] == 'transfer':
            data = service_name
            break
    return render(request, 'pseudo_auth.html', {'service_name': data})


"""Псевдоавторизация"""
pseudo_auth = '/v1/auth/pseudo'

def pseudo_auth_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        service_name = request.POST.get('service_name')
        response = requests.post(url + pseudo_auth, data={'login': login})
        token = response.json()['token']
        return render(request, 'form_pay.html', {'token': token, 'service_name': service_name})

# создание визитки
# TODO сделать запись данных официанта и qr на шаблон

"""История"""

history = '/v1/history'


def history_view(request):
    token = request.GET.get('token')
    print(token)
    response = requests.get(url + history, headers={'Content-Type':'application/json','Authorization': token})
    response_json = response.json()
    return render(request, 'history.html', {'history': response_json, 'token': token})


"""Вывод чаевых на карту"""

transfer = '/v1/payment/transfer-to-card'
def token_view(request):
    token = request.POST.get('token')
    return render(request, 'transfer.html', {'token':token})

def transfer_view(request):
    token = request.POST.get('token')
    print(token)
    summa = request.POST.get('summa')
    response = requests.post(url + transfer, headers={'Content-Type': 'application/json', 'Authorization': token},
                             data=json.dumps({'amount': summa, 'mobile_scripts': True}))
    print(response.json())
    return HttpResponseRedirect(response.json()['frame_url'])

"""Оплата"""

def form_pay_view(request):
    token = request.POST.get('token')
    service_name = request.POST.get('service_name')
    summa = request.POST.get('summa')
    data = json.dumps({
        'service_name': service_name,
        "fields": {
            "amount": summa
        }
    })
    response = requests.post(url + transfer_new, headers={'Content-Type': 'application/json', 'Authorization': token},
                             data=data)
    operation_id = response.json()['operation']['id']

    response_url = requests.post(url + pay_card, headers={'Authorization': token},
                            data={'operation_id': operation_id})
    return HttpResponseRedirect(response_url.json()['frame_url'])

"""ЧЕК"""

receipt = '/v1/history/receipt/'


def receipt_view(request, pk):
    if request.method == 'POST':
        token = request.POST.get('token')
        response = request.get(url + receipt + str(pk), headers={'Authorization': token})
        if response.status_code == 200:
            return render(request, 'receipt.html', {'receipt': response.json()})


def receipt_pdf_view(request, pk):
    if request.method == 'POST':
        token = request.POST.get('token')
        response = request.get(url + receipt + 'pdf/' + str(pk), headers={'Authorization': token})
        if response.status_code == 200:
            return render(request, 'receipt.html', {'receipt': response.json()})



