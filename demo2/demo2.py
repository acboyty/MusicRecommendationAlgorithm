import pandas as pd
import csv


ratings = pd.read_csv('./datasets/ml-latest-small/ratings.csv')    
movies = pd.read_csv('./datasets/ml-latest-small/movies.csv') 
data = pd.merge(movies, ratings, on='movieId')
data = data[['userId','rating','movieId','title']].sort_values('userId').to_csv('./datasets/ml-latest-small/data.csv', index=False, encoding='utf8')
files = pd.read_csv('./datasets/ml-latest-small/data.csv')


# read data.csv
content = []
with open('./datasets/ml-latest-small/data.csv', encoding='utf8') as fp:  
    cr = csv.reader(fp)
    for row in cr:
        # print(row)
        content.append(row)
print('len(content), content[:2]:')
print(len(content), content[:2])

# from list to dictionary
data = {}
for line in content[1:]:  # delete the first row
    # print(line)
    if line[3] not in data.keys():
        data[line[3]] = {line[0]:line[1]}
    else:
        data[line[3]][line[0]] = line[1]
print('len(data), data[\'101\']:')
print(len(data), data['Harry Potter and the Chamber of Secrets (2002)'])
data1 = {}
for line in content[1:]:  # delete the first row
    # print(line)
    if line[0] not in data1.keys():
        data1[line[0]] = {line[3]:line[1]}
    else:
        data1[line[0]][line[3]] = line[1]
print('len(data1), data1[\'101\']:')
print(len(data1), data1['101'])

from math import *

# compute the distance between 2 movies
def Euclidean(movie1, movie2):
    movie1_data=data[movie1]
    movie2_data=data[movie2]
    distance = 0
    count = 0
    # find users that rates both movies
    for key in movie1_data.keys():
        if key in movie2_data.keys():
            distance += pow(float(movie1_data[key]) - float(movie2_data[key]), 2)
            count += 1
    if count > 0:
        distance = sqrt(distance / count)  # [0, 5]
    else:
        distance = 5.5  # if 2 movies have a same user, the greatest distance is 5
 
    return distance  # the smaller, the more similar
 
# compute the similarity with other movies
def top10_simliar(Movie):
    res = []
    for movie in data.keys():
        if not movie == Movie:
            simliarity = Euclidean(movie, Movie)
            res.append((movie, simliarity))
    res.sort(key=lambda val:val[1])
    return res[:10]
 
res = top10_simliar('Harry Potter and the Chamber of Secrets (2002)')
print('res:')
print(res)

def recommend(user):
    rating = []
    for key in data1[user]:
        rating.append((key, data1[user][key]))
    rating.sort(key=lambda val: val[1], reverse=True)
    Movie = rating[0][0]  # This is user likes most
    top10 = top10_simliar(Movie)
    res = []
    for x in top10:
        res.append(x[0])
    return res
 
Recommendations = recommend('1')
print('Recommendations:')
print(Recommendations)