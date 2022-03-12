from collections import defaultdict
import csv
import json

rounds = []
competitors = {}

with open('data/mazalaleague_s1/rounds.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rounds.append(row['ID'])

with open('data/mazalaleague_s1/competitors.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        competitors[row['ID']] = {'name': row['Name'], 'submissions': {}, 'votes' : {}}
        for round_id in rounds:
            competitors[row['ID']]['votes'][round_id] = []

with open('data/mazalaleague_s1/submissions.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        competitors[row['Submitter ID']]['submissions'][row['Round ID']] = row['Spotify URI']

with open('data/mazalaleague_s1/votes.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        competitors[row['Voter ID']]['votes'][row['Round ID']].append({'song': row['Spotify URI'], 'points': row['Points Assigned']})



#print(rounds) 


#print(competitors['43c8053c706643709c37d432b5118001'])

print(json.dumps(competitors['43c8053c706643709c37d432b5118001'], indent = 4)) 