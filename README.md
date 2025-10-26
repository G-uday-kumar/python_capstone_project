# ⚡ EcoWatt: Smart Energy Consumption Forecasting

A comprehensive machine learning project that forecasts energy consumption using time series analysis and provides an intuitive web interface for data visualization and prediction.

## 📋 Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Data Format](#data-format)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ✨ Features

- **Synthetic Data Generation**: Create realistic energy consumption data with seasonal patterns
- **CSV Upload Support**: Upload your own historical energy data
- **Machine Learning Forecasting**: Time series prediction using linear regression with lag features
- **Interactive Web Interface**: Built with Streamlit for easy data exploration
- **Data Visualization**: Charts and statistics for historical and forecasted data
- **Flexible Date/Time Support**: Handle both date-only and date-time formats
- **Export Functionality**: Download forecast results as CSV files

## 🛠 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Web browser (Chrome, Firefox, Safari, etc.)

## 📦 Installation

### Step 1: Clone or Download the Project
Navigate to your desired directory (e.g., Desktop) and ensure the EcoWatt folder is there.

### Step 2: Set Up Python Environment
Open Command Prompt or PowerShell and navigate to the EcoWatt directory:

```bash
cd C:\Users\G Uday Kumar\Desktop\EcoWatt
```

### Step 3: Install Dependencies
Run the following command to install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- streamlit (web interface)
- pandas (data manipulation)
- numpy (numerical computations)
- scikit-learn (machine learning)
- matplotlib (plotting)

## 🏗 Project Structure

```
EcoWatt/
│
├── app.py                 # Main Streamlit application
├── data_generator.py      # Synthetic data generation script
├── model.py              # Machine learning model and prediction logic
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── energy_data.csv       # Generated synthetic data (created after running)
└── energy_model.pkl      # Trained ML model (created after training)
```

## 🚀 Usage

### Step 1: Run the Application
From the EcoWatt directory, execute:

```bash
python -m streamlit run app.py
```

### Step 2: Access the Web Interface
Open your web browser and go to: `http://localhost:8501`

### Step 3: Choose Data Source

#### Option A: Generate Synthetic Data
1. Select "Generate Synthetic Data" from the sidebar
2. Adjust the number of days using the slider (365-1825 days)
3. Click "Generate Data"
4. The synthetic data will be created and displayed

#### Option B: Upload Your Own CSV
1. Select "Upload CSV" from the sidebar
2. Click "Browse files" and select your CSV file
3. Ensure your CSV has the required columns (see Data Format section)
4. The data will be validated and loaded

### Step 4: Train the Model
1. Click "Train Model" in the sidebar
2. Wait for the training process to complete
3. A success message will appear when done

### Step 5: Generate Forecasts
1. Use the slider to select days to forecast (1-90 days)
2. Click "Generate Forecast"
3. View the forecast chart and data table
4. Download the forecast as CSV if needed

## 📊 Data Format

### Required Columns
- `date`: Date in YYYY-MM-DD format (e.g., 2023-01-01)
- `consumption_kwh`: Energy consumption in kilowatt-hours (numeric)

### Optional Column
- `time`: Time in HH:MM:SS format (e.g., 14:30:00)

### CSV Examples

**Date Only:**
```csv
date,consumption_kwh
2023-01-01,120.5
2023-01-02,118.8
2023-01-03,125.2
```

**Date and Time:**
```csv
date,time,consumption_kwh
2023-01-01,08:00:00,120.5
2023-01-01,14:30:00,150.2
2023-01-02,08:00:00,118.8
```

### Data Requirements
- Dates must be in chronological order (app will sort automatically)
- Consumption values should be positive numbers
- No missing values in required columns
- Minimum 8 data points for model training

## 🧠 How It Works

### Data Processing
1. **Input Validation**: Checks for required columns and data types
2. **Date/Time Handling**: Combines date and time columns if present
3. **Data Sorting**: Ensures chronological order for time series analysis

### Machine Learning Model
- **Algorithm**: Linear Regression with lag features
- **Features**: Uses previous 7 days of consumption as predictors
- **Training**: Splits data into 80% training, 20% testing
- **Prediction**: Generates future forecasts based on recent patterns

### Forecasting Process
1. Takes the last 7 days of actual consumption
2. Uses the trained model to predict the next day
3. Uses that prediction as input for the following day
4. Repeats for the desired forecast period

### Synthetic Data Generation
- **Base Consumption**: 100 kWh average
- **Seasonal Patterns**: Yearly cycles (±20 kWh)
- **Weekly Patterns**: Daily variations (±10 kWh)
- **Random Noise**: Realistic variability (±5 kWh)
- **Trend**: Slight upward consumption trend

## 🔧 Troubleshooting

### Common Issues

**"Module not found" errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Try upgrading pip: `python -m pip install --upgrade pip`

**App won't start:**
- Check if port 8501 is available
- Try a different port: `streamlit run app.py --server.port 8502`

**CSV upload fails:**
- Verify column names match exactly: `date`, `consumption_kwh`
- Check date format: YYYY-MM-DD
- Ensure no missing values in required columns

**Model training fails:**
- Need at least 8 data points
- Check for non-numeric values in consumption column
- Ensure dates are parseable

**Forecast generation fails:**
- Train the model first
- Check that data is loaded
- Verify model file exists (energy_model.pkl)

### Performance Tips
- For large datasets (>10,000 rows), consider using more advanced models
- Close other Streamlit apps before running
- Use Chrome browser for best performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the code comments in the Python files
3. Ensure all prerequisites are met

---

**Built with ❤️ using Streamlit, scikit-learn, and Python**
