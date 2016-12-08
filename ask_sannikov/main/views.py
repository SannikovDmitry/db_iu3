# Sannikov Dmitry, 2016

from datetime import datetime
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from forms import QuestionForm, AnswerForm, UserForm, UserProfileForm, ChangePasswordForm
from models import Question, Answer, Hashtag, popular_tags, findPage, UserProfile, Paginator, authors
from django.contrib.auth import authenticate, login

# Create your views here.
@csrf_exempt


# View index page

def index(request, page):
    all_entries_UserProfiles = UserProfile.objects.all()
    if request.user.is_anonymous():
        return render(request, 'index.htm', {'login': 'user', 'flag':'true'})
    else:
        return render(request, 'index.htm', {
            'popular': popular_tags(),
            'questions': findPage(Question.objects.index(), page or 1),
            'pages_total': Question.objects.index().num_pages,
            'whatami': Question.objects.index(),
    })
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Account has blocked!")
        else:
            print "Invalid login details supplied {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html', ())

def registration(request):
    if (request.user.is_authenticated()):
        return render(request, 'registration.html', {})
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()
                registered = True
            else:
                print user_form.errors, profile_form.errors
            registered = True
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
        'registration.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered
    })
def settings(request):
    render(request, 'settings.htm', {})

def change_password(request):
    template_response = views.password_change(request)
    return template_response

def ask(request):
    saved = False
    if request.method == "POST":
        if request.user.is_authenticated():
            qForm = QuestionForm(data=request.POST)
            saved = save_question_from_form(qForm, request.user)
        else:
            return render(request, 'message.htm',
                {'message': 'You must be logged in to post a question!'})
    else:
        qForm = QuestionForm()
        saved = False
    return render(request, 'ask.htm', {
        'popular': popular_tags(),
        'saved': saved,
        'form': qForm,
    })

def top(request, page):
    pager = Question.objects.top()
    return render(request, 'index.htm', {
        'popular': popular_tags(),
        'questions': findPage(pager, page or 1).object_list,
        'pages_total': pager.num_pages
    })

def question(request, question_id, page):
    q = get_object_or_404(Question, id=question_id)
    pager = q.get_answers()
    return render(request, 'question.htm', {
        'question': q,
        'answers': findPage(pager, page or 1),
        'popular': popular_tags(),
        'pages_total': pager.num_pages,
        'whatami': 'question'
    })

def like(request, question_id):
    get_object_or_404(Question, id=question_id).like()
    return render(request, 'message.htm', {
        'message': 'Question ' + question_id + ' liked successfully!',
        'popular': popular_tags(),
    })

def dislike(request, question_id):
    get_object_or_404(Question, id=question_id).dislike()
    context = RequestContext(request, {
        'message': 'Question ' + question_id + ' disliked successfully!',
        'popular': popular_tags(),
    })
    return render(request, 'message.htm', {'context': context})

def tag(request, htag, page):
    pager = Question.objects.by_tag(htag)
    return render(request, 'tag.htm', {
        'questions': pager.page(page or 1).object_list,
        'pages_total': pager.num_pages,
        'popular': popular_tags(),
        'hashtag': htag,
        'whatami': 'tag',
    })

def save_question_from_form(qForm, user):
    if qForm.is_valid():
        title = qForm.cleaned_data['title']
        text = qForm.cleaned_data['text']
        date = datetime.now()
        author = user
        q = Question(title=title, text=text,
            timeStamp=date, author = UserProfile.objects.get(user_id = user.id)
        )
        q.save()
        for tag in qForm.cleaned_data['tags']:
            try:
                htag = Hashtag.objects.get(tag=tag)
                q.hashtags.add(htag)
            except Hashtag.DoesNotExist:
                htag = Hashtag(tag=tag)
                htag.save()
                q.hashtags.add(htag)

        q.save()
        return True
    else:
        return False



def logout (request):
    auth.logout(request)
    return redirect('/')