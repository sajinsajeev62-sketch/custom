from django.db import models

class MovieSearch(models.Model):
    """Model to store movie search history"""
    movie_name = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-search_date']
        verbose_name_plural = "Movie Searches"
    
    def __str__(self):
        return f"{self.movie_name} - {self.search_date.strftime('%Y-%m-%d %H:%M')}"


class MovieData(models.Model):
    """Model to cache movie data to reduce API calls"""
    movie_name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=10)
    rated = models.CharField(max_length=50, blank=True)
    released = models.CharField(max_length=50, blank=True)
    runtime = models.CharField(max_length=50, blank=True)
    genre = models.CharField(max_length=255, blank=True)
    director = models.CharField(max_length=255, blank=True)
    writer = models.CharField(max_length=500, blank=True)
    actors = models.CharField(max_length=500, blank=True)
    plot = models.TextField(blank=True)
    language = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    awards = models.TextField(blank=True)
    poster = models.URLField(blank=True)
    imdb_rating = models.CharField(max_length=10, blank=True)
    imdb_votes = models.CharField(max_length=50, blank=True)
    box_office = models.CharField(max_length=100, blank=True)
    production = models.CharField(max_length=255, blank=True)
    cached_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Movie Data Cache"
    
    def __str__(self):
        return self.title