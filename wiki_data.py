
import re
import sys
import requests

API_URL = "https://dragon-adventures.fandom.com/api.php"
TIMEOUT = 15



def fetch_wikitext(page_title):
    params = {
        "action": "parse",
        "page": page_title,
        "prop": "wikitext",
        "format": "json",
        "formatversion": "2",
    }
    r = requests.get(API_URL, params=params, timeout=TIMEOUT,
                      headers={"User-Agent": "dragon-card-maker/1.0"})
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise ValueError(f"Wiki API error for '{page_title}': {data['error'].get('info')}")
    return data["parse"]["wikitext"]


def clean_wikitext(text):
    if text is None:
        return ""
    text = re.sub(r"<ref[^>]*/?>.*?(</ref>)?", "", text, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"\{\{[^{}]*\}\}", "", text)
    text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[[^\s\]]+\s+([^\]]+)\]", r"\1", text)
    text = text.replace("'''", "").replace("''", "")
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&nbsp;", " ")
    return text.strip(" \t\n|!*:-")


def split_sections(wikitext):
    sections = {"__lead__": ""}
    current = "__lead__"
    for line in wikitext.splitlines():
        m = re.match(r"^(={2,4})\s*(.+?)\s*\1\s*$", line)
        if m:
            current = clean_wikitext(m.group(2))
            sections[current] = ""
        else:
            sections[current] += line + "\n"
    return sections


def extract_wikitables(text):
    return re.findall(r"\{\|.*?\n\|\}", text, flags=re.DOTALL)


def extract_image_names(text):
    names, seen = [], set()
    for m in re.finditer(r"\[\[(?:File|Image):([^|\]]+?)\.(?:png|jpg|jpeg|gif|webp)", text, flags=re.IGNORECASE):
        name = m.group(1).replace("_", " ").strip()
        name = re.sub(r"\s*(icon|swatch|thumb|render)\s*$", "", name, flags=re.IGNORECASE).strip()
        if name and name not in seen:
            seen.add(name)
            names.append(name)
    return names


def parse_table_rows(table_text):
    rows = []
    row_chunks = re.split(r"\n\|-", table_text)
    for chunk in row_chunks:
        cells = []
        for line in chunk.splitlines():
            line = line.strip()
            if not line or line.startswith("{|") or line.startswith("|}"):
                continue
            if line.startswith("!") or line.startswith("|"):
                prefix = line[0]
                line = line[1:]
                if "|" in line and not line.startswith("|"):
                    attrs, _, rest = line.partition("|")
                    if "=" in attrs and "[[" not in attrs:
                        line = rest
                parts = re.split(r"\|\|" if prefix == "|" else r"!!", line)
                cells.extend(clean_wikitext(p) for p in parts if clean_wikitext(p))
        if cells:
            rows.append(cells)
    return rows


def scrape_column(page_title, section=None, column=0, skip_header_rows=1):
    wikitext = fetch_wikitext(page_title)
    if section:
        sections = split_sections(wikitext)
        match = next((v for k, v in sections.items() if k.lower() == section.lower()), None)
        if match is None:
            raise ValueError(
                f"Section '{section}' not found on '{page_title}'. "
                f"Available: {list(sections.keys())}"
            )
        wikitext = match

    values, seen = [], set()
    for table in extract_wikitables(wikitext):
        rows = parse_table_rows(table)
        for row in rows[skip_header_rows:]:
            if column < len(row):
                v = row[column]
                if v and v not in seen:
                    seen.add(v)
                    values.append(v)
    return values



def fetch_html(page_title):
    params = {
        "action": "parse", "page": page_title, "prop": "text",
        "format": "json", "formatversion": "2",
    }
    r = requests.get(API_URL, params=params, timeout=TIMEOUT,
                      headers={"User-Agent": "dragon-card-maker/1.0"})
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise ValueError(f"Wiki API error for '{page_title}': {data['error'].get('info')}")
    return data["parse"]["text"]


def _soup(html):
    from bs4 import BeautifulSoup
    return BeautifulSoup(html, "html.parser")


