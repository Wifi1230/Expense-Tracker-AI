🚀 AI-Powered Professional Expense Tracker
A sophisticated personal finance management tool built with **Python 3.14**, featuring a **Hybrid Anomaly Detection System** that combines classical statistics with modern Machine Learning.

✨ Key Features
* **Hybrid AI Anomaly Detection**: 
    * **Layer 1 (Statistical)**: Real-time **Z-Score** analysis using **NumPy** to catch immediate value outliers based on category history.
    * **Layer 2 (Machine Learning)**: **Isolation Forest** (Unsupervised Learning) via **Scikit-Learn** to detect complex behavioral patterns, analyzing both price and temporal data (Day of Week).
* **Data Engineering**: Advanced manipulation using **Pandas DataFrames** with optimized memory management (`itertuples`, defensive copying to prevent `SettingWithCopyWarning`).
* **Smart Preprocessing**: Automated **Feature Engineering** (encoding Dates into cyclical Day-of-Week numerical features) for ML model compatibility.
* **Robust Validation**: Strict input sanitization, case-insensitive category matching, and "Cold Start" protection for the ML engine (requires min. 10 records to activate).
* **Data Persistence**: Stateless architecture with automated CSV synchronization and in-memory state tracking for high performance.
* **DevOps Ready**: Fully containerized using **Docker** for consistent deployment across any environment.

🛠 Tech Stack
* **Language**: Python 3.14
* **AI/ML**: Scikit-Learn (Isolation Forest), NumPy
* **Data Science**: Pandas
* **Containerization**: Docker
* **Version Control**: Git / GitHub

🐳 Running with Docker (Recommended)
The easiest way to run the application without worrying about local dependencies:
```bash
docker build -t expense-tracker .
docker run -it --name tracker-app expense-tracker
