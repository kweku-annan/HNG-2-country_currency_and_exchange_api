# Country Currency & Exchange API

A RESTful API that fetches country data from external sources, stores it in a MySQL database, and provides CRUD operations with filtering, sorting, and data visualization capabilities.

## 🚀 Features

- Fetch and cache country data from external APIs
- Store country information with currency exchange rates
- Calculate estimated GDP based on population and exchange rates
- Filter countries by region and currency
- Sort countries by GDP
- Generate visual summary images with top countries
- Full CRUD operations on country data

## 📋 Table of Contents

- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Environment Variables](#environment-variables)
- [Running Locally](#running-locally)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [External APIs](#external-apis)
- [Error Handling](#error-handling)

## 🛠 Technologies Used

- **Python 3.12**
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **MySQL** - Database (hosted on Aiven.io)
- **PyMySQL** - MySQL database adapter
- **Pillow (PIL)** - Image generation
- **Requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management
- **Gunicorn** - WSGI HTTP Server for deployment

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher
- MySQL (local) or access to a cloud MySQL service
- pip (Python package manager)
- Git

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/country-currency-exchange-api.git
cd country-currency-exchange-api
```

### 2. Create a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

**Option A: Local MySQL**
```sql
CREATE DATABASE country_currency_exchange;
```

**Option B: Use Aiven.io (Free Tier)**
- Sign up at https://aiven.io/
- Create a free MySQL service
- Note down the connection details

### 5. Configure Environment Variables

Create a `.env` file in the root directory:
```env
DATABASE_URI=mysql+pymysql://username:password@host:port/database_name?ssl_mode=REQUIRED
```

**Example for local MySQL:**
```env
DATABASE_URI=mysql+pymysql://root:your_password@localhost:3306/country_currency_exchange
```

**Example for Aiven.io:**
```env
DATABASE_URI=mysql+pymysql://avnadmin:your_password@mysql-xxxxx.aivencloud.com:12345/defaultdb?ssl_mode=REQUIRED
```

## 🏃 Running Locally

### Start the Application
```bash
python3 app.py
```

The API will be available at `http://localhost:5000`

### Test the API
```bash
# Check if server is running
curl http://localhost:5000/

# Fetch and refresh country data
curl -X POST http://localhost:5000/countries/refresh

# Get all countries
curl http://localhost:5000/countries

# Get status
curl http://localhost:5000/status
```

## 🌐 API Endpoints

### 1. Home
```
GET /
```
**Response:**
```json
"Welcome to the Country Currency & Exchange API"
```

### 2. Refresh Country Data
```
POST /countries/refresh
```
Fetches country data and exchange rates from external APIs, then caches them in the database.

**Response (Success):**
```json
{
  "message": "Countries refreshed successfully!"
}
```

**Response (Error):**
```json
{
  "error": "External data source unavailable",
  "details": "Could not fetch data from Countries API"
}
```
**Status Code:** `503 Service Unavailable`

### 3. Get All Countries
```
GET /countries
```

**Query Parameters:**
- `region` - Filter by region (e.g., `Africa`, `Europe`)
- `currency` - Filter by currency code (e.g., `NGN`, `USD`)
- `sort` - Sort results (`gdp_desc`, `gdp_asc`)

**Examples:**
```bash
GET /countries?region=Africa
GET /countries?currency=NGN
GET /countries?region=Africa&sort=gdp_desc
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Nigeria",
    "capital": "Abuja",
    "region": "Africa",
    "population": 206139589,
    "currency_code": "NGN",
    "exchange_rate": 1600.23,
    "estimated_gdp": 25767448125.2,
    "flag_url": "https://flagcdn.com/ng.svg",
    "last_refreshed_at": "2025-10-29T18:00:00Z"
  }
]
```

### 4. Get Single Country
```
GET /countries/:name
```

**Example:**
```bash
GET /countries/Nigeria
```

**Response (Success):**
```json
{
  "id": 1,
  "name": "Nigeria",
  "capital": "Abuja",
  "region": "Africa",
  "population": 206139589,
  "currency_code": "NGN",
  "exchange_rate": 1600.23,
  "estimated_gdp": 25767448125.2,
  "flag_url": "https://flagcdn.com/ng.svg",
  "last_refreshed_at": "2025-10-29T18:00:00Z"
}
```

**Response (Not Found):**
```json
{
  "error": "Country not found"
}
```
**Status Code:** `404 Not Found`

### 5. Delete Country
```
DELETE /countries/:name
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/countries/Nigeria
```

**Response (Success):**
```json
{
  "message": "Country deleted successfully"
}
```

**Response (Not Found):**
```json
{
  "error": "Country not found"
}
```
**Status Code:** `404 Not Found`

### 6. Get Status
```
GET /status
```

**Response:**
```json
{
  "total_countries": 250,
  "last_refreshed_at": "2025-10-29T18:00:00Z"
}
```

### 7. Get Summary Image
```
GET /countries/image
```

Returns a PNG image showing:
- Total number of countries
- Top 5 countries by estimated GDP
- Last refresh timestamp

**Response:** Image file (PNG)

**Error Response:**
```json
{
  "error": "Summary image not found"
}
```
**Status Code:** `404 Not Found`

## 🚀 Deployment

This project is deployed on **Railway** with a MySQL database hosted on **Aiven.io**.

### Deploy to Railway

1. **Install Railway CLI (Optional)**
```bash
   npm i -g @railway/cli
```

2. **Push to GitHub**
```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
```

3. **Deploy on Railway**
   - Go to https://railway.app/
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variable:
```
     DATABASE_URI=mysql+pymysql://avnadmin:password@host:port/defaultdb?ssl_mode=REQUIRED
```
   - Railway will auto-deploy

4. **Access Your API**
   - Railway will provide a URL like: `https://your-app.up.railway.app`

### Required Files for Deployment

**Procfile:**
```
web: gunicorn app:app
```

**requirements.txt:**
```
Flask==3.0.0
SQLAlchemy==2.0.23
PyMySQL==1.1.0
python-dotenv==1.0.0
requests==2.31.0
Pillow==10.1.0
gunicorn==21.2.0
cryptography==41.0.7
```

**railway.json (optional):**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## 📁 Project Structure
```
country-currency-exchange-api/
├── api/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── countries.py          # Country model definition
│   ├── routes/
│   │   ├── __init__.py
│   │   └── country_routes.py     # API endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── dbStorage.py          # Database operations
│   └── utils/
│       ├── __init__.py
│       ├── fetch_data_helper.py  # External API calls
│       └── image_generator.py    # Image generation
├── cache/
│   └── summary.png               # Generated summary image
├── .env                          # Environment variables (not in repo)
├── .gitignore
├── app.py                        # Flask app entry point
├── config.py                     # Configuration settings
├── Procfile                      # Railway deployment config
├── railway.json                  # Railway settings (optional)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🌍 External APIs

This project fetches data from two external APIs:

### 1. REST Countries API
```
https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies
```
Provides country information including name, capital, region, population, flag, and currencies.

### 2. Exchange Rates API
```
https://open.er-api.com/v6/latest/USD
```
Provides current exchange rates for various currencies against USD.

## ⚠️ Error Handling

The API returns consistent JSON error responses:

### 400 Bad Request
```json
{
  "error": "Validation failed",
  "details": {
    "field_name": "is required"
  }
}
```

### 404 Not Found
```json
{
  "error": "Country not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

### 503 Service Unavailable
```json
{
  "error": "External data source unavailable",
  "details": "Could not fetch data from [API name]"
}
```

## 📝 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URI` | MySQL connection string | `mysql+pymysql://user:pass@host:port/db?ssl_mode=REQUIRED` |

## 🔒 Database Schema

### Countries Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(60) | NOT NULL, UNIQUE | Country name |
| capital | VARCHAR(60) | NULL | Capital city |
| region | VARCHAR(60) | NULL | Geographic region |
| population | INTEGER | NOT NULL | Population count |
| currency_code | VARCHAR(10) | NULL | ISO currency code |
| exchange_rate | DECIMAL(18,2) | NULL | Exchange rate vs USD |
| estimated_gdp | DECIMAL(20,1) | NULL | Calculated GDP estimate |
| flag_url | VARCHAR(100) | NULL | Flag image URL |
| last_refreshed_at | DATETIME | NOT NULL | Last update timestamp |

## 🧪 Testing

### Manual Testing with curl
```bash
# Test refresh
curl -X POST http://localhost:5000/countries/refresh

# Test filters
curl "http://localhost:5000/countries?region=Africa"
curl "http://localhost:5000/countries?currency=USD"
curl "http://localhost:5000/countries?sort=gdp_desc"

# Test single country
curl http://localhost:5000/countries/Nigeria

# Test delete
curl -X DELETE http://localhost:5000/countries/TestCountry

# Test status
curl http://localhost:5000/status

# Download summary image
curl http://localhost:5000/countries/image --output summary.png
```

## 🐛 Troubleshooting

### Issue: "Can't connect to MySQL server"
**Solution:** 
- Verify DATABASE_URI is correct
- Check if MySQL service is running
- For Aiven, ensure service status is "Running"

### Issue: "SSL connection error"
**Solution:** 
- Add `?ssl_mode=REQUIRED` to your DATABASE_URI
- Or use `?ssl_mode=PREFER`

### Issue: "Timeout when calling /countries/refresh"
**Solution:** 
- This is normal for first refresh (250+ countries)
- Should take 5-15 seconds
- Check Railway logs for any errors

### Issue: "Summary image not found"
**Solution:** 
- Call `/countries/refresh` first to generate the image
- Check if `cache/` directory exists and is writable

## 📄 License

This project is part of the HNG Internship program.

## 👤 Author

**Your Name**
- GitHub: [kweku-annan](https://github.com/kweku-annan)
- LinkedIn: [LINKEDIN](https://www.linkedin.com/in/emmanuel-saah)

## 🙏 Acknowledgments

- [REST Countries API](https://restcountries.com/)
- [Open Exchange Rates API](https://open.er-api.com/)
- [HNG Internship](https://hng.tech/)
- [Railway](https://railway.app/)
- [Aiven.io](https://aiven.io/)

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the author.

---

**Live API:** [link](https://hng-2-countrycurrencyandexchangeapi-production.up.railway.app)

**Last Updated:** October 29, 2025