def html_section(soup, heading_keyword):
    headings = soup.find_all(re.compile(r"^h[1-4]$"))
    start = next((h for h in headings if heading_keyword.lower() in h.get_text().lower()), None)
    if start is None:
        return []
    level = int(start.name[1])
    elements = []
    for sib in start.find_next_siblings():
        if re.match(r"^h[1-4]$", sib.name or "") and int(sib.name[1]) <= level:
            break
        elements.append(sib)
    return elements


def names_from_html_tables(elements_or_soup, name_col=0, extra_col_keyword=None):
    tables = []
    for el in (elements_or_soup if isinstance(elements_or_soup, list) else [elements_or_soup]):
        if getattr(el, "name", None) == "table":
            tables.append(el)
        elif hasattr(el, "find_all"):
            tables.extend(el.find_all("table"))
    names, extra, seen = [], {}, set()
    for table in tables:
        rows = table.find_all("tr")
        if not rows:
            continue
        headers = [c.get_text(strip=True).lower() for c in rows[0].find_all(["th", "td"])]
        extra_idx = None
        if extra_col_keyword:
            extra_idx = next((i for i, h in enumerate(headers) if extra_col_keyword in h), None)
        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            if not cells or name_col >= len(cells):
                continue
            cell = cells[name_col]
            text = cell.get_text(strip=True)
            if not text:
                img = cell.find("img")
                if img:
                    text = (img.get("alt") or img.get("title") or "").rsplit(".", 1)[0]
                    text = re.sub(r"^File:", "", text).replace("_", " ").strip()
            if text and text not in seen:
                seen.add(text)
                names.append(text)
                if extra_idx is not None and extra_idx < len(cells):
                    extra[text] = cells[extra_idx].get_text(strip=True)
    return names, extra


def names_from_html_gallery(elements_or_soup):
    items, seen = [], set()
    scope = elements_or_soup if isinstance(elements_or_soup, list) else [elements_or_soup]
    gallery_items = []
    for el in scope:
        if not hasattr(el, "find_all"):
            continue
        if el.get("class") and re.search(r"gallery|wikia-gallery", " ".join(el.get("class"))):
            gallery_items.append(el)
        gallery_items.extend(el.find_all(class_=re.compile(r"gallery|wikia-gallery")))
    candidates = gallery_items or scope
    for container in candidates:
        for item in container.find_all(class_=re.compile(r"lightbox-caption|gallery-caption")) or []:
            text = item.get_text(strip=True)
            if text and text not in seen:
                seen.add(text)
                items.append(text)
    if not items:
        for el in scope:
            for img in el.find_all("img"):
                text = (img.get("alt") or img.get("title") or "").rsplit(".", 1)[0]
                text = re.sub(r"^File:", "", text).replace("_", " ").strip()
                if text and text not in seen:
                    seen.add(text)
                    items.append(text)
    return items


def scrape_names_html(page_title, section=None, strip_suffix=None, exclude=()):
    soup = _soup(fetch_html(page_title))
    scope = html_section(soup, section) if section else soup

    names, _ = names_from_html_tables(scope)
    if len(names) < 3:
        gallery_names = names_from_html_gallery(scope)
        if len(gallery_names) > len(names):
            names = gallery_names

    cleaned, seen = [], set()
    for n in names:
        if strip_suffix:
            n = re.sub(rf"\s*{re.escape(strip_suffix)}\s*$", "", n, flags=re.IGNORECASE).strip()
        if n and n not in seen and n.lower() not in {e.lower() for e in exclude} \
                and n.lower() != page_title.lower():
            seen.add(n)
            cleaned.append(n)
    return cleaned


def load_colors():
    soup = _soup(fetch_html("Colors"))
    names, seen = [], set()
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if not rows:
            continue
        headers = [c.get_text(strip=True).lower() for c in rows[0].find_all(["th", "td"])]
        name_col = next(
            (i for i, h in enumerate(headers) if "color name" in h or "color id" in h),
            1 if len(headers) > 1 else 0,
        )
        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            if name_col >= len(cells):
                continue
            text = cells[name_col].get_text(strip=True)
            text = re.sub(r"\s*Color\s*$", "", text, flags=re.IGNORECASE).strip()
            if text and text not in seen:
                seen.add(text)
                names.append(text)
    return names


