import csv

with open('./u.data.csv', newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        print(row)