from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from flask import jsonify


main_bp = Blueprint('main', __name__)

# SQLite database file
database_file = 'pro_mma_data.db'

@main_bp.route('/')
def index():
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Retrieve information about each event and group by event_title
    cursor.execute('''
        SELECT
            event_title,
            organisation,
            COUNT(*) AS TotalFights,
            ROUND(AVG(round), 2) AS AverageRounds,
            MAX(time) AS LongestFightTime
        FROM fights
        GROUP BY event_title, organisation
        ORDER BY date DESC LIMIT 15
    ''')

    event_info = cursor.fetchall()
    event_columns = ['Event Title', 'Organisation', 'Total Fights', 'Average Rounds', 'Longest Fight Time']

    # Retrieve fighter rankings
    cursor.execute('''
        SELECT 
            fighter_name,
            nickname,
            age,
            weight_class,
            wins,
            losses,
            win_percentage
        FROM fighters 
        ORDER BY wins DESC LIMIT 20
    ''')
    fighter_rankings = cursor.fetchall()
    fighters_columns = ['Fighter Name', 'Nickname', 'Age', 'Weight Class', 'Wins', 'Losses', 'Win Percentage']

    # Close the database connection
    conn.close()

    return render_template('index.html', event_info=event_info, event_columns=event_columns,
                           fighter_rankings=fighter_rankings, fighters_columns=fighters_columns)

@main_bp.route('/fighter/<fighter_name>')
def fighter_details(fighter_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Retrieve fighter details
    cursor.execute('SELECT * FROM fighters WHERE fighter_name = ?', (fighter_name,))
    fighter_details = cursor.fetchone()
    columns = ['Fighter Name', 'Nickname', 'Birth Date', 'Age', 'Death Date',
       'Location', 'Country', 'Height', 'Weight', 'Association',
       'Weight Class', 'Wins', 'Wink by KO', 'Wins by Submission', 'Wins by Decision',
       'Wins Other', 'Losses', 'Losses by KO', 'Losses by Submission',
       'Losses by Decision', 'Losses Other', 'Height (cm)', 'Weight (kg)',
       'Win Percentage', 'BMI', 'Submission Ratio', 'KO Ratio',
       'Decision Ratio']

    # Retrieve fighter's latest fights
    cursor.execute('SELECT * FROM fights WHERE fighter1_name = ? OR fighter2_name = ? ORDER BY date DESC LIMIT 10',
                   (fighter_name, fighter_name))
    fighter_latest_fights = cursor.fetchall()
    fights_columns = ['Id', 'Event Name', 'Organisation', 'Date', 'Location', 'Match Nr.', 'Fighter 1 Name', 'Fighter 2 Name', 'Fighter 1 Result', 'Fighter 2 Result', 'Win Method', 'Win Details', 'Referee', 'Round', 'Time']

    # Close the database connection
    conn.close()

    return render_template('fighter_details.html', fighter_details=fighter_details, columns=columns,
                           fighter_latest_fights=fighter_latest_fights, fights_columns=fights_columns)

@main_bp.route('/fighter_rankings', methods=['GET', 'POST'])
def fighter_rankings():
    return 404

@main_bp.route('/event/<event_title>')
def event_details(event_title):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT
            event_title,
            organisation,
            COUNT(*) AS TotalFights,
            ROUND(AVG(round), 2) AS AverageRounds,
            ROUND(AVG(time)) AS AverageTime,
            MAX(time) AS LongestFightTime
        FROM fights
        GROUP BY event_title, organisation
        ORDER BY date DESC LIMIT 20
    ''')
    event_details = cursor.fetchall()
    event_columns = ['Event Name', 'Organisation', 'Total Fights', 'Avg. Rounds', 'Avg. Time', 'Max Fight Time']

    # Retrieve fights for the event
    cursor.execute('SELECT * FROM fights WHERE event_title = ? ORDER BY date ASC', (event_title,))
    event_fights = cursor.fetchall()
    fights_columns = ['Id', 'Event Name', 'Organisation', 'Date', 'Location', 'Match Nr.', 'Fighter 1 Name', 'Fighter 2 Name', 'Fighter 1 Result', 'Fighter 2 Result', 'Win Method', 'Win Details', 'Referee', 'Round', 'Time']


    # Close the database connection
    conn.close()

    return render_template('event_details.html', event_details=event_details, event_columns=event_columns ,event_fights=event_fights, fights_columns=fights_columns)

@main_bp.route('/filter_events', methods=['GET'])
def filter_events():
    if request.method == 'GET':
        # Handle AJAX request and return filtered data
        event_name_filter = request.args.get('event_name')
        search_term_filter = request.args.get('search_term')

        # Connect to the SQLite database
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # Perform filtering logic and retrieve filtered data
        cursor.execute('''
            SELECT
                event_title,
                organisation,
                COUNT(*) AS TotalFights,
                ROUND(AVG(round), 2) AS AverageRounds,
                MAX(time) AS LongestFightTime
            FROM fights
            WHERE event_title LIKE ? AND organisation LIKE ?
            GROUP BY event_title, organisation
            ORDER BY date DESC LIMIT 15
        ''', ('%' + event_name_filter + '%', '%' + search_term_filter + '%'))

        filtered_data = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Return filtered data as JSON
        return jsonify(filtered_data)

@main_bp.route('/filter_fighters', methods=['GET'])
def filter_fighters():
    if request.method == 'GET':
        fighter_name_filter = request.args.get('fighter_name')
        association_name_filter = request.args.get('association_name')

        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                fighter_name,
                nickname,
                age,
                weight_class,
                wins,
                losses,
                win_percentage
            FROM fighters
            WHERE fighter_name LIKE ? OR association LIKE ?
            ORDER BY wins DESC LIMIT 20
            ''', ('%' + fighter_name_filter + '%', '%' + association_name_filter + '%'))
        
        filtered_data = cursor.fetchall()

        conn.close()

        # Return filtered data as JSON
        return jsonify(filtered_data)