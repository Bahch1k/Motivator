from math import ceil
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView
from .forms import UserCreationForm, MotivationCreateForm
from django.contrib.auth import authenticate, login
import requests
import os
from dotenv import load_dotenv

load_dotenv()

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
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class MotivationList(ListView):
    
    template_name = 'main.html'

    def get(self, request):
        headers = {
            'Authorization': os.getenv('API_KEY', '')
        }
        params = {
            'page' : request.GET.get('page')
        }
        url = os.getenv('API_URL', '')
        response = requests.get(url, headers=headers, params=params)
        page_obj = response.json()
        motivations = page_obj['results']
        pages_count = ceil(page_obj['count']/5)
        context = {
            'motivations': motivations,
            'range': range(1, pages_count+1)
        }
        return render(request, self.template_name, context)

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
        return redirect('main')
    context = {
        'form': form
    }
    return render(request, template, context)


def add_motivation(motivation, user, visibility):
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
    pass
#TODO: Add function logic after solution what messenger will be use.
