from django.contrib import admin
from .models import Star_cast, Movies, Director
# Register your models here.
admin.site.register(Star_cast)
admin.site.register(Director)

class MoviesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'crew', 'year', 'rating', 'cast', 'director', 'language']}),
        
    ]
    list_display = ('title', 'y_o_r')

admin.site.register(Movies, MoviesAdmin)
