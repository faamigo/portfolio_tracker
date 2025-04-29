# API Documentation

This is a Django project with the following setup:

## Setup and Database Management

### Initial Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```

### Database Setup and Migrations

1. Create initial migrations:
```bash
python3 manage.py makemigrations
```
This command will:
- Detect your models
- Create initial migration files in the `migrations` directory
- Store the database schema changes

2. Apply migrations to create the database:
```bash
python3 manage.py migrate
```
This command will:
- Create all necessary database tables
- Apply all migrations in the correct order
- Set up the initial database structure

3. (Optional) Reset the database if needed:
```bash
python3 manage.py flush --noinput
```
This command will:
- Remove all data from the database
- Keep the table structure intact
- Not prompt for confirmation (--noinput flag)

### Start the Development Server

```bash
python3 manage.py runserver
```

The server will be available at http://127.0.0.1:8000/ 

## Portfolios

### GET /api/portfolios/
Returns all portfolios in the system.

**Request:**
```bash
curl "http://localhost:8000/api/portfolios/?page=1&page_size=10"
```

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Portafolio 1",
            "initial_value": "1000000000.00",
            "created_at": "2025-04-25T21:59:46.105029Z",
            "updated_at": "2025-04-25T21:59:46.105102Z"
        }
    ]
}
```

Query parameters:
- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10)

### GET /api/portfolios/{id}/
Returns details of a specific portfolio.

**Request:**
```bash
curl "http://localhost:8000/api/portfolios/1/"
```

**Response:**
```json
{
    "id": 1,
    "name": "Portfolio 1",
    "initial_value": "1000000000.00",
    "created_at": "2025-04-25T21:59:46.105029Z",
    "updated_at": "2025-04-25T21:59:46.105102Z"
}
```

### GET /api/portfolios/{id}/holdings/
Returns all holdings for a specific portfolio.

**Request:**
```bash
curl "http://localhost:8000/api/portfolios/1/holdings/?page=1&page_size=10"
```

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "portfolio_id": 1,
            "asset_id": 1,
            "quantity": "100000.00",
            "date": "2022-02-15",
            "created_at": "2025-04-25T21:59:46.106880Z",
            "updated_at": "2025-04-25T21:59:46.106958Z"
        }
    ]
}
```

Query parameters:
- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10)

### GET /api/portfolios/{id}/weights/
Returns all weights for a specific portfolio.

**Request:**
```bash
curl "http://localhost:8000/api/portfolios/1/weights/?page=1&page_size=10"
```

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "portfolio_id": 1,
            "asset_id": 1,
            "weight": "0.2800",
            "date": "2022-02-15",
            "created_at": "2025-04-25T21:59:46.106880Z",
            "updated_at": "2025-04-25T21:59:46.106958Z"
        }
    ]
}
```

Query parameters:
- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10)

### GET /api/portfolios/{id}/metrics/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
Returns historical metrics for a specific portfolio, including total value and asset weights over time.

**Request:**
```bash
curl "http://localhost:8000/api/portfolios/1/metrics/?start_date=2022-02-15&end_date=2022-12-31&page=1&page_size=10"
```

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "date": "2022-02-15",
            "total_value": 1000000000.00,
            "weights": {
                "EEUU": 0.28278,
                "Europa": 0.081667,
                "Japón": 0.037352,
                "EM Asia": 0.041777
            }
        }
    ]
}
```

Query parameters:
- `start_date`: Start date for metrics (format: YYYY-MM-DD)
- `end_date`: End date for metrics (format: YYYY-MM-DD)
- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10)

### GET /api/portfolios/{id}/assets/
Returns all assets for a specific portfolio with their current holdings and values.

**Request:**
```bash
curl "http://localhost:8000/api/portfolios/1/assets/"
```

**Response:**
```json
{
    "limit": 4,
    "offset": 0,
    "count": 17,
    "next": "http://127.0.0.1:8000/api/portfolios/1/assets/?limit=10&offset=10",
    "previous": null,
    "results": {
        "portfolio_id": 1,
        "date": "2023-02-16",
        "assets": [
            {
                "asset_id": "1",
                "asset_name": "EEUU",
                "quantity": "29.84",
                "price": "8853.02",
                "value": "264174.1168",
                "date": "2023-02-16"
            },
            {
                "asset_id": "2",
                "asset_name": "Europa",
                "quantity": "1409.34",
                "price": "61.16",
                "value": "86195.2344",
                "date": "2023-02-16"
            },
            {
                "asset_id": "3",
                "asset_name": "UK",
                "quantity": "667.05",
                "price": "32.80",
                "value": "21879.2400",
                "date": "2023-02-16"
            },
            {
                "asset_id": "4",
                "asset_name": "Japón",
                "quantity": "97.37",
                "price": "355.54",
                "value": "34618.9298",
                "date": "2023-02-16"
            }
        ]
    }
}
```

Query parameters:
- `limit`: Number of items per page (default: 10)
- `offset`: Starting position for pagination (default: 0)

### POST /api/portfolios/{id}/assets/{asset_id}/buy/
Buy an asset for a portfolio.

**Request:**
```bash
curl -X POST http://localhost:8000/api/portfolios/1/assets/1/buy/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1000.00,
    "date": "2022-02-15"
  }'
```

**Response:**
```json
{
    "message": "Purchase successful",
    "portfolio_id": 1,
    "asset_id": 1,
    "quantity": 1000.00,
    "price": 9383.57,
    "total": 9383570.00
}
```

### POST /api/portfolios/{id}/assets/{asset_id}/sell/
Sell an asset from a portfolio.