def load_special_element_potions():
    soup = _soup(fetch_html("Potions"))
    scope = html_section(soup, "Special Element Potions")
    names, seen = [], set()
    tables = []
    for el in scope:
        if getattr(el, "name", None) == "table":
            tables.append(el)
        elif hasattr(el, "find_all"):
            tables.extend(el.find_all("table"))
    for table in tables:
        rows = table.find_all("tr")
        if not rows:
            continue
        headers = [c.get_text(strip=True).lower() for c in rows[0].find_all(["th", "td"])]
        name_col = headers.index("name") if "name" in headers else \
                   (headers.index("potion") if "potion" in headers else 0)
        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            if name_col >= len(cells):
                continue
            text = cells[name_col].get_text(strip=True)
            text = re.sub(r"\s*Potion\s*$", "", text, flags=re.IGNORECASE).strip()
            if text and text not in seen:
                seen.add(text)
                names.append(text)
    return names


def load_elements():
    wikitext = fetch_wikitext("Elements")
    names, seen = [], set()
    for m in re.finditer(r"\|\s*el\s*=\s*([^\n|}]+)", wikitext):
        name = clean_wikitext(m.group(1))
        if name and name not in seen:
            seen.add(name)
            names.append(name)
    return names


def load_materials():
    return scrape_names_html("Materials", strip_suffix="Material", exclude=["Materials", "MaterialX"])


def load_pupils():
    return scrape_names_html("Pupils", strip_suffix="Pupil", exclude=["Pupils"])


