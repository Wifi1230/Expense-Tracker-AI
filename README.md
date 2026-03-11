#🚀 AI-Powered Professional Expense Tracker
A robust personal finance management tool built with **Python 3.14**, leveraging the power of **Pandas** for data engineering and **NumPy** for statistical analysis. This project demonstrates a full production-ready pipeline, from data validation to containerized deployment.

##✨ Key Features
* **Data Engineering**: Advanced data manipulation using **Pandas DataFrames** (SQL-like logic for sorting and aggregation).
* **AI Anomaly Detection**: Implementation of an unsupervised statistical model using **NumPy** to detect high-value transaction outliers.
* **Data Persistence**: Stateless architecture with automated CSV synchronization.
* **Robust Validation**: Intelligent input handling (supports multiple decimal formats and prevents data corruption).
* **DevOps Ready**: Fully containerized using **Docker** for consistent deployment across any environment.

##🛠 Tech Stack
* **Language**: Python 3.14
* **Libraries**: Pandas, NumPy
* **Containerization**: Docker
* **Version Control**: Git / GitHub

##🐳 Running with Docker (Recommended)
The easiest way to run the application without worrying about local dependencies:
```bash
docker build -t expense-tracker .
docker run -it --name tracker-app expense-tracker
