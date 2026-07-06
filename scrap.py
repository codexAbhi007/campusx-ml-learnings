import requests
from bs4 import BeautifulSoup
import re


url = "https://www.snuniv.ac.in/department-details.aspx"

params = {
    "ajax": "1",
    "section": "faculty",
    "schoolid": "24",
    "deptid": "0"
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest"
}


response = requests.get(url, params=params, headers=headers)
response.raise_for_status()


soup = BeautifulSoup(response.text, "html.parser")


def clean_name(name):
    # Remove text inside brackets
    name = re.sub(r"\(.*?\)", "", name)

    # Remove titles
    name = re.sub(
        r"\b(dr|prof|mr|mrs|ms|miss|ar)\.?\b",
        "",
        name,
        flags=re.IGNORECASE
    )

    # Remove dots
    name = name.replace(".", "")

    # Remove multiple spaces
    name = " ".join(name.split())

    # Convert to Title Case
    return name.title()


faculty_names = []

cards = soup.select("div.entry-content")

for card in cards:
    h5 = card.find("h5")

    if h5:
        name = clean_name(h5.get_text(strip=True))
        faculty_names.append(name)


# Remove duplicates
faculty_names = list(dict.fromkeys(faculty_names))

# Sort alphabetically
faculty_names = sorted(faculty_names)


print(f"\nTotal Faculty Found: {len(faculty_names)}\n")

for i, name in enumerate(faculty_names, start=1):
    print(f"{i}. {name}")
