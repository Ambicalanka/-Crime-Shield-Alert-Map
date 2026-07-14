from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from collections import Counter
import webbrowser
import threading

app = Flask(__name__)  # Your main Flask app


app = Flask(__name__)
app.secret_key = 'your_secret_key'
DB_FILE = 'crime_data.db'

# Function to get zone by location
def get_zone_by_location(lat, lng):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Find zone where given lat/lng falls within boundaries
    cur.execute('''
        SELECT * FROM zones 
        WHERE ? BETWEEN min_lat AND max_lat AND ? BETWEEN min_lng AND max_lng
        LIMIT 1
    ''', (lat, lng))
    zone = cur.fetchone()
    conn.close()
    return zone

# --- Home ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report_crime', methods=['GET', 'POST'])
def report_crime():
    if request.method == 'POST':
        crime_type = request.form['crime_type']
        location = request.form['location']
        description = request.form['description']
        date_reported = request.form['date_reported']

        conn = sqlite3.connect('crime_data.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO crimes (crime_type, location, description, date_reported)
            VALUES (?, ?, ?, ?)
        """, (crime_type, location, description, date_reported))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('report_crime.html')


# --- Route Safety ---
# Updated zones
source_zones = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Odisha",
    "Punjab", "Rajasthan", "West Bengal"
]

destination_zones = [
    "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Sikkim", "Tamil Nadu", "Telangana",
    "Tripura", "Uttar Pradesh", "Uttarakhand"
]

@app.route("/route-safety", methods=["GET", "POST"])
def route_safety():
    conn = sqlite3.connect('crime_data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    zones_source = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Odisha",
        "Punjab", "Rajasthan", "West Bengal"
    ]

    zones_destination_not_safe = [
        "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Manipur",
        "Meghalaya", "Mizoram", "Nagaland", "Sikkim", "Tamil Nadu", "Telangana",
        "Tripura", "Uttar Pradesh", "Uttarakhand"
    ]

    zones_destination_safe = [
        "Andaman and Nicobar Islands", "Delhi", "Lakshadweep", "Punjab", "Rajasthan", 
        "Kerala", "Odisha", "Madhya Pradesh", "Jharkhand", "Himachal Pradesh"
    ]

    zones_destination = zones_destination_not_safe + zones_destination_safe

    source = destination = suggestion = reason = most_common_crime = None
    crimes = []
    crime_counts = {}

    if request.method == "POST":
        source = request.form["source"]
        destination = request.form["destination"]

        cur.execute("SELECT * FROM zones WHERE name = ?", (destination,))
        row = cur.fetchone()

        if row:
            severity = row["severity"]

            # Make sure you fetch crime data even if user typed lowercase
            cur.execute("SELECT crime_type, description FROM crimes WHERE LOWER(location) = LOWER(?)", (destination,))
            crimes = cur.fetchall()

            if severity == 'red':
                if crimes:
                    suggestion = "Danger"
                    crime_types = [c["crime_type"] for c in crimes]
                    crime_counts = dict(Counter(crime_types))
                    most_common_crime = Counter(crime_types).most_common(1)[0][0]
                    reason = f"This is a red zone with recent incidents of {most_common_crime} and other crimes."
                else:
                    suggestion = "Not Safe (No Data)"
                    reason = "Red zone with no reported crimes, but flagged as high risk."

            elif severity == 'yellow':
                suggestion = "Not Safe (No Data)"
                reason = "This zone has no reported crimes but is still marked risky."

            elif severity == 'green':
                suggestion = "Safe"
                reason = "No crimes reported in this zone recently."

        else:
            suggestion = "Safe"
            reason = "Zone not listed in the database. Assuming it is Safe."

    conn.close()

    return render_template("route_safety.html",
                           zones_source=zones_source,
                           zones_destination=zones_destination,
                           source=source,
                           destination=destination,
                           suggestion=suggestion,
                           crimes=crimes,
                           crime_counts=crime_counts,
                           most_common_crime=most_common_crime,
                           reason=reason)

# --- Live Zone Alert Page ---
@app.route("/alert")
def live_zone_alert():
    conn = sqlite3.connect("crime_data.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM zones ORDER BY name")
    zones = [row[0] for row in cur.fetchall()]
    conn.close()
    return render_template("live_zone_alert.html", zones=zones)

# Route to check zone based on latitude and longitude
@app.route("/check_zone")
def check_zone():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    # Example: Use lat/lng to find nearest zone in your DB
    conn = sqlite3.connect('crime_data.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT name, severity FROM zones
        WHERE ABS(center_lat - ?) < 1 AND ABS(center_lng - ?) < 1
        ORDER BY ABS(center_lat - ?) + ABS(center_lng - ?) ASC LIMIT 1
    """, (lat, lng, lat, lng))
    row = cur.fetchone()
    if row:
        return jsonify({'zone': row[0], 'severity': row[1]})
    return jsonify({'zone': 'Unknown', 'severity': 'green'})  # Default safe


