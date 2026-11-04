# 🎬 Le Monde en Films — IMDb Power BI Dashboard

Interactive Power BI dashboard for exploring movie data and cinema trends.

## Project overview

This project combines web scraping, data preparation and interactive visualization to transform IMDb Top 250 movie information into an analytical dashboard.

## Workflow

1. **Collection:** Selenium automates the browser and loads the IMDb Top 250 page.
2. **Extraction:** BeautifulSoup parses movie titles, rankings, years, runtimes, classifications and ratings from the rendered HTML.
3. **Preparation:** Pandas structures the extracted information and derives runtime in minutes.
4. **Visualization:** Power BI is used to explore movie characteristics and cinema trends through interactive visuals and filters.


## Dashboard Preview

![IMDb Power BI Dashboard](screenshots/imdb_dashboard.png)

*Tableau de bord Power BI « Le Monde en Films » : exploration interactive des 250 meilleurs films IMDb, analyse des notes, des votes et des caractéristiques des films.*

## Tools and technologies

- **Power BI Desktop** — data modeling, interactive reports and visualizations
- **Python** — web scraping and data preparation
- **Pandas** — data manipulation (if used in the collection/preparation scripts)

See [`requirements.txt`](requirements.txt) for the Python environment dependencies. Remove packages that are not used by your actual scripts.
=======
## Technologies

- Python
- Selenium
- BeautifulSoup
- Pandas
- Power BI


## Repository structure

```text
IMDb-PowerBI-Dashboard/
├── dashboard/
│   └── Le_Monde_en_Films.pbix
├── data/
│   ├── IMDB_DATA.csv
│   └── README.md
├── screenshots/
├── src/
│   └── scrape_imdb.py
├── .gitattributes
├── .gitignore
├── README.md
└── requirements.txt
```

## Run the scraper

Requirements: Python and Google Chrome installed.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python src/scrape_imdb.py
```

The script saves the extracted records to `data/IMDB_DATA_scraped.csv`.

Selenium 4 uses Selenium Manager to manage the Chrome driver. If IMDb changes its HTML structure, the CSS selectors in the script may need to be updated.

## Dashboard

Open `dashboard/Le_Monde_en_Films.pbix` with Power BI Desktop.

Add screenshots of the report pages to `screenshots/` and embed them here, for example:

```markdown
![Dashboard overview](screenshots/dashboard_overview.png)
```

## Data notes

The supplied `data/IMDB_DATA.csv` contains 250 records and additional `Pays` and `Langue` columns. These enrichment fields are present in the supplied dataset, but their collection logic was not visible in the screenshots used to reconstruct the scraper.

Please respect IMDb's terms of use and applicable data-use restrictions. Do not overload the website with automated requests.

## Author

**Yoldez Boubahri**  
ESSAI — University of Carthage  
[GitHub](https://github.com/yoldezboubahri) · [LinkedIn](https://www.linkedin.com/in/yoldez-boubahri-731b13326/)
