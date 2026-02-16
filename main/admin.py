from django.contrib import admin
from .models import Advisor, Reviewer, Review

admin.site.register(Advisor)
admin.site.register(Reviewer)
admin.site.register(Review)
