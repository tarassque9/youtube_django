from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, RegisterForm, NewVideoForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Video, Comment
import random, string
import os
from wsgiref.util import FileWrapper


class HomeView(View):
    template_name = 'youtube/index.html'
    def get(self, request):
        most_recent_video = Video.objects.order_by('-datetime')[:10]
        return render(request, self.template_name, context={'videos': most_recent_video})

class VideoFileView(View):
    
    def get(self, request, file_name):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = FileWrapper(open(BASE_DIR + '/' + file_name, 'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        reponse['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        return response


class VideoView(View):
    template_name = 'youtube/video.html'

    def get(self, request, id):
        video_by_id = Video.objects.get(id=id)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_by_id.path = BASE_DIR + '/' + video_by_id.path
        context = {'video': video_by_id}

        if request.user.is_authenticated:
            comment_form = CommentForm()
            context['form'] = comment_form

        return render(request, self.template_name, context=context)



class LoginView(View):
    template_name = 'youtube/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/index')
        else:
            form = LoginForm()
            return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # create new entry in table logs
                login(request, user)
                return HttpResponseRedirect('/index')
            else:
                return HttpResponseRedirect('/login')
        return HttpResponse('FORM IS NOT VALID')


class CommentView(View):
    template_name = 'youtube/comment.html'

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            video_id = request.POST['video']
            video = Video.objects.get(id=video_id)

            new_comment = Comment(text=text, user=request.user, video=video)
            new_comment.save()
            return HttpResponseRedirect('/video/{}'.format(str(video_id)))
        return HttpResponse('this is register POST response')


class RegisterView(View):
    template_name = 'youtube/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/index')
        else:
            form = RegisterForm()
            return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['username'])
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            return HttpResponseRedirect('/login')
        return HttpResponse('this is register POST response')



class NewVideo(View):
    template_name = 'youtube/new_video.html'
    def get(self, request):
        if request.user.is_authenticated == False:
            #return HttpResponse('you must be authenticated if you want upload video')
            return render(request, 'youtube/some_error.html', context={'message': 'you must be authenticated if you want upload video'})
        form = NewVideoForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = NewVideoForm(request.POST, request.FILES)
        print(form)
        print(request.POST)
        print(request.FILES)

        if form.is_valid():
            print('HERE')
            #create a new video entry
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']

            print(title)
            print(file)
            random_char = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            path = random_char + file.name
            #redirect to new video template
            new_video = Video(title=title, 
                            description=description, 
                            user=request.user, path=path)
            new_video.save()
            print(new_video)
            return HttpResponseRedirect('/video/{}'.format(new_video.id))
        else:
            # print(form)
            # print(request.POST)
            # print(request.FILES)
            #return render(request, 'youtube/some_error.html', context={'message': 'somethink wrong with your upload'})
            return HttpResponse('wrong!')
        return HttpResponse('this is register POST response')


