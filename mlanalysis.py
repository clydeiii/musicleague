import csv

competitors = {}

with open('data/mazalaleague_s1/competitors.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        competitors[row['ID']] = row['Name']

