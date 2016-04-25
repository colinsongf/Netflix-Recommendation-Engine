import numpy as np
import json
import time
#import Movie_rating.py as mv
from pprint import pprint


class Netflix():
    def __init__(self, filename):
        self.users = []
        self.m = 0.0
        self.avgOneMovie = {}
        self.s = []
        self.data = np.load(filename)
        #self.dataG = json.load(filename)
        self.U = {}
        self.V = {}
        self.num_movies = np.max(self.data[:, 1], axis=0) + 1

    def one_average_user_rating(self, user_idx):
        user_avg_rating = 0.00
        user_rate_count = 0.00
        for i in range(len(self.data)):
            if self.data[i, 0] == user_idx:
                user_avg_rating += self.data[i, 2]
                user_rate_count += 1
        if (user_rate_count == 0):
            return (user_idx, 0)
        return (user_idx, float(user_avg_rating / user_rate_count))

    def user_rating_test(self):
        for i in range(self.num_movies):
            self.users.append(self.one_average_user_rating(i))

    def gabeUserRating(self):
        #data = np.load("train_small_10.npy")
        #test = np.load("test.npy")
        index = 0
        rowNum = 0
        total = 0
        divide = 0
        #person = data[0][0]
        #pprint(data)
        for row in self.data:
            person = row[0]
            check = self.data[index][0]
            index += 1
            #pprint(check)

        if (person not in self.users):
            total = 0
            divide = 0
            total += row[2]
            self.users[person] = total
            divide += 1
        else:
            total += row[2]
            divide += 1
            self.users[person] = total

        if (check + 1 is not person):
            self.users[person] = total / divide
        #return self.users[usr_idx]

    def average_all_movie_ratings(self):
        data = np.load("train_small_10.npy")
        movie_ratings = 0.00
        total_rates = 0.00
        for i in range(len(data)):
            movie_ratings += data[i, 2]
            total_rates += 1
        self.m = movie_ratings / total_rates

    def user_movie_rating(self, user_idx):
        user_movie_rat = []
        for i in self.data:
            if i[0] == user_idx:
                user_movie_rat.append(i[0:3])
        return user_movie_rat

    def genrePredict(self):
        #horrorAvg = 0.0
        #horrorCount = 0
        for i in (self.dataG):
            if i["genre"] == 'horror':

                # for this method i think this is how we should go about it:
                # we need to figure out how to get the average for a single user for each genre.  Like get the
                # average they gave for fantasy, horror, extc.. and then compare the averages to see which one is higher.
                #assign a 1 to the highest and store it into the U dictionary for that user.  ALso find the lowest genre the user
                # rated and assign it a -1 all the genres in between these two assign -.5 or .5 according to there postion.  I will
                # be on later text or call me if you need me to explain this more
                pass

    def one_average_movie_rating(self, movie_idx):
        data = np.load("train_small_10.npy")
        movie_rating0 = 0.00
        movie_rating_user_count = 0.00

        for i in range(len(data)):
            if data[i, 1] == movie_idx:
                movie_rating0 += data[i, 2]
                movie_rating_user_count += 1

        print('movie index: %d' % movie_idx)
        print('number of ratings movie has received: %d' %
              movie_rating_user_count)
        print('total rating: %d' % movie_rating0)
        if movie_rating_user_count == 0:
            print('Not yet rated by users.\n')
        else:
            print('average rating this movie gets: %0.2f\n' %
                  float(movie_rating0 / movie_rating_user_count))
        OneM = float(movie_rating0 / movie_rating_user_count)
        return OneM

    def sMatrix(self):
        user_idx = 1
        user_count = 0
        movie_count = 0
        movie_idx = []
        self.user_rating_test()
        #userMovie = get_user_movie_count()
        user = self.get_user_movie_count()[0]
        movie = self.get_user_movie_count()[1]
        self.s = np.array(self.s)
        self.s = np.zeros((user, movie))
        for i in self.data:
            movie_idx.append(self.user_movie_rating(user_idx)[0][1])
            if (self.user_movie_rating(user_idx) == -1):
                self.s[user_idx][movie_idx] = 0
            else:
                self.s[user_idx][movie_idx] = self.rEquation(
                    self.user_movie_rating(user_idx), user_idx)
            if self.user_movie_rating(user_idx + 1)[0][0] > user_idx and (
                    user_idx + 1) < len(self.user_movie_rating()):
                user_idx += 1

    def rEquation(self, userRate, user_idx):
        #print(type(userRate))
        deltaA = self.m - userRate[user_idx][2]
        deltaB = self.users[user_idx] - userRate[user_idx][2]
        r = self.m + deltaA + deltaB
        sValue = r - self.m - deltaA - deltaB
        return sValue

    def get_user_movie_count(self):
        users = []
        movies = []
        for row in self.data:
            user = row[0]
            movie = row[1]
            if user not in users:
                users.append(user)
            if movie not in movies:
                movies.append(movie)
        return (len(users), len(movies))


n = Netflix('test_small_10.npy')
#n.sMatrix()
#print(n.s)
print(type(n.user_movie_rating()))
#print(n.user_movie_rating(1)[0][0])
#print(n.user_movie_rating(1)[1])
#print(n.user_movie_rating(1, 78))
#print(n.get_user_movie_count()[1])
#print(n.data)
