import csv
import sys
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
rounds = []
competitors = {}

league_name = 'mazala-q5'
if len(sys.argv) > 1:
    league_name = sys.argv[1]

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
            competitors[row['ID']]['votes'][round_id] = {}
        G.add_node(row['Name'])

with open(f"data/{league_name}/submissions.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        competitors[row['Submitter ID']]['submissions'][row['Round ID']] = row['Spotify URI']

with open(f"data/{league_name}/votes.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        competitors[row['Voter ID']]['votes'][row['Round ID']][row['Spotify URI']] = int(row['Points Assigned'])

for competitor in competitors.values():
    biggest_fans = {}
    score = 0
    # loop through all the other players and see if they voted for this person's songs
    for possible_fan in competitors.values():
        if competitor['name'] != possible_fan['name']:
            biggest_fans[possible_fan['name']] = 0

            for round in rounds:
                for votes_in_round in possible_fan['votes'][round]:
                    #first check if the competitor even submitted a song this round
                    if round in competitor['submissions']:
                        # ok great they did submit, so see if possible fan voted for their selection    
                        if competitor['submissions'][round] == votes_in_round:
                            points_received = possible_fan['votes'][round][votes_in_round]
                            biggest_fans[possible_fan['name']] += points_received
            G.add_edge(possible_fan['name'], competitor['name'], weight=biggest_fans[possible_fan['name']])
    sorted_voting_history = sorted(biggest_fans.items(), key=lambda item: item[1])
    print(f"{competitor['name']},{sorted_voting_history[len(sorted_voting_history)-1]},{sorted_voting_history[0]}")

nx.kamada_kawai_layout(G)
nx.write_gexf(G, 'data/'+league_name+'/'+league_name+'.gexf')
#subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
#subax2 = plt.subplot(122)
#nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()

