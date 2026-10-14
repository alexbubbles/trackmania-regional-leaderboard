# 🏎️ Trackmania Seasonal Leaderboard Tracker

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey.svg?logo=flask)
![Frontend](https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JS-E34F26.svg)

A lightweight, fast, and sleek web application built to extract and filter regional leaderboards for Trackmania seasonal campaigns. 

While official tools and Trackmania.io provide global and broad regional rankings, this tool allows players to dig deeper by filtering the global leaderboard for **any specific region, province, or country** (e.g., "Marche", "Italy", "Europe").

## ✨ Features

* **🌍 Custom Regional Filtering:** Search for players based on any specific zone text string found in their Trackmania profile.
* **📅 Complete Campaign History:** Dropdown support for every official seasonal campaign from Summer 2020 up to Summer 2026.
* **🏳️ Dynamic Flags:** Automatically detects the player's country from the API zone data and assigns the correct national flag emoji.
* **🎨 Trackmania.io Inspired UI:** A beautiful, responsive dark-mode interface using *Inter* and *Montserrat* fonts, complete with a custom background and glassmorphism effects.
* **📄 Client-Side Pagination:** Efficiently handles thousands of results by rendering 50 players per page, allowing instant page jumping without re-fetching data.
* **🛡️ Safe API Polling:** Built-in delay mechanisms (`1.5s` per 100 players) to respect Trackmania.io rate limits and prevent IP bans.

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask, `requests`
* **Frontend:** HTML5, Vanilla CSS3 (Custom Dark Theme), Vanilla JavaScript (ES6)
* **API:** [Trackmania.io API](https://trackmania.io/)

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/trackmania-leaderboard-tracker.git](https://github.com/YOUR-USERNAME/trackmania-leaderboard-tracker.git)
   cd trackmania-leaderboard-tracker
