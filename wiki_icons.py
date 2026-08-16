
import os
import re
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

import wiki_data as wd

API_URL = wd.API_URL
TIMEOUT = 20
HEADERS = {"User-Agent": "dragon-card-maker/1.0"}



def _chunks(seq, size=50):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def resolve_file_urls(filenames, width=128):
    urls = {}
    clean_names = [f if f.lower().startswith(("file:", "image:")) else f"File:{f}" for f in filenames]
    for batch in _chunks(clean_names, 50):
        params = {
            "action": "query",
            "titles": "|".join(batch),
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": width,
            "format": "json",
            "formatversion": "2",
        }
        r = requests.get(API_URL, params=params, timeout=TIMEOUT, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        for page in data.get("query", {}).get("pages", []):
            title = re.sub(r"^(File|Image):", "", page.get("title", ""))
            info = page.get("imageinfo")
            if info:
                urls[title] = info[0].get("thumburl") or info[0].get("url")
    return urls


def resolve_page_thumbnails(titles, size=128):
    urls = {}
    for batch in _chunks(list(titles), 50):
        params = {
            "action": "query",
            "titles": "|".join(batch),
            "prop": "pageimages",
            "piprop": "thumbnail",
            "pithumbsize": size,
            "format": "json",
            "formatversion": "2",
        }
        r = requests.get(API_URL, params=params, timeout=TIMEOUT, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        for page in data.get("query", {}).get("pages", []):
            thumb = page.get("thumbnail")
            if thumb:
                urls[page.get("title")] = thumb.get("source")
    return urls


def _best_img_url(img_tag):
    if img_tag is None:
        return None
    for attr in ("data-src", "src"):
        val = img_tag.get(attr)
        if val and not val.startswith("data:"):
            return val
    return None


def _download(url, dest_path):
    r = requests.get(url, timeout=TIMEOUT, headers=HEADERS, stream=True)
    r.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)


def _download_many(jobs, max_workers=10, verbose=True, label="icons", on_progress=None):
    saved = 0
    failed = []
    total = len(jobs)
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_download, url, dest): name for name, url, dest in jobs}
        for i, future in enumerate(as_completed(futures), start=1):
            name = futures[future]
            try:
                future.result()
                saved += 1
            except Exception as e:
                failed.append(name)
                if verbose:
                    print(f"[wiki_icons] {label} '{name}': download failed ({e})")
            if on_progress:
                on_progress(i, total)
    return saved, failed



def element_icon_filenames():
    wikitext = wd.fetch_wikitext("Elements")
    template_re = re.compile(r"\{\{(?:NElement|EElement|SElement|OElement)\b")
    starts = [m.start() for m in template_re.finditer(wikitext)]
    starts.append(len(wikitext))

    result = {}
    for i in range(len(starts) - 1):
        chunk = wikitext[starts[i]:starts[i + 1]]
        name_m = re.search(r"\|\s*el\s*=\s*([^\n|}]+)", chunk)
        if not name_m:
            continue
        name = wd.clean_wikitext(name_m.group(1))

        gallery_m = re.search(r"<gallery[^>]*>(.*?)</gallery>", chunk, flags=re.DOTALL)
        if not gallery_m:
            continue
        lines = [ln.strip() for ln in gallery_m.group(1).splitlines() if ln.strip()]
        best = None
        for ln in lines:
            filename, _, caption = ln.partition("|")
            if caption.strip().lower() in ("current design", "design"):
                best = filename.strip()
                break
        if best is None and lines:
            best = lines[0].partition("|")[0].strip()
        if best and name not in result:
            result[name] = best
    return result


def cosmetic_trait_icon_urls():
    soup = wd._soup(wd.fetch_html("Traits"))
    urls = {}
    for table in wd._tables_in_section(soup, "Cosmetic Traits"):
        rows = table.find_all("tr")
        if not rows:
            continue
        headers = [c.get_text(strip=True).lower() for c in rows[0].find_all(["th", "td"])]
        icon_col = headers.index("icon") if "icon" in headers else 0
        name_col = headers.index("trait") if "trait" in headers else 1
        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            if max(icon_col, name_col) >= len(cells):
                continue
            name = cells[name_col].get_text(strip=True)
            url = _best_img_url(cells[icon_col].find("img"))
            if name and url and name not in urls:
                urls[name] = url
    return urls



def _sanitize(name):
    return re.sub(r'[\\/:*?"<>|]', '', name)


FREDOKA_FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/fredoka/Fredoka%5Bwdth,wght%5D.ttf"


