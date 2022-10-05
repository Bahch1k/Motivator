
from django.core.cache import cache
from math import ceil
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, ListView
from .forms import UserCreationForm, MotivationCreateForm
from django.contrib.auth import authenticate, login
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger('main')

class Register(CreateView):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
             'form': UserCreationForm() 
            }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('http://127.0.0.1:8000/users/motivations/?page=1')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def get_motivations(request):
    headers = {
        'Authorization': os.getenv('API_KEY', ''),
        'If-None-Match': cache.get('etag'+str(request.GET.get('page')))
    }
    params = {
        'page' : request.GET.get('page')
    }
    url = os.getenv('API_URL', '')
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        page_obj = response.json()
        motivations = page_obj['results']
        pages_count = ceil(page_obj['count']/5)
        etag = response.headers['ETag']
        cache.set('etag' + str(request.GET.get('page')), etag)
        context = {
            'motivations': motivations,
            'range': range(1, pages_count+1)
        }
        cache.set('context'+ str(request.GET.get('page')), context)
        return render(request, 'main.html', context)
    else:
        context = cache.get('context'+ str(request.GET.get('page')))
        return render(request, 'main.html', context=context)

class DetailMotivationList(ListView):
    template_name = 'motivation_id.html'

    def get(self, request, id):
        headers = {
            'Authorization': os.getenv('API_KEY', '')
        }
        url = os.getenv('API_URL', '')
        response = requests.get(url + str(id), headers=headers)
        motivation = response.json()
        return render(request, self.template_name, context = motivation)


class RandomMotivation(ListView):

    template_name = 'home.html'

    def get(self, request):
        headers = {
            'Authorization': os.getenv('API_KEY', '')
        }
        url = os.getenv('API_URL_RANDOM', '')
        response = requests.get(url, headers=headers)
        random_motivation = response.json()
        return render(request, self.template_name, {'random_motivation': random_motivation})



def get_form_data(request):
    template = 'post.html'
    form = MotivationCreateForm(request.POST)

    if form.is_valid():
        motivation = form.cleaned_data.get('motivation')
        user = request.user.username
        if request.user.is_anonymous:
            visibility = False
            send_motivation_to_messenger(motivation)
        else:
            visibility = True
        add_motivation(motivation, user, visibility)
        return redirect('http://127.0.0.1:8000/users/motivations/?page=1')
    context = {
        'form': form
    }
    return render(request, template, context)


def add_motivation(motivation, user, visibility):
    if user != '':
        logger.info(f'Motivation from {user} saved to database.')
    else:
        logger.info('Motivation saved to database but hidden.')
    headers = {
        'Authorization': os.getenv('API_KEY', '')
    }
    url = os.getenv('API_URL', '')
    response = requests.post(url,  headers=headers, json={
        'nickname': user,
        'motivation': motivation,
        'is_visible': visibility
    })
    return response
def send_motivation_to_messenger(motivation):
    logger.info('Motivation sends to messenger')
#TODO: Add function logic after solution what messenger will be use.
