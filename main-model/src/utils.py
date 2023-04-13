'''
Utility Class chứa các function tiện ích
'''

import pandas as pd
import numpy as np
import random
import constants as const


class Util(object):

    '''
    # Mục đích của ratings
    => tham gia vào clean_subset và preprocess để tạo ra train
    => tham gia vào hàm calculate_scores trong RBM
    '''
    def read_data(self, dir, filename):
        print("Reading the data")
        data = pd.read_json(dir + filename, orient='records')
        return data


    '''
    Function to clean and subset the data according    
    to individual machine power
    '''
    def clean_subset(self, ratings, num_rows):
        print("Extracting num_rows from ratings")
        temp = ratings.sort_values(by=['user_id'], ascending=True)
        ratings = temp.iloc[:num_rows, :]
        return ratings


    '''
    Tiền xử lý dữ liệu "rating"
    Preprocess data for feeding into the network
    '''
    def preprocess(self, ratings):
        print("Preprocessing the dataset")
        unique_att = ratings.attraction_id.unique()
        unique_att.sort()
        att_index = [i for i in range(len(unique_att))]
        rbm_att_df = pd.DataFrame(list(zip(att_index,unique_att)), columns =['rbm_att_id','attraction_id'])

        joined = ratings.merge(rbm_att_df, on='attraction_id')
        joined = joined[['user_id','attraction_id','rbm_att_id','rating']]
        readers_group = joined.groupby('user_id')

        total = []
        for readerID, curReader in readers_group:
            temp = np.zeros(len(ratings))
            for num, book in curReader.iterrows():
                temp[book['rbm_att_id']] = book['rating']/5.0
            total.append(temp)

        return joined, total


    '''
    Function to split into training and validation sets
    '''
    def split_data(self, total_data):
        print("Free energy required, dividing into train and validation sets")
        random.shuffle(list(total_data))
        len_data = len(total_data)
        print("Total size of the data is: {0}".format(len_data))
        size_train = int(len_data * const.RATIO_TRAIN_DATA)
        X_train = total_data[:size_train]
        X_valid = total_data[size_train:]
        print("Size of the training data is: {0}".format(len(X_train)))
        print("Size of the validation data is: {0}".format(len(X_valid)))
        return X_train, X_valid


    '''
    Function to compute the free energy
    '''
    def free_energy(self, v_sample, W, vb, hb):
        wx_b = np.dot(v_sample, W) + hb
        vbias_term = np.dot(v_sample, vb)
        hidden_term = np.sum(np.log(1 + np.exp(wx_b)), axis = 1)
        return -hidden_term - vbias_term
