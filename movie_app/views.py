from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MovieSearch, MovieData
from omdbapi.movie_search import GetMovie
from datetime import datetime, timedelta

# Initialize OMDB API
movie_api = GetMovie(api_key='501181a6')


def index(request):
    recent_searches = MovieSearch.objects.values('id', 'movie_name').distinct().order_by('-search_date')[:10]
    
    context = {
        'movie': None,
        'error': None,
        'search_query': None,
        'recent_searches': recent_searches,
    }
    return render(request, 'index.html', context)


def search_movie(request):
    """Handle movie search request"""
    context = {
        'movie': None,
        'error': None,
        'search_query': None,
        'recent_searches': MovieSearch.objects.values('id', 'movie_name').distinct().order_by('-search_date')[:10],
    }
    
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name', '').strip()
        
        if not movie_name:
            context['error'] = 'Please enter a movie name'
            return render(request, 'index.html', context)
        
        try:
            movie_data = None  # ← INITIALIZE TO NONE FIRST!
            
            # Check if we have cached data for this movie
            cached_movie = MovieData.objects.filter(
                movie_name__iexact=movie_name
            ).first()
            
            if cached_movie:
                cache_age = datetime.now().replace(tzinfo=None) - cached_movie.cached_date.replace(tzinfo=None)
                if cache_age < timedelta(days=7):
                    movie_data = cached_movie
                else:
                    movie_data = fetch_from_api(movie_name)
            else:
                movie_data = fetch_from_api(movie_name)
            
            if movie_data:
                context['movie'] = {
                    'title': movie_data.title,
                    'year': movie_data.year,
                    'rated': movie_data.rated,
                    'released': movie_data.released,
                    'runtime': movie_data.runtime,
                    'genre': movie_data.genre,
                    'genres': movie_data.genre.split(', ') if movie_data.genre else [],
                    'director': movie_data.director,
                    'writer': movie_data.writer,
                    'actors': movie_data.actors,
                    'plot': movie_data.plot,
                    'language': movie_data.language,
                    'country': movie_data.country,
                    'awards': movie_data.awards,
                    'poster': movie_data.poster,
                    'imdb_rating': movie_data.imdb_rating,
                    'imdb_votes': movie_data.imdb_votes,
                    'box_office': movie_data.box_office,
                    'production': movie_data.production,
                }
                context['search_query'] = movie_name
                
                # Save search to database
                last_search = MovieSearch.objects.filter(
                    movie_name__iexact=movie_name
                ).order_by('-search_date').first()
                
                should_save = True
                if last_search:
                    time_diff = datetime.now().replace(tzinfo=None) - last_search.search_date.replace(tzinfo=None)
                    if time_diff < timedelta(hours=1):
                        should_save = False
                
                if should_save:
                    MovieSearch.objects.create(movie_name=movie_name)
            else:
                context['error'] = 'Movie not found. Please try another search.'
                context['search_query'] = movie_name
                
        except Exception as e:
            context['error'] = f'Error fetching movie data: {str(e)}'
            context['search_query'] = movie_name
    
    return render(request, 'index.html', context)
def search_by_history(request, movie_name):
    """Handle search when clicking on recent searches"""
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['movie_name'] = movie_name
        request.method = 'POST'
        return search_movie(request)
    
    return redirect('index')


def clear_history(request):
    """Clear all search history"""
    if request.method == 'POST':
        MovieSearch.objects.all().delete()
    return redirect('index')


def delete_search(request, search_id):
    """Delete a specific search from history"""
    try:
        search = MovieSearch.objects.get(id=search_id)
        search.delete()
    except MovieSearch.DoesNotExist:
        pass
    return redirect('index')


def fetch_from_api(movie_name):
    """
    Fetch movie data from OMDB API and cache it
    Returns: MovieData object or None
    """
    try:
        # Fetch from API
        movie_data = movie_api.get_movie(title=movie_name, plot='full')
        
        if not movie_data:
            return None
        
        # Get actors separately
        actors = movie_api.get_data('actors')
        
        # Create or update cache
        movie_obj, created = MovieData.objects.update_or_create(
            movie_name=movie_name,
            defaults={
                'title': movie_data.get('title', 'N/A'),
                'year': movie_data.get('year', 'N/A'),
                'rated': movie_data.get('rated', 'N/A'),
                'released': movie_data.get('released', 'N/A'),
                'runtime': movie_data.get('runtime', 'N/A'),
                'genre': movie_data.get('genre', 'N/A'),
                'director': movie_data.get('director', 'N/A'),
                'writer': movie_data.get('writer', 'N/A'),
                'actors': actors or movie_data.get('actors', 'N/A'),
                'plot': movie_data.get('plot', 'N/A'),
                'language': movie_data.get('language', 'N/A'),
                'country': movie_data.get('country', 'N/A'),
                'awards': movie_data.get('awards', 'N/A'),
                'poster': movie_data.get('poster', ''),
                'imdb_rating': movie_data.get('imdb_rating', 'N/A'),
                'imdb_votes': movie_data.get('imdb_votes', 'N/A'),
                'box_office': movie_data.get('box_office', 'N/A'),
                'production': movie_data.get('production', 'N/A'),
            }
        )
        
        return movie_obj
        
    except Exception as e:
        print(f"Error fetching from API: {str(e)}")
        return None