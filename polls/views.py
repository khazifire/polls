from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin



class IndexView(LoginRequiredMixin,generic.ListView):
    login_url = '/accounts/login/'
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        #return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin,generic.DetailView):
    login_url = '/accounts/login/'
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(LoginRequiredMixin,generic.DetailView):
    login_url = '/accounts/login/'
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def reset(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    selected_choice = question.choice_set.all()
    for x in selected_choice:
        x.votes =0
        x.save()
    context = {'question': question}
    return render(request, 'polls/results.html', context)

    
 
    