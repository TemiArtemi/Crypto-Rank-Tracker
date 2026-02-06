# 📊 Crypto Rank Tracker (Top 400)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://crypto-rank-tracker.streamlit.app)

**Monitor the historical ranking evolution of the top 400 cryptocurrencies.**

This project is an automated tool that tracks daily market positions using the **CoinMarketCap API** and visualizes trends through an interactive **Streamlit** dashboard.

## 🚀 Live Demo
👉 **[Click here to open the Dashboard](https://crypto-rank-tracker.streamlit.app)**

---

## ✨ Key Features
* **📈 Historical Tracking**: Automatically saves the rank of the top 400 coins every day.
* **🤖 Fully Automated**: A GitHub Actions robot runs every morning (09:00 UTC) to fetch new data without human intervention.
* **📊 Interactive Visualization**:
    * Dynamic charts using **Plotly**.
    * Inverted Y-Axis (Rank #1 is at the top).
    * Filter by **Daily**, **Weekly**, or **Monthly** frequency.
* **🔍 Smart Search**: Easily find any token by name or ticker (e.g., "Polkadot (DOT)").

## 🛠️ Tech Stack
* **Python 3.9**
* **Streamlit** (Web Dashboard)
* **Pandas** (Data Processing & Deduplication)
* **Plotly Express** (Data Visualization)
* **GitHub Actions** (CI/CD Automation)
* **CoinMarketCap API** (Data Source)

## ⚙️ How it Works
1.  **Data Collection**: The script `ranking_code.py` fetches the top 400 cryptocurrencies via API.
2.  **Data Cleaning**: It merges new data with the existing history in `historico_top400_ranking.csv`, ensuring no duplicates exist for the same day.
3.  **Automation**: The `.github/workflows/daily_update.yml` workflow executes the script automatically every 24 hours.
4.  **Visualization**: The `app.py` script reads the updated CSV directly from the repository to render the charts in real-time.

## 📦 Installation (Local)
If you want to run this project on your own machine:

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/TemiArtemi/Crypto-Rank-Tracker.git](https://github.com/TemiArtemi/Crypto-Rank-Tracker.git)
    cd Crypto-Rank-Tracker
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Key**:
    Create a `.streamlit/secrets.toml` file and add your CoinMarketCap key:
    ```toml
    API_KEY = "your_api_key_here"
    ```

4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

---
*Created by [TemiArtemi](https://github.com/TemiArtemi)*