def fetch_category_members(category, namespace=0, limit=500):
    titles = []
    cmcontinue = None
    while True:
        params = {
            "action": "query", "list": "categorymembers",
            "cmtitle": f"Category:{category}", "cmnamespace": namespace,
            "cmlimit": limit, "format": "json", "formatversion": "2",
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue
        r = requests.get(API_URL, params=params, timeout=TIMEOUT,
                          headers={"User-Agent": "dragon-card-maker/1.0"})
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            raise ValueError(f"Wiki API error for Category:{category}: {data['error'].get('info')}")
        titles.extend(m["title"] for m in data["query"]["categorymembers"])
        cmcontinue = data.get("continue", {}).get("cmcontinue")
        if not cmcontinue:
            break
    return titles


SPECIES_CATEGORY_JUNK = {
    "Baby Dragons",
}


RARITY_CATEGORIES = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Relic"]


def load_species_rarity():
    rarity = {}
    for r in RARITY_CATEGORIES:
        try:
            for name in fetch_category_members(f"Rarity: {r}"):
                rarity[name] = r
        except Exception as e:
            print(f"[wiki_data] rarity category '{r}' failed: {e}")
    return rarity


def load_species(with_rarity=True):
    species = sorted(m for m in fetch_category_members("Dragons") if m not in SPECIES_CATEGORY_JUNK)
    rarity = load_species_rarity() if with_rarity else {}
    return species, rarity


def load_cosmetic_traits_from_category():
    titles = fetch_category_members("Cosmetic Traits")
    names, seen = [], set()
    for t in titles:
        name = re.sub(r"\s*Cosmetic Trait$", "", t, flags=re.IGNORECASE).strip()
        if name and name not in seen:
            seen.add(name)
            names.append(name)
    return sorted(names)


def find_section(sections, keyword):
    for heading, content in sections.items():
        if keyword.lower() in heading.lower():
            return content
    return None


def _tables_in_section(soup, heading_keyword):
    scope = html_section(soup, heading_keyword)
    tables = []
    for el in scope:
        if getattr(el, "name", None) == "table":
            tables.append(el)
        elif hasattr(el, "find_all"):
            tables.extend(el.find_all("table"))
    return tables


def _name_column_index(table, header_label="trait"):
    rows = table.find_all("tr")
    if not rows:
        return 0
    headers = [c.get_text(strip=True).lower() for c in rows[0].find_all(["th", "td"])]
    return headers.index(header_label) if header_label in headers else 0


def load_cosmetic_traits():
    soup = _soup(fetch_html("Traits"))
    names, seen = [], set()
    for table in _tables_in_section(soup, "Cosmetic Traits"):
        col = _name_column_index(table, "trait")
        for row in table.find_all("tr")[1:]:
            cells = row.find_all(["td", "th"])
            if col < len(cells):
                name = cells[col].get_text(strip=True)
                if name and name not in seen:
                    seen.add(name)
                    names.append(name)
    return names


def load_positive_negative_traits():
    soup = _soup(fetch_html("Traits"))
    positive, negative = [], []
    for table in _tables_in_section(soup, "Genetic Traits"):
        rows = table.find_all("tr")
        if not rows:
            continue
        header_text = " ".join(c.get_text(strip=True) for c in rows[0].find_all(["th", "td"])).lower()
        col = _name_column_index(table, "trait")
        names = []
        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            if col < len(cells):
                name = cells[col].get_text(strip=True)
                if name:
                    names.append(name)
        if "debuff" in header_text:
            negative.extend(names)
        elif "buff" in header_text:
            positive.extend(names)
    return positive, negative



_FALLBACK = {
    "elements": ["Fire", "Water", "Grass"],
    "materials": ["Scales", "Fur Tufts", "Metal"],
    "pupils": ["Round", "Slit", "Empty"],
    "species": (["Aeroseys"], {"Aeroseys": "Common"}),
    "cosmetic_traits": [],
    "traits": (["None"], ["None"]),
    "sda_excluded": [],
    "colors": ["White", "Black", "Red"],
    "elemental_potions": [],
}


def load_sda_excluded():
    wikitext = fetch_wikitext("Achievements")
    sections = split_sections(wikitext)
    trivia = find_section(sections, "trivia") or wikitext

    names, seen = set(), set()
    for sentence in re.split(r"(?<=[.!?])\s+", trivia):
        low = sentence.lower()
        if "adventurer" in low and ("count" in low or "exclud" in low):
            for m in re.finditer(r"\[\[([^|\]#]+)(?:#[^|\]]*)?(?:\|[^\]]+)?\]\]", sentence):
                name = m.group(1).strip()
                if name and name not in seen:
                    seen.add(name)
                    names.add(name)
    return names


def load_all(verbose=True, cache_path="wiki_data_cache.json"):
    import json
    import os
    from datetime import datetime, timezone

    cache = {}
    cache_file = None
    if cache_path:
        cache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), cache_path)
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache = json.load(f)
            except Exception:
                cache = {}

    result = {}
    result["_last_updated"] = cache.get("_last_updated")

    had_live_success = [False]

    def safe(key, fn):
        try:
            value = fn()
            count = len(value[0]) if isinstance(value, tuple) else len(value)
            if count == 0:
                raise ValueError("fetched 0 entries - treating as a failure")
            if verbose:
                print(f"[wiki_data] {key}: loaded {count} entries")
            had_live_success[0] = True
            return value
        except Exception as e:
            if key in cache:
                cached_value = cache[key]
                if isinstance(cached_value, list) and len(cached_value) == 2 \
                        and key in ("species", "traits"):
                    cached_value = tuple(cached_value)
                count = len(cached_value[0]) if isinstance(cached_value, tuple) else len(cached_value)
                if verbose:
                    print(f"[wiki_data] {key}: FAILED ({e}) - using cached data ({count} entries)")
                return cached_value
            if verbose:
                print(f"[wiki_data] {key}: FAILED ({e}) - no cache available, using tiny fallback")
            return _FALLBACK[key]

    result["ELEMENT_LIST"] = safe("elements", load_elements)
    result["MATERIAL_LIST"] = safe("materials", load_materials)
    result["PUPIL_LIST"] = safe("pupils", load_pupils)
    result["COLOR_LIST"] = safe("colors", load_colors)
    if "Legendary" not in result["COLOR_LIST"]:
        result["COLOR_LIST"] = result["COLOR_LIST"] + ["Legendary"]
    result["SPECIES_LIST"], result["SPECIES_RARITY"] = \
        safe("species", lambda: load_species(with_rarity=True))
    result["COSMETIC_TRAIT_LIST"] = safe("cosmetic_traits", load_cosmetic_traits)
    result["POSITIVE_TRAIT_LIST"], result["NEGATIVE_TRAIT_LIST"] = \
        safe("traits", load_positive_negative_traits)
    result["SDA_EXCLUDED"] = set(safe("sda_excluded", lambda: sorted(load_sda_excluded())))
    result["ELEMENTAL_POTIONS"] = safe("elemental_potions", load_special_element_potions)

    if cache_file:
        try:
            if had_live_success[0]:
                result["_last_updated"] = datetime.now(timezone.utc).isoformat()
            to_cache = {
                "_last_updated": result["_last_updated"],
                "elements": result["ELEMENT_LIST"],
                "materials": result["MATERIAL_LIST"],
                "pupils": result["PUPIL_LIST"],
                "colors": result["COLOR_LIST"],
                "species": [result["SPECIES_LIST"], result["SPECIES_RARITY"]],
                "cosmetic_traits": result["COSMETIC_TRAIT_LIST"],
                "traits": [result["POSITIVE_TRAIT_LIST"], result["NEGATIVE_TRAIT_LIST"]],
                "sda_excluded": sorted(result["SDA_EXCLUDED"]),
                "elemental_potions": result["ELEMENTAL_POTIONS"],
            }
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(to_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            if verbose:
                print(f"[wiki_data] warning: could not write cache ({e})")

    if verbose and not had_live_success[0] and result.get("_last_updated"):
        print(f"[wiki_data] running entirely on cached data from {result['_last_updated']}")

    return result


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--dump":
        page = sys.argv[2] if len(sys.argv) > 2 else "Elements"
        soup = _soup(fetch_html(page))
        tables = soup.find_all("table")
        print(f"Found {len(tables)} <table> elements on '{page}'\n")
        for i, t in enumerate(tables):
            rows = t.find_all("tr")
            print(f"--- table {i} ({len(rows)} rows), class={t.get('class')} ---")
            for row in rows[:4]:
                cells = row.find_all(["td", "th"])
                cell_summaries = []
                for c in cells:
                    text = c.get_text(strip=True)
                    img = c.find("img")
                    img_alt = (img.get("alt") or img.get("title")) if img else None
                    cell_summaries.append(text or f"<img alt={img_alt!r}>" or "<empty>")
                print("   row:", cell_summaries)
            if len(rows) > 4:
                print(f"   ... ({len(rows) - 4} more rows)")
            print()

        gallery_divs = soup.find_all(class_=re.compile(r"gallery|wikia-gallery"))
        print(f"Found {len(gallery_divs)} gallery-class <div> containers")
        for i, g in enumerate(gallery_divs[:2]):
            items = g.find_all(class_=re.compile(r"gallery-item|lightbox-caption"))
            print(f"--- gallery {i}: {len(items)} caption/item elements, first few: "
                  f"{[it.get_text(strip=True) for it in items[:5]]}")

        swatch_divs = soup.find_all(style=re.compile(r"background-?color", re.IGNORECASE))
        print(f"\nFound {len(swatch_divs)} elements with an inline background-color style")
        for el in swatch_divs[:8]:
            print(f"   <{el.name} style={el.get('style')!r} title={el.get('title')!r}> "
                  f"text={el.get_text(strip=True)!r}")

        headings = soup.find_all(re.compile(r"^h[1-4]$"))
        print("\nHeadings on page:", [h.get_text(strip=True) for h in headings])
        sys.exit(0)

    data = load_all(verbose=True)
    print()
    for key, value in data.items():
        if isinstance(value, dict):
            sample = dict(list(value.items())[:5])
            print(f"{key} ({len(value)}): {sample} ...")
        else:
            print(f"{key} ({len(value)}): {value[:10]} ...")
    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        import json
        print("\n--- FULL OUTPUT ---")
        print(json.dumps(data, indent=2, ensure_ascii=False))




