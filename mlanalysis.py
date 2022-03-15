from collections import defaultdict
import csv
import json
from typing import DefaultDict

rounds = []
competitors = {}
submissions_by_round = {}
round_winners = {}
round_losers = {}

league_name = 'mazalaleague_s1'

print(f"music league data for {league_name}")

with open(f"data/{league_name}/rounds.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rounds.append(row['ID'])
        submissions_by_round[row['ID']] = DefaultDict(int)

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
        competitors[row['Voter ID']]['votes'][row['Round ID']].append({row['Spotify URI']: row['Points Assigned']})
        submissions_by_round[row['Round ID']][row['Spotify URI']] += int(row['Points Assigned'])

for round in rounds:
    round_winners[round] = max(submissions_by_round[round], key=submissions_by_round[round].get)
    round_losers[round] = min(submissions_by_round[round], key=submissions_by_round[round].get)

#print(json.dumps(competitors['43c8053c706643709c37d432b5118001'], indent = 4)) 
#print(json.dumps(round_winners, indent = 4))
#quit()

# get taste maker and taste faker (who most often voted for the "worst" song)
taste_makers = DefaultDict(int)
taste_fakers = DefaultDict(int)
for competitor in competitors.values():
    for round in rounds:
        print(round_winners[round])
        print(competitor['votes'][round])
        if any(round_winners[round] in songs for songs in competitor['votes'][round]):
            taste_makers[competitor['name']] += 1

        if any(round_losers[round] in songs for songs in competitor['votes'][round]):
            taste_fakers[competitor['name']] += 1

print("Taste Maker Scores:")
print(json.dumps(taste_makers, indent = 4))
print("Taste Faker Scores:")
print(json.dumps(taste_fakers, indent = 4))
#quit()

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
                    # first determine if this other player even submitted a song this round
                    if round in other_player['submissions']:
                        # great they did, so now see if that other player's submission was in this round
                        if any(other_player['submissions'][round] in song for song in votes_in_round):
                            votes_for_song = int(votes_in_round[other_player['submissions'][round]])
                            who_they_voted_for[other_player['name']][0] += votes_for_song
                            total_points_assigned += votes_for_song
                            if(votes_for_song > 0):
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
                    #first check if the competitor even submitted a song this round
                    if round in competitor['submissions']:
                        # ok great they did submmit, so see if possible fan voted for their selection    
                        if any(competitor['submissions'][round] in song for song in votes_in_round):
                            points_received = int(votes_in_round[competitor['submissions'][round]])
                            biggest_fans[possible_fan['name']][0] += points_received
                            score += points_received
                            if(points_received > 0):
                                biggest_fans[possible_fan['name']][1] += 1 # tally how rounds they voted for this person (regardless of points assigned)
    sorted_voting_history = sorted(biggest_fans.items(), key=lambda item: item[1])
    print(f"{competitor['name']}'s voted for history ({score}): {sorted_voting_history}")
    print(f"{competitor['name']}'s biggest fan is {sorted_voting_history[len(sorted_voting_history)-1]} and their nemesis is {sorted_voting_history[0]}")


#print(rounds) 


#print(competitors['43c8053c706643709c37d432b5118001'])

