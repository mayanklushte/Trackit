from django.contrib import admin
from .models import register, comdetails, Event, message, relation

# Register your models here.

admin.site.register(register)
admin.site.register(comdetails)
admin.site.register(Event)
admin.site.register(message)
admin.site.register(relation)
