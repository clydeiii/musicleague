from collections import defaultdict
import csv
import json

rounds = []
competitors = {}

league_name = 'american-soldier'

print(f"music league data for {league_name}")

with open(f"data/{league_name}/rounds.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rounds.append(row['ID'])

with open(f"data/{league_name}/competitors.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        competitors[row['ID']] = {'name': row['Name'], 'submissions': {}, 'votes' : {}}
        for round_id in rounds:
            competitors[row['ID']]['votes'][round_id] = []

with open(f"data/{league_name}/submissions.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        competitors[row['Submitter ID']]['submissions'][row['Round ID']] = row['Spotify URI']

with open(f"data/{league_name}/votes.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        competitors[row['Voter ID']]['votes'][row['Round ID']].append({'song': row['Spotify URI'], 'points': row['Points Assigned']})

#print(json.dumps(competitors['43c8053c706643709c37d432b5118001'], indent = 4)) 

# find michelle's 'how many points did i assign to each other player and in how many rounds'
for competitor in competitors.values():
    who_they_voted_for = {}
    total_points_assigned = 0
    # loop through all the other players
    for other_player in competitors.values():
        if competitor['name'] != other_player['name']:
            who_they_voted_for[other_player['name']] = [0, 0]
            for round in rounds:
                for votes_in_round in competitor['votes'][round]:
                    if votes_in_round['song'] in other_player['submissions'].values():
                        who_they_voted_for[other_player['name']][0] += int(votes_in_round['points'])
                        total_points_assigned += int(votes_in_round['points'])
                        if(int(votes_in_round['points']) > 0):
                            who_they_voted_for[other_player['name']][1] += 1
    sorted_voting_history = sorted(who_they_voted_for.items(), key=lambda item: item[1])
    print(f"{competitor['name']}'s voting history ({total_points_assigned}): {sorted_voting_history}")

#quit()

# find each competitor's "biggest fan" and "nemesis"
for competitor in competitors.values():
    biggest_fans = {}
    score = 0
    # loop through all the other players and see if they voted for this person's songs
    for possible_fan in competitors.values():
        if competitor['name'] != possible_fan['name']:
            biggest_fans[possible_fan['name']] = [0, 0]

            for round in rounds:
                for votes_in_round in possible_fan['votes'][round]:
                    if votes_in_round['song'] in competitor['submissions'].values():
                        biggest_fans[possible_fan['name']][0] += int(votes_in_round['points'])
                        score += int(votes_in_round['points'])
                        if(int(votes_in_round['points']) > 0):
                            biggest_fans[possible_fan['name']][1] += 1




    sorted_voting_history = sorted(biggest_fans.items(), key=lambda item: item[1])
    print(f"{competitor['name']}'s voted for history ({score}): {sorted_voting_history}")

    print(f"{competitor['name']}'s biggest fan is {sorted_voting_history[len(sorted_voting_history)-1]} and their nemesis is {sorted_voting_history[0]}")


#print(rounds) 


#print(competitors['43c8053c706643709c37d432b5118001'])

