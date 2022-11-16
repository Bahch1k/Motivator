# import from standart libraries
from math import ceil
import os

# import from third party libraries
from django.http.response import HttpResponse
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView
from django.contrib.auth import authenticate, login
import requests
from dotenv import load_dotenv
import logging

# import from current project
from .forms import UserCreationForm, MotivationCreateForm

# presetting
load_dotenv()
logger = logging.getLogger('main')


# Class for user's registration.
class Register(CreateView):
    template_name = 'registration/register.html'

    # get registration form.
    def get(self, request):
        context = {
             'form': UserCreationForm() 
            }
        return render(request, self.template_name, context)

    # Save user to database.
    def post(self, request):

        form = UserCreationForm(request.POST)

        # check validity of form data.
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # autologin on service
            user = authenticate(username=username, password=password)
            login(request, user)

            # redirect to main page with all motivations
            return redirect('http://127.0.0.1:8000/users/motivations/?page=1')

        # if form not valid.
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def get_motivations(request):

    # request to API for get data.
    headers = {
        'Authorization': os.getenv('API_KEY', ''),
        'If-None-Match': cache.get('etag' + str(request.GET.get('page')))
    }
    params = {
        'page': request.GET.get('page')
    }
    url = os.getenv('API_URL', '')
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 404:
        return HttpResponse('Something went wrong!')

    elif response.status_code == 200:
        # get all motivations from response.
        page_obj = response.json()
        motivations = page_obj['results']

        # setup range for pages in pagination
        pages_range = range(int(request.GET.get('page')), int(request.GET.get('page')) + 6)


        # ETag header for caching pages
        etag = response.headers['ETag']
        cache.set('etag' + str(request.GET.get('page')), etag)

        context = {
            'motivations': motivations,
            'range': pages_range
        }
        
        # caching context from response
        cache.set('context' + str(request.GET.get('page')), context)

        return render(request, 'main.html', context)

    else:
        # get caching page if response status code != 200
        context = cache.get('context' + str(request.GET.get('page')))
        return render(request, 'main.html', context=context)


class DetailMotivationList(ListView):

    template_name = 'motivation_id.html'

    def get(self, request, id):

        # request to API to get object by id.
        headers = {
            'Authorization': os.getenv('API_KEY', '')
        }
        url = os.getenv('API_URL', '')
        response = requests.get(url + str(id), headers=headers)

        # show object by id on page.
        motivation = response.json()
        return render(request, self.template_name, context=motivation)


class RandomMotivation(ListView):

    template_name = 'home.html'

    def get(self, request):

        # request to API to get random object.
        headers = {
            'Authorization': os.getenv('API_KEY', '')
        }
        url = os.getenv('API_URL_RANDOM', '')
        response = requests.get(url, headers=headers)

        random_motivation = response.json()
        return render(request, self.template_name, {'random_motivation': random_motivation})


# function to decide where the valid object will be sent.
def get_form_data(request):

    template = 'post.html'
    form = MotivationCreateForm(request.POST)

    # make deсision where valid object will be sent.
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

    # if form not valid.
    context = {
        'form': form
    }
    return render(request, template, context)


def add_motivation(motivation, user, visibility):

    # logging of saving object to the database.
    if user != '':
        logger.info(f'Motivation from {user} saved to database.')
    else:
        logger.info('Motivation saved to database but hidden.')

    # request to API to create new object
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
# TODO: Add function logic after solution what messenger will be use.
