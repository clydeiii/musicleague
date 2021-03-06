import csv
import sys
from typing import DefaultDict

rounds = []
competitors = {}
submissions_by_round = {}
round_winners = {}
round_losers = {}

league_name = 'mazala-q3'
if len(sys.argv) > 1:
    league_name = sys.argv[1]

print(f"music league data for {league_name}")

with open(f"data/{league_name}/rounds.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rounds.append(row['ID'])
        submissions_by_round[row['ID']] = DefaultDict(int)

with open(f"data/{league_name}/competitors.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        competitors[row['ID']] = {'name': row['Name'], 'submissions': {}, 'votes' : {}, 'chatty_score': 0, 'sheep_score': 0, 'picky_score': 0, 'taste_maker': 0, 'taste_faker': 0}
        for round_id in rounds:
            competitors[row['ID']]['votes'][round_id] = {}

with open(f"data/{league_name}/submissions.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        competitors[row['Submitter ID']]['submissions'][row['Round ID']] = row['Spotify URI']

with open(f"data/{league_name}/votes.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if int(row['Points Assigned']) > 0: 
            competitors[row['Voter ID']]['votes'][row['Round ID']][row['Spotify URI']] = int(row['Points Assigned'])
            competitors[row['Voter ID']]['picky_score'] += 1 # award them a picky point for voting for a song
        else: 
            competitors[row['Voter ID']]['chatty_score'] += 1 # if they awarded 0 points it means they left a comment but no points, give them chatty points
        # award points to this submission for this particular round
        submissions_by_round[row['Round ID']][row['Spotify URI']] += int(row['Points Assigned'])

# use the number of points assigned to each submission for each round to determine the winner and loser (ignore ties)
for round in rounds:
    round_winners[round] = max(submissions_by_round[round], key=submissions_by_round[round].get)
    round_losers[round] = min(submissions_by_round[round], key=submissions_by_round[round].get)

print("\nchatty score is the number of times you left a comment on a song you awarded zero points to")
for competitor in competitors.values():
    print(f"{competitor['name']}'s chatty score: {competitor['chatty_score']}")

print("\npicky score is the number of times you awarded a song any number of points (the lower the score, the pickier)")
for competitor in competitors.values():
    print(f"{competitor['name']}'s picky score: {competitor['picky_score']}")


# get taste maker and taste faker (who most often voted for the "best" and "worst" songs)
for competitor in competitors.values():
    for round in rounds:
        # did they vote for the first place song?
        if any(round_winners[round] in songs for songs in competitor['votes'][round]):
            competitor['taste_maker'] += competitor['votes'][round][round_winners[round]] #give them taste maker points equal to the amount of votes they gave the winning song
        # did they vote for the last place song?
        if any(round_losers[round] in songs for songs in competitor['votes'][round]):
            competitor['taste_faker'] += competitor['votes'][round][round_losers[round]]
        # loop through all of the song submisisons this round and award this competitor sheep points for voting with others
        for submission in submissions_by_round[round]:
            # did this user vote for this submission?
            if submission in competitor['votes'][round]:
                # sheep score = all points given this round to this submisison multiplied by how many points this person gave it
                # example: a song is awarded 20 points this round and this user gave it 5, therefore it adds 100 to their sheep score
                competitor['sheep_score'] += submissions_by_round[round][submission] * competitor['votes'][round][submission] 

print("\nsheep score is how often you voted with the herd")
for competitor in competitors.values():
    print(f"{competitor['name']}'s sheep score: {competitor['sheep_score']}")

print('\nmost influential = (1/picky) x sheep x tastemaker')
for competitor in competitors.values():
    print(f"{competitor['name']}'s influence score score: {1/competitor['picky_score'] * competitor['sheep_score'] * competitor['taste_maker']}")


print("\nTaste Maker Scores (who most often voted for the best song):")
for competitor in competitors.values():
    print(f"{competitor['name']}'s TasteMaker score: {competitor['taste_maker']}")
print("\nTaste Faker Scores (who most often voted for the worst song):")
for competitor in competitors.values():
    print(f"{competitor['name']}'s taste faker: {competitor['taste_faker']}")


# find 'how many points did i assign to each other player and in how many rounds'
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
                        if other_player['submissions'][round] == votes_in_round:
                            votes_for_song = competitor['votes'][round][votes_in_round]
                            who_they_voted_for[other_player['name']][0] += votes_for_song
                            total_points_assigned += votes_for_song
                            if(votes_for_song > 0):
                                who_they_voted_for[other_player['name']][1] += 1
    sorted_voting_history = sorted(who_they_voted_for.items(), key=lambda item: item[1])
    #print(f"{competitor['name']}'s voting history ({total_points_assigned}): {sorted_voting_history}")

#quit()

# find each competitor's "biggest fan" and "nemesis"
print("\nbiggest fan and nemesis")
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
                        # ok great they did submit, so see if possible fan voted for their selection    
                        if competitor['submissions'][round] == votes_in_round:
                            points_received = possible_fan['votes'][round][votes_in_round]
                            biggest_fans[possible_fan['name']][0] += points_received
                            score += points_received
                            if(points_received > 0):
                                biggest_fans[possible_fan['name']][1] += 1 # tally how rounds they voted for this person (regardless of points assigned)
    sorted_voting_history = sorted(biggest_fans.items(), key=lambda item: item[1])
    #print(f"{competitor['name']}'s voted for history ({score}): {sorted_voting_history}")
    print(f"{competitor['name']}'s biggest fan is {sorted_voting_history[len(sorted_voting_history)-1]} and their nemesis is {sorted_voting_history[0]}")


