import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.http import JsonResponse

from forum.models import (
    Question,
    QuestionVote,
    QuestionView,
    Answer,
    AnswerVote
)
from forum.forms import (
    AnswerCreateForm,
    QuestionCreateForm
)

class HomeView(View):
    template_name = "home.html"
    
    def get(self, request):
        return redirect(reverse('question-list'))
    
class QuestionListView(ListView):
    model = Question
    template_name = "questions/index.html"
    paginate_by = 20
    context_object_name = "questions"
    
    def get_queryset(self):
        return Question.objects.select_related('user').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = context["object_list"]
        return context
    
class QuestionDetailView(DetailView):
    model = Question
    context_object_name = "question"
    template_name = "questions/detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["answers"] = Answer.objects.filter(question__pk=self.object.pk)
        context["answer_creation_form"] = AnswerCreateForm()
        context["question_upvoted"] = self.get_question_voted(True)
        context["answers_upvoted"] = self.get_answers_voted(context["answers"], True)
        context["answers_downvoted"] = self.get_answers_voted(context["answers"], False)
        return context

    def get_answers_voted(self, answers, upvoted = True):
        user = self.request.user
        if user.is_authenticated:
            return list(AnswerVote.objects.filter(user=user, answer__in=answers, type=upvoted).values_list("answer_id", flat=True))
        
        return []
            
class QuestionDetailView(DetailView):
    model = Question
    context_object_name = "question"
    template_name = "questions/detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["answers"] = Answer.objects.filter(question__pk=self.object.pk)
        context["answer_creation_form"] = AnswerCreateForm()
        context["question_upvoted"] = self.get_question_voted(True)
        context["question_downvoted"] = self.get_question_voted(False)
        context["answers_upvoted"] = self.get_answers_voted(context["answers"], True)
        context["answers_downvoted"] = self.get_answers_voted(context["answers"], False)
        return context

    def get_answers_voted(self, answers, upvoted = True):
        user = self.request.user
        if user.is_authenticated:
            return list(AnswerVote.objects.filter(user=user, answer__in=answers, type=upvoted).values_list("answer_id", flat=True))
        
        return []
            
    def get_question_voted(self, upvoted=True):
        user = self.request.user
        if user.is_authenticated:
            return QuestionVote.objects.filter(user=user, question=self.object, type=upvoted).exists()
        
        return False
        
            
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if "answer_submit" in request.POST:
            self.handle_answer_submission(request)
        elif "comment_submit" in request.POST:
            self.handle_comment_submission(request)
    
        return self.get(request, *args, **kwargs)
    
    def handle_answer_submission(self, request):
        form = AnswerCreateForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = self.object
            answer.save()
        
        return redirect(self.object.get_absolute_url())
    
    def handle_comment_submission(self, request):
        pass

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = "questions/create.html"
    form_class = QuestionCreateForm
    context_object_name = "question_create_form"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    # Override this function to change the form name in the request data
    # Also changes what we use to render on the frontend
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_create_form"] = context["form"] 
        return context
    
class QuestionDeleteView(CreateView):
    model = Question
    template_name = "question/delete.html"
    
class QuestionVoteView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        question_id = data.get('question_id')
        vote_type = data.get('vote_type')
        
        if not question_id or vote_type not in ["upvote", "downvote"]:
            return JsonResponse({'error': 'Missing or invalid question_id or vote_type'}, status=400)
        
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)
        
        user = request.user
        vote_value = vote_type == "upvote"
        
        vote, created = QuestionVote.objects.update_or_create(
            question=question, user=user,
            defaults={'type': vote_value}
        )
        
        return JsonResponse({
            'vote_count': question.vote_count,
            'vote_value': vote_value,
        })
     
class QuestionViewView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        question_id = data.get('question_id')
        
        if not question_id:
            return JsonResponse({'error': 'Missing or invalid querstion_id'}, status=400)
        
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)
        
        question_view, created = QuestionView.objects.get_or_create(
            question=question,
            user=request.user
        )
        
        return JsonResponse({
            'view_count': question.view_count,
        })
    
class AnswerVoteView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        answer_id = data.get('answer_id')
        vote_type = data.get('vote_type')

        if not answer_id or vote_type not in ["upvote", "downvote"]:
            return JsonResponse({'error': 'Missing or invalid answer_id or vote_type'}, status=400)
        
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return JsonResponse({'error': 'Answer not found'}, status=404)

        user = request.user
        vote_value = vote_type == "upvote"

        vote, created = AnswerVote.objects.update_or_create(
            answer=answer, user=user,
            defaults={'type': vote_value}
        )

        return JsonResponse({
            'vote_count': answer.vote_count,
            'vote_value': vote_value,
        })