**Request:**
```bash
curl -X POST http://localhost:8000/api/portfolios/1/assets/1/sell/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 500.00,
    "date": "2022-02-15"
  }'
```

**Response:**
```json
{
    "message": "Sale successful",
    "portfolio_id": 1,
    "asset_id": 1,
    "quantity": 500.00,
    "price": 9383.57,
    "total": 4691785.00
}
```

### POST /api/portfolios/{id}/rebalance/
Rebalance a portfolio. Sell and buy assets and return operations status with recalculated metrics.

**Request:**
```bash
curl -X POST http://localhost:8000/api/portfolios/1/rebalance/ \
  -H "Content-Type: application/json" \
  -d '{
    "sell_asset_id": 1,
    "buy_asset_id": 2,
    "sell_amount": 1000.00,
    "buy_amount": 1000.00,
    "start_date": "2022-02-15",
    "end_date": "2022-12-31"
  }'
```

**Response:**
```json
{
    "sell_transaction": {
        "message": "Sale successful",
        "portfolio_id": 1,
        "asset_id": 1,
        "quantity": 0.0005,
        "price": 9383.57,
        "total": 5.33
    },
    "buy_transaction": {
        "message": "Purchase successful",
        "portfolio_id": 1,
        "asset_id": 2,
        "quantity": 11.4680,
        "price": 66.03,
        "total": 757.23
    },
    "metrics": [
        {
            "date": "2022-02-15",
            "total_value": 2000.00,
            "weights": {
                "EEUU": 0.2828,
                "Europa": 0.0817,
                "Japón": 0.0374,
                "EM Asia": 0.0418
            }
        }
    ]
}
```

## Visualization

The portfolio visualization dashboard is available at:
```
http://localhost:8000/portfolios/{portfolio_id}/metrics/plot/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```

This dashboard provides interactive charts showing:
- Portfolio performance over time
- Asset allocation and weights
- Historical metrics and comparisons

Required query parameters:
- `start_date`: Start date for the metrics visualization (format: YYYY-MM-DD)
- `end_date`: End date for the metrics visualization (format: YYYY-MM-DD)

Example:
```
http://localhost:8000/portfolios/1/metrics/plot/?start_date=2022-02-15&end_date=2022-12-31
```

---

# Command Line Tools

## Initialize Data from Excel
Command to load data from Excel and initialize portfolio holdings:

```bash
python3 manage.py init_data --excel-file data/data.xlsx
```

This command will:
1. Load data from the specified Excel file:
   - Create assets from the 'activos' column
   - Create portfolios based on the Excel columns
   - Load historical prices from the 'Precios' sheet
   - Load portfolio weights from the 'weights' sheet

## Setup Portfolios
Command to setup portfolios with initial values and create initial holdings:

```bash
python3 manage.py setup_portfolios --csv-file data/portfolio_values.csv --date 2022-02-15
```

**Response:**
```
Data initialized correctly
```

**Excel File Structure:**
The Excel file should be named `portfolios.xlsx` and placed in the `data/` directory with two sheets:
1. "weights":
   - Column 'Date': Dates
   - Column 'asset': Asset names
   - Additional columns: One per portfolio with weight values

2. "prices":
   - Column 'Date'
   - Additional columns: One per asset with price values

# Project Questions Answers

## 1. Project Modeling
The project is modeled with the following entities:
- `Asset`: Financial assets
- `Portfolio`: Investment portfolios
- `Price`: Historical asset prices
- `Holding`: Asset quantities in each portfolio
- `Weight`: Asset weights in each portfolio

## 2. ETL Function
To load data from the Excel file, use the command:
```bash
python3 manage.py init_data --excel-file data/data.xlsx
```

## 3. Initial Quantities Calculation
To set the initial value of $1,000,000,000 on 02/15/22 and calculate initial quantities:
```bash
python3 manage.py setup_portfolios --csv-file data/portfolio_values.csv --date 2022-02-15
```
Where `portfolio_values.csv` should contain:
```csv
Portafolio 1,1000000000
Portafolio 2,1000000000
```

## 4. Evolution of Weights and Values
Use the metrics endpoint to get both weights and total values:
```bash
curl "http://localhost:8000/api/portfolios/1/metrics/?start_date=2022-02-15&end_date=2022-12-31"
```
The response includes:
- `total_value`: Portfolio total value ($V_t$)
- `weights`: Dictionary with asset weights ($w_{i,t}$)

## 5. Visualization (Bonus 1)
Access the visualization at:
```
http://localhost:8000/portfolios/1/metrics/plot/?start_date=2022-02-15&end_date=2022-12-31
```
This will show:
- Stacked area chart for weights
- Line chart for total value

## 6. Buy/Sell Processing (Bonus 2)
To execute the buy/sell operation on 05/15/2022 and get metrics for the following month:
```bash
curl -X POST http://localhost:8000/api/portfolios/1/rebalance/ \
  -H "Content-Type: application/json" \
  -d '{
    "sell_asset_id": 1,  # ID for USA
    "buy_asset_id": 2,   # ID for Europe
    "sell_amount": 200000000.00,
    "buy_amount": 200000000.00,
    "start_date": "2022-05-15",
    "end_date": "2022-06-15"
  }'
```

## 7. Project Structure (Bonus)
The project follows the Django style guide with:
- Clear separation of concerns (models, views, services, selectors)
- Use of serializers for data validation
- Service layer for business logic
- Selectors for database queries
- Unit and API tests
- Complete endpoint documentation
