# Reddit-Forum-Analysis-and-Clustering

This project combines Reddit forum analysis and stock trading algorithms, implemented with Python and MySQL.

## Project Structure
```
├── models/
│   ├── moving_averages.py
│   ├── prophet_model.py
│   ├── rsi.py
│   └── time_series_transformer.py
├── sql-scripts/
│   └── init.sql
├── venv/                      # Python virtual environment
├── docker-compose.yaml        # Docker configuration
├── dsci565_lab4_2.py         # Part 2 implementation
├── init.sql                   # Database initialization
├── main.py                    # Main application
├── mysql_utils.py            # Database utilities
└── requirements.txt          # Python dependencies
```

## Prerequisites

1. Make sure you have installed:
   - Docker and docker-compose
   - Python 3.10 or higher
   - MySQL (local installation)

2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Quick Start

1. Ensure MySQL root password is set to "easy" and initialize the database:
```bash
mysql -u root -p < init.sql
```

2. Start MySQL container:
```bash
docker-compose up -d
```

3. Run the main application:
```bash
python main.py
```

## Detailed Setup

### 1. Database Configuration
- The `init.sql` script creates necessary database and tables
- Database name: `reddit`
- Root password: "easy"
- Access phpMyAdmin at: http://localhost:8080/phpmyadmin

### 2. Environment Setup
```bash
# Install required packages
pip install -r requirements.txt

# Configure MySQL connection
# MySQL connection settings are in mysql_utils.py
```

### 3. Docker Setup
```bash
# Start containers
docker-compose up -d

# Check status
docker ps

# Stop containers
docker-compose down
```

## Features

### Part 1: Reddit Analysis
- Web scraping from Reddit
- Data preprocessing
- MySQL storage
- Topic analysis

### Part 2: Trading Algorithms
- Stock data collection
- Moving average strategies
- RSI calculations
- Time series analysis
- Prophet model predictions

## Usage

### Running Analysis
```bash
# Part 1: Reddit Analysis
python main.py

# Part 2: Trading Analysis
python dsci565_lab4_2.py
```

### Database Operations
Access via phpMyAdmin or MySQL client:
```bash
mysql -u root -p reddit
```

## Database Schema

```sql
-- Example table structures (adjust according to your init.sql)
CREATE TABLE reddit_posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    content TEXT,
    created_at TIMESTAMP
);

-- Add other table schemas as needed
```

## Troubleshooting

1. If MySQL connection fails:
   - Verify MySQL service is running
   - Check password in mysql_utils.py
   - Ensure database 'reddit' exists

2. Docker Issues:
   - Run `docker-compose down` then `docker-compose up -d`
   - Check logs: `docker-compose logs`

3. Python Dependencies:
   - Ensure you're in virtual environment
   - Reinstall requirements if needed

## Contributing
This project is part of DSCI-560 coursework at USC.

## License
Academic Project - All Rights Reserved
