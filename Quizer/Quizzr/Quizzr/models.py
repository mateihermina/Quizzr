from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from datetime import time

AuthUserModel = get_user_model()


class Profile(models.Model):
    class Meta:
        db_table = 'profiles'

    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0)])


class Category(models.Model):
    class Meta:
        db_table = 'categories'

    category_name = models.CharField(max_length=255, default="Undefined Name")
    category_description = models.CharField(max_length=255, default="Undefined Description")


class Question(models.Model):
    class Meta:
        db_table = 'questions'

    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=255, default="No text")
    max_answer_time = models.TimeField(auto_now=False, auto_now_add=False, default=time(0, 0, 0))
    points = models.IntegerField(default=10)
    banned = models.BooleanField(default=False)


class Answer(models.Model):
    class Meta:
        db_table = 'answers'

    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=255, default="No text")
    is_correct = models.BooleanField(default=False)


class QuestionFeedback(models.Model):
    class Meta:
        abstract = True

    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, default=None)


class QuestionLike(QuestionFeedback):
    class Meta:
        db_table = 'question_likes'


class QuestionDislike(QuestionFeedback):
    class Meta:
        db_table = 'question_dislikes'



class QuestionWrongAnswer(QuestionFeedback):
    class Meta:
        db_table = 'question_wrong_answers'


class UserQuestion(models.Model):
    class Meta:
        db_table = 'user_questions'

    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, default=None)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, default=None)

    answer_time = models.TimeField(auto_now=False, auto_now_add=False, default=time(0, 0, 0))
