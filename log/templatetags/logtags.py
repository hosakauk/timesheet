from django import template

register = template.Library()

@register.filter(name='timetotal')
def timetotal(time_list):
    return sum(d['jobtime'] for d in time_list)

@register.filter(name='format_datetime')
def format_datetime(value):
    hours, rem = divmod(value.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return float('{}.{}'.format(hours, minutes))

@register.filter(name='multiply')
def multiply(value, arg):
    return float(value) * float(arg)

@register.filter(name='running_total')
def running_total(value):
    return sum(d.cost for d in value)

@register.filter(name='runningtime')
def runningtime(value):
    return sum(d.jobtime for d in value)
