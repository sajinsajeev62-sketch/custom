from django.contrib import admin
from .models import MovieSearch, MovieData

@admin.register(MovieSearch)
class MovieSearchAdmin(admin.ModelAdmin):
    """Admin interface for MovieSearch model"""
    list_display = ['movie_name', 'search_date', 'time_ago']
    list_filter = ['search_date']
    search_fields = ['movie_name']
    ordering = ['-search_date']
    readonly_fields = ['search_date']
    date_hierarchy = 'search_date'
    
    def time_ago(self, obj):
        """Display how long ago the search was"""
        from django.utils.timezone import now
        from django.utils.timesince import timesince
        return f"{timesince(obj.search_date)} ago"
    time_ago.short_description = 'Time'
    
    def has_add_permission(self, request):
        """Prevent manual addition from admin"""
        return False


@admin.register(MovieData)
class MovieDataAdmin(admin.ModelAdmin):
    """Admin interface for MovieData cache"""
    list_display = ['title', 'movie_name', 'year', 'cached_date', 'cache_age']
    list_filter = ['cached_date', 'year']
    search_fields = ['title', 'movie_name']
    ordering = ['-cached_date']
    readonly_fields = ['movie_name', 'cached_date']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('movie_name', 'title', 'year', 'poster')
        }),
        ('Details', {
            'fields': ('rated', 'released', 'runtime', 'genre', 'country', 'language')
        }),
        ('Credits', {
            'fields': ('director', 'writer', 'actors', 'production')
        }),
        ('Ratings', {
            'fields': ('imdb_rating', 'imdb_votes', 'awards')
        }),
        ('Story', {
            'fields': ('plot',)
        }),
        ('Financial', {
            'fields': ('box_office',)
        }),
        ('Cache Info', {
            'fields': ('cached_date',),
            'classes': ('collapse',)
        }),
    )
    
    def cache_age(self, obj):
        """Display how old the cache is"""
        from django.utils.timezone import now
        from django.utils.timesince import timesince
        return f"{timesince(obj.cached_date)} old"
    cache_age.short_description = 'Cache Age'
    
    def has_add_permission(self, request):
        """Prevent manual addition from admin"""
        return False