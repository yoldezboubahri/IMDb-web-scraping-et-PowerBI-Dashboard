from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Optional

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "data"
OUTPUT_FILE = OUTPUT_DIR / "IMDB_DATA_scraped.csv"
IMDB_TOP_250_URL = "https://www.imdb.com/chart/top/"


def clean_text(value: Optional[str]) -> str:
    """Normalize whitespace and non-breaking spaces."""
    if not value:
        return ""
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def parse_duration_to_minutes(duration: str) -> Optional[int]:
    """Convert IMDb duration strings such as '2h 22m' to minutes."""
    if not duration:
        return None

    hours = re.search(r"(\d+)\s*h", duration, flags=re.IGNORECASE)
    minutes = re.search(r"(\d+)\s*m", duration, flags=re.IGNORECASE)

    total = 0
    if hours:
        total += int(hours.group(1)) * 60
    if minutes:
        total += int(minutes.group(1))

    return total if total else None


def parse_rating_and_votes(rating_element) -> tuple[str, str]:
    """
    Extract rating and vote count when IMDb exposes them in the rating element.
    The vote count is kept as displayed text because IMDb may use k/M suffixes.
    """
    if rating_element is None:
        return "", ""

    rating_text = clean_text(rating_element.get_text(" ", strip=True))
    aria_label = clean_text(rating_element.get("aria-label", ""))

    # Current IMDb markup often exposes e.g. "IMDb rating: 9.3".
    rating_match = re.search(r"(\d+[.,]\d+|\d+)", aria_label or rating_text)
    rating = rating_match.group(1).replace(".", ",") if rating_match else ""

    # Vote count may be in a nearby element or title attribute.
    vote_text = ""
    parent = rating_element.parent
    if parent is not None:
        vote_element = parent.select_one(
            ".ipc-rating-star--voteCount, "
            "[data-testid='ratingGroup--container'] .ipc-rating-star--voteCount"
        )
        if vote_element is not None:
            vote_text = clean_text(vote_element.get_text(" ", strip=True))

    if not vote_text:
        title_attr = clean_text(rating_element.get("title", ""))
        vote_match = re.search(r"\(([^()]*)\)", title_attr)
        if vote_match:
            vote_text = vote_match.group(1)

    return rating, vote_text


def create_driver() -> webdriver.Chrome:
    """Create a Chrome session using Selenium Manager."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--lang=fr-FR")
    # Uncomment for headless execution:
    # options.add_argument("--headless=new")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    return webdriver.Chrome(options=options)


def load_top_250_page(driver: webdriver.Chrome) -> None:
    """Open IMDb Top 250 and wait for movie cards to appear."""
    driver.get(IMDB_TOP_250_URL)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
            )
        )
    except TimeoutException as exc:
        raise RuntimeError(
            "Les éléments du Top 250 n'ont pas été chargés. "
            "IMDb a peut-être modifié sa page ou bloqué la requête."
        ) from exc


def scroll_to_load_movies(driver: webdriver.Chrome, target_count: int = 250) -> None:
    """Scroll progressively until the target number of movie cards is loaded."""
    last_count = 0
    unchanged_rounds = 0

    for _ in range(30):
        cards = driver.find_elements(
            By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item"
        )
        current_count = len(cards)
        print(f"Films chargés : {current_count}/{target_count}")

        if current_count >= target_count:
            break

        if current_count == last_count:
            unchanged_rounds += 1
        else:
            unchanged_rounds = 0

        if unchanged_rounds >= 3:
            break

        last_count = current_count
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(2)

    # Return to the top before taking the page source.
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)


def extract_movies(page_source: str) -> list[dict]:
    """Parse movie cards from the rendered IMDb HTML."""
    soup = BeautifulSoup(page_source, "html.parser")
    movies = []

    movie_cards = soup.find_all(
        "li", class_="ipc-metadata-list-summary-item"
    )

    for index, movie in enumerate(movie_cards, start=1):
        title_tag = movie.find("h3", class_="ipc-title__text")

        if title_tag:
            title_parts = clean_text(title_tag.get_text()).split(". ", 1)
            if len(title_parts) == 2 and title_parts[0].isdigit():
                rank = int(title_parts[0])
                title = title_parts[1]
            else:
                rank = index
                title = clean_text(title_tag.get_text())
        else:
            rank = index
            title = ""

        # Metadata: year, duration and certificate/classification.
        year = ""
        duration = ""
        classification = ""

        metadata_div = movie.find("div", class_="cli-title-metadata")
        if metadata_div:
            spans = metadata_div.find_all("span", recursive=True)
            metadata_values = [
                clean_text(span.get_text())
                for span in spans
                if clean_text(span.get_text())
            ]

            # IMDb cards generally list year, runtime, then certificate.
            if len(metadata_values) >= 1:
                year_match = re.search(r"\b(18|19|20)\d{2}\b", metadata_values[0])
                year = year_match.group(0) if year_match else metadata_values[0]

            if len(metadata_values) >= 2:
                duration = metadata_values[1]

            if len(metadata_values) >= 3:
                classification = metadata_values[2]

        # Rating and votes.
        rating_element = movie.select_one(
            "span.ipc-rating-star, "
            ".ipc-rating-star--rating"
        )
        rating, votes = parse_rating_and_votes(rating_element)

        movies.append(
            {
                "Index": index - 1,
                "Rank": rank,
                "Titre": title,
                "Année": year,
                "Durée": duration,
                "Classification": classification,
                "Note": rating,
                "Votes": votes,
            }
        )

    return movies


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    driver = None

    try:
        print("Ouverture d'IMDb Top 250...")
        driver = create_driver()
        load_top_250_page(driver)

        print("Chargement des films...")
        scroll_to_load_movies(driver)

        print("Extraction des données...")
        movies = extract_movies(driver.page_source)

        if not movies:
            raise RuntimeError(
                "Aucun film n'a été extrait. Vérifiez la structure HTML d'IMDb."
            )

        df = pd.DataFrame(movies)

        # Add a numeric runtime column when duration is available.
        df["Durée (min)"] = df["Durée"].apply(parse_duration_to_minutes)

        # Keep a consistent column order.
        columns = [
            "Index",
            "Rank",
            "Titre",
            "Année",
            "Durée",
            "Classification",
            "Note",
            "Votes",
            "Durée (min)",
        ]
        df = df.reindex(columns=columns)

        df.to_csv(OUTPUT_FILE, sep=";", index=False, encoding="utf-8-sig")

        print(f"\nExtraction terminée : {len(df)} films récupérés.")
        print(f"Fichier enregistré : {OUTPUT_FILE}")
        print(df.head())

    except (RuntimeError, WebDriverException) as error:
        print(f"Erreur Selenium / IMDb : {error}")
    except Exception as error:
        print(f"Une erreur inattendue est survenue : {error}")
        raise
    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
