import tmdbsimple as tmdb

tmdb.API_KEY = '1ce9398920594a5521f0d53e9b33c52f'

movie = tmdb.Movies(603)
response = movie.info()

print(response)


tconst = movie.external_ids()

print(tconst)



