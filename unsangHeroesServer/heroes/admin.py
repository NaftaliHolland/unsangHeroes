from django.contrib import admin
from .models import (
    Tag,
    Hero,
    Nomination,
    Story,
    Interview,
)

admin.site.register(Tag)
admin.site.register(Hero)
admin.site.register(Nomination)
admin.site.register(Story)
admin.site.register(Interview)
