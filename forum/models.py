from django.utils.translation import gettext as _

from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field

user_model = get_user_model()

class Question(models.Model):
    user = models.ForeignKey(user_model, null=True, on_delete=models.SET_NULL, related_name="questions")
    title = models.CharField(max_length=255, blank=False, null=False)
    text = CKEditor5Field(blank=True, null=False, config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("question-detail", kwargs={"pk": self.pk})

    @property
    def vote_count(self):
        upvotes = self.votes.filter(type=True).count()
        downvotes = self.votes.filter(type=False).count()
        return upvotes - downvotes
    
    @property
    def view_count(self):
        return self.views.all().count()
    
class QuestionVote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(user_model, null=True, on_delete=models.SET_NULL, related_name="question_votes")
    type = models.BooleanField()
    
    class Meta:
        unique_together = ('question', 'user')
        verbose_name = _("QuestionVote")
        verbose_name_plural = _("QuestionVotes")
    
class QuestionView(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(user_model, null=True, on_delete=models.SET_NULL, related_name="question_views")
    
    class Meta:
        unique_together = ('question', 'user')
        verbose_name = _("QuestionView")
        verbose_name_plural = _("QuestionViews")
    
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(user_model, null=True, on_delete=models.SET_NULL, related_name="answers")
    text = CKEditor5Field(blank=True, null=False, config_name='extends')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self):
        return self.text[:50]

    def get_absolute_url(self):
        return reverse("answer-detail", kwargs={"pk": self.pk})

    @property
    def vote_count(self):
        upvotes = self.votes.filter(type=True).count()
        downvotes = self.votes.filter(type=False).count()
        return upvotes - downvotes

class AnswerVote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(user_model, null=True, on_delete=models.SET_NULL, related_name="answer_votes")
    type = models.BooleanField()
    
    class Meta:
        unique_together = ('answer', 'user')
        verbose_name = _("AnswerVote")
        verbose_name_plural = _("AnswerVotes")
    
class Comment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(user_model, null=True, on_delete=models.SET_NULL, related_name="comments")
    text = CKEditor5Field(blank=True, null=False, config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("comment-detail", kwargs={"pk": self.pk})