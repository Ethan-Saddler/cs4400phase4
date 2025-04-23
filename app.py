import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
import mysql.connector
import pymysql

app = Flask(__name__)

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_NAME = 'flight_tracking'

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='<enter password>',
        database='flight_tracking',
        cursorclass=pymysql.cursors.DictCursor
    )

def safe_str(value):
    return value if value not in (None, '') else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_airplane', methods=['POST'])
def add_airplane():
    airlineID = request.form.get('airlineID')
    tail_num = request.form.get('tail_num')
    seat_capacity = request.form.get('seat_capacity')
    speed = request.form.get('speed')
    locationID = request.form.get('locationID')
    plane_type = request.form.get('plane_type')
    maintenanced = request.form.get('maintenanced')
    model = safe_str(request.form.get('model'))
    neo = request.form.get('neo')

    if maintenanced:
        maintenanced = True if maintenanced == "true" else False
    if neo:
        neo = True if neo == "true" else False
    

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.callproc('add_airplane', [airlineID, tail_num, int(seat_capacity), int(speed), locationID,plane_type, maintenanced, model, neo])
        conn.commit()
        cur.execute("SELECT * FROM airplane WHERE airlineID = %s AND tail_num = %s", (airlineID, tail_num))
        airplane = cur.fetchone()

        if not airplane:
            message = "Airplane NOT added. Check stored procedure constraints."
        else:
            print(airplane)
            message = "Airplane successfully added."

    except Exception as e:
        message = f"Error calling add_airplane: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/add_airport', methods=['POST'])
def add_airport():
    airportID = request.form.get('airportID')
    airport_name = request.form.get('airport_name')
    city = request.form.get('city')
    state = request.form.get('state')
    country = request.form.get('country')
    locationID = request.form.get('locationID')

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('add_airport', [airportID, airport_name, city, state, country, locationID])
        conn.commit()
        cur.execute("SELECT * FROM airport WHERE airportID = %s", (airportID,))
        airport = cur.fetchone()
        if airport:
            message = "Airport successfully added."
        else:
            message = "Airport NOT added. Check stored procedure constraints."
    except Exception as e:
        message = f"Error calling add_airport: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/add_person', methods=['POST'])
def add_person():
    personID = request.form.get('personID')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    locationID = request.form.get('locationID')
    taxID = safe_str(request.form.get('taxID'))
    experience = safe_str(request.form.get('experience'))
    miles = safe_str(request.form.get('miles'))
    funds = safe_str(request.form.get('funds'))

    exp_val = int(experience) if experience else None
    miles_val = int(miles) if miles else None
    funds_val = int(funds) if funds else None

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('add_person', [personID, first_name, last_name, locationID,taxID, exp_val, miles_val, funds_val])
        conn.commit()
        cur.execute("SELECT * FROM person WHERE personID = %s", (personID,))
        person = cur.fetchone()
        if person:
            message = "Person successfully added."
        else:
            message = "Person NOT added. Check stored procedure constraints."
    except Exception as e:
        message = f"Error calling add_person: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/grant_or_revoke_pilot_license', methods=['POST'])
def grant_or_revoke_pilot_license():
    personID = request.form.get('personID')
    license_str = request.form.get('license')

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('grant_or_revoke_pilot_license', [personID, license_str])
        conn.commit()
        cur.execute("SELECT * FROM pilot_licenses WHERE personID = %s AND license = %s",(personID, license_str))
        license_rec = cur.fetchone()
        if license_rec:
            message = f"License '{license_str}' is now active for person {personID}."
        else:
            message = f"License '{license_str}' is now inactive for person {personID}."
    except Exception as e:
        message = f"Error calling grant_or_revoke_pilot_license: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/grant_or_revoke_pilot_license', methods=['POST'])
