# needed for end= print syntax
from __future__ import print_function
from pprint import pprint
from sklearn.metrics import mean_squared_error
import numpy as np
import math
import sys
import os

__author__ = 'Andrew Watts'
__Python__ = '2.7.11'
__version__ = '1.3'
__email__ = 'wattsap@appstate.edu'
__usage__ = 'python filename.py test.npy'


class Movie_Rating:
    '''
    @function: init
    @param filename: npy filename to load
    '''

    def __init__(self, filename):
        self.json_data = None
        self.m = 0
        self.x = []
        self.user_avg_rate = []
        self.train_test = None
        if os.path.isfile(filename) and filename.endswith('.npy'):
            self.data = np.load(filename)
            index = np.lexsort(self.data[:, :2].T)
            self.data = self.data[index, :]
            self.num_movies = np.max(self.data[:, 1], axis=0) + 1
            h = np.zeros((self.num_movies, 1))
            k0 = 0
            for j in range(self.num_movies):
                print('%5.1f%%' % (100 * j / self.num_movies), end='\r')
                k1 = k0 + 1
                while k1 < len(self.data) and self.data[k1, 1] == j:
                    k1 += 1
                h[j] = np.mean(self.data[k0:k1, 2])
                k0 = k1
        else:
            sys.exit('File corruption. Be sure file exists\n'
                     'and it is a .npy file\n')

    '''
    @function gabe_movie ratings: implementation of gabes method for user ratings
    @author: Andrew Watts based on Gabe Mercer's code
    '''

    def gabe_movie_rating(self):
        movies = {}
        idx = 0
        ratings = 0
        ratings_count = 0

        for row in self.data:
            movie = row[1]
            movie_idx = self.data[idx][1]
            idx += 1
            if movie not in movies:
                ratings = 0
                ratings_count = 0
                ratings += row[2]
                movies[movie] = ratings
                ratings_count += 1
            else:
                ratings += row[2]
                ratings_count += 1
                movies[movie] = ratings

            if (movie_idx + 1 is not movie):
                movies[movie] = ratings / ratings_count
        pprint(movies)

    '''
    @function gabe_user_rating: finds rating for each user
    @author: Gabe Mercer
    '''

    def gabe_user_rating(self):
        users = {}
        index = 0
        total = 0
        divide = 0
        for row in self.data:
            person = row[0]
            check = self.data[index][0]
            index += 1
            if (person not in users):
                total = 0
                divide = 0
                total += row[2]
                users[person] = total
                divide += 1
            else:
                total += row[2]
                divide += 1
                users[person] = total

            if (check + 1 is not person):
                users[person] = total / divide
        pprint(users)

    '''
    @function movie_rating_test: gets the rating for many movies
    @param test_length: number of indices to test
    @param test: boolean to determine if testing portion or whole
    '''

    def movie_rating_test(self, test_length, test):
        for i in range(self.num_movies):
            if test is True:
                if i == test_length:
                    break
            print(self.one_average_movie_rating(i))

    '''
    @function: user_rating_test
    @param test_length: number of indices to test
    @param test: boolean to determine if testing portion or whole
    '''

    def user_rating_test(self, test_length, test):
        x = self.data[0, :]
        for i in range(self.num_movies):
            if test is True:
                if i == test_length:
                    break
            self.user_avg_rate = None * len(self.data)
            for i in range(len(self.data)):
                if i + 1 == x:
                    self.user_avg_rate[i] = (self.one_average_user_rating(i))

    '''
    @function one_average_rating: gets the rating for one movie
    @param movie_idx: index of movie to get
    '''

    def one_average_movie_rating(self, movie_idx):
        movie_rating0 = 0.00
        movie_rating_user_count = 0.00

        for i in range(len(self.data)):
            if self.data[i, 1] == movie_idx:
                movie_rating0 += self.data[i, 2]
                movie_rating_user_count += 1
        if movie_rating_user_count > 0:
            return float(movie_rating0 / movie_rating_user_count)
        return -1

    '''
    @function: one_average_user_rating
    @param user_idx: user index number
    '''

    def one_average_user_rating(self, user_idx):
        user_avg_rating = 0.00
        user_rate_count = 0.00

        for i in range(len(self.data)):
            if self.data[i, 0] == user_idx:
                user_avg_rating += self.data[i, 2]
                user_rate_count += 1
        if user_rate_count > 0:
            return float(user_avg_rating / user_rate_count)
        return -1

    '''
    @function average_all_ratings: gets average of all movie ratings
    '''

    def average_all_movie_ratings(self):
        movie_ratings = 0.00
        total_rates = 0.00
        for i in range(len(self.data)):
            movie_ratings += self.data[i, 2]
            total_rates += 1
        return movie_ratings / total_rates

    '''
    @shitty testing suite: Dont judge me!
    - options for single index rating or multi-indice ratings
    - choose how many indices you want, or all of them
    '''

    def test(self):
        num = raw_input(
            'hello, choose one of the following: 1 for one movie rating, ' +
            '2 for all movie ratings, or 3 for one user rating, ' +
            'or 4 for all user ratings, or 5 for an average of all ratings, ' +
            'or 6 for gabes user rating implementation, ' +
            'or  7 for gabes movie rating implementation, or 8 for RMSE ratings!: ')

        if num == '1':
            num2 = raw_input('What movie index would you like to look at?: ')
            print(self.one_average_movie_rating(int(num2)))
        elif num == '2':
            num3 = raw_input(
                'Enter 1 to Run full test, or 2 to Run partial test: ')
            if num3 == '1':
                self.movie_rating_test(80000, False)
            elif num3 == '2':
                num4 = raw_input('How many indices would you like?: ')
                self.movie_rating_test(int(num4), True)
            else:
                print('Read options better next time!')
        elif num == '3':
            num5 = raw_input('What user index would you like to look at?: ')
            print(self.one_average_user_rating(int(num5)))
        elif num == '4':
            num6 = raw_input(
                'Enter 1 to run full test, or 2 to run partial test: ')
            if num6 == '1':
                self.user_rating_test(20000, False)
            elif num6 == '2':
                num7 = raw_input('How many indices would you like?: ')
                self.user_rating_test(int(num7), True)
        elif num == '5':
            print('Total average rating: %0.2f\n' %
                  self.average_all_movie_ratings())
        elif num == '6':
            self.gabe_user_rating()
        elif num == '7':
            self.gabe_movie_rating()
            '''
        elif num == '8':
            num8 = raw_input(
                'Enter test type, choose 1 for R = m, 2 for R = m+b, ' +
                '3 for R = m+a, 4 for R = m+a+b, or 5 for R=S: ')
            print(self.Root_mean(int(num8)))
            '''
        else:
            print('goodbye')

    '''
    @function concat_array: concatenates two np.arrays together
    @param filename: filename for np.array to be concatenated to 
    original filename np.array
    '''

    def concat_array(self, filename):
        array2 = np.load(filename)
        self.data = np.concatenate((self.data, array2), axis=0)

    '''
    @function train_m: gets the m value, a.k.a. the average of all movie
    ratings
    '''

    def train_m(self):
        self.m = self.average_all_movie_ratings()

    '''
    @function test_m: gets the RMSE from r-hat
    '''

    def test_m(self):
        rms = math.sqrt(mean_squared_error(self.data[:, 2], self.x))
        return float('{0:.4f}'.format(rms))

    '''
    @function predict_m: creation of r-hat with m
    '''

    def predict_m(self):
        for i in range(len(self.data[:, 2])):
            self.x.append(self.m)
        self.x = np.array(self.x)

    '''
    @function predict_m_b: creation of r-hat with m + b
    '''

    def predict_m_b(self):
        n = self.data[:, 2].copy()
        for i in range(len(self.data[:, 2])):
            if self.m + (self.m - n[i]) > 5.0:
                self.x.append(5)
            elif self.m + (self.m - n[i]) <= 0:
                self.x.append(1.0)
            else:
                self.x.append(self.m + (self.m - n[i]))
        self.x = np.array(self.x)

    '''
    @function predict_m_b_u: creation of r-hat with m + b + u
    '''

    def predict_m_b_u(self):
        n = self.data[:, 2].copy()
        for i in range(len(self.data[:, 2])):
            if self.m + (self.m - n[i]) > 4.0:
                self.x.append(1.9)
            elif self.m + (self.m - n[i]) <= 0:
                self.x.append(1.0)
            else:
                self.x.append(self.m + (self.m - n[i] + 1.0) + 0.19 + 0.5)
        self.x = np.array(self.x)

    '''
    @function predict_m_b_a: creation of r-hat with m + a + b
    - utter failure
    '''

    def predict_m_b_a(self):
        n = self.data[:, 2].copy()
        for i in range(len(self.data[:, 2])):
            if self.m + (self.m - n[i]) + (self.user_avg_rate[i] - n[i]) > 5.0:
                self.x.append(5.0)
            elif self.m + (self.m - n[i]) <= 0:
                self.x.append(1.0)
            else:
                self.x.append(self.m + (self.m - n[i]) + (self.user_avg_rate[i]
                                                          - n[i]))
        self.x = np.array(self.x)


if len(sys.argv) == 2:
    b = Movie_Rating(sys.argv[1])
else:
    b = raw_input('Enter the name of the data file: ')

#b.test()
#b.concat_array('test.npy')
#b.concat_array('test_small_10.npy')
b.train_m()
#print(b.data)
#print(b.data[:, 2])
#print(b.m)
#b.predict_m()
b.predict_m()
#b.predict_m_b_a()
#print(b.x)
print(b.test_m())
#b.print_validate()
