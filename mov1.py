import pandas as pd
import numpy as np

movie = pd.read_csv(r'C:\Users\Hp\Downloads\movie recommender\movies.csv')
movie.info()
movie.describe()
movie.columns
movie.isnull().sum()
movie = movie[['id', 'title','genres','overview' ]]
movie
movie.loc[:, 'tags'] = movie['overview'] + movie['genres']
new = movie.drop(columns = [ 'genres','overview' ] )


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 5000, stop_words = 'english')

v = cv.fit_transform(new['tags'].values.astype('U')).toarray()
v.shape

from sklearn.metrics.pairwise import cosine_similarity
sim = cosine_similarity(v)


sim_aligned, new_aligned = pd.DataFrame(sim).align(new, axis=0, join='inner')


def recommend(movie_title):
    if movie_title not in new_aligned['title'].values:
        print(f"Movie '{movie_title}' not found.")
        return

    index = new_aligned[new_aligned['title'] == movie_title].index[0]
    distance = sorted(enumerate(sim_aligned.iloc[index]), reverse=True, key=lambda v: v[1])

    print(f"Movies similar to '{movie_title}':")
    for i, dist in distance[1:6]:
        print(new_aligned.iloc[i].title)




import pickle

pickle.dump(new_aligned, open('movie_list.pkl', 'wb'))
pickle.dump(sim_aligned, open('sim.pkl', 'wb'))


new_loaded = pickle.load(open('movie_list.pkl', 'rb'))
sim_loaded = pickle.load(open('sim.pkl', 'rb'))



print('Loaded Movie DataFrame:')
print(new_loaded.head())

print('\n Loaded Similarity DataFrame:')
print(sim_loaded.head())

