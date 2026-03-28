# 📱 PhonePe Pulse — Data Analysis & Visualization

An end-to-end data science project that **extracts**, **transforms**, **analyzes**, and **visualizes** PhonePe Pulse digital payment data across India (2018–2024). Built with Python, SQLite, Streamlit, and Scikit-learn.

---

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [Key Insights](#key-insights)
- [Screenshots](#screenshots)

---

## 🎯 Problem Statement

With the increasing reliance on digital payment systems like PhonePe, understanding the dynamics of transactions, user engagement, and insurance-related data is crucial for improving services and targeting users effectively. This project aims to:

- Analyze and visualize **aggregated payment categories**
- Create **geographical maps** for total values at state and district levels
- Identify **top-performing states, districts, and pin codes**
- Build **ML models** to predict transaction volumes

---

## 📁 Project Structure

```
Phone Pe/
│
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Files excluded from Git
│
├── src/                         # Source code
│   ├── data_extraction.py       # ETL pipeline — JSON → SQLite
│   └── app.py                   # Streamlit interactive dashboard
│
├── notebooks/                   # Jupyter notebooks
│   ├── PhonePe_EDA_v2.ipynb     # Exploratory Data Analysis (20+ charts)
│   └── PhonePe_ML_v2.ipynb      # ML models (RF, GBM, Ridge)
│
├── docs/                        # Documentation & presentations
│   ├── Phone Pe.docx            # Problem statement document
│   └── Phone Pe.pptx            # Presentation slides
│
├── pulse-master/                # PhonePe Pulse raw dataset (JSON)
│   └── data/
│       ├── aggregated/          # Aggregated transaction/user/insurance
│       ├── map/                 # State & district level data
│       └── top/                 # Top states/districts/pincodes
│
└── models/                      # Saved model artifacts (generated locally)
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12+ |
| Database | SQLite |
| ETL | Pandas, JSON, os |
| Visualization | Matplotlib, Seaborn, Plotly |
| Dashboard | Streamlit |
| ML Models | Scikit-learn (Random Forest, GBM, Ridge) |
| Version Control | Git & GitHub |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/PhonePe-Pulse-Analysis.git
cd PhonePe-Pulse-Analysis
```

### 2. Create a virtual environment
```bash
python -m venv phonepe
# Windows
phonepe\Scripts\activate
# macOS/Linux
source phonepe/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the ETL pipeline (builds the SQLite database)
```bash
python src/data_extraction.py
```

### 5. Launch the Streamlit dashboard
```bash
streamlit run src/app.py
```

---

## 🔑 Key Insights

- **UPI dominance:** Peer-to-peer and Merchant payments account for the vast majority of digital transactions.
- **Southern states lead:** Maharashtra, Karnataka, and Telangana consistently rank in the top 3 by transaction volume.
- **Mobile brand concentration:** Xiaomi and Samsung together represent ~45% of registered users.
- **Insurance is a growth segment:** Insurance transactions grew exponentially from 2020 onwards.
- **Urban concentration:** A small number of metro districts and pincodes drive disproportionate transaction value.

---

## 📊 Screenshots

> _Run the Streamlit dashboard to explore interactive visualizations._

---

## 📜 License

Dataset licensed under [CDLA-Permissive-2.0](https://github.com/PhonePe/pulse/blob/master/LICENSE).

---

## 🙏 Acknowledgements

- [PhonePe Pulse](https://github.com/PhonePe/pulse) for the open dataset
- Built as part of a Data Science capstone project
