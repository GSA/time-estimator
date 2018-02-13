import csv
from collections import Counter
from datetime import datetime
from git import Repo
from os.path import dirname, join, realpath
from random import random, shuffle
from subprocess import check_output
import time

from config import *


def split_data():

    with open(data_path) as f:
        
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        training_file = open(training_path, "w")
        training_file_writer = csv.DictWriter(training_file, fieldnames=fieldnames)
        training_file_writer.writeheader()
        
        testing_file = open(testing_path, "w")
        testing_file_writer = csv.DictWriter(testing_file, fieldnames=fieldnames)
        testing_file_writer.writeheader()
        
        for line in reader:
            if random() > 0.2:
                training_file_writer.writerow(line)
            else:
                testing_file_writer.writerow(line)
                
split_data()