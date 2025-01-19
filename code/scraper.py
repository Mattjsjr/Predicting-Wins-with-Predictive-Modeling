from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import csv

def getStandings(standings_table):
    standings = []
    for row in standings_table.find_all('tr'):
        data = [cell.text.strip() for cell in row]  

        # Gets rid of playoff seeding
        if data[0][-1] == 'z' or data[0][-1] == 'y' or data[0][-1] == 'w':
            data[0] = data[0][0:-1]

        # Fixes A's bug
        if data[0] == "Athletics":
            data[0] = "Oakland Athletics"
        
        standings.append(data)
    return standings[1:]

def getStats(table):
    stats = []
    count = 0
    for row in table.find_all('tr'):
        data = [cell.text.strip().replace('\u200c', '') for cell in row]

        double_digit = data[0][:2].isdigit()
        is_header = data[0][0] == 'T'
        if is_header:
            data[0] = data[0][0:4]
        elif not double_digit:
            data[0] = data[0][1:-1]
        else:
            data[0] = data[0][2:-2]

        split_names = data[0].split()
        split_names_length = len(split_names)

        # Handles City Team
        if split_names_length == 2 and count != 0:
            duplicate_name = re.split(r'(?=[A-Z])', split_names[-1])
            duplicate_name.pop(-1)
            data[0] = split_names[0] + ' ' + duplicate_name[-1]

        # Handles City Team Team
        elif split_names_length == 3 and count != 0:
            duplicate_name = re.split(r'(?=[A-Z])', split_names[-1])
            duplicate_name.pop(-1)
            data[0] = split_names[0] + ' ' + split_names[1] + ' ' + duplicate_name[-1]
        
        # Handles City City Team
        elif split_names_length >= 4:
            if split_names[2] == split_names[3] + split_names[1]:
                data[0] = split_names[0] + ' ' + split_names[1] + ' ' + split_names[3]

        stats.append(data)

        if count == 31:
            count = 0
        else:
            count += 1
    return stats[1:]

def sort_combine(stats, pitching, standings):
    standings.sort(key=lambda x: x[0])
    stats.sort(key=lambda x: x[0])
    pitching.sort(key=lambda x: x[0])
    row = 0
    combined = []
    for statRow in stats: 

        if statRow[0] != standings[row][0] or standings[row][0] != pitching[row][0]:
            print("stopped")
            print(statRow[0])
            print(standings[0][0])
            print(pitching[0][0])
        statRow += standings[row]
        statRow += pitching[row]
        combined.append(statRow)
        row+= 1
    return combined

if __name__ == '__main__':

    csv_file = "total_team_stats.csv"

    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        for year in range(2024, 1992, -1):

            url = 'https://mlb.com/stats/team/on-base-percentage'
            pitching_url = 'https://www.mlb.com/stats/team/pitching/wins'
            standings_url = 'https://www.mlb.com/standings/mlb'

            if year != 2024:
                url = url + "/" + str(year)
                standings_url = standings_url + "/" + str(year)
                pitching_url = pitching_url + "/" + str(year)

            standings_response = requests.get(standings_url)
            standings_soup = BeautifulSoup(standings_response.content, 'html.parser')
            standings_div = standings_soup.find('div', {'class': 'tablestyle__TableContainer-sc-wsl6eq-2 gzGGfc'})
            standings_table = standings_div.find('table')

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            div = soup.find('div', {'class': 'table-wrapper-mxbeN3qL'})
            table = div.find('table')

            pitching_response = requests.get(pitching_url)
            pitching_soup = BeautifulSoup(pitching_response.content, 'html.parser')
            pitching_div = pitching_soup.find('div', {'class': 'table-wrapper-mxbeN3qL'})
            pitching_table = pitching_div.find('table')

            standings = getStandings(standings_table)
            stats = getStats(table)
            pitching = getStats(pitching_table)

            combined = sort_combine(stats, pitching, standings)
            
            writer.writerows(combined)

    

    
