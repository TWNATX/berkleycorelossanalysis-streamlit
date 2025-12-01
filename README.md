# BerkleyCore Loss Analysis Platform - Streamlit Edition

A comprehensive commercial insurance claims analysis tool for loss control consultants, now powered by Streamlit for easy deployment and enhanced interactivity.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

## Quick Start

### Option 1: Deploy to Streamlit Cloud (Recommended)

1. Fork or push this repo to your GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → Select your repo → Set `app.py` → Deploy
4. Done! Share your URL: `https://your-app.streamlit.app`

### Option 2: Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## Features

### 📊 Dashboard
- Real-time KPI metrics (Total Claims, Incurred, Average Claim, Open Claims)
- Risk score assessment with visual indicators
- Interactive charts for loss causes, trends, and status distribution

### 🔍 Detailed Analysis
- Monthly and yearly trend analysis
- Geographic distribution maps
- Severity and lag time distributions
- Filterable data tables with export capability

### 🛡️ Risk Control
- Automated risk scoring (0-100 scale)
- Prioritized mitigation recommendations
- ROI calculations with payback periods
- Implementation action plans

### 📄 Reports & Export
- Executive summary reports
- Markdown export for documentation
- CSV exports for data and recommendations

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup

1. Clone or download this directory:
```bash
cd berkleycore_streamlit
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser to `http://localhost:8501`

## Usage

### Data Upload
- Click the file uploader in the sidebar
- Supported formats: CSV, Excel (.xlsx, .xls)
- Automatically detects Tableau export format
- Universal field mapping handles 50+ column name variations

### Sample Data
- Click "Load Sample Data" to explore the platform with demo data
- 500 sample claims across multiple years and coverage lines

### Navigation
Use the navigation tabs to access different sections:
- **Dashboard**: Overview metrics and key visualizations
- **Analysis**: Deep-dive analysis with filters
- **Risk Control**: Recommendations and ROI calculations
- **Reports**: Generate and export reports

## File Structure

```
berkleycore_streamlit/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── config/
│   ├── __init__.py
│   ├── field_mappings.py     # Universal column mappings
│   └── risk_strategies.py    # Risk mitigation strategies
├── utils/
│   ├── __init__.py
│   ├── data_processing.py    # File loading & standardization
│   ├── calculations.py       # Insurance metrics & ROI
│   └── visualizations.py     # Plotly chart builders
└── pages/                    # (For multi-page apps)
```

## Deployment Options

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

### Azure App Service
1. Create Azure Web App (Python 3.11)
2. Configure startup command: `streamlit run app.py --server.port 8000`
3. Deploy via GitHub Actions or Azure CLI

## Data Format Requirements

### Standard Format
The platform recognizes common column names including:
- Claim identifiers: `Claim Number`, `ClaimNumber`, `Claim #`, etc.
- Dates: `Loss Date`, `Report Date`, `Closed Date`
- Financials: `Incurred`, `Paid`, `Reserve`, `Expense`
- Categories: `Loss Cause`, `State`, `Status`, `Line of Business`

### Tableau Export Format
Supports pivot exports with:
- `Measure Names` column
- `Measure Values` column
- Standard dimension columns

## Coverage Lines Supported
- Workers Compensation
- General Liability
- Commercial Auto
- Property
- Professional Liability (E&O)
- Cyber Liability

## Technical Notes

- All calculations use conservative actuarial assumptions
- ROI projections include confidence factors based on claim volume
- Risk scores align with industry benchmarks
- Field mapping adapts to Guidewire, Duck Creek, and other major systems

## License

Proprietary - BerkleyCore Platform

## Support

For questions or issues, contact the development team.

---

*BerkleyCore Loss Analysis Platform v2.0 - Streamlit Edition*
