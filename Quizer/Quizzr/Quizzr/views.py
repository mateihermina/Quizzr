from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Answer, Category, Question, Profile, QuestionLike, QuestionDislike, QuestionWrongAnswer
from random import sample
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import AnonymousUser


def homepage_view(request):
    user = request.user
    answers = Answer.objects.all()
    return render(
        request,
        'homepage.html',
        {
            "answers": answers,
            "user": user
        }
    )


def categories_view(request):
    categories = Category.objects.all()
    return render(
        request,
        'categories.html',
        {
            "categories": categories
        }
    )


class Query:
    def __init__(self, question):
        self.question = question
        self.answers = Answer.objects.filter(question=question.id).all()
        self.correct_answer = next((answer for answer in self.answers if answer.is_correct),
                                   "Error: No Answer Marked As Correct")


def quiz_view(request, category_id):
    user = request.user
    profile = Profile.objects.filter(user=user).all()
    questions = Question.objects.filter(category=category_id).all()
    questions = set(questions)
    questions = sample(questions, 3)
    queries = [Query(question) for question in questions]

    return render(
        request,
        'quiz.html',
        {
            "queries": queries,
            "user": user,
            "profile": profile
        }
    )


def register(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/")

    else:
        form = UserCreationForm()

    return render(response, "register.html", {"form": form})


@csrf_exempt
def update_total_score(request):
    user = request.user
    print(user.username)
    if request.method == 'POST':
        if 'to_add' in request.POST:
            print("funciton called")
            to_add = request.POST["to_add"]
            print(to_add)
            profile = Profile.objects.get(user=user)
            profile.score += int(to_add)
            profile.save()
            return HttpResponse('success')

    return HttpResponse('Nup nu vrea, dar in python')


@csrf_exempt
def update_feedback(request):
    user = request.user
    print(user.username)
    if request.method == 'POST':
        if 'feedback[]' in request.POST:
            feedback = request.POST.getlist("feedback[]")

        if 'question_id[]' in request.POST:
            question_id = request.POST.getlist("question_id[]")
            questions = []
            for id in question_id:
                questions.append(Question.objects.get(id=id))

        feedback_dict = dict(zip(questions, feedback))
        print(feedback_dict)

        for key in feedback_dict:
            #print(feedback_dict[key])
            if feedback_dict[key] == "Like":
                #l = QuestionLike.objects.create(question__id=key.id, user__id=user.id)
                l = QuestionLike(question=key, user=user)
                l.save()
            if feedback_dict[key] == "Dislike":
                print("aiurea")
                #l = QuestionDislike.objects.create(question__id=key.id, user__id=user.id)
                #l.save()
            if feedback_dict[key] == "Report":
                print("aiurea")
                #l = QuestionWrongAnswer.objects.create(question__id=key.id, user__id=user.id)
                #l.save()

        return HttpResponse('success')
    else:
        return HttpResponse('Mijlocel')

    return HttpResponse('Nup nu vrea, dar in python')
