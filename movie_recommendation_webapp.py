import difflib
import numpy as np
import pickle
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies_data = pd.read_csv("movies.csv")
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director', 'production_companies']
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director'] + ' ' + movies_data['production_companies']

vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors)
close_match = ""

def input():
    movie_name = st.text_input("Enter Movie name: ")
    list_of_all_titles = movies_data["original_title"].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    if len(find_close_match) != 0:
        close_match = find_close_match[0]
        st.text(close_match)
        index_of_the_movie = movies_data[movies_data['original_title'] == close_match].index.values[0]
        print(index_of_the_movie)
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x:x[1], reverse=True)
        print("Movies suggested for you: \n")
        i = 1
        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = movies_data[movies_data.index==index]['original_title'].values[0]
            if (i<=10):
                st.text(str(i)+'.'+title_from_index)
                i = i + 1
    else:
        st.text("Movie name not found!!")

def process():
    index_of_the_movie = movies_data[movies_data['original_title'] == close_match].index.values[0]
    print(index_of_the_movie)
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x:x[1], reverse=True)
    print("Movies suggested for you: \n")
    i = 1
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movies_data[movies_data.index==index]['original_title'].values[0]
        if (i<=10):
            st.title(i,'.',title_from_index)
            i = i + 1

def main():
    st.title("Movie Recommender")

    input()

if __name__ == '__main__':
    main()