def download_fredoka_font(fonts_dir, verbose=True):
    os.makedirs(fonts_dir, exist_ok=True)
    dest = os.path.join(fonts_dir, "Fredoka-Variable.ttf")
    if os.path.exists(dest):
        if verbose:
            print("[wiki_icons] Fredoka font: already cached")
        return dest
    try:
        _download(FREDOKA_FONT_URL, dest)
        if verbose:
            print("[wiki_icons] Fredoka font: downloaded")
        return dest
    except Exception as e:
        if verbose:
            print(f"[wiki_icons] Fredoka font: download failed ({e})")
        return None


MISC_ICON_FILES = {
    "Dragon Head": "dragonhead.png",
    "Happy Icon": "happy_icon.png",
    "Mutations": "mut.png",
    "Age": "age.png",
    "Male Icon": "male.png",
    "Female Icon": "female.png",
    "Soul Bound Icon": "soulbound.png",
}

MENUICON_FILES = {
    "Happy Icon": "quickadd.png",
    "Gold Star": "SDA.png",
    "Appearance": "themes.png",
    "Tracking": "select.png",
    "Accessories Icon": "elemental.png",
}


def ensure_ico(png_path, ico_path, verbose=True):
    if os.path.exists(ico_path):
        return ico_path
    if not os.path.exists(png_path):
        return None
    try:
        from PIL import Image
        img = Image.open(png_path).convert("RGBA")
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_path, format="ICO", sizes=sizes)
        if verbose:
            print(f"[wiki_icons] converted {os.path.basename(png_path)} -> {os.path.basename(ico_path)}")
        return ico_path
    except Exception as e:
        if verbose:
            print(f"[wiki_icons] icon conversion failed: {e}")
        return None


def download_ui_icons(misc_dir, menuicons_dir, verbose=True, on_progress=None):
    os.makedirs(misc_dir, exist_ok=True)
    os.makedirs(menuicons_dir, exist_ok=True)

    dest_paths, to_fetch = {}, {}
    for wiki_name, local_filename in MISC_ICON_FILES.items():
        dest = os.path.join(misc_dir, local_filename)
        dest_paths[f"misc:{local_filename}"] = dest
        if not os.path.exists(dest):
            to_fetch[dest] = f"{wiki_name}.png"
    for wiki_name, local_filename in MENUICON_FILES.items():
        dest = os.path.join(menuicons_dir, local_filename)
        dest_paths[f"menuicons:{local_filename}"] = dest
        if not os.path.exists(dest):
            to_fetch[dest] = f"{wiki_name}.png"

    if not to_fetch:
        if verbose:
            print(f"[wiki_icons] ui icons: all {len(dest_paths)} already cached")
        return dest_paths

    urls = resolve_file_urls(list(set(to_fetch.values())))

    unresolved = {dest: wf for dest, wf in to_fetch.items() if wf not in urls}
    if unresolved:
        alt_names = {}
        for wf in set(unresolved.values()):
            base = wf[:-4]
            if base.lower().endswith(" icon"):
                alt = base[:-5].strip() + ".png"
            else:
                alt = base + " Icon.png"
            alt_names[wf] = alt
        alt_urls = resolve_file_urls(list(set(alt_names.values())))
        for dest, wf in list(unresolved.items()):
            alt = alt_names[wf]
            if alt in alt_urls:
                urls[wf] = alt_urls[alt]
                if verbose:
                    print(f"[wiki_icons] ui icon: '{wf}' not found, used '{alt}' instead")

    jobs = [(dest, urls[wf], dest) for dest, wf in to_fetch.items() if wf in urls]
    if jobs:
        saved, failed = _download_many(jobs, verbose=verbose, label="ui icon", on_progress=on_progress)
        if verbose:
            print(f"[wiki_icons] ui icons: downloaded {saved}/{len(jobs)}")
    return dest_paths


def legendary_shift_icon_filenames():
    wikitext = wd.fetch_wikitext("Elements")
    template_re = re.compile(r"\{\{(?:NElement|EElement|SElement|OElement)\b")
    starts = [m.start() for m in template_re.finditer(wikitext)]
    starts.append(len(wikitext))

    result = {}
    for i in range(len(starts) - 1):
        chunk = wikitext[starts[i]:starts[i + 1]]
        name_m = re.search(r"\|\s*el\s*=\s*([^\n|}]+)", chunk)
        if not name_m:
            continue
        name = wd.clean_wikitext(name_m.group(1))

        gallery_m = re.search(r"<gallery[^>]*>(.*?)</gallery>", chunk, flags=re.DOTALL)
        if not gallery_m:
            continue
        for ln in gallery_m.group(1).splitlines():
            ln = ln.strip()
            if not ln:
                continue
            filename, _, caption = ln.partition("|")
            if caption.strip().lower() == "legendary shift":
                result[name] = filename.strip()
                break
    return result


