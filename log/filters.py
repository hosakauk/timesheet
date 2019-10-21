from .models import LogEntry, Project
from django_filters import DateFromToRangeFilter
from django_filters import FilterSet
import django_filters
import datetime
from django.db.models import Avg, Sum

class LogFilter(FilterSet):

    datetoday = datetime.datetime.today().strftime("%Y-%m-%d")
    starttime = DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
        attrs={'placeholder': datetoday, 'class': 'form-control',}),label='Search Dates')

    class Meta():
        
        model = LogEntry
        fields = {
            'starttime': ['exact'],
             'project':['exact'],
             'worker':['exact'],
             'loggedjob':['contains'],
            }

# if staff status render worker field ?

    @property
    def totaltimespent(self):
        qs = super().qs
        return qs.aggregate(Sum('jobtime'))['jobtime__sum']

    @property
    def totalcost(self):
        qs = super().qs
        cost = qs.aggregate(Sum('cost'))['cost__sum']
        if cost is not None:
            return format(round(cost,2))
