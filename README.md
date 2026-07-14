# 🚨 Crime Shield Alert Map

A comprehensive **Flask-based web application** for tracking, reporting, and visualizing crime incidents across India. Features real-time alerts, zone-based crime analytics, route safety recommendations, and predictive crime forecasting.

---

## 🎯 Features

✅ **Crime Reporting System** - Users can report crimes with location, type, and description  
✅ **Live Zone Alerts** - Real-time crime alerts for specific geographic zones  
✅ **Crime Dashboard** - Interactive visualizations and statistics  
✅ **Route Safety Checker** - Check safety of travel routes between zones  
✅ **Crime Predictions** - Forecasted crime trends (2021-2027)  
✅ **Admin Panel** - Manage crimes, zones, and users  
✅ **Zone-based Mapping** - Color-coded zones (Red/Yellow/Green) for safety levels  
✅ **User Authentication** - Secure login and registration system  
✅ **SQLite Database** - Pre-populated with India-wide crime data  

---

## 📋 Project Structure

```
Crime-Shield-Alert-Map/
├── app.py                           # Main Flask application
├── setup_db.py                      # Database initialization script
├── crime_data.db                    # SQLite database
├── requirements.txt                 # Python dependencies
├── templates/                       # HTML templates
│   ├── index.html                  # Home page
│   ├── login.html                  # Admin login
│   ├── admin_dashboard.html        # Admin control panel
│   ├── report_crime.html           # Crime reporting form
│   ├── alert.html                  # Live alerts display
│   ├── route_safety.html           # Route checker
│   ├── prediction_charts.html      # Crime forecasts
│   ├── crime_dashboard.html        # Statistics dashboard
│   └── map_view.html               # Interactive map
├── static/                          # Static files
│   ├── style.css                   # Styling
│   ├── script.js                   # JavaScript functionality
│   ├── india_zones.geojson         # Geographic data
│   └── image/                      # Images and icons
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
└── LICENSE                         # MIT License
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Ambicalanka/-Crime-Shield-Alert-Map.git
cd "Crime Shield Alert Map"
```

**2. Create a virtual environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Initialize the database**
```bash
python setup_db.py
```

**5. Run the application**
```bash
python app.py
```

**6. Open in browser**
Navigate to: `http://localhost:5000`

---

## 📱 Usage

### For Regular Users:
1. Go to **Home Page** to view crime statistics
2. Click **"Report Crime"** to submit a crime incident
3. Use **"Route Safety"** to check travel safety between zones
4. View **"Live Alerts"** for real-time crime notifications
5. Check **"Crime Dashboard"** for detailed analytics

### For Administrators:
1. Login at `/admin_login` with admin credentials
2. Access **Admin Dashboard** to manage:
   - Add/Edit/Delete zones
   - Add/View crimes
   - Manage user accounts
3. View **Crime Statistics** and trends

---

## 🔐 Admin Credentials

Default admin login (if enabled):
- **Username:** admin
- **Password:** admin123

⚠️ **Important:** Change these credentials in production!

---

## 🛠️ Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Flask** | Web framework (Python) |
| **SQLite** | Database management |
| **HTML/CSS** | Frontend UI |
| **JavaScript** | Interactive features |
| **Pandas** | Data analysis |
| **GeoJSON** | Geographic data format |

---

## 📊 Database Schema

### Tables:
- **crimes** - Crime incident records
- **zones** - Geographic zones/regions
- **users** - User accounts
- **admins** - Administrator accounts

### Sample Data:
- Pre-loaded with India-wide crime statistics
- Data covering 28 states and 8 union territories
- Crime data from 2021-2024

---

## 🔄 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/report_crime` | GET/POST | Report a crime |
| `/route-safety` | GET/POST | Check route safety |
| `/dashboard` | GET | Crime statistics |
| `/api/crime-stats` | GET | Get crime data (JSON) |
| `/admin_login` | GET/POST | Admin login |

---

## 🎓 Learning Resources

This project demonstrates:
- ✅ Flask web application development
- ✅ SQLite database design and queries
- ✅ User authentication and authorization
- ✅ Data visualization and analytics
- ✅ Geospatial data handling
- ✅ HTML/CSS/JavaScript integration
- ✅ RESTful API design

---

## 🐛 Known Issues

- Prediction accuracy depends on historical data quality
- GeoJSON rendering requires proper browser support
- Database size may impact performance with large datasets

---

## 📈 Future Enhancements

- [ ] Machine learning-based crime prediction
- [ ] Mobile app (iOS/Android)
- [ ] Real-time notification system
- [ ] Integration with law enforcement APIs
- [ ] Advanced data analytics with ML models
- [ ] Multi-language support
- [ ] Cloud deployment (AWS/Heroku)

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- Use this project for personal or commercial purposes
- Modify and distribute the code
- Use it in private or public projects

---

## 👨‍💻 Author

**Ambica**  
GitHub: [@Ambicalanka](https://github.com/Ambicalanka)

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues before creating new ones
- Provide detailed descriptions and error messages

---

## 🙏 Acknowledgments

- Flask documentation and community
- India geographic data sources
- Open-source community for tools and libraries

---

## 📝 Changelog

### Version 1.0 (2026-07-14)
- Initial release
- Core features implemented
- Database populated with sample data
- Admin panel functionality

---

**Last Updated:** July 14, 2026  
**Status:** Active Development ✅