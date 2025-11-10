# DreamShift SEO Dashboard 📊

*Lightweight Streamlit dashboard for visualizing DreamShift blog performance directly from Google Search Console.*

[![Platform](https://img.shields.io/badge/Platform-Streamlit-FF4B4B)](#)
[![Data%20Source](https://img.shields.io/badge/Data-Google%20Search%20Console-1a73e8)](#)
[![Language](https://img.shields.io/badge/Language-Python-3776AB)](#)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)](#)
[![License](https://img.shields.io/badge/License-MIT-black)](#)

---

## 🔗 Live Dashboard

**Streamlit App:**

```text
https://dreamshift-seo-dashboard.streamlit.app
```

---

## ✨ Overview

Version 1 of the DreamShift SEO Dashboard helps visualize blog performance metrics directly from **Google Search Console**.

* Displays **clicks, impressions, and trends** over time.
* Identifies **top-performing articles** by clicks and impressions.
* Includes flexible date filters: **last 7, 30, 90, 365 days or custom range**.
* Built entirely with **Streamlit + Google Search Console API**.

Future updates will integrate **GA4 metrics**, author segmentation, and **automated reporting.**

---

## 🧠 Core Features

* 🔍 Pulls live data using **Google Search Console API**.
* 📆 Date filtering: weekly, monthly, quarterly, yearly, or custom.
* 🏆 Highlights top 5 articles by clicks & impressions.
* 📈 Interactive trend charts for clicks & impressions.
* 📰 Counts total blog articles with impressions.

---

## 📁 Project Structure

```bash
dreamshift-seo-dashboard/
│
├── app.py                    # Main Streamlit dashboard
├── .streamlit/
│   └── secrets.toml          # Google service account credentials
├── requirements.txt          # Dependencies
├── README.md                 # Project overview (this file)
├── .gitignore                # Git ignore rules
└── LICENSE                   # MIT license
```

---

## ⚙️ Setup Guide

### 1️⃣ Enable Search Console API

1. Go to **Google Cloud Console** → Create a new project.
2. Enable **Search Console API** under *APIs & Services*.
3. Create a **Service Account** and download the JSON key.
4. Add that service account email to your Search Console property with **Read Access**.

---

### 2️⃣ Add credentials to `.streamlit/secrets.toml`

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "search-console-reader@your-project-id.iam.gserviceaccount.com"
client_id = "..."
token_uri = "https://oauth2.googleapis.com/token"
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

or manually:

```bash
pip install streamlit google-api-python-client google-auth pandas python-dateutil
```

---

### 4️⃣ Run locally

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔧 Environment Variables

Edit in `app.py`:

```python
PROPERTY_URI = "https://dreamshift.lk/"  # Replace with your verified domain
BLOG_PATH_KEYWORD = "/blog/"             # Adjust if needed (e.g., /insights/)
```

---

## 🧱 Roadmap

* [ ] Integrate **GA4** metrics (sessions, conversions)
* [ ] Add **author/category** filters
* [ ] Automate **weekly summary email reports**
* [ ] Export CSV and visualization snapshots

---

## 🪪 License

This project is licensed under the **MIT License**.
See [`LICENSE`](./LICENSE) for full details.