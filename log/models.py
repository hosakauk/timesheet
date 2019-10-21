from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Project(models.Model):
    projectname = models.CharField('Project Name', max_length=255)
    projectleader = models.ForeignKey(User, related_name='Leader', null=True, blank=True, default=1, on_delete=models.SET_DEFAULT)
    costperhour = models.DecimalField('Cost Per Hour', max_digits=10, decimal_places=2, default=0)
    def totalcost(self):
        costs = LogEntry.objects.aggregate(totalcost=(Sum('cost')))
        costformat = format(round(costs['totalcost'],2))
        return costformat
    def __str__(self):
        return self.projectname

class LogEntry(models.Model):
    loggedjob = models.CharField('Job Name',max_length=255)
    starttime = models.DateTimeField('Start Time')
    finishtime = models.DateTimeField('Finish Time')
    jobtime = models.DurationField(editable=False)
    project = models.ForeignKey(Project, default="None", on_delete=models.CASCADE)
    description = models.CharField('Description',max_length=255, blank=True)
    cost = models.DecimalField('Job Cost', decimal_places=2, max_digits=20, editable=False, default=0)
    worker = models.ForeignKey(User, related_name="worker", null=True, blank=True, default=1, on_delete=models.SET_DEFAULT)
    def save(self, *args, **kwargs):
        self.jobtime = None
        self.cost = None
        if not self.jobtime:
            self.jobtime = self.finishtime-self.starttime
        if not self.cost:
            self.jtime = float(self.jobtime.total_seconds())
            self.cost = float(self.project.costperhour)
            self.hours = ((self.jtime/60)/60)
            self.hoursround = format(round(self.hours,2))
            self.cost = format(round(self.cost*(self.jtime/60)/60,2))
        super().save(*args, **kwargs)
    def __str__(self):
        return self.loggedjob
