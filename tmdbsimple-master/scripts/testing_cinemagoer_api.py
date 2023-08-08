from imdb import Cinemagoer

# create an instance of the Cinemagoer class
ia = Cinemagoer()

# get a movie
movie = ia.get_movie('0133093')
print(movie)

plot = movie.summary()
print(plot)

poster = movie.get_fullsizeURL()
print(poster)


# print the names of the directors of the movie
print('Directors:')
for director in movie['directors']:
    print(director['name'])

# # print the genres of the movie
# print('Genres:')
# for genre in movie['genres']:
#     print(genre)
#
# moviePlot = ia.get_movie('0133093', info=['plot'])
#
# # search for a person name
# people = ia.search_person('Mel Gibson')
# for person in people:
#     print(person.personID, person['name'])