def download_legendary_shift_icons(legendary_shift_dir, elements=None, verbose=True, on_progress=None):
    os.makedirs(legendary_shift_dir, exist_ok=True)
    name_to_file = legendary_shift_icon_filenames()
    if elements:
        name_to_file = {k: v for k, v in name_to_file.items() if k in elements}

    dest_paths, to_fetch = {}, {}
    for name, wiki_filename in name_to_file.items():
        dest = os.path.join(legendary_shift_dir, f"{_sanitize(name).lower().replace(' ', '_')}.png")
        dest_paths[name] = dest
        if not os.path.exists(dest):
            to_fetch[name] = wiki_filename

    if to_fetch:
        urls = resolve_file_urls(list(set(to_fetch.values())))
        jobs = [(name, urls[wf], dest_paths[name]) for name, wf in to_fetch.items() if wf in urls]
        if jobs:
            saved, _ = _download_many(jobs, verbose=verbose, label="legendary shift", on_progress=on_progress)
            if verbose:
                print(f"[wiki_icons] legendary shifts: downloaded {saved}/{len(jobs)}")
    elif verbose:
        print(f"[wiki_icons] legendary shifts: all {len(name_to_file)} already cached")
    return dest_paths


def potion_icon_urls():
    soup = wd._soup(wd.fetch_html("Potions"))
    scope = wd.html_section(soup, "Special Element Potions")
    urls = {}
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
        icon_col = headers.index("icon") if "icon" in headers else 0
        name_col = headers.index("name") if "name" in headers else \
                   (headers.index("potion") if "potion" in headers else 1)
        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            if max(icon_col, name_col) >= len(cells):
                continue
            name = cells[name_col].get_text(strip=True)
            name = re.sub(r"\s*Potion\s*$", "", name, flags=re.IGNORECASE).strip()
            url = _best_img_url(cells[icon_col].find("img"))
            if name and url and name not in urls:
                urls[name] = url
    return urls


def download_potion_icons(potion_icon_dir, potions=None, verbose=True, on_progress=None):
    os.makedirs(potion_icon_dir, exist_ok=True)
    urls_by_name = potion_icon_urls()
    if potions:
        urls_by_name = {k: v for k, v in urls_by_name.items() if k in potions}

    dest_paths, to_fetch = {}, {}
    for name, url in urls_by_name.items():
        dest = os.path.join(potion_icon_dir, f"{_sanitize(name).lower().replace(' ', '_')}.png")
        dest_paths[name] = dest
        if not os.path.exists(dest):
            to_fetch[name] = url

    if to_fetch:
        jobs = [(name, url, dest_paths[name]) for name, url in to_fetch.items()]
        saved, _ = _download_many(jobs, verbose=verbose, label="potion", on_progress=on_progress)
        if verbose:
            print(f"[wiki_icons] potions: downloaded {saved}/{len(jobs)}")
    elif verbose:
        print(f"[wiki_icons] potions: all {len(urls_by_name)} already cached")
    return dest_paths


def _prepare_element_jobs(icon_dir, elements=None, verbose=True):
    os.makedirs(icon_dir, exist_ok=True)
    name_to_file = element_icon_filenames()
    if elements:
        name_to_file = {k: v for k, v in name_to_file.items() if k in elements}

    dest_paths, to_fetch = {}, {}
    for name, wiki_filename in name_to_file.items():
        dest = os.path.join(icon_dir, f"{_sanitize(name).lower().replace(' ', '_')}.png")
        dest_paths[name] = dest
        if not os.path.exists(dest):
            to_fetch[name] = wiki_filename

    jobs = []
    if to_fetch:
        urls = resolve_file_urls(list(set(to_fetch.values())))
        jobs = [(name, urls[wf], dest_paths[name]) for name, wf in to_fetch.items() if wf in urls]
    if verbose:
        print(f"[wiki_icons] elements: {len(jobs)} to download, {len(name_to_file) - len(to_fetch)} already cached")
    return dest_paths, jobs


def _prepare_species_jobs(dragon_icons_dir, species_list, verbose=True):
    os.makedirs(dragon_icons_dir, exist_ok=True)
    dest_paths, to_fetch = {}, []
    for name in species_list:
        dest = os.path.join(dragon_icons_dir, f"{_sanitize(name)}_Icon.png")
        dest_paths[name] = dest
        if not os.path.exists(dest):
            to_fetch.append(name)

    jobs = []
    if to_fetch:
        urls = resolve_page_thumbnails(to_fetch)
        jobs = [(name, urls[name], dest_paths[name]) for name in to_fetch if name in urls]
    if verbose:
        print(f"[wiki_icons] species: {len(jobs)} to download, {len(species_list) - len(to_fetch)} already cached")
    return dest_paths, jobs


