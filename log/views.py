from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from bootstrap_datepicker_plus import DateTimePickerInput
from .models import LogEntry
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .filters import LogFilter
from django.shortcuts import render


def LogChart(request):
    if request.user.is_staff == False:
        currentuser = request.user
        job_list = LogEntry.objects.all().filter(worker=currentuser)
    else:
        job_list = LogEntry.objects.all()
    #job_list = LogEntry.objects.all()
    job_filter = LogFilter(request.GET, queryset=job_list)
    return render(request, 'log/job_chart.html', {'filter': job_filter})

def search(request):
    if request.user.is_staff == False:
        currentuser = request.user
        job_list = LogEntry.objects.all().filter(worker=currentuser)
    else:
        job_list = LogEntry.objects.all()
    #job_list = LogEntry.objects.all()
    job_filter = LogFilter(request.GET, queryset=job_list)
    return render(request, 'log/job_filter.html', {'filter': job_filter})

class LogDetail(DetailView):
    model = LogEntry
    template_name = 'log/job_detail.html'
    def get_queryset(self):
        if self.request.user.is_staff == False:
            return self.model.objects.filter(worker=self.request.user)
        else:
            return self.model.objects.all()

class LogCreate(CreateView):
    model = LogEntry
    fields = ['loggedjob', 'starttime', 'finishtime', 'description', 'project']
    def get_form(self):
        form = super().get_form()
        form.fields['loggedjob']
        form.fields['description']
        form.fields['starttime'].widget = DateTimePickerInput(format='%Y-%m-%d %H:%M:%S')
        form.fields['finishtime'].widget = DateTimePickerInput(format='%Y-%m-%d %H:%M:%S')
        return form
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.worker = self.request.user
        return super(CreateView, self).form_valid(form)
    success_url = reverse_lazy('search')
    template_name = 'log/job_form.html'

class LogUpdate(UpdateView):
    model = LogEntry
    fields = ['loggedjob', 'starttime', 'finishtime', 'description']
    success_url = reverse_lazy('search')
    template_name = 'log/job_form.html'
    def get_queryset(self):
        if self.request.user.is_staff == False:
            return self.model.objects.filter(worker=self.request.user)
        else:
            return self.model.objects.all()

class LogDelete(DeleteView):
    model = LogEntry
    success_url = reverse_lazy('search')
    template_name = 'log/job_confirm_delete.html'
    def get_queryset(self):
        if self.request.user.is_staff == False:
            return self.model.objects.filter(worker=self.request.user)
        else:
            return self.model.objects.all()
