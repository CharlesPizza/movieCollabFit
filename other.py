import numpy as np
from scipy.sparse import csr_matrix


class GarbageDay():
    pass



def create_matrix1(df):
    n_user = len(df.userId.unique())
    n_movie = len(df.movieId.unique())
    user_map = dict(zip(np.unique(df.userId), list(range(n_user))))
    movie_map = dict(zip(np.unique(df.movieId), list(range(n_movie))))
#     inverted maps
    user_imap = dict(zip(list(range(n_user)), np.unique(df.userId)))
    movie_imap = dict(zip(list(range(n_movie)), np.unique(df.movieId)))
    
    user_idx = [user_map[i] for i in df.userId]
    movie_idx = [movie_map[i] for i in df.movieId]
    
    X = csr_matrix((df['rating'], (movie_idx, user_idx)), shape=(n_movie, n_user))
    return X, user_map, movie_map, user_imap, movie_imap


def find_similar_items(movie_id, X, k, metric='cosine', show=False):
    neighbors = []
    movie_idx = movie_map[movie_id]
    movie_vec = X[movie_idx]
    k+=1
    kNN = NearestNeighbors(n_neighbors=k, algorithm='brute', metric=metric)
    kNN.fit(X)
    movie_vec = movie_vec.reshape(1,-1)
    neighbor = kNN.kneighbors(movie_vec, return_distance=False)
    for i in range(0, k):
        n = neighbor.item(i)
        neighbors.append(movie_imap[n])
    neighbors.pop(0)
    return neighbors


def recommend_user(user_id, X):
    similar_movies = {}
    user_ratings = ratings_df.query(f'userId == {user_id}')
    user_ratings = user_ratings.query('rating >=4')
    recently_liked = user_ratings.sort_values(by='timestamp', ascending=False).head(10)
    recently_liked.drop(['timestamp'], axis=1,inplace=True)
    
    for movie in recently_liked.movieId:
        similar_movies[movie] = find_similar_items(movie, X, k=5)
    df = recently_liked.merge(pd.DataFrame(list(similar_movies.items()),
                                      columns=['movieId', 'recommendations']), on='movieId')
    return df