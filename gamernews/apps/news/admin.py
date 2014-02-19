from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Blob, BlobInstance


class BlobAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ("title",)} 

    date_hierarchy = "timestamp"
    list_display = ('title', 'timestamp', 'user',) 
    list_filter = ('timestamp',)

class BlobInstanceAdmin(admin.ModelAdmin):
    date_hierarchy = "timestamp"
    list_display = ('title', 'timestamp', 'user',) 
    list_filter = ('timestamp',)


admin.site.register(Blob, BlobAdmin)
admin.site.register(BlobInstance, BlobInstanceAdmin)