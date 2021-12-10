from django.shortcuts import render
from django.http import Http404
from django.http.response import HttpResponseRedirect
from .models import Notes
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NotesForm


class NotesDeleteView(DeleteView):
    model = Notes
    success_url = '/smart/notes'
    template_name = 'notes/notes_delete.html'

class NotesUpdateView(UpdateView):
    model = Notes
    form_class = NotesForm
    success_url = '/smart/notes'
    template_name = 'notes/notes_form.html'

class NotesCreateView(CreateView):
    model = Notes
    form_class = NotesForm
    success_url = '/smart/notes'
    template_name = 'notes/notes_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = "notes"
    template_name = 'notes/all_notes.html'
    login_url = '/login'

    def get_queryset(self):
        return self.request.user.notes.all()

def detail(request, pk):
    try:
        note = Notes.objects.get(pk=pk)
    except:
        raise Http404("Note doesn't exist")
    return render(request, 'notes/detail.html', {'note': note})