def _prepare_cosmetic_trait_jobs(cosmetic_trait_icon_dir, traits=None, verbose=True):
    os.makedirs(cosmetic_trait_icon_dir, exist_ok=True)
    urls_by_name = cosmetic_trait_icon_urls()
    if traits:
        urls_by_name = {k: v for k, v in urls_by_name.items() if k in traits}

    dest_paths, to_fetch = {}, {}
    for name, url in urls_by_name.items():
        dest = os.path.join(cosmetic_trait_icon_dir, f"{_sanitize(name).lower().replace(' ', '_')}_icon.png")
        dest_paths[name] = dest
        if not os.path.exists(dest):
            to_fetch[name] = url

    jobs = [(name, url, dest_paths[name]) for name, url in to_fetch.items()]
    if verbose:
        print(f"[wiki_icons] cosmetic traits: {len(jobs)} to download, {len(urls_by_name) - len(to_fetch)} already cached")
    return dest_paths, jobs


def download_element_icons(icon_dir, elements=None, verbose=True, on_progress=None):
    dest_paths, jobs = _prepare_element_jobs(icon_dir, elements, verbose)
    if jobs:
        saved, _ = _download_many(jobs, verbose=verbose, label="element", on_progress=on_progress)
        if verbose:
            print(f"[wiki_icons] elements: downloaded {saved} new icons")
    return dest_paths


def download_species_icons(dragon_icons_dir, species_list, verbose=True, on_progress=None):
    dest_paths, jobs = _prepare_species_jobs(dragon_icons_dir, species_list, verbose)
    if jobs:
        saved, _ = _download_many(jobs, verbose=verbose, label="species", on_progress=on_progress)
        if verbose:
            print(f"[wiki_icons] species: downloaded {saved} new icons")
    return dest_paths


def download_cosmetic_trait_icons(cosmetic_trait_icon_dir, traits=None, verbose=True, on_progress=None):
    dest_paths, jobs = _prepare_cosmetic_trait_jobs(cosmetic_trait_icon_dir, traits, verbose)
    if jobs:
        saved, _ = _download_many(jobs, verbose=verbose, label="cosmetic trait", on_progress=on_progress)
        if verbose:
            print(f"[wiki_icons] cosmetic traits: downloaded {saved} new icons")
    return dest_paths


def download_all_icons(icon_dir, dragon_icons_dir, cosmetic_trait_icon_dir,
                        species_list, elements=None, traits=None, verbose=True,
                        on_progress=None):
    dest_paths = {"elements": {}, "species": {}, "cosmetic_traits": {}}
    all_jobs = []

    try:
        dest_paths["elements"], jobs = _prepare_element_jobs(icon_dir, elements, verbose)
        all_jobs.extend(jobs)
    except Exception as e:
        if verbose:
            print(f"[wiki_icons] elements: category failed entirely ({e})")

    try:
        dest_paths["species"], jobs = _prepare_species_jobs(dragon_icons_dir, species_list, verbose)
        all_jobs.extend(jobs)
    except Exception as e:
        if verbose:
            print(f"[wiki_icons] species: category failed entirely ({e})")

    try:
        dest_paths["cosmetic_traits"], jobs = _prepare_cosmetic_trait_jobs(cosmetic_trait_icon_dir, traits, verbose)
        all_jobs.extend(jobs)
    except Exception as e:
        if verbose:
            print(f"[wiki_icons] cosmetic traits: category failed entirely ({e})")

    if all_jobs:
        saved, failed = _download_many(all_jobs, verbose=verbose, label="icon", on_progress=on_progress)
        if verbose:
            print(f"[wiki_icons] total: downloaded {saved}/{len(all_jobs)} new icons ({len(failed)} failed)")
    elif on_progress:
        on_progress(0, 0)

    return dest_paths


if __name__ == "__main__":
    import wiki_data
    data = wiki_data.load_all(verbose=True)
    download_all_icons(
        icon_dir="assets/icons",
        dragon_icons_dir="assets/dragonicons",
        cosmetic_trait_icon_dir="assets/misc/cosmetictrait",
        species_list=data["SPECIES_LIST"][:10],
        elements=data["ELEMENT_LIST"][:10],
        traits=data["COSMETIC_TRAIT_LIST"][:10],
        verbose=True,
    )




