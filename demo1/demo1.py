import pandas as pd
ratings = pd.read_csv('./datasets/ml-latest-small/ratings.csv')    
print(ratings.head(20))

movies = pd.read_csv('./datasets/ml-latest-small/movies.csv') 
print(movies.head(5))

data = pd.merge(movies, ratings, on='movieId')
print(data.head(5))
data = data[['userId','rating','movieId','title']].sort_values('userId').to_csv('./datasets/ml-latest-small/data.csv', index=False, encoding='utf8')
files = pd.read_csv('./datasets/ml-latest-small/data.csv')
print(files.head(5))

import csv

# read data.csv
content = []
with open('./datasets/ml-latest-small/data.csv', encoding='utf8') as fp:  
    cr = csv.reader(fp)
    for row in cr:
        # print(row)
        content.append(row)
print(len(content), content[:2])

# from list to dictionary
data = {}
for line in content[1:]:  # delete the first row
    # print(line)
    if line[0] not in data.keys():
        data[line[0]] = {line[3]:line[1]}
    else:
        data[line[0]][line[3]] = line[1]
print(len(data), data['101'])

from math import *

# compute the distance between 2 users
def Euclidean(user1, user2):
    user1_data=data[user1]
    user2_data=data[user2]
    distance = 0
    count = 0
    # find movies that 2 users both give ratings, and compute distance
    for key in user1_data.keys():
        if key in user2_data.keys():
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)
            count += 1
    if count > 0:
        distance = sqrt(distance / count)  # [0, 5]
    else:
        distance = 5.5  # if 2 users have a same movie, the greatest distance is 5
 
    return distance  # the smaller, the more similar
 
# compute the similarity with other users
def top10_simliar(userID):
    res = []
    for userid in data.keys():
        if not userid == userID:
            simliarity = Euclidean(userID,userid)
            res.append((userid, simliarity))
    res.sort(key=lambda val:val[1])
    return res[:10]
 
res = top10_simliar('1')
print(res)

def recommend(user):
    top_sim_user = top10_simliar(user)[0][0]
    items = data[top_sim_user]
    recommendations = []
    # recommend movies the user did not watch
    for item in items.keys():
        if item not in data[user].keys():
            recommendations.append((item, items[item]))
    recommendations.sort(key=lambda val:val[1], reverse=True)
    return recommendations[:10]  # return 10 movies with highest ratings
 
Recommendations = recommend('1')
print(Recommendations)