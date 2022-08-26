from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView
from .forms import UserCreationForm, MotivationCreateForm
from django.contrib.auth import authenticate, login
import requests


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
            'Authorization': ')tt1bNA71hEja@:RJoFb+cb:GnD)Zmx8'
        }
        params = {
            'page' : request.GET.get('page')
        }
        response = requests.get('http://motivations:9000/motivations/', headers=headers, params=params)
        page_obj = response.json()
        motivations = page_obj['results']
        return render(request, self.template_name, {'motivations':motivations})

class DetailMotivationList(ListView):
    template_name = 'motivation_id.html'

    def get(self, request, id):
        headers = {
            'Authorization': ')tt1bNA71hEja@:RJoFb+cb:GnD)Zmx8'
        }
        url = 'http://motivations:9000/motivations/'
        response = requests.get(url + str(id), headers=headers)
        motivation = response.json()
        return render(request, self.template_name, context = motivation)


class RandomMotivation(ListView):

    template_name = 'home.html'

    def get(self, request):
        headers = {
            'Authorization': ')tt1bNA71hEja@:RJoFb+cb:GnD)Zmx8'
        }
        response = requests.get('http://motivations:9000/motivations/random', headers=headers)
        random_motivation = response.json()
        return render(request, self.template_name, {'random_motivation': random_motivation})


class MotivationCreate(CreateView):
    template_name = 'post.html'

    def get(self, request):
        form = MotivationCreateForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MotivationCreateForm(request.POST)

        if form.is_valid():
            new_motivaion = form.cleaned_data.get('motivation')
            user = request.user.username
            headers = {
            'Authorization': ')tt1bNA71hEja@:RJoFb+cb:GnD)Zmx8'
        }
            response = requests.post('http://motivations:9000/motivations/',headers=headers, json={
                'nickname': user,
                'motivation': new_motivaion
            })
            return redirect('main')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
