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

#print(json.dumps(competitors['43c8053c706643709c37d432b5118001'], indent = 4)) 

# find each competitor's "biggest fan" and "nemesis"
for competitor in competitors.values():
    biggest_fans = {}
    # loop through all the other players and see if they voted for this person's songs
    for possible_fan in competitors.values():
        if competitor['name'] != possible_fan['name']:
            biggest_fans[possible_fan['name']] = 0 
            for round in rounds:
                for votes_in_round in possible_fan['votes'][round]:
                    if votes_in_round['song'] in competitor['submissions'].values():
                        biggest_fans[possible_fan['name']] += int(votes_in_round['points'])

    sorted_fans = sorted(biggest_fans.items(), key=lambda item: item[1])
    print(f"{competitor['name']}'s biggest fan is {sorted_fans[len(sorted_fans)-1]} and their nemesis is {sorted_fans[0]}")



#print(rounds) 


#print(competitors['43c8053c706643709c37d432b5118001'])

