import os
import re
import zipfile
import csv
import io
import requests
from requests.auth import HTTPBasicAuth

from individual import * 

if (not os.path.exists('./data')):
    os.mkdir('./data')
      
if (not os.path.exists('./saved_data')):
    os.mkdir('./saved_data')

if __name__ == '__main__':

    DATABASE_URL = 'https://dcapswoz.ict.usc.edu/wwwdaicwoz/'
    AUTH_TOKEN = HTTPBasicAuth('daicwozuser', 'Tqiy7T7CD9OBTa1VZ5CLjgni')

    TRAIN_PATH = 'train_split_Depression_AVEC2017.csv'
    TEST_PATH = 'full_test_split.csv'
    DEV_PATH = 'dev_split_Depression_AVEC2017.csv'

    req = requests.get(DATABASE_URL, auth=AUTH_TOKEN, stream=True)
    ind_ids = re.findall('href="(.*?)_P.zip"', str(req.text))

    for id in ind_ids:
        req = requests.get(DATABASE_URL + id + '_P.zip', auth=AUTH_TOKEN, stream=True)
        z = zipfile.ZipFile(io.BytesIO(req.content))
        z.extractall(path='./data/')
    
    train_file = requests.get(DATABASE_URL + TRAIN_PATH, auth=AUTH_TOKEN, stream=True)
    test_file = requests.get(DATABASE_URL + TEST_PATH, auth=AUTH_TOKEN, stream=True)
    dev_file = requests.get(DATABASE_URL + DEV_PATH, auth=AUTH_TOKEN, stream=True)

    with open('./data/train_split.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for line in train_file.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))

    with open('./data/test_split.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for line in test_file.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))

    with open('./data/dev_split.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for line in dev_file.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))

    AudioDataset('train')
    VideoDataset('train')
    TextDataset('train')