def grant_or_revoke_pilot_license_route():
    personID    = request.form.get('personID')
    license_str = request.form.get('license')

    conn = get_db_connection(); cur = conn.cursor()
    try:
        cur.callproc('grant_or_revoke_pilot_license', [personID, license_str])
        conn.commit()
        cur.execute(
            "SELECT * FROM pilot_licenses WHERE personID = %s AND license = %s",
            (personID, license_str)
        )
        license_rec = cur.fetchone()
        if license_rec:
            message = f"License '{license_str}' is now ACTIVE for person {personID}."
        else:
            message = f"License '{license_str}' is now INACTIVE for person {personID}."
    except Exception as e:
        message = f"Error calling grant_or_revoke_pilot_license: {e}"
    finally:
        cur.close(); conn.close()
    return message

@app.route('/offer_flight', methods=['POST'])
def offer_flight():
    flightID = request.form.get('flightID')
    routeID = request.form.get('routeID')
    support_airline = request.form.get('support_airline')
    support_tail = request.form.get('support_tail')
    progress = request.form.get('progress')
    next_time = request.form.get('next_time')
    cost = request.form.get('cost')

    prog_val = int(progress) if progress else 0
    cost_val = int(cost) if cost else 0

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('offer_flight', [flightID, routeID, support_airline, support_tail, prog_val, next_time, cost_val])
        conn.commit()
        cur.execute("SELECT * FROM flight WHERE flightID = %s", (flightID,))
        flight = cur.fetchone()
        if flight:
            message = "Flight successfully offered."
        else:
            message = "Flight NOT offered. Check stored procedure constraints."
    except Exception as e:
        message = f"Error calling offer_flight: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/flight_landing', methods=['POST'])
def flight_landing():
    flightID = request.form.get('flightID')
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('flight_landing', [flightID])
        conn.commit()
        cur.execute("SELECT airplane_status FROM flight WHERE flightID = %s", (flightID,))
        record = cur.fetchone()
        if record and record.get('airplane_status') == 'on_ground':
            message = f"Flight {flightID} landed successfully."
        else:
            message = f"Flight {flightID} landing failed or no status change occurred."
    except Exception as e:
        message = f"Error calling flight_landing: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/flight_takeoff', methods=['POST'])
def flight_takeoff():
    flightID = request.form.get('flightID')
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('flight_takeoff', [flightID])
        conn.commit()
        cur.execute("SELECT airplane_status FROM flight WHERE flightID = %s", (flightID,))
        record = cur.fetchone()
        if record and record.get('airplane_status') == 'in_flight':
            message = f"Flight {flightID} took off successfully."
        else:
            message = f"Flight {flightID} takeoff failed or has been delayed (e.g. due to pilot shortage)."
    except Exception as e:
        message = f"Error calling flight_takeoff: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/passengers_board', methods=['POST'])
def passengers_board():
    flightID = request.form.get('flightID')
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('passengers_board', [flightID])
        conn.commit()
        cur.execute("""
            SELECT a.locationID AS airplane_location 
            FROM flight f 
            JOIN airplane a ON f.support_airline = a.airlineID AND f.support_tail = a.tail_num
            WHERE f.flightID = %s
            """, (flightID,))
        rec = cur.fetchone()
        if rec:
            airplane_location = rec.get("airplane_location")
            cur.execute("SELECT COUNT(*) as count FROM person WHERE locationID = %s", (airplane_location,))
            count_rec = cur.fetchone()
            boarded_count = count_rec.get("count", 0)
            message = f"Passengers boarding completed. {boarded_count} passenger(s) are now on the airplane."
        else:
            message = "Passengers boarding completed but airplane location could not be determined."
    except Exception as e:
        message = f"Error calling passengers_board: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/passengers_disembark', methods=['POST'])
