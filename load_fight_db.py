import sqlite3
import csv

# SQLite database file
database_file = 'pro_mma_data.db'

# CSV files to import
fighters_csv = 'data/fighter_data_clean.csv'
fights_csv = 'data/fight_data_clean.csv'

# Connect to the SQLite database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fighters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fighter_name TEXT NOT NULL,                    
        nickname TEXT NULL,
        birth_date DATE NULL,
        age INTEGER NULL,
        death_date DATE NULL,
        location TEXT NULL,
        country TEXT NULL,
        height REAL NOT NULL,
        weight REAL NOT NULL,
        association TEXT NOT NULL,
        weight_class TEXT NULL,
        wins INTEGER NOT NULL,
        wins_ko INTEGER NOT NULL,
        wins_submission INTEGER NOT NULL,
        wins_decision INTEGER NOT NULL,
        wins_other INTEGER NUT NULL,
        losses INTEGER NOT NULL,
        losses_ko INTEGER NOT NULL,
        losses_submission INTEGER NOT NULL,
        losses_decision INTEGER NOT NULL,
        losses_other INTEGER NOT NULL,
        height_cm REAL NOT NULL,
        weight_kg REAL NOT NULL,
        win_percentage REAL NOT NULL,
        bmi REAL NULL,
        submission_ratio REAL NULL,
        ko_ratio REAL NULL,
        decision_ratio REAL NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS fights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_title TEXT,
        organisation TEXT NOT NULL,
        date DATE NOT NULL,
        location TEXT NOT NULL,
        match_nr INTEGER NOT NULL,
        fighter1_name TEXT NOT NULL,
        fighter2_name TEXT NOT NULL,
        fighter1_result TEXT NOT NULL,
        fighter2_result TEXT NOT NULL,
        win_method TEXT NOT NULL,
        win_details TEXT NOT NULL,
        referee TEXT NULL,
        round INTEGER NOT NULL,
        time TEXT NOT NULL
    )
''')


# Read data from fighters CSV and insert into the fighters table
with open(fighters_csv, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        cursor.execute('''
            INSERT INTO fighters (
                fighter_name, nickname, birth_date, age, death_date,
                location, country, height, weight, association, weight_class,
                wins, wins_ko, wins_submission, wins_decision,
                wins_other, losses, losses_ko, losses_submission,
                losses_decision, losses_other, height_cm, weight_kg, 
                win_percentage, bmi, submission_ratio, ko_ratio, decision_ratio
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['fighter_name'], row['nickname'], row['birth_date'], row['age'], row['death_date'],
            row['location'], row['country'], row['height'], row['weight'], row['association'],
            row['weight_class'], row['wins'], row['wins_ko'], row['wins_submission'], row['wins_decision'],
            row['wins_other'], row['lossess'], row['losses_ko'], row['losses_submission'],
            row['losses_decision'], row['losses_other'], row['height(cm)'], row['weight(kg)'], 
            row['win_percentage'], row['bmi'], row['submission_ratio'], row['ko_ratio'], row['decision_ratio']
        ))

# Read data from fights CSV and insert into the fights table
with open(fights_csv, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        cursor.execute('''
            INSERT INTO fights (
                event_title, organisation, date, location, match_nr,
                fighter1_name, fighter2_name, fighter1_result, fighter2_result,
                win_method, win_details, referee, round, time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['event_title'], row['organisation'], row['date'], row['location'], row['match_nr'],
            row['fighter1_name'], row['fighter2_name'], row['fighter1_result'], row['fighter2_result'],
            row['win_method'], row['win_details'], row['referee'], row['round'], row['time']
        ))

# Commit changes and close connection
conn.commit()
conn.close()
