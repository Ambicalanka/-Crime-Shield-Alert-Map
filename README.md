# Crime Detection System

This project is a Crime Detection System built using Flask, designed to help users report crimes and provide real-time alerts about crime zones. It also includes an admin panel for managing crime data.

## Project Structure

```
CrimeDetectionSystem
├── app.py                           # Flask backend (handles routes, logic)
├── setup_db.py                      # Script to populate crime_data.db with India-wide data
├── crime_data.db                    # SQLite database with crime zones, cities, and crime records
├── templates/                       # HTML templates (for user and admin views)
│   ├── index.html                   # Home page
│   ├── login.html                   # Admin login page
│   ├── admin_dashboard.html         # Admin panel with add/view/edit zones & crimes
│   ├── add_zone.html                # Add new zone form (admin)
│   ├── report_crime.html            # User form to report crimes
│   ├── alert.html                   # Live zone alert display for users
│   ├── route_safety.html            # Route checker with live safety info
│   ├── prediction_charts.html       # Future crime predictions charts (2021–2027)
│   └── map_view.html                # Google Maps-style map with zones (red/yellow/green)
├── static/                          # CSS, JS, and images
│   ├── style.css                    # Stylesheets for the dashboard
│   ├── script.js                    # JS for interactive elements (dropdowns, alerts, etc.)
│   ├── india_zones.geojson          # Optional: GeoJSON data for map rendering (India zones)
├── india_crime_data.csv             # Raw CSV data used for initial DB population (2021–2024)
├── requirements.txt                 # Python dependencies (Flask, pandas, etc.)
├── README.md                        # Instructions to run in VS Code (Windows)
└── demo_script.md                   # YouTube-style demo steps and narration
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd CrimeDetectionSystem
   ```

2. **Install dependencies**:
   Make sure you have Python installed. Then, run:
   ```
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   Run the `setup_db.py` script to create and populate the SQLite database:
   ```
   python setup_db.py
   ```

4. **Run the application**:
   Start the Flask application:
   ```
   python app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000`.

## Features

- **User Reporting**: Users can report crimes in their area through a dedicated form.
- **Admin Dashboard**: Admins can log in to manage crime zones and records.
- **Real-time Alerts**: Users receive live alerts about crime zones.
- **Route Safety Checker**: Users can check the safety of specific routes based on crime data.
- **Crime Predictions**: Charts displaying future crime trends from 2021 to 2027.
- **Map View**: A visual representation of crime zones using color coding.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.