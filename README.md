# 🎬 Le Monde en Films — IMDb Power BI Dashboard

Interactive dashboard for exploring movie data and cinema trends with **Power BI**.

## Project overview

**Le Monde en Films** is a data analytics and visualization project built around IMDb-related movie data. It covers the main stages of an analytics workflow:

- Data collection through web scraping
- Data cleaning, preparation and structuring
- Exploratory data analysis
- Creation of analytical indicators
- Interactive visualization in Power BI

The dashboard uses visualizations and filters to make it easier to explore movie characteristics and trends.

## Dashboard Preview

![IMDb Power BI Dashboard](screenshots/imdb_dashboard.png)

*Tableau de bord Power BI « Le Monde en Films » : exploration interactive des 250 meilleurs films IMDb, analyse des notes, des votes et des caractéristiques des films.*

## Tools and technologies

- **Power BI Desktop** — data modeling, interactive reports and visualizations
- **Python** — web scraping and data preparation
- **Pandas** — data manipulation (if used in the collection/preparation scripts)

See [`requirements.txt`](requirements.txt) for the Python environment dependencies. Remove packages that are not used by your actual scripts.

## Repository structure

```text
IMDb-PowerBI-Dashboard/
├── dashboard/
│   └── Le_Monde_en_Films.pbix
├── data/
│   └── README.md
├── screenshots/
│   └── (add dashboard screenshots here)
├── .gitignore
├── .gitattributes
├── LICENSE
├── README.md
└── requirements.txt
```

## Getting started

### 1. View the dashboard

1. Install [Power BI Desktop](https://powerbi.microsoft.com/desktop/).
2. Clone or download this repository.
3. Open `dashboard/Le_Monde_en_Films.pbix` in Power BI Desktop.
4. Explore the report pages, filters and visualizations.

### 2. Set up the Python environment

Python dependencies are listed in `requirements.txt`.

```bash
python -m venv .venv
```

Activate the environment:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> The repository currently contains the Power BI report, not the original scraping scripts. The requirements file is a starting environment for the data collection/preparation workflow; keep only the packages actually used by your scripts.

## Data and reproducibility

The source dataset and scraping scripts are not included in this repository. See [`data/README.md`](data/README.md) for notes on data provenance, usage and future additions.

If you add scripts later, place them in a dedicated folder (for example, `src/`) and document the exact execution steps here. Do not commit API keys, credentials, personal data or datasets you are not authorized to redistribute.

## Author

**Yoldez Boubahri**  
Engineering student in Statistics and Information Analysis  
ESSAI — University of Carthage

- [GitHub](https://github.com/yoldezboubahri)
- [LinkedIn](https://www.linkedin.com/in/yoldez-boubahri-731b13326/)
