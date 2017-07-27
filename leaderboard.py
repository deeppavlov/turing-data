#!/usr/bin/env python3

from scipy.stats import spearmanr
import sys
import json
import csv

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("example: leaderboard.py <labels.csv> [<data.json>]", file=sys.stderr)
    sys.exit(1)

lines = None
if len(sys.argv) == 2:
    lines = sys.stdin.readlines()
    line = "[" + ",".join(lines) + "]"
else:
    with open(sys.argv[2]) as f:
        line = f.read()
data = json.loads(line)

users_bot_flags = {}
for d in data:
    if d['evaluation'][0]['userId'] == 'Alice':
        users_bot_flags[d['dialogId']] = ( (int(d['evaluation'][0]['quality']), int(d['evaluation'][1]['quality'])) )
    else:
        users_bot_flags[d['dialogId']] = ( (int(d['evaluation'][1]['quality']), int(d['evaluation'][0]['quality'])) )

users_bot_predicted_probs = []
users_bot_fact_labaels = []
with open(sys.argv[1], 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        dialog = int(row[0])
        if dialog in users_bot_flags:
            users_bot_fact_labaels.append(users_bot_flags[dialog][0])
            users_bot_predicted_probs.append(float(row[1]))

            users_bot_fact_labaels.append(users_bot_flags[dialog][1])
            users_bot_predicted_probs.append(float(row[2]))
        else:
            print("dialog %s not in dataset" % dialog, file=sys.stderr)

assert len(users_bot_flags) == len(users_bot_fact_labaels) // 2 == len(users_bot_predicted_probs) // 2

print(sys.argv[1], ": ", spearmanr(users_bot_fact_labaels, users_bot_predicted_probs).correlation)