def passengers_disembark():
    flightID = request.form.get('flightID')
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('passengers_disembark', [flightID])
        conn.commit()
        cur.execute("SELECT routeID, progress FROM flight WHERE flightID = %s", (flightID,))
        flight_info = cur.fetchone()
        if flight_info:
            routeID = flight_info['routeID']
            progress = flight_info['progress']
            cur.execute("""
                SELECT l.arrival 
                FROM route_path rp JOIN leg l ON rp.legID = l.legID 
                WHERE rp.routeID = %s AND rp.sequence = %s
                """, (routeID, progress))
            leg_info = cur.fetchone()
            if leg_info:
                airport_code = leg_info['arrival']
                cur.execute("SELECT locationID FROM airport WHERE airportID = %s", (airport_code,))
                airport_rec = cur.fetchone()
                if airport_rec:
                    airport_location = airport_rec['locationID']
                    cur.execute("SELECT COUNT(*) as count FROM person WHERE locationID = %s", (airport_location,))
                    count_rec = cur.fetchone()
                    count_at_airport = count_rec.get("count", 0)
                    message = f"Passengers disembarked. {count_at_airport} person(s) now at the airport."
                else:
                    message = "Failed to determine airport location after disembarkation."
            else:
                message = "Failed to determine arrival leg for disembarkation."
        else:
            message = "Flight record not found for disembarkation check."
    except Exception as e:
        message = f"Error calling passengers_disembark: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/assign_pilot', methods=['POST'])
def assign_pilot():
    flightID = request.form.get('flightID')
    personID = request.form.get('personID')
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('assign_pilot', [flightID, personID])
        conn.commit()
        cur.execute("SELECT commanding_flight FROM pilot WHERE personID = %s", (personID,))
        pilot_rec = cur.fetchone()
        if pilot_rec and pilot_rec.get("commanding_flight") == flightID:
            message = "Pilot successfully assigned."
        else:
            message = "Pilot assignment failed. Check constraints."
    except Exception as e:
        message = f"Error calling assign_pilot: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/recycle_crew', methods=['POST'])
def recycle_crew():
    flightID = request.form.get('flightID')
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('recycle_crew', [flightID])
        conn.commit()
        cur.execute("SELECT COUNT(*) as cnt FROM pilot WHERE commanding_flight = %s", (flightID,))
        count_rec = cur.fetchone()
        if count_rec and count_rec.get("cnt", 0) == 0:
            message = "Crew successfully recycled."
        else:
            message = "Crew recycling failed. Some pilots remain assigned."
    except Exception as e:
        message = f"Error calling recycle_crew: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/retire_flight', methods=['POST'])
def retire_flight():
    flightID = request.form.get('flightID')
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('retire_flight', [flightID])
        conn.commit()
        cur.execute("SELECT * FROM flight WHERE flightID = %s", (flightID,))
        if cur.fetchone() is None:
            message = f"Flight {flightID} retired successfully."
        else:
            message = f"Flight {flightID} retirement failed."
    except Exception as e:
        message = f"Error calling retire_flight: {e}"
    finally:
        cur.close()
        conn.close()

    return message

@app.route('/simulation_cycle', methods=['POST'])
def simulation_cycle():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.callproc('simulation_cycle', [])
        conn.commit()
        message = "Simulation cycle executed. Please review state changes via the views."
    except Exception as e:
        message = f"Error calling simulation_cycle: {e}"
    finally:
        cur.close()
        conn.close()

    return message

def fetch_view_data(view_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {view_name}")
    rows = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return col_names, rows

@app.route('/view/<view_name>', methods=['GET'])
def show_view_data(view_name):
    try:
        col_names, rows = fetch_view_data(view_name)
    except Exception as e:
        return f"<div class='error'>Error fetching data from view {view_name}: {e}</div>"

    html = f"""
    <html>
    <head>
        <title>View: {view_name}</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>View: {view_name}</h1>
        <div class="table-wrapper">
            <table class="data-table">
                <thead>
                    <tr>
                        {''.join(f"<th>{col}</th>" for col in col_names)}
                    </tr>
                </thead>
                <tbody>
                    {''.join(
                        "<tr>" + ''.join(f"<td>{val}</td>" for val in row.values()) + "</tr>"
                        for row in rows
                    )}
                </tbody>
            </table>
        </div>
        <p><a class="s-button" href="/">Back to Home</a></p>
    </body>
    </html>
    """
    return html


@app.before_request
def check_request():
    print("Request IP:", request.remote_addr)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)

