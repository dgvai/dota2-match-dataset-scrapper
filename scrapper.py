import requests
import pandas as pd
import glob
import os
import time 

last_match_id = '6547480206' # the last Match ID as OpenAPI documents
NoError = True
CSV_FILE = 'matches.csv'

while NoError:
    response = requests.get(f'https://api.opendota.com/api/publicMatches?less_than_match_id={last_match_id}')
    
    dataset = []
    for match in response.json():
        data = []
        print(f"Scrapping: {match['match_id']}")
        
        data.append(match['match_id'])
        data.append(match['duration'])
        response2 = requests.get(f"https://api.opendota.com/api/matches/{match['match_id']}")
        heroes = {0: [], 1: []}
        try:
            for player in response2.json()['players']:
                team = 0 if player['isRadiant'] else 1
                hero = []
                hero.append(player['hero_id'])
                hero.append(player['kills'])
                hero.append(player['deaths'])
                hero.append(player['assists'])
                heroes[team].append(hero)

            for t in heroes:
                for players in heroes[t]:
                    data.append(players[0])
                    data.append(players[1])
                    data.append(players[2])
                    data.append(players[3])
        except KeyError:
            print(f"Error at: {match['match_id']}")
            NoError = False

        data.append(0 if match['radiant_win'] else 1)
        dataset.append(data)
        time.sleep(1) # keep 1 second delay as OpenAPI documents
        last_match_id = match['match_id']
        
    df = pd.DataFrame(dataset, columns=["Match ID","Duration","rad_hero1_id","rad_hero1_kills","rad_hero1_deaths","rad_hero1_assists","rad_hero2_id","rad_hero2_kills","rad_hero2_deaths","rad_hero2_assists","rad_hero3_id","rad_hero3_kills","rad_hero3_deaths","rad_hero3_assists","rad_hero4_id","rad_hero4_kills","rad_hero4_deaths","rad_hero4_assists","rad_hero5_id","rad_hero5_kills","rad_hero5_deaths","rad_hero5_assists","dir_hero1_id","dir_hero1_kills","dir_hero1_deaths","dir_hero1_assists","dir_hero2_id","dir_hero2_kills","dir_hero2_deaths","dir_hero2_assists","dir_hero3_id","dir_hero3_kills","dir_hero3_deaths","dir_hero3_assists","dir_hero4_id","dir_hero4_kills","dir_hero4_deaths","dir_hero4_assists","dir_hero5_id","dir_hero5_kills","dir_hero5_deaths","dir_hero5_assists","winner"])
    df.to_csv(CSV_FILE, mode='a', index=False, header=False)