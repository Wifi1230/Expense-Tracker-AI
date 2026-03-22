🚀 AI-Powered Expense Tracker
A personal finance tracking tool built with Python, featuring a Hybrid Anomaly Detection System that combines statistical methods with machine learning.

✨ Key Features
* **Hybrid Anomaly Detection**: 
    * **Layer 1 (Statistical)**: Real-time **Z-Score** analysis using **NumPy** to detect unusual expenses within a category.
    * **Layer 2 (Machine Learning)**: **Isolation Forest** via **Scikit-Learn** to identify more complex spending anomalies based on price and day of the week.
* **Data Preprocessing**: Efficient handling of data using Pandas DataFrames.
* **Feature Engineering**: Automatic extraction of day-of-week from transaction dates for ML model input.
* **Robust Validation**: Input checks for price, category, and empty fields; cold-start protection for ML (requires min. 10 records).
* **Data Persistence**: Automatic CSV synchronization and in-memory tracking of expenses.

🛠 Tech Stack
* **Language**: Python 3.14
* **AI/ML**: Scikit-Learn (Isolation Forest), NumPy
* **Data Analysis**: Pandas
* **Containerization**: Docker
* **Version Control**: Git / GitHub

🐳 Running with Docker (Recommended)
The easiest way to run the application without worrying about local dependencies:
```bash
docker build -t expense-tracker .
docker run -it --name tracker-app expense-tracker
