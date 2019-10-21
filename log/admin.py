from django.contrib import admin
from .models import LogEntry
from .models import Project


class LogInline(admin.TabularInline):
    model = LogEntry

class LogEntryGraph(admin.ModelAdmin):
    
    def projectcost(self):
        return self.project.costperhour

    projectcost.short_description = "Cost Per Hour"
    list_display = ['project','loggedjob',
                    'starttime','finishtime','jobtime',
                    'description','worker', 'cost', projectcost]
    list_display_links = ['loggedjob']
    date_hierarchy = 'starttime'
    list_filter = ['starttime','finishtime','project','worker']
    search_fields = ['description','loggedjob']
    save_as = True
    save_on_top = True
    change_list_template = 'change_list_graph.html'
    
    class Meta:
        model = LogEntry


class ProjectGraph(admin.ModelAdmin):

    #inlines = [LogInline]
    list_display = ['projectname','projectleader','costperhour']
    search_fields = ['projectname','projectleader']
    list_filter = ['projectname', 'projectleader']
    save_as = True
    save_on_top = True
    change_list_template = 'change_list_project_graph.html'

    class Meta:
        model = Project


admin.site.register(LogEntry, LogEntryGraph)
admin.site.register(Project, ProjectGraph)
