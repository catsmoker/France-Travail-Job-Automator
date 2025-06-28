# France Travail Job Automator

A powerful and flexible Python bot to automate job applications on the [France Travail](https://candidat.francetravail.fr) website using the Playwright library.

### 🔄 Default Mode: Seasonal Jobs (`Saisonnier`)

Easily customizable to apply for any job title or location.

---

## 🚀 Features

* ✅ **Automated Applications** – Log in once and let the bot handle the rest.
* 🎯 **Smart Filtering** – Skips jobs requiring experience by checking for numbers in the “skills” section.
* 🍪 **Persistent Login** – Saves your session with `auth.json`, no need to log in every time.
* 📄 **Pagination Support** – Automatically clicks “Show More” to load all job listings.
* 🧠 **Duplicate Detection** – Skips jobs you've already applied to.
* 🔧 **Custom Search Support** – Modify a single URL to target your desired roles or locations.

---

## ⚠️ Disclaimer

> **Use this script at your own risk.**

* **Terms of Service Violation:** Automating France Travail likely violates their terms and may result in account suspension.
* **Ethical Concerns:** Mass-applying may hurt your credibility. Personalized applications are more effective.
* **No Warranty:** France Travail’s website may change. You may need to update the script manually if selectors break.

---

## 🧰 Requirements

* Python 3.8+
* [Git](https://git-scm.com/) (or download the repo ZIP manually)
* [Playwright](https://playwright.dev/python/)

---

## 🛠️ Installation

```bash
# Clone this repo
git clone https://github.com/catsmoker/France-Travail-Job-Automator.git
cd Saisonnier-Job-Bot

# Create and activate virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
echo playwright > requirements.txt
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

---

## 🔐 First-Time Setup (Login)

Run this **once** to save your session:

```bash
python save_state.py
```

* A browser window will open.
* Log in to your France Travail account manually.
* Once logged in, close the window.
* `auth.json` will be created — this file stores your session.

---

## 🔎 Customize Your Job Search

1. Go to France Travail and perform a search manually.
2. Copy the full search URL from your browser.
3. Open `job_automator.py` and replace this line:

```python
search_url = "https://candidat.francetravail.fr/offres/recherche?motsCles=Saisonnier&offresPartenaires=true&rayon=10&tri=0"
```

---

## ▶️ Run the Bot

```bash
python job_automator.py
```

The bot will:

* Load your saved session.
* Fetch job listings from your custom URL.
* Apply automatically if the job doesn’t require experience.

---

## 🧯 Troubleshooting

| Issue                | Fix                                                    |
| -------------------- | ------------------------------------------------------ |
| 🔍 Element not found | Update CSS selectors using browser DevTools            |
| 🔓 Not logging in    | Delete `auth.json`, re-run `save_state.py`             |
| ❌ Errors on start    | Ensure Playwright and browsers are installed correctly |




---