# --- Utility to fetch zones from DB with severity and coordinates ---
def get_zones():
    conn = sqlite3.connect('crime_data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name, severity, center_lat as lat, center_lng as lng FROM zones")
    rows = cur.fetchall()
    zones = []
    for row in rows:
        zones.append({
            'name': row['name'],
            'severity': row['severity'],
            'lat': row['lat'],
            'lng': row['lng']
        })
    conn.close()
    return zones

# --- API endpoint to return zones as JSON ---
from flask import Flask, jsonify

# --- API ROUTE: Returns all zones with coordinates and severity ---
@app.route('/api/zones')
def api_zones():
    try:
        conn = sqlite3.connect('crime_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT zone_name, min_lat, max_lat, min_lng, max_lng, severity FROM zones")
        zones = [{
            'zone': row[0],
            'min_lat': row[1],
            'max_lat': row[2],
            'min_lng': row[3],
            'max_lng': row[4],
            'severity': row[5]
        } for row in cursor.fetchall()]
        conn.close()
        return jsonify(zones)
    except Exception as e:
        print("Error fetching from DB:", e)
        # fallback static
        fallback_zones = [
           {"name": "Delhi", "lat": 28.6139, "lng": 77.2090, "severity": "red"},
        {"name": "Kerala", "lat": 10.8505, "lng": 76.2711, "severity": "green"},
        {"name": "Maharashtra", "lat": 19.7515, "lng": 75.7139, "severity": "red"},
        {"name": "Gujarat", "lat": 22.2587, "lng": 71.1924, "severity": "yellow"},
        {"name": "Tamil Nadu", "lat": 11.1271, "lng": 78.6569, "severity": "green"},
        {"name": "West Bengal", "lat": 22.9868, "lng": 87.8550, "severity": "red"},
        {"name": "Karnataka", "lat": 15.3173, "lng": 75.7139, "severity": "green"},
        {"name": "Uttar Pradesh", "lat": 26.8467, "lng": 80.9462, "severity": "yellow"},
        {"name": "Bihar", "lat": 25.0961, "lng": 85.3131, "severity": "red"},
        {"name": "Odisha", "lat": 20.9517, "lng": 85.0985, "severity": "green"}
        ]
        return jsonify(fallback_zones)

# Route to render live zone map
@app.route('/live_zone_map')
def live_zone_map():
    return render_template('live_zone_map.html')

# --- Full Zone Map View ---
@app.route('/map')
def map_view():
    return render_template('zone_map.html')


# --- Admin Login ---
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

# --- Admin Dashboard ---
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('crime_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM zones")
    zones = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        name = request.form['zone_name']
        severity = request.form['severity']
        min_lat = float(request.form['min_lat'])
        max_lat = float(request.form['max_lat'])
        min_lng = float(request.form['min_lng'])
        max_lng = float(request.form['max_lng'])

        conn = sqlite3.connect('crime_data.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO zones (zone_name, severity, min_lat, max_lat, min_lng, max_lng)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, severity, min_lat, max_lat, min_lng, max_lng))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_dashboard.html', zones=zones)

# --- API: Check Zone Status ---
@app.route('/check_zone_status')
def check_zone_status():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    conn = sqlite3.connect('crime_data.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT zone_name, severity FROM zones
        WHERE ? BETWEEN min_lat AND max_lat
        AND ? BETWEEN min_lng AND max_lng
    """, (lat, lon))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({'zone': result[0], 'status': result[1]})
    else:
        return jsonify({'zone': 'Unknown', 'status': 'Safe'})

# Zone severity route
@app.route("/get_zone_severity/<state>")
def get_zone_severity(state):
    conn = sqlite3.connect("crime_data.db")
    cur = conn.cursor()
    cur.execute("SELECT severity FROM zones WHERE name = ?", (state,))
    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({"severity": row[0]})
    else:
        return jsonify({"severity": "yellow"})  # default: unknown = yellow


# --- Logout ---
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route("/dashboard")
def crime_dashboard():
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    total_crimes = [380000, 420000, 400000, 450000, 470000, 490000]

    crime_types = ["Theft", "Assault", "Fraud", "Drug Trafficking", "Robbery"]
    crime_counts = [120000, 90000, 80000, 70000, 60000]

    future_years = ["2025", "2026", "2027"]
    future_predictions = [510000, 530000, 560000]

    return render_template("crime_dashboard.html",
                           years=years,
                           total_crimes=total_crimes,
                           crime_types=crime_types,
                           crime_counts=crime_counts,
                           future_years=future_years,
                           future_predictions=future_predictions)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard-data")
def dashboard_data():
    conn = sqlite3.connect("crime_data.db")
    cur = conn.cursor()

    # Crimes by year (2019–2027)
    cur.execute("SELECT strftime('%Y', date), COUNT(*) FROM crimes WHERE date BETWEEN '2019-01-01' AND '2027-12-31' GROUP BY strftime('%Y', date)")
    yearly_crimes = cur.fetchall()
    crimes_by_year = {year: count for year, count in yearly_crimes}

    # Crimes by type
    cur.execute("SELECT crime_type, COUNT(*) FROM crimes GROUP BY crime_type")
    crimes_by_type = cur.fetchall()
    crimes_by_type = [{"type": c[0], "count": c[1]} for c in crimes_by_type]

    # Crimes by state (top 5)
    cur.execute("SELECT location, COUNT(*) FROM crimes GROUP BY location ORDER BY COUNT(*) DESC LIMIT 5")
    crimes_by_state = cur.fetchall()
    top_states = [{"state": s[0], "count": s[1]} for s in crimes_by_state]

    # Gender distribution
    cur.execute("SELECT gender, COUNT(*) FROM crimes GROUP BY gender")
    gender_dist = cur.fetchall()
    gender_stats = {"Male": 0, "Female": 0, "Other": 0}
    for gender, count in gender_dist:
        if gender in gender_stats:
            gender_stats[gender] = count

    # Age group distribution (assumes ages are stored in a field called 'age')
    age_groups = {
        "0-17": 0,
        "18-35": 0,
        "36-50": 0,
        "51+": 0
    }
    cur.execute("SELECT age FROM crimes WHERE age IS NOT NULL")
    for (age,) in cur.fetchall():
        if age <= 17:
            age_groups["0-17"] += 1
        elif age <= 35:
            age_groups["18-35"] += 1
        elif age <= 50:
            age_groups["36-50"] += 1
        else:
            age_groups["51+"] += 1

    conn.close()

    return jsonify({
        "crimes_by_year": crimes_by_year,
        "crimes_by_type": crimes_by_type,
        "top_states": top_states,
        "gender_stats": gender_stats,
        "age_groups": age_groups
    })

@app.route('/dashboard-image')
def dashboard_image():
    return render_template('dashboard_image.html')

# --- Main ---
if __name__ == '__main__':
    # Open browser in a separate thread after Flask starts
    def open_browser():
        import time
        import os
        time.sleep(2)  # Wait for Flask to start
        url = 'http://localhost:5000'
        try:
            # Try to open with webbrowser
            webbrowser.open(url)
        except Exception as e:
            print(f"Could not open browser automatically: {e}")
        
        # Print URL for manual access
        print(f"\n✓ Application is running at: {url}")
        print("If browser doesn't open, copy this URL to Chrome or Firefox manually\n")
    
    threading.Thread(target=open_browser, daemon=True).start()
    print("Starting Crime Shield Alert Map...")
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)