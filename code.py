import colorsys
import copy
import ctypes
import hashlib
import json
import math
import os
import calendar
import subprocess
import threading
import zipfile
import urllib.request
import sys
from datetime import date
import uuid
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageChops, ImageGrab

import wiki_data
_WIKI_BG = {"thread": None, "data": None}


def _wiki_bg_fetch():
    _WIKI_BG["data"] = wiki_data.load_all()


_WIKI_BG["thread"] = threading.Thread(target=_wiki_bg_fetch, daemon=True)
_WIKI_BG["thread"].start()

_WIKI_DATA = {
    "MATERIAL_LIST": [], "ELEMENT_LIST": [], "SPECIES_LIST": [],
    "SPECIES_RARITY": {}, "PUPIL_LIST": [], "COSMETIC_TRAIT_LIST": [],
    "POSITIVE_TRAIT_LIST": [], "NEGATIVE_TRAIT_LIST": [], "COLOR_LIST": [],
    "ELEMENTAL_POTIONS": [],
}


PALETTE = {
    "bg_outer":      "#5C4A93",
    "panel_fill":    "#473B72",
    "panel_border":  "#8874C9",
    "tag_fill":      "#2E2550",
    "badge_fill":    "#F2A93B",
    "badge_border":  "#8B5A2B",
    "title_fill":    "#FFA63D",
    "title_outline": "#B85C00",
    "label_text":    "#C9B8F0",
    "bar_track":     "#2B3D22",
    "bar_fill":      "#7ED957",
    "bar_border":    "#3C7A2E",
    "swatch_bg":     "#F4F4F4",
    "card_fill":     "#5A4A8E",
    "card_border":   "#8874C9",
    "row_fill":      "#3A2F5C",
    "row_border":    "#2B2148",
    "header_band":        "#8B6F47",
    "header_band_border": "#5C4A30",
    "value_text":    "#FFFFFF",
    "value_outline": "#2B2148",
    "pill_text":     "#3FA9E0",
    "pill_outline":  "#173145",
    "name_fill":     "#FBBB28",
    "name_outline":  "#722509",
    "name_shadow":   "#3A1204",
    "lair_bg":       "#403365",
    "info_card_fill": "#685991",
}

RARITY_COLORS = {
    "Common":    "#B5B5B5",
    "Uncommon":  "#52C724",
    "Rare":      "#1AB7FF",
    "Epic":      "#B622FF",
    "Legendary": "#FF990A",
    "Relic":     "#FF1C2B",
}
RARITY_LIST = list(RARITY_COLORS.keys())
RARITY_DEFAULT_COLOR = "#9499F7"

SPECIES_CAN_FLY = {
    'Aeroseys': True,
    'Aethereus': True,
    'Alatura': True,
    'Allpehourn': True,
    'Amaris': True,
    'Amoonita': True,
    'Ancient Aranga': True,
    'Ancient Skriffei': True,
    'Ancient Tosknir': True,
    'Andronaut': True,
    'Araneaix': True,
    'Aranga': True,
    'Archogine': True,
    'Arielisces': True,
    'Astraeisis': True,
    'Atravanta': True,
    'Aurutentia': True,
    'Avarakuma': True,
    'Avefir': True,
    'Ayatrice': True,
    'Balgunyur': True,
    'Betevial': True,
    'Bylendarach': True,
    'Caelydris': True,
    'Calimaki': True,
    'Canyarches': True,
    'Carnealgon': True,
    'Casirius': True,
    'Catruca': True,
    'Caudembris': True,
    'Caunaris': True,
    'Chameleaf': True,
    'Chippychiip': True,
    'Chronocus': True,
    'Chrysaloom': False,
    'Cirquemaar': True,
    'Cogitergosyn': True,
    'Constello': True,
    'Corrupted Chronocus': True,
    'Cosmalisk': True,
    'Cryptillow': True,
    'Cutiepatoo': True,
    'Cybernid': True,
    'Cynphion-Noire': True,
    'Desygual': True,
    'Diraixos': True,
    'Djaevelhest': True,
    'Dratheros': True,
    'Dysuva': True,
    'Eisendrache': True,
    'Eryndiorn': True,
    'Eteralix': True,
    'Fabledrak': True,
    'Falugeis': True,
    'Fayrah': True,
    'Featherfang': True,
    'Fernifex': True,
    'Firifeller': True,
    'Fleurianthus': False,
    'Flornymphis': True,
    'Fueguin': True,
    'Fulong': True,
    'Garutagoyle': True,
    'Gaulyra': False,
    'Geoteryx': True,
    'Glaquacus': True,
    'Goelica': True,
    'Goliatomb': True,
    'Gordigourd': True,
    'Guilmoros': True,
    'Gundrakken': True,
    'Gyngefared': True,
    'Gyrocopter': True,
    'Harvitius': True,
    'Hexalios': True,
    'Hielochiim': True,
    'Hoarusn': True,
    'Hongliang': True,
    'Ignicaris': True,
    'Impiavolo': True,
    'Iridesia': True,
    'Karukiri': True,
    'Khalknirik': True,
    'Khorgeryn': True,
    'Kikien': True,
    'Kostragula': True,
    'Ladonix': True,
    'Lepilon': True,
    'Livalient': True,
    'Lucklif': True,
    'Lum Luenh': True,
    'Lumenigh': True,
    'Lunaesol': True,
    'Lyria': True,
    'Makoura': True,
    'Mallopii': True,
    'Malupentys': True,
    'Mechanoxide': False,
    'Mielebee': True,
    'Mistrasune': True,
    'Moixaura': True,
    'Mosuraki': True,
    'Motorouk': False,
    'Mountain Dragon': True,
    'Nadaler': True,
    'Nakahii': False,
    'Nightmare Paranox': True,
    'Noctorius': True,
    "Nor'gan": True,
    'Nyxavoid': True,
    'Onagajin': True,
    'Oroalas': True,
    'Ortarouk': False,
    'Ovicirus': True,
    'Pagulau': True,
    'Paladianos': True,
    'Pananisea': True,
    'Paranox': True,
    'Paukiki': True,
    'Penguitus': True,
    'Phocaphan': True,
    'Phyllantis': True,
    'Polairistel': True,
    'Putrefacceum': True,
    'Quahtona': True,
    'Quasaldrus': True,
    'Quetzaloctli': True,
    'Radidon': True,
    'Raikami': True,
    'Rhyndac': True,
    'Riyu': True,
    'Robodon': True,
    'Roborus X': True,
    'Rozora': False,
    'Scrawei': True,
    'Seikarin': True,
    'Sentalius': True,
    'Silvestratus': True,
    'Skelltor': True,
    'Skriffei': True,
    'Skyrix': True,
    'Smokgien': True,
    'Snoballista': True,
    'Solarizon': True,
    'Soukeyi': True,
    'Source Dragon of Energy': True,
    'Source Dragon of Motion': True,
    'Stellaris': True,
    'Stratalix': True,
    'Stymelisk': True,
    'Suiikipon': True,
    'Sunfloris': True,
    'Syliru': True,
    'Taligris': True,
    'Tarotta': True,
    'Tempiritus': True,
    'Tenebis': True,
    'Terruak': True,
    'Thorkonyx': True,
    'Tianma': True,
    'Tlalocun': True,
    'Torneidus': True,
    'Tosknir': True,
    'Trametos': True,
    'Trilinaris': True,
    'Tronat': True,
    'Tsukuizan': True,
    'Uheailes': True,
    'Valkiero': True,
    'Varana': False,
    'Veidreki': True,
    'Venid': True,
    'Verdrakor': True,
    'Verscervus': True,
    'Viridik': True,
    'Volkumos': True,
    'Voltagen': True,
    'Voltstorm': True,
    'Vulcoramor': True,
    'Vulpiruth': True,
    'Vyreas': True,
    'Woodluma': True,
    'Wuonghou': True,
    'Xellatruce': True,
    'Xerthos': True,
    'Yaruakura': True,
    'Yggdraten': False,
    'Yueshi': True,
    'Yulereinn': True,
    'Zinthros': False,
    'Wisp': True,
    'Rocky': True,
}


LEGACY_EXAMPLE_ACCOUNTS = {"tamaraa123", "DragonTamerSuu", "WobblyPengu"}


COLOR_HEX_MAP = {
    'White': '#FFFFFF',
    'Snowflake': '#F7F9F9',
    'Whisp': '#EAEDEF',
    'Whale': '#D0CFD7',
    'Mist': '#C3C8CD',
    'Storm': '#A1ABB3',
    'Silver': '#AFAFAF',
    'Gravel': '#888F8D',
    'Felt': '#9C8E8D',
    'Bluesteel': '#6A7185',
    'Stone': '#636268',
    'Tin': '#5A6050',
    'Spirit': '#545365',
    'Gloom': '#595451',
    'Coal': '#4C4C4C',
    'Gabbro': '#4D484F',
    'Asphalt': '#413C40',
    'Ash': '#3B3736',
    'Basalt': '#332D25',
    'Scoria': '#302722',
    'Boulder': '#26262C',
    'Black': '#1A1A1B',
    'Pitch': '#0E1011',
    'Night': '#1F1A23',
    'Depth': '#22263D',
    'Blackberry': '#471A43',
    'Berry': '#4C2A4F',
    'Loulou': '#553348',
    'Lilac': '#6E235D',
    'Amarklor': '#551199',
    'Grape': '#863290',
    'Petal': '#9778BE',
    'Satin': '#7F6195',
    'Haunted': '#5C415D',
    'Ghost': '#735B77',
    'Lavender': '#8E7F9E',
    'Amethyst': '#A794B2',
    'Dart': '#AA96A6',
    'Pansy': '#E1CDFE',
    'Bubble': '#CCA4E0',
    'Plum': '#DA4FFF',
    'Purple': '#9C50D3',
    'Royal': '#7958B1',
    'Eggplant': '#993BD1',
    'Midnight': '#7930B5',
    'Urchin': '#5317B5',
    'Jelly': '#4D2C89',
    'Smog': '#3F2B66',
    'Sapphire': '#0D0A5B',
    'Angler': '#2B0D88',
    'Bluebell': '#2D237A',
    'Aster': '#484AA1',
    'Smoke': '#525195',
    'Uranus': '#4866D5',
    'Rain': '#757ADB',
    'Periwinkle': '#9499F7',
    'Stream': '#7895C1',
    'Aegean': '#4E6EA0',
    'Harpy': '#444F69',
    'Blue': '#324BA9',
    'Denim': '#212B5F',
    'Morpho': '#023489',
    'Raindrop': '#023AE2',
    'Marine': '#1C51E7',
    'Ocean': '#2F83FF',
    'Drip': '#6394DD',
    'Cool': '#76A8FF',
    'Sky': '#AEC8FF',
    'Cloud': '#89A4C0',
    'Aluminum': '#556979',
    'Iron': '#2F4557',
    'Dream': '#263746',
    'Abyss': '#0D1E25',
    'Trench': '#0B2D46',
    'Twilight': '#0A3D67',
    'Mountain': '#094869',
    'Azure': '#2B768F',
    'Shell': '#0086CE',
    'Cerulean': '#00B4D5',
    'Icecap': '#9CDDD3',
    'Winter': '#B3E1F1',
    'Glacier': '#E0FFFF',
    'Glow': '#91FFF7',
    'Cyan': '#00FFF1',
    'Bermuda': '#77DDDA',
    'Lagoon': '#09E0C7',
    'Plankton': '#18D3A9',
    'Turquoise': '#3CA2A4',
    'History': '#3A8684',
    'Spruce': '#8DBCB4',
    'Water': '#72C4C4',
    'Glass': '#9AEAEF',
    'Pistachio': '#E2FFE6',
    'Dolphin': '#B3FFD8',
    'Mint': '#9AFFC7',
    'Seafoam': '#B2E2BD',
    'Caterpillar': '#A6DBA7',
    'Jade': '#61AB89',
    'Spearmint': '#148E67',
    'Essence': '#1F565D',
    'Rainforest': '#233253',
    'Seaweed': '#153F4B',
    'Algae': '#114D41',
    'Forest': '#1F483A',
    'Hydra': '#005D48',
    'Emerald': '#20603F',
    'Shamrock': '#236825',
    'Pear': '#66903C',
    'Jungle': '#1E361A',
    'Swamp': '#1E2716',
    'Root': '#1F281D',
    'Moonrock': '#495547',
    'Snake': '#425035',
    'Camo': '#51684C',
    'Prismarine': '#4D6A6E',
    'Scale': '#516760',
    'Ivy': '#687F67',
    'Mantis': '#97AF8B',
    'Micah': '#A7B08C',
    'Pea': '#9BFF9D',
    'Synthesizer': '#03FF7D',
    'Malachite': '#87E34D',
    'Fern': '#7ECE73',
    'Stem': '#7BBD5D',
    'Green': '#629C3F',
    'Grass': '#567C34',
    'Clover': '#3ABB3B',
    'Cactus': '#8ECE56',
    'Leaf': '#A5E32D',
    'Toxin': '#C6FF00',
    'Uranium': '#CDFE6C',
    'Corrosion': '#9FFF00',
    'Peridot': '#E8FCB4',
    'Cabbage': '#D1E572',
    'Chartreuse': '#B4CD3D',
    'Prehistoric': '#A9A032',
    'Alligator': '#828335',
    'Olive': '#697135',
    'Murk': '#4B4420',
    'Bark': '#7E7645',
    'Amber': '#C18E1B',
    'Sponge': '#BEA55D',
    'Haze': '#D1B045',
    'Swallowtail': '#D1B300',
    'Lemon': '#FFE63B',
    'Wasp': '#F9E255',
    'Yolk': '#F7FF6F',
    'Banana': '#FFEC80',
    'Honey': '#FDD68B',
    'Squash': '#FDE9AC',
    'Sanddollar': '#EDE8B0',
    'Mellow': '#FFFDEA',
    'Lychee': '#FDF1E1',
    'Creme': '#FFEFDC',
    'Pelt': '#F7DEBF',
    'Ivory': '#FFD297',
    'Peanut': '#F6BF6C',
    'Gold': '#F2AD0C',
    'Marigold': '#FFB53C',
    'Apricot': '#FA912B',
    'Poppy': '#FF8500',
    'Yam': '#FF984F',
    'Orange': '#FFA147',
    'Peach': '#FFB576',
    'Silt': '#FCC4AD',
    'Sahara': '#F0B392',
    'Pecan': '#E29C7A',
    'Saffron': '#D5602B',
    'Chestnut': '#CB732D',
    'Bronze': '#B2560D',
    'Sandstone': '#B24407',
    'Carrot': '#FF5500',
    'Fire': '#EF5C23',
    'Pumpkin': '#FF6841',
    'Sunrise': '#FF7360',
    'Cinnamon': '#C15A39',
    'Caramel': '#C47149',
    'Acorn': '#B27749',
    'Tortilla': '#9A7B4F',
    'Hide': '#C3996F',
    'Beige': '#CABBA2',
    'Pine': '#827A64',
    'Soil': '#6D675B',
    'Coffee': '#564D48',
    'Cocoa': '#3C3030',
    'Chocolate': '#766259',
    'Cappuccino': '#977B6C',
    'Beach': '#BFA18F',
    'Gingerbread': '#8A6059',
    'Maple': '#7A4D4D',
    'Hazel': '#774840',
    'Coconut': '#6B3C34',
    'Clay': '#603E3D',
    'Sable': '#57372C',
    'Penny': '#432711',
    'Umber': '#301E1A',
    'Brownie': '#22110A',
    'Birch': '#2F1B1B',
    'Feldspar': '#5A4534',
    'Walnut': '#72573A',
    'Grain': '#855B33',
    'Ginger': '#91532A',
    'Starfish': '#90553A',
    'Brown': '#8E5B3F',
    'Slate': '#563012',
    'Auburn': '#7B3C1D',
    'Copper': '#A44B28',
    'Rust': '#8B3220',
    'Tomato': '#BA311C',
    'Vermillion': '#E22D18',
    'Pepper': '#CE000D',
    'Cherry': '#AA0024',
    'Crimson': '#850012',
    'Ruby': '#7A0E1E',
    'Garnet': '#581014',
    'Sanguine': '#2D0102',
    'Blood': '#451717',
    'Rose': '#652127',
    'Cranberry': '#8C272D',
    'Redwood': '#C1272D',
    'Strawberry': '#DF3236',
    'Fruit': '#FC6D68',
    'Carmine': '#B13A3A',
    'Cerise': '#A12928',
    'Brick': '#9A534D',
    'Coral': '#CC6F6F',
    'Blush': '#FEA0A0',
    'Macaron': '#FFE2E6',
    'Sakura': '#FFB7B4',
    'Flamingo': '#FEA1B3',
    'Peony': '#FFE5E5',
    'Dust': '#EBE0DF',
    'Ribbon': '#FF839B',
    'Charm': '#C67A80',
    'Taffy': '#D696B6',
    'Candy': '#EB799A',
    'Bubblegum': '#FB5E79',
    'Watermelon': '#DB518D',
    'Magenta': '#E934AA',
    'Fuschia': '#E7008B',
    'Tulip': '#CB0381',
    'Razzmatazz': '#ED2061',
    'Rubellite': '#AA004C',
    'Raspberry': '#8A024A',
    'Syrah': '#4D0F28',
    'Mauve': '#9C4975',
    'Radish': '#C44674',
    'Gum': '#E77FBF',
    'Quartz': '#E5A9FF',
    'Confetti': '#E8CCFF',
    'Petalite': '#FFD6F6',
    'Pearl': '#FBEDFA',
    'Legendary': '#FFD700',
    'Error: 2F1B1C': '#2F1B1C',
    'Error: 211919': '#211919',
    'Error: 28292B': '#28292B',
    'Error: 8C272F': '#8C272F',
    'Error: 7A87A1': '#7A87A1',
    'Error: 567C3F': '#567C3F',
    'Error: 013485': '#013485',
    'Error: 0F0A09': '#0F0A09',
    'Error: AB5D29': '#AB5D29',
    'Error: 134805': '#134805',
}

COLOR_LIST = _WIKI_DATA["COLOR_LIST"]
ELEMENTAL_POTIONS = _WIKI_DATA["ELEMENTAL_POTIONS"]

MATERIAL_LIST = _WIKI_DATA["MATERIAL_LIST"]

ELEMENT_LIST = _WIKI_DATA["ELEMENT_LIST"]

SPECIES_LIST = _WIKI_DATA["SPECIES_LIST"]

SPECIES_RARITY_FALLBACK = {
    'Cogitergosyn': 'Legendary',
    'Putrefacceum': 'Relic',
    'Veidreki': 'Relic',
    'Voltstorm': 'Relic',
    'Alatura': 'Legendary',
    'Allpehourn': 'Legendary',
    'Amaris': 'Legendary',
    'Ancient Aranga': 'Legendary',
    'Ancient Skriffei': 'Legendary',
    'Ancient Tosknir': 'Legendary',
    'Aranga': 'Legendary',
    'Aurutentia': 'Legendary',
    'Avarakuma': 'Legendary',
    'Betevial': 'Legendary',
    'Bylendarach': 'Legendary',
    'Catruca': 'Legendary',
    'Chippychiip': 'Legendary',
    'Constello': 'Legendary',
    'Corrupted Chronocus': 'Legendary',
    'Cosmalisk': 'Legendary',
    'Cryptillow': 'Legendary',
    'Cynphion-Noire': 'Legendary',
    'Djaevelhest': 'Legendary',
    'Dratheros': 'Legendary',
    'Eryndiorn': 'Legendary',
    'Eteralix': 'Legendary',
    'Fabledrak': 'Legendary',
    'Flornymphis': 'Legendary',
    'Fulong': 'Legendary',
    'Gaulyra': 'Legendary',
    'Goelica': 'Legendary',
    'Guilmoros': 'Legendary',
    'Gundrakken': 'Legendary',
    'Gyrocopter': 'Legendary',
    'Ignicaris': 'Legendary',
    'Khorgeryn': 'Legendary',
    'Kikien': 'Legendary',
    'Kostragula': 'Legendary',
    'Ladonix': 'Legendary',
    'Livalient': 'Legendary',
    'Lumenigh': 'Legendary',
    'Lyria': 'Legendary',
    'Mallopii': 'Legendary',
    'Malupentys': 'Legendary',
    'Moixaura': 'Legendary',
    'Motorouk': 'Legendary',
    'Oroalas': 'Legendary',
    'Ortarouk': 'Legendary',
    'Paladianos': 'Legendary',
    'Penguitus': 'Legendary',
    'Polairistel': 'Legendary',
    'Quetzaloctli': 'Legendary',
    'Raikami': 'Legendary',
    'Riyu': 'Legendary',
    'Roborus V': 'Legendary',
    'Seikarin': 'Legendary',
    'Sentalius': 'Legendary',
    'Silvestratus': 'Legendary',
    'Source Dragon of Energy': 'Legendary',
    'Source Dragon of Motion': 'Legendary',
    'Stellaris': 'Legendary',
    'Stratalix': 'Legendary',
    'Taligris': 'Legendary',
    'Terruak': 'Legendary',
    'Tianma': 'Legendary',
    'Tlalocun': 'Legendary',
    'Tosknir': 'Legendary',
    'Tronat': 'Legendary',
    'Uheailes': 'Legendary',
    'Verdrakor': 'Legendary',
    'Voltagen': 'Legendary',
    'Vulcoramor': 'Legendary',
    'Vyreas': 'Legendary',
    'Xellatruce': 'Legendary',
    'Yggdraten': 'Legendary',
    'Aeroseys': 'Epic',
    'Aethereus': 'Epic',
    'Amoonita': 'Epic',
    'Andronaut': 'Epic',
    'Araneaix': 'Epic',
    'Arielisces': 'Epic',
    'Astraeisis': 'Epic',
    'Atravanta': 'Epic',
    'Balgunyur': 'Epic',
    'Caelydris': 'Epic',
    'Calimaki': 'Epic',
    'Carnealgon': 'Epic',
    'Casirius': 'Epic',
    'Caudembris': 'Epic',
    'Caunaris': 'Epic',
    'Chameleaf': 'Epic',
    'Chrysaloom': 'Epic',
    'Cirquemaar': 'Epic',
    'Cutiepatoo': 'Epic',
    'Desygual': 'Epic',
    'Diraixos': 'Epic',
    'Eisendrache': 'Epic',
    'Falugeis': 'Epic',
    'Fernifex': 'Epic',
    'Firifeller': 'Epic',
    'Fleurianthus': 'Epic',
    'Fueguin': 'Epic',
    'Geoteryx': 'Epic',
    'Glaquacus': 'Epic',
    'Goliatomb': 'Epic',
    'Gordigourd': 'Epic',
    'Gyngefared': 'Epic',
    'Harvitius': 'Epic',
    'Hoarusn': 'Epic',
    'Hongliang': 'Epic',
    'Impiavolo': 'Epic',
    'Iridesia': 'Epic',
    'Karukiri': 'Epic',
    'Khalknirik': 'Epic',
    'Lucklif': 'Epic',
    'Lum Luenh': 'Epic',
    'Lunaesol': 'Epic',
    'Makoura': 'Epic',
    'Mechanoxide': 'Epic',
    'Mielebee': 'Epic',
    'Mistrasune': 'Epic',
    'Mosuraki': 'Epic',
    'Mountain Dragon': 'Epic',
    'Nakahii': 'Epic',
    'Nightmare Paranox': 'Epic',
    'Noctorius': 'Epic',
    "Nor'gan": 'Epic',
    'Nyxavoid': 'Epic',
    'Ovicirus': 'Epic',
    'Pagulau': 'Epic',
    'Pananisea': 'Epic',
    'Phocaphan': 'Epic',
    'Phyllantis': 'Epic',
    'Quahtona': 'Epic',
    'Quasaldrus': 'Epic',
    'Robodon': 'Epic',
    'Roborus X': 'Epic',
    'Rozora': 'Epic',
    'Smokgien': 'Epic',
    'Snoballista': 'Epic',
    'Stymelisk': 'Epic',
    'Sunfloris': 'Epic',
    'Syliru': 'Epic',
    'Tempiritus': 'Epic',
    'Tenebis': 'Epic',
    'Thorkonyx': 'Epic',
    'Torneidus': 'Epic',
    'Trametos': 'Epic',
    'Trilinaris': 'Epic',
    'Tsukuizan': 'Epic',
    'Valkiero': 'Epic',
    'Varana': 'Epic',
    'Verscervus': 'Epic',
    'Viridik': 'Epic',
    'Volkumos': 'Epic',
    'Vulpiruth': 'Epic',
    'Woodluma': 'Epic',
    'Wuonghou': 'Epic',
    'Yueshi': 'Epic',
    'Alrenoth': 'Rare',
    'Coralina': 'Rare',
    'Dunvolth': 'Rare',
    'Dysuva': 'Rare',
    'Fayrah': 'Rare',
    'Featherfang': 'Rare',
    'Ferorex': 'Rare',
    'Glacegar': 'Rare',
    'Hexalios': 'Rare',
    'Hielochiim': 'Rare',
    'Krekiz': 'Rare',
    'Lepilon': 'Rare',
    'Mother Dragon': 'Rare',
    'Nadaler': 'Rare',
    'Onagajin': 'Rare',
    'Paranox': 'Rare',
    'Radidon': 'Rare',
    'Solarizon': 'Rare',
    'Soukeyi': 'Rare',
    'Xerthos': 'Rare',
    'Yulereinn': 'Rare',
    'Zinthros': 'Rare',
    'Avefir': 'Uncommon',
    'Ayatrice': 'Uncommon',
    'Bisonture': 'Uncommon',
    'Bizaltidath': 'Uncommon',
    'Chronocus': 'Uncommon',
    'Cybernid': 'Uncommon',
    'Magmip': 'Uncommon',
    'Paukiki': 'Uncommon',
    'Scrawei': 'Uncommon',
    'Sylva': 'Uncommon',
    'Taraka': 'Uncommon',
    'Tarotta': 'Uncommon',
    'Tigrilia': 'Uncommon',
    'Tuskaryn': 'Uncommon',
    'Venid': 'Uncommon',
    'Yaruakura': 'Uncommon',
    'Zeipera': 'Uncommon',
    'Agricos': 'Common',
    'Amphyll': 'Common',
    'Atarix': 'Common',
    'Cocovira': 'Common',
    'Dexyn': 'Common',
    'Enkylous': 'Common',
    'Geliklen': 'Common',
    'Howler': 'Common',
    'Khepera': 'Common',
    'Neroxide': 'Common',
    'Numine': 'Common',
    'Palus': 'Common',
    'Rhyndac': 'Common',
    'Rocirus': 'Common',
    'Saurium': 'Common',
    'Skelltor': 'Common',
    'Skriffei': 'Common',
    'Skyrix': 'Common',
    'Suiikipon': 'Common',
    'Taihoa': 'Common',
    'Venu': 'Common',
    'Canyarches': 'Legendary',
    'Garutagoyle': 'Legendary',
    'Archogine': 'Legendary',
    'Flame': 'Epic',
    'Shard': 'Epic',
    'Wisp': 'Epic',
    'Rocky': 'Epic',
}

SPECIES_RARITY = {**SPECIES_RARITY_FALLBACK, **_WIKI_DATA["SPECIES_RARITY"]}

PUPIL_LIST = _WIKI_DATA["PUPIL_LIST"]

COSMETIC_TRAIT_LIST = ["None"] + _WIKI_DATA["COSMETIC_TRAIT_LIST"]


FLYING_ONLY_POSITIVE  = {"Strong Wing Membrane"}
NONFLYING_ONLY_POSITIVE = {"Swifter Leap"}
FLYING_ONLY_NEGATIVE  = {"Thin Wing Membrane"}


def species_can_fly(species):
    return SPECIES_CAN_FLY.get(species, True)


def available_positive_traits(species):
    if species_can_fly(species):
        return [t for t in POSITIVE_TRAIT_LIST if t not in NONFLYING_ONLY_POSITIVE]
    else:
        return [t for t in POSITIVE_TRAIT_LIST if t not in FLYING_ONLY_POSITIVE]


def available_negative_traits(species):
    if species_can_fly(species):
        return list(NEGATIVE_TRAIT_LIST)
    else:
        return [t for t in NEGATIVE_TRAIT_LIST if t not in FLYING_ONLY_NEGATIVE]

MUTATION_CAP = 5
GENDER_LIST = ["Male", "Female"]
SDA_EXCLUDED_FALLBACK = {
    'Flame',
    'Great Devourer',
    'Mountain Dragon',
    'Riyu',
    'Rocky',
    'Shard',
    'Source Dragon of Energy',
    'Source Dragon of Motion',
    'Ultra Dragon',
    'Wisp',
}
SDA_EXCLUDED = set(SDA_EXCLUDED_FALLBACK)
AGE_LIST = ["Baby", "Juvenile", "Adult", "Elder"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
BIRTHDAY_MIN_YEAR = 1969

POSITIVE_TRAIT_LIST = ["None"] + _WIKI_DATA["POSITIVE_TRAIT_LIST"]
NEGATIVE_TRAIT_LIST = ["None"] + _WIKI_DATA["NEGATIVE_TRAIT_LIST"]
MAX_POSITIVE_TRAITS = 5
MAX_NEGATIVE_TRAITS = 2
TRAIT_TIER_MIN, TRAIT_TIER_MAX = 1, 10

ELEMENT_COLOR_OVERRIDES = {
    "Fire": "#FF5C2E", "Grass": "#4CAF50", "Water": "#3D8EDB", "Lightning": "#F2D11D",
    "Ice": "#7FD8F2", "Dark": "#1A1A22", "Light": "#FFF3C2", "Toxic": "#9FFF00",
    "Demon": "#7A0E1E", "Angel": "#FFE9A8", "Sun": "#FFB300", "Moon": "#C9D6E8",
    "Lava": "#FF4500", "Air": "#D9F2EA", "Ocean": "#2F83FF", "Abyss": "#0D1E25",
    "Bone": "#E8DFC8", "Ghost": "#C9C2E8", "Christmas": "#C8102E", "Gold": "#F2AD0C",
    "Diamond": "#BEEFFF", "Rainbow": "#FF6FCB", "Storm": "#6E7B8B", "Frostbite": "#AEE9FF",
    "Antimatter": "#2B0D88", "Corrosive": "#9FFF00", "Death": "#3B3736", "Life": "#3ABB3B",
    "Equinox": "#B884FF", "Wraith": "#5C415D", "Celestial": "#9499F7", "Metal": "#9C9C9C",
    "Plasma": "#E934AA", "Eclipse": "#22110A", "Solar Winds": "#FF8500", "Battle": "#8B3220",
    "Warrior": "#A44B28", "Love": "#FB5E79", "Honey": "#FDD68B", "Carrot": "#FF8500",
    "Moss": "#3ABB3B", "Sakura": "#FFB7B4", "Bluefire": "#2F83FF", "Relic": "#B2560D",
    "Tempest": "#6E7B8B",
}


def element_hash_color(name):
    h = int(hashlib.md5(name.encode("utf-8")).hexdigest(), 16)
    hue = (h % 360) / 360.0
    sat = 0.55 + ((h // 360) % 30) / 100.0
    light = 0.42 + ((h // 360 // 30) % 22) / 100.0
    r, g, b = colorsys.hls_to_rgb(hue, light, sat)
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def get_element_color(name):
    return ELEMENT_COLOR_OVERRIDES.get(name) or element_hash_color(name)


def get_color_hex(name, element=None):
    if name == "Legendary" and element:
        return get_element_color(element)
    return COLOR_HEX_MAP.get(name, "#777777")


def readable_text_color(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#1A1A1B" if luminance > 0.55 else "#FFFFFF"


if getattr(sys, "frozen", False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(SCRIPT_DIR, "dragons_data.json")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
ICON_DIR = os.path.join(SCRIPT_DIR, "assets", "icons")
LEGENDARY_SHIFT_DIR = os.path.join(SCRIPT_DIR, "assets", "legendary_shifts")
MISC_DIR = os.path.join(SCRIPT_DIR, "assets", "misc")
MENUICONS_DIR = os.path.join(SCRIPT_DIR, "assets", "misc", "menuicons")
DRAGON_ICONS_DIR = os.path.join(SCRIPT_DIR, "assets", "dragonicons")
DRAGON_IMAGES_DIR = os.path.join(SCRIPT_DIR, "assets", "dragon_images")
COSMETIC_TRAIT_ICON_DIR = os.path.join(SCRIPT_DIR, "assets", "misc", "cosmetictrait")
POTION_ICON_DIR = os.path.join(SCRIPT_DIR, "assets", "misc", "potions")
FONTS_DIR = os.path.join(SCRIPT_DIR, "assets", "fonts")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ICON_DIR, exist_ok=True)
os.makedirs(LEGENDARY_SHIFT_DIR, exist_ok=True)
os.makedirs(MISC_DIR, exist_ok=True)
os.makedirs(MENUICONS_DIR, exist_ok=True)
os.makedirs(DRAGON_ICONS_DIR, exist_ok=True)
os.makedirs(DRAGON_IMAGES_DIR, exist_ok=True)
os.makedirs(COSMETIC_TRAIT_ICON_DIR, exist_ok=True)
os.makedirs(POTION_ICON_DIR, exist_ok=True)
os.makedirs(FONTS_DIR, exist_ok=True)

_UI_ICONS_BG = {"thread": None, "paths": None}


def _ui_icons_bg_fetch():
    try:
        import wiki_icons
        _UI_ICONS_BG["paths"] = wiki_icons.download_ui_icons(MISC_DIR, MENUICONS_DIR, verbose=True)
        wiki_icons.download_fredoka_font(FONTS_DIR, verbose=True)
        wiki_icons.ensure_ico(
            os.path.join(MISC_DIR, "dragonhead.png"),
            os.path.join(MISC_DIR, "dragonhead.ico"),
            verbose=True,
        )
    except Exception as e:
        print(f"[wiki_icons] ui icon fetch skipped: {e}")


_UI_ICONS_BG["thread"] = threading.Thread(target=_ui_icons_bg_fetch, daemon=True)
_UI_ICONS_BG["thread"].start()


APP_FONT_FAMILY = "Fredoka SemiBold"
APP_VERSION = "1.6.3"
GITHUB_REPO = "I-Verian/Lairkeeper-API"
APP_FONT_WEIGHT = "normal"


def load_custom_fonts():
    lines = []

    def log(msg):
        lines.append(msg)
        print(msg)

    if sys.platform != "win32":
        log(f"[fonts] Not on Windows — skipping private font loading. "
            f"'{APP_FONT_FAMILY}' must be installed normally for it to show up.")
    else:
        font_files = [f for f in os.listdir(FONTS_DIR) if f.lower().endswith((".ttf", ".otf"))]
        if not font_files:
            log(f"[fonts] No .ttf/.otf files found in: {FONTS_DIR}")
            log(f"        Drop an '{APP_FONT_FAMILY}' font file in there for it to be used.")
        else:
            FR_PRIVATE = 0x10
            for fname in font_files:
                try:
                    n_added = ctypes.windll.gdi32.AddFontResourceExW(
                        os.path.join(FONTS_DIR, fname), FR_PRIVATE, 0)
                    if n_added:
                        log(f"[fonts] Registered: {fname} ({n_added} face(s) added)")
                    else:
                        log(f"[fonts] FAILED to register {fname} — Windows returned 0 faces added "
                            f"(file may be corrupt or not a valid font)")
                except Exception as e:
                    log(f"[fonts] Failed to register {fname}: {e}")

    try:
        resolved = tkfont.Font(family=APP_FONT_FAMILY, size=20, weight=APP_FONT_WEIGHT).actual()
        if resolved.get("family", "").lower() == APP_FONT_FAMILY.lower():
            log(f"[fonts] SUCCESS — Tk resolved ('{APP_FONT_FAMILY}', 20, '{APP_FONT_WEIGHT}') "
                f"to itself: {resolved}")
        else:
            log(f"[fonts] NOT APPLIED — asked for '{APP_FONT_FAMILY}' but Tk is actually using "
                f"'{resolved.get('family')}' instead: {resolved}")
            log(f"        This usually means either (a) the font file's INTERNAL name doesn't "
                f"match '{APP_FONT_FAMILY}' exactly (filenames don't count — open the font in "
                f"Windows' Font Viewer to check the real name), or (b) the file didn't register.")
    except Exception as e:
        log(f"[fonts] Could not verify font resolution: {e}")

    try:
        with open(os.path.join(SCRIPT_DIR, "font_debug.log"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception:
        pass


def fit_text_size(text, family, max_size, min_size, max_width, weight=APP_FONT_WEIGHT):
    size = max_size
    while size > min_size:
        try:
            measured = tkfont.Font(family=family, size=size, weight=weight).measure(text)
        except Exception:
            return size
        if measured <= max_width:
            return size
        size -= 1
    return min_size


DEFAULT_DRAGONS = {}

LEGACY_DEMO_DRAGON_IDS = {"ferorex", "zinthros", "amoonita"}


def species_icon_path(species):
    base_underscore = species.replace(" ", "_")
    base_nospace = species.replace(" ", "")
    base_lower = species.lower().replace(" ", "_")
    base_lower_nospace = species.lower().replace(" ", "")
    candidates = [
        f"{base_underscore}_Icon.png",
        f"{base_underscore}_icon.png",
        f"{base_underscore}.png",
        f"{base_nospace}_Icon.png",
        f"{base_nospace}_icon.png",
        f"{base_nospace}.png",
        f"{species}_Icon.png",
        f"{species}_icon.png",
        f"{species}.png",
        f"{base_lower}_icon.png",
        f"{base_lower}.png",
        f"{base_lower_nospace}_icon.png",
        f"{base_lower_nospace}.png",
    ]
    try:
        existing = {fname.lower(): fname for fname in os.listdir(DRAGON_ICONS_DIR)}
    except Exception:
        existing = {}
    for candidate in candidates:
        match = existing.get(candidate.lower())
        if match:
            return os.path.join(DRAGON_ICONS_DIR, match)
    return os.path.join(DRAGON_ICONS_DIR, candidates[0])


def migrate_dragon(d):
    if "Colors" not in d and "Patterns" in d:
        d["Colors"] = d.pop("Patterns")
    if "Materials" not in d or isinstance(d.get("Materials"), list):
        if "Finish" in d:
            d["Materials"] = d.pop("Finish")
        else:
            d["Materials"] = {"P": "-", "S": "-", "T": "-"}
    d.pop("Finish", None)
    d.pop("Title", None)
    d.pop("Hunger", None)
    d.pop("MaxHunger", None)
    d.pop("Health", None)
    d.pop("MaxHealth", None)
    d.pop("Image", None)
    d.setdefault("Generation", "-")
    d.setdefault("MaxMutations", MUTATION_CAP)
    d.setdefault("CosmeticTrait", "None")
    d.setdefault("Pupil", "-")
    d.setdefault("Element", "-")
    d.setdefault("Gender", "")
    d.setdefault("Soulbound", False)
    d.setdefault("Element2", None)
    d.setdefault("Note", "")
    d.setdefault("Rebirths", 0)
    d.setdefault("Birthday", None)
    d.setdefault("OriginalOwner", None)
    d.setdefault("Level", "-")
    d.setdefault("Age", "-")
    d.setdefault("PositiveTraits", [])
    d.setdefault("NegativeTraits", [])

    return d


TABS_KEY = "__tabs__"
import shutil


def _account_dir(account_name):
    return os.path.join(DATA_DIR, account_name)


def _dragon_path(account_name, dragon_id):
    return os.path.join(_account_dir(account_name), f"{dragon_id}.json")


def _tabs_path(account_name):
    return os.path.join(_account_dir(account_name), "__tabs__.json")


def _settings_path(account_name):
    return os.path.join(_account_dir(account_name), "__settings__.json")


def load_account_settings(account_name):
    p = _settings_path(account_name)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_account_settings(account_name, settings):
    adir = _account_dir(account_name)
    os.makedirs(adir, exist_ok=True)
    try:
        with open(_settings_path(account_name), "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Could not save settings for {account_name}:", e)


def _global_settings_path():
    return os.path.join(DATA_DIR, "__global_settings__.json")


def load_global_settings():
    p = _global_settings_path()
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_global_settings(settings):
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(_global_settings_path(), "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print("Could not save global settings:", e)


global_settings = load_global_settings()
global_settings.setdefault("EnableSDA", True)
global_settings.setdefault("EnableElemental", True)
global_settings.setdefault("CompactMode", False)


account_settings = {}
current_themes = {}


def _themes_path(account_name):
    return os.path.join(_account_dir(account_name), "__themes__.json")


def load_themes(account_name):
    p = _themes_path(account_name)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_themes(account_name, themes_dict):
    adir = _account_dir(account_name)
    os.makedirs(adir, exist_ok=True)
    try:
        with open(_themes_path(account_name), "w", encoding="utf-8") as f:
            json.dump(themes_dict, f, indent=2)
    except Exception as e:
        print(f"Could not save themes for {account_name}:", e)


def _write_account(account_name, dragon_dict, tabs_dict):
    adir = _account_dir(account_name)
    os.makedirs(adir, exist_ok=True)

    try:
        with open(_tabs_path(account_name), "w", encoding="utf-8") as f:
            json.dump(tabs_dict, f, indent=2)
    except Exception as e:
        print(f"Could not save tabs for {account_name}:", e)

    for did, d in dragon_dict.items():
        try:
            with open(_dragon_path(account_name, did), "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2)
        except Exception as e:
            print(f"Could not save dragon {did}:", e)

    try:
        existing_ids = {
            fname[:-5] for fname in os.listdir(adir)
            if fname.endswith(".json") and fname != "__tabs__.json"
        }
        for orphan in existing_ids - set(dragon_dict.keys()):
            try:
                os.remove(_dragon_path(account_name, orphan))
            except Exception:
                pass
    except Exception:
        pass


def _read_account(account_name):
    adir = _account_dir(account_name)
    dragon_dict = {}
    tabs_dict = {}

    if not os.path.isdir(adir):
        return dragon_dict, tabs_dict

    tabs_file = _tabs_path(account_name)
    if os.path.exists(tabs_file):
        try:
            with open(tabs_file, "r", encoding="utf-8") as f:
                tabs_dict = json.load(f)
        except Exception as e:
            print(f"Could not read tabs for {account_name}:", e)

    for fname in os.listdir(adir):
        if not fname.endswith(".json") or fname == "__tabs__.json":
            continue
        dragon_id = fname[:-5]
        try:
            with open(os.path.join(adir, fname), "r", encoding="utf-8") as f:
                dragon_dict[dragon_id] = migrate_dragon(json.load(f))
        except Exception as e:
            print(f"Could not read dragon file {fname}:", e)

    return dragon_dict, tabs_dict


def _migrate_from_legacy():
    if not os.path.exists(DATA_FILE):
        return
    if os.path.exists(DATA_DIR):
        return

    print("[data] Migrating from dragons_data.json to per-dragon files…")
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        print("[data] Could not read legacy file:", e)
        return

    if not raw:
        return

    first_value = next(iter(raw.values()))
    if isinstance(first_value, dict) and "Nickname" in first_value:
        raw = {"Player1": raw}

    for acc, roster in raw.items():
        if acc in LEGACY_EXAMPLE_ACCOUNTS:
            continue
        tabs = roster.pop(TABS_KEY, {})
        dragons_in_acc = {k: migrate_dragon(v) for k, v in roster.items()}
        _write_account(acc, dragons_in_acc, tabs)

    try:
        os.rename(DATA_FILE, DATA_FILE + ".migrated")
        print("[data] Migration complete. Old file renamed to dragons_data.json.migrated")
    except Exception:
        pass


def load_all_accounts():
    _migrate_from_legacy()

    data = {}
    if os.path.isdir(DATA_DIR):
        for account_name in os.listdir(DATA_DIR):
            if not os.path.isdir(_account_dir(account_name)):
                continue
            if account_name in LEGACY_EXAMPLE_ACCOUNTS:
                continue
            dragon_dict, tabs_dict = _read_account(account_name)
            data[account_name] = {**dragon_dict, TABS_KEY: tabs_dict}

    return data


def save_all_accounts(data):
    for acc, roster in data.items():
        tabs = roster.get(TABS_KEY, {})
        dragons_in_acc = {k: v for k, v in roster.items() if k != TABS_KEY}
        _write_account(acc, dragons_in_acc, tabs)


all_accounts_data = load_all_accounts()
current_account = None
dragons = {}
current_tabs = {}


def get_account_dragons():
    return {k: v for k, v in all_accounts_data.get(current_account, {}).items()
            if k != TABS_KEY}


def switch_account(account_name):
    global dragons, current_tabs, current_account, account_settings, current_themes
    current_account = account_name
    slot = all_accounts_data.setdefault(account_name, {})
    if TABS_KEY not in slot:
        slot[TABS_KEY] = {}
    dragons = {k: v for k, v in slot.items() if k != TABS_KEY}
    current_tabs = slot[TABS_KEY]
    account_settings = load_account_settings(account_name)
    current_themes = load_themes(account_name)


def persist():
    account_slot = all_accounts_data.setdefault(current_account, {})
    account_slot[TABS_KEY] = current_tabs
    for k, v in dragons.items():
        account_slot[k] = v
    for k in list(account_slot.keys()):
        if k != TABS_KEY and k not in dragons:
            del account_slot[k]
    _write_account(current_account, dragons, current_tabs)


def create_tab(name):
    tab_id = uuid.uuid4().hex[:10]
    current_tabs[tab_id] = {"name": name, "members": []}
    persist()
    return tab_id


def delete_tab(tab_id):
    current_tabs.pop(tab_id, None)
    persist()


def rename_tab(tab_id, new_name):
    if tab_id in current_tabs:
        current_tabs[tab_id]["name"] = new_name
        persist()


def add_dragon_to_tab(tab_id, dragon_id):
    if tab_id in current_tabs and dragon_id not in current_tabs[tab_id]["members"]:
        current_tabs[tab_id]["members"].append(dragon_id)
        persist()


def remove_dragon_from_tab(tab_id, dragon_id):
    if tab_id in current_tabs and dragon_id in current_tabs[tab_id]["members"]:
        current_tabs[tab_id]["members"].remove(dragon_id)
        persist()


def move_dragon_to_account(dragon_id, dest_account):
    if dragon_id not in dragons or dest_account == current_account:
        return False

    record = dragons.pop(dragon_id)

    for tab in current_tabs.values():
        if dragon_id in tab.get("members", []):
            tab["members"].remove(dragon_id)

    dest_slot = all_accounts_data.setdefault(dest_account, {})
    if TABS_KEY not in dest_slot:
        dest_slot[TABS_KEY] = {}

    new_id = dragon_id
    if new_id in dest_slot:
        new_id = uuid.uuid4().hex[:10]
    dest_slot[new_id] = record

    persist()

    dest_dragons = {k: v for k, v in dest_slot.items() if k != TABS_KEY}
    _write_account(dest_account, dest_dragons, dest_slot.get(TABS_KEY, {}))

    return True


def center(win, w, h):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = max(0, min((sw - w) // 2, sw - w))
    y = max(0, min((sh - h) // 2, sh - h))
    win.geometry(f"{w}x{h}+{x}+{y}")


def set_window_icon(win):
    ico_path = os.path.join(MISC_DIR, "dragonhead.ico")
    if sys.platform == "win32" and os.path.exists(ico_path):
        try:
            win.iconbitmap(default=ico_path)
        except Exception:
            pass
    try:
        path = os.path.join(MISC_DIR, "dragonhead.png")
        photo = ImageTk.PhotoImage(Image.open(path))
        win._icon_ref = photo
        win.iconphoto(True, photo)
    except Exception:
        pass


def lighten(hex_color, amount=18):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (max(0, min(255, c + amount)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def round_rect(canvas, x1, y1, x2, y2, r=18, **kwargs):
    r = min(r, abs(x2 - x1) / 2, abs(y2 - y1) / 2)
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def draw_capsule(canvas, x1, y1, x2, y2, **kwargs):
    h = y2 - y1
    r = h / 2
    canvas.create_oval(x1, y1, x1 + h, y2, **kwargs)
    canvas.create_oval(x2 - h, y1, x2, y2, **kwargs)
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs)


def outline_text(canvas, x, y, text, font, fill, outline, **kwargs):
    offsets = [(-2, 0), (2, 0), (0, -2), (0, 2),
               (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for dx, dy in offsets:
        canvas.create_text(x + dx, y + dy, text=text, font=font,
                            fill=outline, **kwargs)
    canvas.create_text(x, y, text=text, font=font, fill=fill, **kwargs)


def shadowed_name_text(canvas, x, y, text, font, **kwargs):
    shadow_dx, shadow_dy = 3, 3
    canvas.create_text(x + shadow_dx, y + shadow_dy, text=text, font=font,
                        fill=PALETTE["name_shadow"], **kwargs)
    outline_text(canvas, x, y, text, font, PALETTE["name_fill"], PALETTE["name_outline"], **kwargs)


def draw_star(canvas, cx, cy, r, fill, outline):
    pts = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append(cx + rad * math.cos(angle))
        pts.append(cy - rad * math.sin(angle))
    canvas.create_polygon(pts, fill=fill, outline=outline, width=2)


def draw_bar(canvas, x, y, w, h, value, max_value, text=None):
    round_rect(canvas, x, y, x + w, y + h, r=h / 2,
                fill=PALETTE["bar_track"], outline=PALETTE["bar_border"], width=2)

    frac = 1.0 if not max_value else max(0.0, min(1.0, value / max_value))
    fill_w = max(h, w * frac)
    if frac > 0:
        round_rect(canvas, x, y, x + fill_w, y + h, r=h / 2,
                    fill=PALETTE["bar_fill"], outline="", width=0)
        round_rect(canvas, x, y, x + fill_w, y + h, r=h / 2,
                    fill="", outline=PALETTE["bar_border"], width=2)

    if text is None:
        text = f"{value:,}/{max_value:,}" if isinstance(value, int) else f"{value}/{max_value}"
    outline_text(canvas, x + w / 2, y + h / 2, text, (APP_FONT_FAMILY, 12, APP_FONT_WEIGHT),
                 "white", "#1A3D10")


def setup_ttk_style(root):
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure("Dragon.TCombobox",
                     fieldbackground=PALETTE["tag_fill"],
                     background=PALETTE["card_fill"],
                     foreground="white",
                     arrowcolor="white",
                     bordercolor=PALETTE["panel_border"],
                     selectbackground=PALETTE["tag_fill"],
                     selectforeground="white")
    style.map("Dragon.TCombobox",
              fieldbackground=[("readonly", PALETTE["tag_fill"])],
              foreground=[("readonly", "white")])

    root.option_add("*TCombobox*Listbox.background", PALETTE["tag_fill"])
    root.option_add("*TCombobox*Listbox.foreground", "white")
    root.option_add("*TCombobox*Listbox.selectBackground", PALETTE["card_fill"])
    root.option_add("*TCombobox*Listbox.selectForeground", "white")
    root.option_add("*TCombobox*Listbox.relief", "flat")
    root.option_add("*TCombobox*Listbox.borderWidth", "0")


def bind_mousewheel(canvas):
    canvas.configure(yscrollincrement=20)

    def _scroll(event):
        canvas.yview_scroll(int(-2 * (event.delta / 120)), "units")

    def _on_enter(_event):
        canvas.bind_all("<MouseWheel>", _scroll)

    def _on_leave(_event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", _on_enter)
    canvas.bind("<Leave>", _on_leave)


def rounded_button(canvas, x, y, w, h, text, command, r=16,
                    fill=None, outline=None, text_fill="white",
                    font=(APP_FONT_FAMILY, 13, APP_FONT_WEIGHT)):
    fill = fill or PALETTE["card_fill"]
    outline = outline or PALETTE["card_border"]
    rect_id = round_rect(canvas, x, y, x + w, y + h, r=r,
                          fill=fill, outline=outline, width=3)
    text_id = canvas.create_text(x + w / 2, y + h / 2, text=text,
                                  fill=text_fill, font=font)

    def on_click(_event):
        command()

    def on_enter(_event):
        canvas.itemconfig(rect_id, fill=lighten(fill))

    def on_leave(_event):
        canvas.itemconfig(rect_id, fill=fill)

    for item in (rect_id, text_id):
        canvas.tag_bind(item, "<Button-1>", on_click)
        canvas.tag_bind(item, "<Enter>", on_enter)
        canvas.tag_bind(item, "<Leave>", on_leave)
    return rect_id, text_id


def rounded_button_with_icon(canvas, x, y, w, h, text, icon_path, command, r=12,
                              fill=None, outline=None, text_fill="white",
                              font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT), text_align="center"):
    fill = fill or PALETTE["card_fill"]
    outline = outline or PALETTE["card_border"]
    rect_id = round_rect(canvas, x, y, x + w, y + h, r=r, fill=fill, outline=outline, width=3)

    icon_size = h - 10
    icon_cx = x + 8 + icon_size // 2
    icon_id = None
    text_left = x + 12

    try:
        img = Image.open(icon_path).convert("RGBA")
        img = fit_contain(img, icon_size, icon_size)
        photo = ImageTk.PhotoImage(img)
        if not hasattr(canvas, "_btn_icon_refs"):
            canvas._btn_icon_refs = []
        canvas._btn_icon_refs.append(photo)
        icon_id = canvas.create_image(icon_cx, y + h / 2, image=photo)
        text_left = x + 8 + icon_size + 8
    except Exception:
        pass

    if text_align == "left":
        text_id = canvas.create_text(text_left, y + h / 2, text=text,
                                      fill=text_fill, font=font, anchor="w")
    else:
        text_cx = text_left + (x + w - text_left - 8) / 2
        text_id = canvas.create_text(text_cx, y + h / 2, text=text,
                                      fill=text_fill, font=font)

    items = [i for i in (rect_id, icon_id, text_id) if i is not None]

    def on_click(_e): command()
    def on_enter(_e): canvas.itemconfig(rect_id, fill=lighten(fill))
    def on_leave(_e): canvas.itemconfig(rect_id, fill=fill)

    for item in items:
        canvas.tag_bind(item, "<Button-1>", on_click)
        canvas.tag_bind(item, "<Enter>", on_enter)
        canvas.tag_bind(item, "<Leave>", on_leave)
    return rect_id, text_id


def autocrop_to_content(img):
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    bbox = img.split()[-1].getbbox()
    return img.crop(bbox) if bbox else img


def fit_contain(img, w, h):
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    fitted = img.copy()
    fitted.thumbnail((w, h), Image.LANCZOS)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(fitted, ((w - fitted.width) // 2, (h - fitted.height) // 2), fitted)
    return canvas


def make_contained_photo(path, w, h, bg=(0, 0, 0, 0)):
    img = Image.open(path).convert("RGBA")
    img = autocrop_to_content(img)
    img.thumbnail((w, h), Image.LANCZOS)
    canvas = Image.new("RGBA", (w, h), bg)
    paste_x = (w - img.width) // 2
    paste_y = (h - img.height) // 2
    canvas.paste(img, (paste_x, paste_y), img)
    return ImageTk.PhotoImage(canvas)


def make_rounded_photo(path, w, h, radius=16):
    img = Image.open(path).convert("RGBA")
    img = autocrop_to_content(img)
    img = ImageOps.fit(img, (w, h), method=Image.LANCZOS, centering=(0.5, 0.5))
    corner_mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(corner_mask).rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    combined_alpha = ImageChops.multiply(img.split()[-1], corner_mask)
    img.putalpha(combined_alpha)
    return ImageTk.PhotoImage(img)


def draw_pill(canvas, x, y, w, h, text, fill,
              text_fill=None, text_outline=None, font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT), radius=None):
    text_fill = text_fill or PALETTE["pill_text"]
    text_outline = text_outline or PALETTE["pill_outline"]
    r = radius if radius is not None else h / 2
    round_rect(canvas, x, y, x + w, y + h, r=r,
                fill=fill, outline=fill, width=2)
    cx, cy = x + w / 2, y + h / 2
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        canvas.create_text(cx + dx, cy + dy, text=text, font=font, fill=text_outline)
    canvas.create_text(cx, cy, text=text, font=font, fill=text_fill)


def draw_legendary_pill(canvas, x, y, w, h, element, text="Legendary", font=None, radius=None):
    r = radius if radius is not None else int(h / 2)
    try:
        photo = make_rounded_photo(legendary_shift_path(element), int(w), int(h), radius=r)
    except Exception:
        return False

    canvas._refs.append(photo)
    canvas.create_image(x + w / 2, y + h / 2, image=photo)
    round_rect(canvas, x, y, x + w, y + h, r=h / 2, fill="", outline="#1C1430", width=2)

    cx, cy = x + w / 2, y + h / 2
    font = font or (APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        canvas.create_text(cx + dx, cy + dy, text=text, font=font, fill="#000000")
    canvas.create_text(cx, cy, text=text, font=font, fill="#FFFFFF")
    return True


def draw_orb(canvas, cx, cy, r, color):
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                        fill=color, outline=lighten(color, -50), width=2)
    canvas.create_oval(cx - r * 0.5, cy - r * 0.65, cx - r * 0.05, cy - r * 0.15,
                        fill=lighten(color, 90), outline="")


def try_icon(canvas, x, y, path, size=24):
    try:
        img = Image.open(path).convert("RGBA")
        img = autocrop_to_content(img)
        img = fit_contain(img, size, size)
        photo = ImageTk.PhotoImage(img)
        canvas._refs.append(photo)
        canvas.create_image(x, y, image=photo)
        return True
    except Exception:
        return False


def draw_triangle(canvas, x, y, size, fill):
    canvas.create_polygon(x, y - size, x, y + size, x + size * 1.3, y,
                           fill=fill, outline="")


def draw_appearance_row_bg(canvas, x, y, w, h):
    return round_rect(canvas, x, y, x + w, y + h, r=12,
                        fill=PALETTE["row_fill"], outline="", width=0)


ROW_ICON_FILES = {
    "Mutations": "mut.png",
    "Age":       "age.png",
}
ROW_ICON_FALLBACK_EMOJI = {
    "Mutations": "\U0001F9EC",
    "Age":       "\u23F3",
}


def draw_row_icon(canvas, x, y, label, icon_value):
    if label == "Cosmetic Trait":
        if not icon_value or icon_value == "None":
            return
        if not try_icon(canvas, x, y, cosmetic_trait_icon_path(icon_value), size=24):
            try_icon(canvas, x, y, os.path.join(MISC_DIR, "costrait.png"), size=24)
    elif label in ROW_ICON_FILES:
        path = os.path.join(MISC_DIR, ROW_ICON_FILES[label])
        if not try_icon(canvas, x, y, path, size=24):
            canvas.create_text(x, y, text=ROW_ICON_FALLBACK_EMOJI[label], font=(APP_FONT_FAMILY, 17))
    else:
        if not try_icon(canvas, x, y, element_icon_path(icon_value), size=24):
            draw_orb(canvas, x, y, 11, get_element_color(icon_value))


def draw_trait_row(canvas, x, y, w, h, trait_entry, accent_color):
    round_rect(canvas, x, y, x + w, y + h, r=10, fill=PALETTE["row_fill"], outline="", width=0)
    if trait_entry and trait_entry.get("Trait"):
        tier = trait_entry.get("Tier", 1)
        name = trait_entry.get("Trait", "-")
        badge_cx, badge_cy, badge_r = x + 20, y + h / 2, 14
        canvas.create_oval(badge_cx - badge_r, badge_cy - badge_r, badge_cx + badge_r, badge_cy + badge_r,
                            fill=PALETTE["tag_fill"], outline=accent_color, width=3)
        canvas.create_text(badge_cx, badge_cy, text=str(tier), fill="white", font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT))
        canvas.create_text(x + 42, y + h / 2, text=name, fill=PALETTE["value_text"],
                            font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), anchor="w", width=int(w - 50))
    else:
        canvas.create_text(x + w / 2, y + h / 2, text="Empty Slot", fill=PALETTE["label_text"],
                            font=(APP_FONT_FAMILY, 9, "italic"))


genetic_traits_expanded = {}
note_expanded = {}
_sda_icon_cache = {}


def show_details(parent, container, name, refresh_grid=None, active_tab=None):
    d = dragons[name]

    for w in container.winfo_children():
        w.destroy()

    viewport = container.master if isinstance(container.master, tk.Canvas) else container
    avail_w = max(1, (viewport.winfo_width() or 640) - 40)
    compact = global_settings.get("CompactMode", False)
    scale = 1.0 if compact else max(0.4, min(2.4, avail_w / 640))

    def F(n):
        return max(7, round(n * scale))

    def S(n):
        return round(n * scale)

    W = min(380, avail_w) if compact else S(640)
    is_traits_expanded = genetic_traits_expanded.get(name, False)
    is_note_expanded = note_expanded.get(name, False)
    has_note = bool(d.get("Note", "").strip())
    is_note_expanded = note_expanded.get(name, False)

    extra_optional_rows = sum(1 for v in (d.get("Birthday"), d.get("OriginalOwner"), d.get("Element2")) if v)
    if d.get("Rebirths", 0):
        extra_optional_rows += 1

    base_H = S(728)
    traits_extra = S(262) if is_traits_expanded else 0

    note_section_h = S(44) + S(14)
    if is_note_expanded:
        if has_note:
            note_text = d.get("Note", "").strip()
            try:
                _nf = tkfont.Font(family=APP_FONT_FAMILY, size=10)
                _avail = (W - 40) - 32
                note_lines = max(1, -(-_nf.measure(note_text) // max(1, _avail)))
            except Exception:
                note_lines = max(1, -(-len(note_text) // 55))
            note_section_h += note_lines * S(18) + S(20)
        else:
            note_section_h += S(36) + S(6)

    H = base_H + extra_optional_rows * S(46) + traits_extra + note_section_h
    c = tk.Canvas(container, width=W, height=H,
                   bg=PALETTE["lair_bg"], highlightthickness=0)
    if compact:
        c.pack(anchor="nw", padx=(20, 20), pady=18)
    else:
        c.pack(padx=20, pady=18)
    c._refs = []

    round_rect(c, S(4), S(4), W - S(4), H - S(4), r=S(28),
                fill=PALETTE["info_card_fill"], outline=PALETTE["panel_border"], width=5)

    img_x, img_y, img_w, img_h = S(16), S(16), S(100), S(100)
    round_rect(c, img_x, img_y, img_x + img_w, img_y + img_h, r=14,
                fill="#2A2143", outline="", width=0)
    try:
        custom_path = custom_dragon_image_path(name)
        icon_path = custom_path if os.path.exists(custom_path) else species_icon_path(d.get("Species", ""))
        photo = make_rounded_photo(icon_path, img_w, img_h, radius=14)
        c._refs.append(photo)
        c.create_image(img_x + img_w / 2, img_y + img_h / 2, image=photo)
    except Exception:
        c.create_text(img_x + img_w / 2, img_y + img_h / 2,
                      text="No Icon\nFound", fill="#9B8FCC",
                      font=(APP_FONT_FAMILY, F(10), APP_FONT_WEIGHT), justify="center")

    right_edge = W - S(24)
    gender = d.get("Gender", "")
    level = d.get("Level", "-")

    if compact:
        name_left = img_x + img_w + S(12)
        name_max_width = right_edge - name_left - S(4)

        gl_y = img_y + S(10)
        level_id = c.create_text(name_left, gl_y, text=f"Lv. {level}", fill=PALETTE["label_text"],
                                  font=(APP_FONT_FAMILY, F(13), APP_FONT_WEIGHT), anchor="w")
        if gender:
            icon_size = S(18)
            bbox = c.bbox(level_id)
            icon_cx = (bbox[2] + 8 + icon_size / 2) if bbox else (name_left + 50)
            try:
                gimg = Image.open(gender_icon_path(gender)).convert("RGBA")
                gimg = autocrop_to_content(gimg)
                gimg = fit_contain(gimg, icon_size, icon_size)
                gphoto = ImageTk.PhotoImage(gimg)
                c._refs.append(gphoto)
                c.create_image(icon_cx, gl_y, image=gphoto)
            except Exception:
                is_male = gender.lower() == "male"
                symbol = "\u2642" if is_male else "\u2640"
                symbol_color = "#5AA9E6" if is_male else "#E667A8"
                c.create_text(icon_cx, gl_y, text=symbol, fill=symbol_color,
                              font=(APP_FONT_FAMILY, F(14), APP_FONT_WEIGHT))

        name_size = fit_text_size(d["Nickname"], APP_FONT_FAMILY, F(20), F(11), name_max_width)
        shadowed_name_text(c, name_left, img_y + S(46), d["Nickname"],
                           (APP_FONT_FAMILY, name_size, APP_FONT_WEIGHT), anchor="w")
        c.create_text(name_left, img_y + S(72), text=d["Species"],
                      fill=PALETTE["label_text"], font=(APP_FONT_FAMILY, F(13), APP_FONT_WEIGHT), anchor="w")
        c.create_text(name_left, img_y + S(92), text=d.get("Rarity", "-"),
                      fill=RARITY_COLORS.get(d.get("Rarity", ""), RARITY_DEFAULT_COLOR),
                      font=(APP_FONT_FAMILY, F(13), APP_FONT_WEIGHT), anchor="w")
    else:
        gl_y = img_y + S(18)
        level_id = c.create_text(right_edge, gl_y, text=f"Lv. {level}", fill=PALETTE["label_text"],
                                  font=(APP_FONT_FAMILY, F(18), APP_FONT_WEIGHT), anchor="e")
        if gender:
            icon_size = S(26)
            bbox = c.bbox(level_id)
            icon_cx = (bbox[0] - 8 - icon_size / 2) if bbox else (right_edge - 70)
            try:
                gimg = Image.open(gender_icon_path(gender)).convert("RGBA")
                gimg = autocrop_to_content(gimg)
                gimg = fit_contain(gimg, icon_size, icon_size)
                gphoto = ImageTk.PhotoImage(gimg)
                c._refs.append(gphoto)
                c.create_image(icon_cx, gl_y, image=gphoto)
            except Exception:
                is_male = gender.lower() == "male"
                symbol = "\u2642" if is_male else "\u2640"
                symbol_color = "#5AA9E6" if is_male else "#E667A8"
                c.create_text(icon_cx, gl_y, text=symbol, fill=symbol_color, font=(APP_FONT_FAMILY, F(20), APP_FONT_WEIGHT))

        name_max_width = right_edge - (img_x + img_w) - 10
        name_size = fit_text_size(d["Nickname"], APP_FONT_FAMILY, F(24), F(12), name_max_width)
        shadowed_name_text(c, right_edge, img_y + S(50), d["Nickname"],
                           (APP_FONT_FAMILY, name_size, APP_FONT_WEIGHT), anchor="e")
        c.create_text(right_edge, img_y + S(80), text=d["Species"],
                      fill=PALETTE["label_text"], font=(APP_FONT_FAMILY, F(16), APP_FONT_WEIGHT), anchor="e")
        c.create_text(right_edge, img_y + S(104), text=d.get("Rarity", "-"),
                      fill=RARITY_COLORS.get(d.get("Rarity", ""), RARITY_DEFAULT_COLOR),
                      font=(APP_FONT_FAMILY, F(16), APP_FONT_WEIGHT), anchor="e")

    if d.get("Soulbound"):
        sb_size = S(32)
        sb_x = img_x + img_w - sb_size // 2 - 2
        sb_y = img_y + img_h - sb_size // 2 - 2
        sb_path = os.path.join(MISC_DIR, "soulbound.png")
        try:
            sbimg = Image.open(sb_path).convert("RGBA")
            sbimg = autocrop_to_content(sbimg)
            sbimg = fit_contain(sbimg, sb_size, sb_size)
            sbphoto = ImageTk.PhotoImage(sbimg)
            c._refs.append(sbphoto)
            c.create_image(sb_x, sb_y, image=sbphoto)
        except Exception as e:
            print(f"[soulbound] Failed to load {sb_path!r}: {e}")
            c.create_text(sb_x, sb_y, text="\u26d4", fill="#FFD700",
                          font=(APP_FONT_FAMILY, F(18), APP_FONT_WEIGHT))

    def handle_edit():
        def after_save():
            if refresh_grid:
                refresh_grid()
            show_details(parent, container, name, refresh_grid, active_tab)

        open_dragon_form(parent, after_save, dragon_id=name)

    def handle_delete():
        if messagebox.askyesno("Delete dragon", f"Delete {d['Nickname']}? This can't be undone."):
            dragons.pop(name, None)
            persist()
            for w in container.winfo_children():
                w.destroy()
            tk.Label(container, text="Select a dragon from the list",
                     fg=PALETTE["label_text"], bg=PALETTE["lair_bg"],
                     font=(APP_FONT_FAMILY, 12, APP_FONT_WEIGHT)).pack(pady=40)
            if refresh_grid:
                refresh_grid()

    def handle_add_to_collection():
        if not current_tabs:
            messagebox.showinfo("No tabs yet",
                                "Create a tab first using '+ New Tab' in the tab bar.")
            return
        dlg = tk.Toplevel(parent)
        dlg.title("Add to Collection")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 300, min(60 + len(current_tabs) * 50, 400))
        tk.Label(dlg, text=f'Add "{d["Nickname"]}" to:',
                 fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                 font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(16, 8))
        for tab_id, tab in current_tabs.items():
            already_in = name in tab.get("members", [])
            label = f'✓ {tab["name"]}' if already_in else tab["name"]
            color = PALETTE["bar_fill"] if already_in else PALETTE["card_fill"]
            def make_click(tid=tab_id, ain=already_in):
                def click():
                    if ain:
                        remove_dragon_from_tab(tid, name)
                    else:
                        add_dragon_to_tab(tid, name)
                    if refresh_grid:
                        refresh_grid()
                    dlg.destroy()
                return click
            tk.Button(dlg, text=label, command=make_click(),
                       bg=color, fg="white", relief="flat",
                       font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT),
                       width=24).pack(pady=4)

    def handle_move_to_account():
        other_accounts = [a for a in all_accounts_data.keys() if a != current_account]
        if not other_accounts:
            messagebox.showinfo("No other accounts",
                                "Create another account first from the Account Select screen.")
            return
        dlg = tk.Toplevel(parent)
        dlg.title("Move to Account")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 300, min(60 + len(other_accounts) * 46, 420))
        tk.Label(dlg, text=f'Move "{d["Nickname"]}" to:',
                 fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                 font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(16, 8))

        def make_click(dest=None):
            def click():
                if messagebox.askyesno("Confirm move",
                                        f'Move "{d["Nickname"]}" to "{dest}"?\n'
                                        f"It will be removed from this account.",
                                        parent=dlg):
                    move_dragon_to_account(name, dest)
                    dlg.destroy()
                    for w in container.winfo_children():
                        w.destroy()
                    tk.Label(container, text="Select a dragon from the list",
                             fg=PALETTE["label_text"], bg=PALETTE["lair_bg"],
                             font=(APP_FONT_FAMILY, 12, APP_FONT_WEIGHT)).pack(pady=40)
                    if refresh_grid:
                        refresh_grid()
            return click

        for acc in other_accounts:
            tk.Button(dlg, text=acc, command=make_click(acc),
                       bg=PALETTE["card_fill"], fg="white", relief="flat",
                       font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT),
                       width=24).pack(pady=4)

    def handle_note():
        current_note = d.get("Note", "")
        dlg = tk.Toplevel(parent)
        dlg.title(f"Note — {d['Nickname']}")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 460, 320)
        tk.Label(dlg, text="Note (max 1000 characters)", fg=PALETTE["label_text"],
                 bg=PALETTE["bg_outer"], font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(
            anchor="w", padx=14, pady=(14, 4))
        txt = tk.Text(dlg, width=50, height=10, bg=PALETTE["tag_fill"], fg="white",
                       insertbackground="white", relief="flat", wrap="word",
                       font=(APP_FONT_FAMILY, 10), highlightthickness=1,
                       highlightbackground=PALETTE["panel_border"])
        txt.pack(fill="both", expand=True, padx=14, pady=(0, 4))
        txt.insert("1.0", current_note)
        counter_var = tk.StringVar(value=f"{len(current_note)}/1000")
        tk.Label(dlg, textvariable=counter_var, fg=PALETTE["label_text"],
                 bg=PALETTE["bg_outer"], font=(APP_FONT_FAMILY, 8, APP_FONT_WEIGHT),
                 anchor="e").pack(fill="x", padx=14)

        def on_key(_e=None):
            content = txt.get("1.0", "end-1c")
            if len(content) > 1000:
                txt.delete(f"1.0+{1000}c", "end")
                content = content[:1000]
            counter_var.set(f"{len(content)}/1000")

        txt.bind("<KeyRelease>", on_key)

        def save_note():
            d["Note"] = txt.get("1.0", "end-1c").strip()
            dragons[name] = d
            persist()
            dlg.destroy()

        btn_row = tk.Frame(dlg, bg=PALETTE["bg_outer"])
        btn_row.pack(pady=10)
        tk.Button(btn_row, text="Save Note", command=save_note,
                   bg=PALETTE["bar_fill"], fg="#16330F", relief="flat",
                   font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), padx=16, pady=6).pack(side="left", padx=6)
        tk.Button(btn_row, text="Cancel", command=dlg.destroy,
                   bg=PALETTE["tag_fill"], fg="white", relief="flat",
                   font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), padx=16, pady=6).pack(side="left", padx=6)
        txt.focus_set()

    def handle_duplicate():
        new_id = uuid.uuid4().hex[:10]
        new_d = copy.deepcopy(d)
        nick = new_d.get("Nickname", "Dragon")
        new_d["Nickname"] = nick + " (Copy)" if len(nick) <= 13 else nick[:13] + " (Cp)"
        dragons[new_id] = new_d
        persist()
        if refresh_grid:
            refresh_grid()
        show_details(parent, container, new_id, refresh_grid, active_tab)

    title_stack_bottom = img_y + S(92) + S(10) if compact else img_y + S(104) + S(10)
    btn_font = (APP_FONT_FAMILY, F(11), APP_FONT_WEIGHT)

    if compact:
        action_y0, action_h = title_stack_bottom, 0
        menu_btn_w = S(90)
        menu_btn_h = S(28)
        menu_x0 = right_edge - menu_btn_w
        menu_y0 = img_y

        def open_action_menu():
            menu = tk.Menu(c, tearoff=0, bg=PALETTE["card_fill"], fg="white",
                            activebackground=PALETTE["tag_fill"], activeforeground="white",
                            font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT))
            menu.add_command(label="+ Collection", command=handle_add_to_collection)
            menu.add_command(label="Move", command=handle_move_to_account)
            menu.add_command(label="Dupe", command=handle_duplicate)
            menu.add_command(label="Edit Dragon", command=handle_edit)
            menu.add_separator()
            menu.add_command(label="Delete", command=handle_delete)
            try:
                x = c.winfo_rootx() + menu_x0
                y = c.winfo_rooty() + menu_y0 + menu_btn_h
                menu.tk_popup(int(x), int(y))
            finally:
                menu.grab_release()

        rounded_button(c, menu_x0, menu_y0, menu_btn_w, menu_btn_h, "\u2630 Edit",
                        open_action_menu, r=10,
                        fill=PALETTE["card_fill"], outline=PALETTE["card_border"], font=btn_font)
    else:
        action_y0, action_h = max(img_y + img_h, title_stack_bottom) + S(10), S(30)
        btn_w, btn_gap = S(72), S(6)
        delete_x0 = W - S(20) - btn_w
        edit_x0 = delete_x0 - btn_gap - btn_w
        dup_x0 = edit_x0 - btn_gap - btn_w
        move_x0 = dup_x0 - btn_gap - btn_w
        coll_x0 = move_x0 - btn_gap - S(96)
        rounded_button(c, coll_x0, action_y0, S(96), action_h, "+ Collection",
                        handle_add_to_collection, r=10,
                        fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"], font=btn_font)
        rounded_button(c, move_x0, action_y0, btn_w, action_h, "Move",
                        handle_move_to_account, r=10,
                        fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"], font=btn_font)
        rounded_button(c, dup_x0, action_y0, btn_w, action_h, "Dupe",
                        handle_duplicate, r=10,
                        fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"], font=btn_font)
        rounded_button(c, edit_x0, action_y0, btn_w, action_h, "Edit", handle_edit, r=10,
                        fill=PALETTE["card_fill"], outline=PALETTE["card_border"], font=btn_font)
        rounded_button(c, delete_x0, action_y0, btn_w, action_h, "Delete", handle_delete, r=10,
                        fill="#7A2020", outline="#4A1010", font=btn_font)

    rx, rw = S(20), W - S(40)
    header_y0 = action_y0 + action_h + S(14)
    header_y1 = header_y0 + S(44)

    round_rect(c, rx, header_y0, rx + rw, header_y1, r=14,
                fill=PALETTE["header_band"], outline=PALETTE["header_band_border"], width=2)
    outline_text(c, rx + S(24), (header_y0 + header_y1) / 2, "Appearance",
                 (APP_FONT_FAMILY, F(16), APP_FONT_WEIGHT), "#FFD24C", "#5C3A12", anchor="w")

    row_h, row_gap = S(40), S(6)
    element = d.get("Element", "Ice")
    row_defs = [
        ("coat", "Primary Coat", "P", None),
        ("coat", "Secondary Coat", "S", None),
        ("coat", "Tertiary Coat", "T", None),
        ("icon", "Mutations", None,
         f"{d.get('Mutations', 0)}/{d.get('MaxMutations', 0)}"),
        ("icon", "Age", None, d.get("Age", "-")),
        ("icon", "Cosmetic Trait", d.get("CosmeticTrait", "None"), d.get("CosmeticTrait", "None")),
        ("icon", "Element", element, element),
        ("icon", "Pupil", element, d.get("Pupil", "-")),
        ("plain", "Generation", None, d.get("Generation", "-")),
    ]
    if d.get("Rebirths", 0):
        row_defs.append(("plain", "Rebirths", None, str(d["Rebirths"])))

    element2 = d.get("Element2")
    if element2:
        row_defs.insert(row_defs.index(("icon", "Pupil", element, d.get("Pupil", "-"))),
                         ("icon", "Element 2", element2, element2))

    if d.get("Birthday"):
        try:
            bdt = date.fromisoformat(d["Birthday"])
            bday_text = f"{MONTH_NAMES[bdt.month - 1]} {bdt.day}, {bdt.year}"
        except Exception:
            bday_text = d["Birthday"]
        row_defs.append(("plain", "Birthday", None, bday_text))

    if d.get("OriginalOwner"):
        row_defs.append(("plain", "Original Owner", None, d["OriginalOwner"]))

    ry = header_y1 + S(8)
    for kind, label, icon, value in row_defs:
        draw_appearance_row_bg(c, rx, ry, rw, row_h)
        rcy = ry + row_h / 2

        if kind == "coat":
            slot = icon
            color_name = d.get("Colors", {}).get(slot, "-")
            material = d.get("Materials", {}).get(slot, "-")
            color_hex = get_color_hex(color_name, element)
            pill_font = (APP_FONT_FAMILY, F(11), APP_FONT_WEIGHT)

            if compact:
                short_label = {"P": "P. Col:", "S": "S. Col:", "T": "T. Col:"}.get(slot, label)
                c.create_text(rx + S(16), rcy, text=short_label, fill=PALETTE["label_text"],
                              font=(APP_FONT_FAMILY, F(13), APP_FONT_WEIGHT), anchor="w")
                sq_w = S(40)
                sq_h = S(22)
                sq_x = rx + S(78)
                sq_r = min(6, sq_h / 3)
                if color_name == "Legendary":
                    if not draw_legendary_pill(c, sq_x, rcy - sq_h / 2, sq_w, sq_h, element, text="", radius=int(sq_r)):
                        round_rect(c, sq_x, rcy - sq_h / 2, sq_x + sq_w, rcy + sq_h / 2, r=sq_r,
                                    fill=color_hex, outline="#1C1430", width=2)
                else:
                    round_rect(c, sq_x, rcy - sq_h / 2, sq_x + sq_w, rcy + sq_h / 2, r=sq_r,
                                fill=color_hex, outline="#1C1430", width=2)

                try:
                    _mf = tkfont.Font(family=APP_FONT_FAMILY, size=F(11))
                    mat_pill_w = min(S(85), max(S(40), _mf.measure(material) + S(22)))
                except Exception:
                    mat_pill_w = S(70)
                mat_pill_h = S(24)
                mat_x = sq_x + sq_w + S(16)
                draw_pill(c, mat_x, rcy - mat_pill_h / 2, mat_pill_w, mat_pill_h, material, "#FFFFFF",
                          text_fill="#2F7FBF", text_outline="#BFE0F5", font=pill_font, radius=8)
            else:
                c.create_text(rx + S(20), rcy, text=label, fill=PALETTE["label_text"],
                              font=(APP_FONT_FAMILY, F(14), APP_FONT_WEIGHT), anchor="w")
                text_fill = readable_text_color(color_hex)
                text_outline = "#000000" if text_fill == "#FFFFFF" else "#FFFFFF"
                pill_w, pill_h, pill_gap = S(110), S(28), S(8)
                p2x = rx + rw - S(18) - pill_w
                p1x = p2x - pill_gap - pill_w
                p1y = rcy - pill_h / 2
                if color_name == "Legendary":
                    if not draw_legendary_pill(c, p1x, p1y, pill_w, pill_h, element, font=pill_font, radius=10):
                        draw_pill(c, p1x, p1y, pill_w, pill_h, color_name, color_hex,
                                  text_fill=text_fill, text_outline=text_outline, font=pill_font, radius=10)
                else:
                    draw_pill(c, p1x, p1y, pill_w, pill_h, color_name, color_hex,
                              text_fill=text_fill, text_outline=text_outline, font=pill_font, radius=10)
                draw_pill(c, p2x, rcy - pill_h / 2, pill_w, pill_h, material, "#FFFFFF",
                          text_fill="#2F7FBF", text_outline="#BFE0F5", font=pill_font, radius=10)
        elif kind == "plain":
            c.create_text(rx + S(20), rcy, text=label, fill=PALETTE["label_text"],
                          font=(APP_FONT_FAMILY, F(14), APP_FONT_WEIGHT), anchor="w")
            if compact:
                try:
                    _lf = tkfont.Font(family=APP_FONT_FAMILY, size=F(14), weight="bold")
                    label_w = _lf.measure(label)
                except Exception:
                    label_w = S(90)
                outline_text(c, rx + S(28) + label_w, rcy, str(value), (APP_FONT_FAMILY, F(13), APP_FONT_WEIGHT),
                             PALETTE["value_text"], PALETTE["value_outline"], anchor="w")
            else:
                outline_text(c, rx + rw - S(18), rcy, str(value), (APP_FONT_FAMILY, F(15), APP_FONT_WEIGHT),
                             PALETTE["value_text"], PALETTE["value_outline"], anchor="e")
        else:
            draw_row_icon(c, rx + S(18), rcy, label, icon)
            if compact:
                outline_text(c, rx + S(44), rcy, str(value), (APP_FONT_FAMILY, F(13), APP_FONT_WEIGHT),
                             PALETTE["value_text"], PALETTE["value_outline"], anchor="w")
            else:
                c.create_text(rx + S(44), rcy, text=label, fill=PALETTE["label_text"],
                              font=(APP_FONT_FAMILY, F(14), APP_FONT_WEIGHT), anchor="w")
                outline_text(c, rx + rw - S(18), rcy, str(value), (APP_FONT_FAMILY, F(15), APP_FONT_WEIGHT),
                             PALETTE["value_text"], PALETTE["value_outline"], anchor="e")

        ry += row_h + row_gap

    note_header_y0 = ry + S(14)
    note_header_y1 = note_header_y0 + S(44)

    def toggle_note():
        note_expanded[name] = not note_expanded.get(name, False)
        show_details(parent, container, name, refresh_grid, active_tab)

    note_hdr_id = round_rect(c, rx, note_header_y0, rx + rw, note_header_y1, r=14,
                               fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"], width=2)
    note_arrow_id = c.create_text(rx + S(22), (note_header_y0 + note_header_y1) / 2,
                                   text=("\u25BC" if is_note_expanded else "\u25B6"),
                                   fill=PALETTE["label_text"],
                                   font=(APP_FONT_FAMILY, F(13), APP_FONT_WEIGHT))
    outline_text(c, rx + S(50), (note_header_y0 + note_header_y1) / 2, "Note",
                 (APP_FONT_FAMILY, F(16), APP_FONT_WEIGHT),
                 PALETTE["title_fill"], PALETTE["title_outline"], anchor="w")

    note_btn_label = "Edit Note" if has_note else "Add Note"
    note_btn_x = rx + rw - S(94)
    note_btn_y0 = note_header_y0 + S(8)
    note_btn_id = round_rect(c, note_btn_x, note_btn_y0, note_btn_x + S(84), note_btn_y0 + S(28),
                              r=8, fill=PALETTE["card_fill"], outline=PALETTE["panel_border"], width=1)
    note_btn_lbl_id = c.create_text(note_btn_x + S(42), note_btn_y0 + S(14), text=note_btn_label,
                                     fill="white", font=(APP_FONT_FAMILY, F(9), APP_FONT_WEIGHT))

    for item in (note_hdr_id, note_arrow_id):
        c.tag_bind(item, "<Button-1>", lambda _e: toggle_note())
    for item in (note_btn_id, note_btn_lbl_id):
        c.tag_bind(item, "<Button-1>", lambda _e: handle_note())

    if is_note_expanded:
        note_body_y = note_header_y1 + S(6)
        if has_note:
            note_text = d["Note"].strip()
            try:
                _nf = tkfont.Font(family=APP_FONT_FAMILY, size=10)
                _avail = rw - 32
                note_lines = max(1, -(-_nf.measure(note_text) // max(1, _avail)))
            except Exception:
                note_lines = max(1, -(-len(note_text) // 55))
            note_body_h = note_lines * S(18) + S(20)
            draw_appearance_row_bg(c, rx, note_body_y, rw, note_body_h)
            c.create_text(rx + S(16), note_body_y + S(10), text=note_text,
                           fill=PALETTE["value_text"],
                           font=(APP_FONT_FAMILY, F(10)), anchor="nw",
                           width=rw - S(32), justify="left")
            ry = note_body_y + note_body_h + S(6)
        else:
            draw_appearance_row_bg(c, rx, note_body_y, rw, S(36))
            c.create_text(rx + S(16), note_body_y + S(18), text="No note added yet. Click \"Add Note\" to write one.",
                           fill=PALETTE["label_text"], font=(APP_FONT_FAMILY, F(9)),
                           anchor="w")
            ry = note_body_y + S(36) + S(6)
    else:
        ry = note_header_y1 + S(6)

    traits_header_y0 = ry + S(14)
    traits_header_y1 = traits_header_y0 + S(44)

    def toggle_traits():
        genetic_traits_expanded[name] = not genetic_traits_expanded.get(name, False)
        show_details(parent, container, name, refresh_grid, active_tab)

    traits_header_id = round_rect(c, rx, traits_header_y0, rx + rw, traits_header_y1, r=14,
                                   fill=PALETTE["header_band"], outline=PALETTE["header_band_border"], width=2)
    arrow_id = c.create_text(rx + S(22), (traits_header_y0 + traits_header_y1) / 2,
                              text=("\u25BC" if is_traits_expanded else "\u25B6"),
                              fill="#F2A93B", font=(APP_FONT_FAMILY, F(13), APP_FONT_WEIGHT))
    outline_text(c, rx + S(50), (traits_header_y0 + traits_header_y1) / 2, "Genetic Traits",
                 (APP_FONT_FAMILY, F(16), APP_FONT_WEIGHT), "#FFD24C", "#5C3A12", anchor="w")
    for clickable in (traits_header_id, arrow_id):
        c.tag_bind(clickable, "<Button-1>", lambda _e: toggle_traits())

    if is_traits_expanded:
        positive_traits = d.get("PositiveTraits", [])
        negative_traits = d.get("NegativeTraits", [])

        if compact:
            all_traits = [(t.get("Trait", "-"), t.get("Tier", 1), "#52C724") for t in positive_traits if t.get("Trait")]
            all_traits += [(t.get("Trait", "-"), t.get("Tier", 1), "#FF4D4D") for t in negative_traits if t.get("Trait")]

            trait_font = (APP_FONT_FAMILY, F(10), APP_FONT_WEIGHT)
            try:
                _tf = tkfont.Font(family=APP_FONT_FAMILY, size=F(10), weight="bold")
                longest = max((_tf.measure(name) for name, _, _ in all_traits), default=S(80))
            except Exception:
                longest = S(80)
            pill_w = longest + S(46)
            pill_h = S(30)
            pill_gap = S(8)

            tx, ty = rx, traits_header_y1 + S(10)
            if not all_traits:
                c.create_text(rx + rw / 2, ty + S(10), text="No genetic traits yet",
                              fill=PALETTE["label_text"], font=(APP_FONT_FAMILY, F(10), "italic"))
            for name, tier, accent in all_traits:
                if tx + pill_w > rx + rw and tx > rx:
                    tx = rx
                    ty += pill_h + pill_gap
                round_rect(c, tx, ty, tx + pill_w, ty + pill_h, r=pill_h / 2,
                            fill=PALETTE["row_fill"], outline=accent, width=2)
                badge_cx, badge_r = tx + S(16), S(10)
                c.create_oval(badge_cx - badge_r, ty + pill_h / 2 - badge_r,
                              badge_cx + badge_r, ty + pill_h / 2 + badge_r,
                              fill=PALETTE["tag_fill"], outline=accent, width=2)
                c.create_text(badge_cx, ty + pill_h / 2, text=str(tier), fill="white",
                              font=(APP_FONT_FAMILY, F(9), APP_FONT_WEIGHT))
                c.create_text(tx + S(30), ty + pill_h / 2, text=name, fill=PALETTE["value_text"],
                              font=trait_font, anchor="w")
                tx += pill_w + pill_gap
        else:
            col_gap = S(12)
            col_w = (rw - col_gap) / 2
            pos_x0, neg_x0 = rx, rx + col_w + col_gap
            cols_y0 = traits_header_y1 + S(10)

            c.create_text(pos_x0 + col_w / 2, cols_y0 + S(12), text="Positive",
                          fill="#7CFC6E", font=(APP_FONT_FAMILY, F(14), APP_FONT_WEIGHT))
            c.create_text(neg_x0 + col_w / 2, cols_y0 + S(12), text="Negative",
                          fill="#FF6B6B", font=(APP_FONT_FAMILY, F(14), APP_FONT_WEIGHT))

            trait_row_h, trait_row_gap = S(40), S(6)
            trait_rows_y0 = cols_y0 + S(28)

            for i in range(MAX_POSITIVE_TRAITS):
                entry = positive_traits[i] if i < len(positive_traits) else None
                row_y = trait_rows_y0 + i * (trait_row_h + trait_row_gap)
                draw_trait_row(c, pos_x0, row_y, col_w, trait_row_h, entry, "#52C724")

            for i in range(MAX_NEGATIVE_TRAITS):
                entry = negative_traits[i] if i < len(negative_traits) else None
                row_y = trait_rows_y0 + i * (trait_row_h + trait_row_gap)
                draw_trait_row(c, neg_x0, row_y, col_w, trait_row_h, entry, "#FF4D4D")


def make_dragon_card(parent, name, d, on_click):
    w, h = 150, 190
    c = tk.Canvas(parent, width=w, height=h, bg=PALETTE["lair_bg"], highlightthickness=0)
    rect_id = round_rect(c, 5, 5, w - 5, h - 5, r=18,
                          fill=PALETTE["card_fill"], outline=PALETTE["card_border"], width=3)
    c._refs = []

    try:
        custom_path = custom_dragon_image_path(name)
        icon_path = custom_path if os.path.exists(custom_path) else species_icon_path(d.get("Species", ""))
        photo = make_rounded_photo(icon_path, 100, 100, radius=14)
        c._refs.append(photo)
        c.create_image(w / 2, 70, image=photo)
    except Exception:
        round_rect(c, w / 2 - 45, 25, w / 2 + 45, 115, r=12,
                    fill=RARITY_COLORS.get(d["Rarity"], "#888888"))
        c.create_text(w / 2, 70, text=name, fill="white",
                      font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), width=80, justify="center")

    if d.get("Note", "").strip():
        c.create_oval(w - 22, 10, w - 10, 22, fill=PALETTE["badge_fill"],
                       outline=PALETTE["badge_border"], width=1)
        c.create_text(w - 16, 16, text="\u270f", fill="#3A2A06",
                       font=(APP_FONT_FAMILY, 7, APP_FONT_WEIGHT))

    colors = d.get("Colors", {})
    block_w, block_h, block_gap = 36, 8, 3
    total_w = 3 * block_w + 2 * block_gap
    bx = (w - total_w) // 2
    by = 123
    for slot in ("P", "S", "T"):
        color_name = colors.get(slot, "-")
        hex_color = get_color_hex(color_name, d.get("Element", ""))
        round_rect(c, bx, by, bx + block_w, by + block_h, r=3, fill=hex_color, outline="", width=0)
        bx += block_w + block_gap

    card_name_size = fit_text_size(d["Nickname"], APP_FONT_FAMILY, 12, 7, w - 16)
    shadowed_name_text(c, w / 2, 142, d["Nickname"], (APP_FONT_FAMILY, card_name_size, APP_FONT_WEIGHT))
    c.create_text(w / 2, 162, text=d.get("Species", "-"),
                  fill=PALETTE["label_text"], font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT))

    def handler(_event):
        on_click(name)

    def on_enter(_event):
        c.itemconfig(rect_id, fill=lighten(PALETTE["card_fill"]))

    def on_leave(_event):
        c.itemconfig(rect_id, fill=PALETTE["card_fill"])

    c.bind("<Button-1>", handler)
    c.bind("<Enter>", on_enter)
    c.bind("<Leave>", on_leave)
    return c


def open_sda_tracker(parent_win):
    owned_species = set()
    best_mutations = {}
    for d in dragons.values():
        sp = d.get("Species", "")
        if sp:
            owned_species.add(sp)
            mut = int(d.get("Mutations", 0))
            best_mutations[sp] = max(best_mutations.get(sp, 0), mut)

    def badge_color(sp):
        mut = best_mutations.get(sp, 0)
        if mut >= 5:
            return "#52C724"
        if mut >= 1:
            return "#FFB300"
        return "#8B1A1A"

    total = sum(1 for s in SPECIES_LIST if s not in SDA_EXCLUDED)
    owned_count = sum(1 for s in SPECIES_LIST if s in owned_species and s not in SDA_EXCLUDED)
    sda_count = sum(1 for s in SPECIES_LIST
                    if best_mutations.get(s, 0) >= 5 and s not in SDA_EXCLUDED)

    owned_color = "#52C724"
    sda_header_color = "#FFB300"

    win = tk.Toplevel(parent_win)
    win.title("Supreme Dragon Adventurer Tracker")
    win.configure(bg=PALETTE["bg_outer"])
    center(win, 980, 760)
    win.minsize(600, 400)

    header_frame = tk.Frame(win, bg=PALETTE["panel_fill"])
    header_frame.pack(fill="x")

    header_canvas = tk.Canvas(header_frame, bg=PALETTE["panel_fill"], highlightthickness=0, height=100)
    header_canvas.pack(fill="x")

    def redraw_header(event=None):
        w = header_canvas.winfo_width() or 980
        header_canvas.delete("all")
        outline_text(header_canvas, w // 2, 26, "Supreme Dragon Adventurer Tracker",
                     (APP_FONT_FAMILY, 18, APP_FONT_WEIGHT), PALETTE["title_fill"], PALETTE["title_outline"])
        header_canvas.create_text(w // 4, 66,
                                   text=f"Owned:  {owned_count} / {total}",
                                   fill=owned_color, font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT))
        header_canvas.create_text(w * 3 // 4, 66,
                                   text=f"SDA-Ready (5/5):  {sda_count} / {total}",
                                   fill=sda_header_color, font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT))

    header_canvas.bind("<Configure>", lambda e: redraw_header())

    body_outer = tk.Frame(win, bg=PALETTE["bg_outer"])
    body_outer.pack(fill="both", expand=True)

    scroll_canvas = tk.Canvas(body_outer, bg=PALETTE["bg_outer"], highlightthickness=0)
    scroll_canvas.pack(side="left", fill="both", expand=True)
    vscroll = tk.Scrollbar(body_outer, command=scroll_canvas.yview)
    vscroll.pack(side="right", fill="y")
    scroll_canvas.configure(yscrollcommand=vscroll.set)
    bind_mousewheel(scroll_canvas)

    grid_frame = tk.Frame(scroll_canvas, bg=PALETTE["bg_outer"])
    win_id = scroll_canvas.create_window((0, 0), window=grid_frame, anchor="nw")

    icon_cache = _sda_icon_cache

    def build_grid(available_width):
        for w in grid_frame.winfo_children():
            w.destroy()

        PAD = 8
        MIN_CELL_W = 200
        cols = max(2, available_width // (MIN_CELL_W + PAD))
        cell_w = (available_width - PAD * (cols + 1)) // cols
        icon_s = max(44, min(80, cell_w // 3))
        cell_h = icon_s + 24
        name_font_size = max(9, min(13, cell_w // 18))
        badge_font_size = max(7, name_font_size - 2)

        visible_species = [s for s in SPECIES_LIST if s not in SDA_EXCLUDED]
        for idx, species in enumerate(visible_species):
            row_i = idx // cols
            col_i = idx % cols

            is_owned = species in owned_species
            sp_mut = best_mutations.get(species, 0)

            icon_species = species

            cell = tk.Canvas(grid_frame, width=cell_w, height=cell_h,
                              bg=PALETTE["panel_fill"], highlightthickness=0)
            cell.grid(row=row_i, column=col_i, padx=PAD // 2, pady=PAD // 2)
            round_rect(cell, 2, 2, cell_w - 2, cell_h - 2, r=10,
                        fill=PALETTE["row_fill"], outline=PALETTE["panel_border"], width=1)

            icon_cx = icon_s // 2 + 8
            icon_cy = cell_h // 2

            cache_key = (icon_species, icon_s)
            if cache_key not in icon_cache:
                try:
                    icon_cache[cache_key] = make_rounded_photo(
                        species_icon_path(icon_species), icon_s, icon_s, radius=8)
                except Exception:
                    icon_cache[cache_key] = None

            photo = icon_cache[cache_key]
            if photo:
                cell._ref = photo
                cell.create_image(icon_cx, icon_cy, image=photo)
            else:
                cell.create_rectangle(8, (cell_h - icon_s) // 2, 8 + icon_s,
                                       (cell_h + icon_s) // 2,
                                       fill=PALETTE["tag_fill"], outline="")

            text_x = icon_s + 16
            text_w = cell_w - text_x - 8
            name_color = "#3EBF2F" if is_owned else "#8B1A1A"

            show_badge = sp_mut is not None
            fitted_size = fit_text_size(species, APP_FONT_FAMILY,
                                        name_font_size + 3, 8, text_w)
            text_y = icon_cy - (10 if show_badge else 0)
            cell.create_text(text_x + text_w // 2, text_y, text=species, fill=name_color,
                              font=(APP_FONT_FAMILY, fitted_size, APP_FONT_WEIGHT),
                              width=text_w, justify="center", anchor="center")

            if show_badge:
                bc = badge_color(species)
                bw, bh = 38, 17
                bx = text_x + (text_w - bw) // 2
                by = icon_cy + 10
                round_rect(cell, bx, by, bx + bw, by + bh, r=5,
                            fill=PALETTE["tag_fill"], outline=bc, width=1)
                cell.create_text(bx + bw // 2, by + bh // 2,
                                  text=f"{sp_mut}/5",
                                  fill=bc, font=(APP_FONT_FAMILY, badge_font_size, APP_FONT_WEIGHT))

        grid_frame.update_idletasks()
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    last_width = {"w": 0}

    def on_canvas_resize(event):
        w = event.width
        scroll_canvas.itemconfig(win_id, width=w)
        if abs(w - last_width["w"]) > 4:
            last_width["w"] = w
            build_grid(w)

    scroll_canvas.bind("<Configure>", on_canvas_resize)

    win.update_idletasks()
    build_grid(scroll_canvas.winfo_width() or 960)


AGE_QUICK_MAP = {
    "B": "Baby", "J": "Juvenile", "A": "Adult", "E": "Elder",
    "baby": "Baby", "juvenile": "Juvenile", "adult": "Adult", "elder": "Elder",
}


def potion_icon_path(potion_name):
    import re as _re
    fname = _re.sub(r'[\\/:*?"<>|]', '', potion_name).lower().replace(' ', '_') + ".png"
    return os.path.join(POTION_ICON_DIR, fname)


_elemental_icon_cache = {}


def open_elemental_tracker(parent_win):
    checked = account_settings.setdefault("ElementalChecked", {})

    def save_checked():
        save_account_settings(current_account, account_settings)

    total = len(ELEMENTAL_POTIONS)

    win = tk.Toplevel(parent_win)
    win.title("Elemental Tracker")
    win.configure(bg=PALETTE["bg_outer"])
    center(win, 980, 760)
    win.minsize(600, 400)

    header_frame = tk.Frame(win, bg=PALETTE["panel_fill"])
    header_frame.pack(fill="x")

    header_canvas = tk.Canvas(header_frame, bg=PALETTE["panel_fill"], highlightthickness=0, height=100)
    header_canvas.pack(fill="x")

    def redraw_header(event=None):
        w = header_canvas.winfo_width() or 980
        header_canvas.delete("all")
        outline_text(header_canvas, w // 2, 26, "Elemental Tracker",
                     (APP_FONT_FAMILY, 18, APP_FONT_WEIGHT), PALETTE["title_fill"], PALETTE["title_outline"])
        got = sum(1 for p in ELEMENTAL_POTIONS if checked.get(p))
        header_canvas.create_text(w // 2, 66,
                                   text=f"Collected:  {got} / {total}",
                                   fill="#52C724", font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT))

    header_canvas.bind("<Configure>", lambda e: redraw_header())

    body_outer = tk.Frame(win, bg=PALETTE["bg_outer"])
    body_outer.pack(fill="both", expand=True)

    scroll_canvas = tk.Canvas(body_outer, bg=PALETTE["bg_outer"], highlightthickness=0)
    scroll_canvas.pack(side="left", fill="both", expand=True)
    vscroll = tk.Scrollbar(body_outer, command=scroll_canvas.yview)
    vscroll.pack(side="right", fill="y")
    scroll_canvas.configure(yscrollcommand=vscroll.set)
    bind_mousewheel(scroll_canvas)

    grid_frame = tk.Frame(scroll_canvas, bg=PALETTE["bg_outer"])
    win_id = scroll_canvas.create_window((0, 0), window=grid_frame, anchor="nw")

    icon_cache = _elemental_icon_cache

    if not ELEMENTAL_POTIONS:
        tk.Label(grid_frame, text="No elemental potions loaded yet —\ncheck your internet connection and relaunch.",
                 fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                 font=(APP_FONT_FAMILY, 12, APP_FONT_WEIGHT), justify="center").pack(pady=60)

    def build_grid(available_width):
        for w in grid_frame.winfo_children():
            w.destroy()
        if not ELEMENTAL_POTIONS:
            return

        PAD = 8
        MIN_CELL_W = 200
        cols = max(2, available_width // (MIN_CELL_W + PAD))
        cell_w = (available_width - PAD * (cols + 1)) // cols
        icon_s = max(44, min(80, cell_w // 3))
        cell_h = icon_s + 24
        name_font_size = max(9, min(13, cell_w // 18))

        def make_toggle(potion):
            def _toggle(_e=None):
                checked[potion] = not checked.get(potion, False)
                save_checked()
                redraw_header()
                build_grid(available_width)
            return _toggle

        for idx, potion in enumerate(ELEMENTAL_POTIONS):
            row_i = idx // cols
            col_i = idx % cols
            is_checked = checked.get(potion, False)

            cell = tk.Canvas(grid_frame, width=cell_w, height=cell_h,
                              bg=PALETTE["panel_fill"], highlightthickness=0, cursor="hand2")
            cell.grid(row=row_i, column=col_i, padx=PAD // 2, pady=PAD // 2)
            border_color = "#52C724" if is_checked else PALETTE["panel_border"]
            round_rect(cell, 2, 2, cell_w - 2, cell_h - 2, r=10,
                        fill=PALETTE["row_fill"], outline=border_color, width=2)

            icon_cx = icon_s // 2 + 8
            icon_cy = cell_h // 2

            cache_key = (potion, icon_s)
            if cache_key not in icon_cache:
                try:
                    icon_cache[cache_key] = make_contained_photo(
                        potion_icon_path(potion), icon_s, icon_s)
                except Exception:
                    icon_cache[cache_key] = None

            photo = icon_cache[cache_key]
            if photo:
                cell._ref = photo
                cell.create_image(icon_cx, icon_cy, image=photo)
            else:
                cell.create_rectangle(8, (cell_h - icon_s) // 2, 8 + icon_s,
                                       (cell_h + icon_s) // 2,
                                       fill=PALETTE["tag_fill"], outline="")

            text_x = icon_s + 16
            text_w = cell_w - text_x - 28
            name_color = "#52C724" if is_checked else PALETTE["label_text"]
            fitted_size = fit_text_size(potion, APP_FONT_FAMILY,
                                        name_font_size + 3, 8, text_w)
            cell.create_text(text_x + text_w // 2, icon_cy, text=potion, fill=name_color,
                              font=(APP_FONT_FAMILY, fitted_size, APP_FONT_WEIGHT),
                              width=text_w, justify="center", anchor="center")

            check_x, check_y, check_s = cell_w - 24, 8, 16
            round_rect(cell, check_x, check_y, check_x + check_s, check_y + check_s, r=4,
                        fill=("#52C724" if is_checked else PALETTE["tag_fill"]),
                        outline=PALETTE["panel_border"], width=2)
            if is_checked:
                cell.create_text(check_x + check_s // 2, check_y + check_s // 2, text="\u2714",
                                  fill="white", font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT))

            cell.bind("<Button-1>", make_toggle(potion))

        grid_frame.update_idletasks()
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    last_width = {"w": 0}

    def on_canvas_resize(event):
        w = event.width
        scroll_canvas.itemconfig(win_id, width=w)
        if abs(w - last_width["w"]) > 4:
            last_width["w"] = w
            build_grid(w)

    scroll_canvas.bind("<Configure>", on_canvas_resize)

    win.update_idletasks()
    build_grid(scroll_canvas.winfo_width() or 960)
    redraw_header()



_QUICK_TRAIT_MAPS = None


def get_quick_trait_maps():
    global _QUICK_TRAIT_MAPS
    if _QUICK_TRAIT_MAPS is None:
        import re as _re
        pos_map = {}
        neg_map = {}
        for trait in POSITIVE_TRAIT_LIST:
            if trait == "None":
                continue
            abbrev = "".join(w[0].upper() for w in trait.split())
            pos_map[abbrev] = trait
            pos_map[trait.lower()] = trait
        for trait in NEGATIVE_TRAIT_LIST:
            if trait == "None":
                continue
            abbrev = "".join(w[0].upper() for w in trait.split())
            neg_map[abbrev] = trait
            neg_map[trait.lower()] = trait
        _QUICK_TRAIT_MAPS = (pos_map, neg_map)
    return _QUICK_TRAIT_MAPS


def _canon(raw, options):
    if not raw:
        return raw, True
    raw_lower = raw.lower()
    match = (
        next((o for o in options if o.lower() == raw_lower), None) or
        next((o for o in options if o.lower().startswith(raw_lower)), None) or
        next((o for o in options if raw_lower in o.lower()), None)
    )
    if match:
        return match, True
    return raw.title(), False


def _parse_quick_birthday(raw):
    raw = raw.strip()
    if not raw:
        return None, True
    import re as _re
    m = _re.match(r"^(\d{1,4})[/\-](\d{1,2})[/\-](\d{1,2})$", raw)
    if not m:
        return None, False
    year, month, day = (int(g) for g in m.groups())
    try:
        parsed = date(year, month, day)
    except ValueError:
        return None, False
    if not (BIRTHDAY_MIN_YEAR <= year <= date.today().year) or parsed > date.today():
        return None, False
    return parsed.isoformat(), True


def parse_quick_dragon(text):
    import re as _re
    lines = text.splitlines()

    def get(i):
        return lines[i].strip() if i < len(lines) else ""

    pos_map, neg_map = get_quick_trait_maps()

    species, species_ok = _canon(get(1), SPECIES_LIST)
    nickname = get(0) or species
    gender_raw = get(2).capitalize()
    gender = gender_raw if gender_raw in ("Male", "Female") else ""
    age_raw = get(3).strip()
    age = AGE_QUICK_MAP.get(age_raw, AGE_QUICK_MAP.get(age_raw.lower(), "Baby"))

    rebirths_raw = get(4)
    try:
        rebirths = max(0, int(rebirths_raw)) if rebirths_raw else 0
    except ValueError:
        rebirths = 0

    p_color, p_color_ok = _canon(get(5), COLOR_LIST)
    s_color, s_color_ok = _canon(get(6), COLOR_LIST)
    t_color, t_color_ok = _canon(get(7), COLOR_LIST)
    p_mat, p_mat_ok = _canon(get(8), MATERIAL_LIST)
    s_mat, s_mat_ok = _canon(get(9), MATERIAL_LIST)
    t_mat, t_mat_ok = _canon(get(10), MATERIAL_LIST)
    p_color, s_color, t_color = p_color or "-", s_color or "-", t_color or "-"
    p_mat, s_mat, t_mat = p_mat or "-", s_mat or "-", t_mat or "-"

    mut_raw = get(11)
    try:
        mutations = max(0, min(5, int(mut_raw)))
    except ValueError:
        mutations = 0

    cosmetic_raw = get(12).strip()
    if cosmetic_raw and cosmetic_raw.lower() != "none":
        cosmetic, cosmetic_ok = _canon(cosmetic_raw, COSMETIC_TRAIT_LIST)
    else:
        cosmetic, cosmetic_ok = "None", True
    element, element_ok = _canon(get(13), ELEMENT_LIST)
    element = element or (ELEMENT_LIST[0] if ELEMENT_LIST else "-")
    pupil, pupil_ok = _canon(get(14), PUPIL_LIST)
    pupil = pupil or (PUPIL_LIST[0] if PUPIL_LIST else "-")
    gen_raw = get(15)
    generation = int(gen_raw) if gen_raw.lstrip("-").isdigit() else (gen_raw or "1")
    if isinstance(generation, int):
        generation = max(1, generation)

    soulbound = get(16).lower() in ("yes", "y", "true")
    birthday, birthday_ok = _parse_quick_birthday(get(17))
    owner = get(18) or None

    pos_traits, neg_traits = [], []
    for i in range(19, len(lines)):
        line = lines[i].strip()
        if not line:
            continue
        clean = _re.sub(r'\([^)]*\)', '', line).strip()
        parts = clean.rsplit(None, 1)
        tier = 1
        name_part = clean
        if len(parts) == 2:
            try:
                tier = max(1, min(10, int(parts[1])))
                name_part = parts[0].strip()
            except ValueError:
                pass
        abbrev = name_part.upper()
        full_lower = name_part.lower()
        if abbrev in pos_map:
            pos_traits.append({"Trait": pos_map[abbrev], "Tier": tier})
        elif full_lower in pos_map:
            pos_traits.append({"Trait": pos_map[full_lower], "Tier": tier})
        elif abbrev in neg_map:
            neg_traits.append({"Trait": neg_map[abbrev], "Tier": tier})
        elif full_lower in neg_map:
            neg_traits.append({"Trait": neg_map[full_lower], "Tier": tier})

    d = {
        "Nickname": nickname,
        "Species": species,
        "Rarity": SPECIES_RARITY.get(species, "Common"),
        "Gender": gender,
        "Age": age,
        "Rebirths": rebirths,
        "Colors": {"P": p_color, "S": s_color, "T": t_color},
        "Materials": {"P": p_mat, "S": s_mat, "T": t_mat},
        "Mutations": mutations,
        "MaxMutations": MUTATION_CAP,
        "CosmeticTrait": cosmetic,
        "Element": element,
        "Pupil": pupil,
        "Generation": generation,
        "Soulbound": soulbound,
        "Birthday": birthday,
        "OriginalOwner": owner,
        "Level": 1,
        "Element2": None,
        "Note": "",
        "PositiveTraits": pos_traits[:5],
        "NegativeTraits": neg_traits[:2],
    }
    validation = {
        "Species": species_ok,
        "PrimaryColor": p_color_ok, "SecondaryColor": s_color_ok, "TertiaryColor": t_color_ok,
        "PrimaryMaterial": p_mat_ok, "SecondaryMaterial": s_mat_ok, "TertiaryMaterial": t_mat_ok,
        "CosmeticTrait": cosmetic_ok, "Element": element_ok, "Pupil": pupil_ok,
        "Birthday": birthday_ok,
    }
    return d, validation


QUICK_ADD_REFERENCE = [
    "1.  Nickname (blank = species name)",
    "2.  Species",
    "3.  Gender  (Male / Female)",
    "4.  Age     (B / J / A / E)",
    "5.  Rebirths (blank = 0)",
    "6.  Primary Color",
    "7.  Secondary Color",
    "8.  Tertiary Color",
    "9.  Primary Material",
    "10. Secondary Material",
    "11. Tertiary Material",
    "12. Mutations  (0-5)",
    "13. Cosmetic Trait  (or None)",
    "14. Element",
    "15. Pupil",
    "16. Generation",
    "17. Soulbound  (Yes / No)",
    "18. Birthday  (optional, YYYY/MM/DD)",
    "19. Original Owner  (optional)",
    "20. Traits  (SWM 8 or",
    "    Strong Wing Membrane 8)",
]


def open_quick_add(parent_win, refresh_callback):
    dlg = tk.Toplevel(parent_win)
    dlg.title("Quick Add Dragon")
    dlg.configure(bg=PALETTE["bg_outer"])
    sw = dlg.winfo_screenwidth()
    sh = dlg.winfo_screenheight()
    dw = max(720, min(820, sw - 60))
    dh = min(620, sh - 80)
    center(dlg, dw, dh)
    dlg.resizable(True, True)
    dlg.minsize(720, 480)

    header = tk.Frame(dlg, bg=PALETTE["bg_outer"])
    header.pack(fill="x", padx=16, pady=(14, 6))
    tk.Label(header, text="Quick Add Dragon", fg=PALETTE["title_fill"],
             bg=PALETTE["bg_outer"], font=(APP_FONT_FAMILY, 16, APP_FONT_WEIGHT)).pack(side="left")

    body = tk.Frame(dlg, bg=PALETTE["bg_outer"])
    body.pack(fill="both", expand=True, padx=16, pady=4)

    right = tk.Frame(body, bg=PALETTE["panel_fill"], width=220)
    right.pack(side="right", fill="y")
    right.pack_propagate(False)
    tk.Label(right, text="Line order:", fg=PALETTE["title_fill"],
             bg=PALETTE["panel_fill"], font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(
        anchor="w", padx=10, pady=(10, 4))
    for ref in QUICK_ADD_REFERENCE:
        tk.Label(right, text=ref, fg=PALETTE["label_text"],
                  bg=PALETTE["panel_fill"], font=(APP_FONT_FAMILY, 8),
                  justify="left", anchor="w").pack(anchor="w", padx=10)

    left = tk.Frame(body, bg=PALETTE["bg_outer"])
    left.pack(side="left", fill="both", expand=True, padx=(0, 10))
    tk.Label(left, text="One field per line:", fg=PALETTE["label_text"],
             bg=PALETTE["bg_outer"], font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT)).pack(anchor="w")

    txt_frame = tk.Frame(left, bg=PALETTE["bg_outer"])
    txt_frame.pack(fill="both", expand=True, pady=(4, 0))
    txt = tk.Text(txt_frame, bg=PALETTE["tag_fill"], fg="white",
                   insertbackground="white", relief="flat", wrap="none",
                   font=(APP_FONT_FAMILY, 11), highlightthickness=1,
                   highlightbackground=PALETTE["panel_border"])
    txt_scroll = tk.Scrollbar(txt_frame, command=txt.yview)
    txt.configure(yscrollcommand=txt_scroll.set)
    txt.pack(side="left", fill="both", expand=True)
    txt_scroll.pack(side="right", fill="y")

    preview_var = tk.StringVar(value="")
    preview = tk.Label(dlg, textvariable=preview_var, fg=PALETTE["label_text"],
                        bg=PALETTE["bg_outer"], font=(APP_FONT_FAMILY, 9),
                        justify="left", anchor="w", wraplength=530)
    preview.pack(fill="x", padx=16, pady=(6, 2))

    def _on_dlg_resize(e):
        if e.widget is dlg:
            preview.configure(wraplength=max(300, e.width - 260))

    dlg.bind("<Configure>", _on_dlg_resize)

    btn_row = tk.Frame(dlg, bg=PALETTE["bg_outer"])
    btn_row.pack(pady=10)

    def do_parse(_e=None):
        raw = txt.get("1.0", "end-1c").strip()
        if not raw:
            preview_var.set("")
            return
        d, v = parse_quick_dragon(raw)
        sp = d["Species"]

        def mark(text, ok):
            return text if ok else f"{text} ✗"

        lines = [
            f"Nickname: {d['Nickname']}  |  Species: {mark(sp, v['Species'])}  |  Rarity: {d['Rarity']}",
            f"Gender: {d['Gender'] or '—'}  |  Age: {d['Age']}  |  Rebirths: {d['Rebirths']}  |  Soulbound: {'Yes' if d['Soulbound'] else 'No'}",
            f"Colors: {mark(d['Colors']['P'], v['PrimaryColor'])} / "
            f"{mark(d['Colors']['S'], v['SecondaryColor'])} / "
            f"{mark(d['Colors']['T'], v['TertiaryColor'])}",
            f"Materials: {mark(d['Materials']['P'], v['PrimaryMaterial'])} / "
            f"{mark(d['Materials']['S'], v['SecondaryMaterial'])} / "
            f"{mark(d['Materials']['T'], v['TertiaryMaterial'])}",
            f"Mutations: {d['Mutations']}  |  Element: {mark(d['Element'], v['Element'])}  |  "
            f"Pupil: {mark(d['Pupil'], v['Pupil'])}  |  Gen: {d['Generation']}",
            f"Cosmetic: {mark(d['CosmeticTrait'], v['CosmeticTrait'])}",
            f"Birthday: {mark(d['Birthday'] or '—', v['Birthday'])}",
        ]
        if any(not v[k] for k in v if k != "Birthday"):
            lines.append("✗ = not recognised - check spelling, or it may not exist on the wiki yet")
        if not v["Birthday"]:
            lines.append(f"Birthday ✗ = must be a real date between {BIRTHDAY_MIN_YEAR} and {date.today().year}")
        if d["PositiveTraits"]:
            lines.append("Positive: " + ", ".join(f"{t['Trait']} T{t['Tier']}" for t in d["PositiveTraits"]))
        if d["NegativeTraits"]:
            lines.append("Negative: " + ", ".join(f"{t['Trait']} T{t['Tier']}" for t in d["NegativeTraits"]))
        preview_var.set("\n".join(lines))
        return d

    def do_add():
        raw = txt.get("1.0", "end-1c").strip()
        if not raw:
            messagebox.showwarning("Empty", "Enter dragon info first.", parent=dlg)
            return
        d, _v = parse_quick_dragon(raw)
        if not d["Species"]:
            messagebox.showwarning("Missing species", "Line 2 must be a species name.", parent=dlg)
            return
        new_id = uuid.uuid4().hex[:10]
        dragons[new_id] = d
        persist()
        if refresh_callback:
            refresh_callback()
        dlg.destroy()

    def do_full_preview():
        raw = txt.get("1.0", "end-1c").strip()
        if not raw:
            messagebox.showwarning("Empty", "Enter dragon info first.", parent=dlg)
            return
        d, _v = parse_quick_dragon(raw)
        if not d["Species"]:
            messagebox.showwarning("Missing species", "Line 2 must be a species name.", parent=dlg)
            return

        preview_key = "__quick_add_preview__"
        dragons[preview_key] = d

        preview_win = tk.Toplevel(dlg)
        preview_win.title(f"Preview — {d['Nickname']}")
        preview_win.configure(bg=PALETTE["lair_bg"])
        center(preview_win, 700, 780)
        preview_win.minsize(400, 400)

        def on_preview_close():
            dragons.pop(preview_key, None)
            preview_win.destroy()

        preview_win.protocol("WM_DELETE_WINDOW", on_preview_close)

        outer = tk.Frame(preview_win, bg=PALETTE["lair_bg"])
        outer.pack(fill="both", expand=True)
        pv_canvas = tk.Canvas(outer, bg=PALETTE["lair_bg"], highlightthickness=0)
        pv_canvas.pack(side="left", fill="both", expand=True)
        pv_vscroll = tk.Scrollbar(outer, orient="vertical", command=pv_canvas.yview)
        pv_vscroll.pack(side="right", fill="y")
        pv_canvas.configure(yscrollcommand=pv_vscroll.set)
        bind_mousewheel(pv_canvas)

        pv_inner = tk.Frame(pv_canvas, bg=PALETTE["lair_bg"])
        pv_window_id = pv_canvas.create_window((0, 0), window=pv_inner, anchor="nw")

        def _sync_preview(_e=None):
            canvas_w = pv_canvas.winfo_width()
            content_w = pv_inner.winfo_reqwidth()
            pv_canvas.itemconfig(pv_window_id, width=max(canvas_w, content_w))
            pv_canvas.configure(scrollregion=pv_canvas.bbox("all"))

        pv_canvas.bind("<Configure>", _sync_preview)
        pv_inner.bind("<Configure>", _sync_preview)

        show_details(preview_win, pv_inner, preview_key, refresh_grid=None, active_tab=None)

    txt.bind("<KeyRelease>", lambda _e: do_parse())
    tk.Button(btn_row, text="Preview", command=do_full_preview,
               bg=PALETTE["tag_fill"], fg="white", relief="flat",
               font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), padx=16, pady=6).pack(side="left", padx=8)
    tk.Button(btn_row, text="Add Dragon", command=do_add,
               bg=PALETTE["bar_fill"], fg="#16330F", relief="flat",
               font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), padx=16, pady=6).pack(side="left", padx=8)
    tk.Button(btn_row, text="Cancel", command=dlg.destroy,
               bg=PALETTE["row_fill"], fg="white", relief="flat",
               font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), padx=16, pady=6).pack(side="left", padx=8)
    txt.focus_set()


def open_theme_manager(parent_win):
    dlg = tk.Toplevel(parent_win)
    dlg.title("Dragon Themes")
    dlg.configure(bg=PALETTE["bg_outer"])
    center(dlg, 820, 560)
    dlg.resizable(True, True)

    outline_text_on = lambda c, x, y, t, f: c.create_text(x, y, text=t, fill=PALETTE["title_fill"],
                                                            font=f, anchor="center")

    top = tk.Frame(dlg, bg=PALETTE["bg_outer"])
    top.pack(fill="x", padx=14, pady=(14, 6))
    tk.Label(top, text="Dragon Themes", fg=PALETTE["title_fill"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 16, APP_FONT_WEIGHT)).pack(side="left")
    tk.Label(top, text="Create named presets to quickly apply colors & traits to dragons",
             fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(side="left", padx=12)

    mid = tk.Frame(dlg, bg=PALETTE["bg_outer"])
    mid.pack(fill="both", expand=True, padx=14, pady=4)

    left_col = tk.Frame(mid, bg=PALETTE["bg_outer"], width=200)
    left_col.pack(side="left", fill="y", padx=(0, 10))
    left_col.pack_propagate(False)

    tk.Label(left_col, text="Saved Themes", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(anchor="w", pady=(0, 4))

    lb_frame = tk.Frame(left_col, bg=PALETTE["bg_outer"])
    lb_frame.pack(fill="both", expand=True)
    lb = tk.Listbox(lb_frame, bg=PALETTE["tag_fill"], fg="white",
                     selectbackground=PALETTE["card_fill"], selectforeground="white",
                     relief="flat", font=(APP_FONT_FAMILY, 10), highlightthickness=1,
                     highlightbackground=PALETTE["panel_border"], exportselection=False,
                     activestyle="none")
    lb_scroll = tk.Scrollbar(lb_frame, command=lb.yview)
    lb.configure(yscrollcommand=lb_scroll.set)
    lb.pack(side="left", fill="both", expand=True)
    lb_scroll.pack(side="right", fill="y")

    btn_row = tk.Frame(left_col, bg=PALETTE["bg_outer"])
    btn_row.pack(fill="x", pady=(6, 0))
    new_btn = tk.Button(btn_row, text="+ New", bg=PALETTE["bar_fill"], fg="#16330F",
                         relief="flat", font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), pady=4)
    new_btn.pack(side="left", padx=(0, 4), fill="x", expand=True)
    del_btn = tk.Button(btn_row, text="Delete", bg="#7A2020", fg="white",
                         relief="flat", font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), pady=4)
    del_btn.pack(side="left", fill="x", expand=True)

    right_col = tk.Frame(mid, bg=PALETTE["bg_outer"])
    right_col.pack(side="right", fill="both", expand=True)

    right_canvas = tk.Canvas(right_col, bg=PALETTE["bg_outer"], highlightthickness=0)
    right_canvas.pack(side="left", fill="both", expand=True)
    right_vscroll = tk.Scrollbar(right_col, command=right_canvas.yview)
    right_vscroll.pack(side="right", fill="y")
    right_canvas.configure(yscrollcommand=right_vscroll.set)

    right_inner = tk.Frame(right_canvas, bg=PALETTE["bg_outer"])
    right_canvas_win = right_canvas.create_window((0, 0), window=right_inner, anchor="nw")
    right_canvas.bind("<Configure>", lambda e: right_canvas.itemconfig(right_canvas_win, width=e.width))
    right_inner.bind("<Configure>", lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all")))

    def _theme_scroll_route(event):
        w = event.widget
        cur = w
        while cur:
            if isinstance(cur, tk.Listbox):
                cur.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return "break"
            cur = getattr(cur, "master", None)
        right_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    right_canvas.bind("<Enter>", lambda _e: dlg.bind_all("<MouseWheel>", _theme_scroll_route))
    right_canvas.bind("<Leave>", lambda _e: dlg.unbind_all("<MouseWheel>"))

    edit_frame = tk.Frame(right_inner, bg=PALETTE["bg_outer"])
    empty_label = tk.Label(right_inner, text="Select a theme to edit\nor click + New",
                            fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                            font=(APP_FONT_FAMILY, 11), justify="center")
    empty_label.pack(expand=True, pady=40)

    editing_id = {"v": None}

    def build_editor(theme_id):
        editing_id["v"] = theme_id
        theme = current_themes.get(theme_id, {})

        empty_label.pack_forget()
        for w in edit_frame.winfo_children():
            w.destroy()
        edit_frame.pack(fill="both", expand=True, padx=10, pady=6)

        body = tk.Frame(edit_frame, bg=PALETTE["bg_outer"])
        body.pack(fill="both", expand=True)

        def lfield(parent, label):
            tk.Label(parent, text=label, fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                      font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT)).pack(anchor="w", pady=(8, 2))

        lfield(body, "Theme Name")
        name_var = tk.StringVar(value=theme.get("name", ""))
        name_entry = tk.Entry(body, textvariable=name_var, bg=PALETTE["tag_fill"], fg="white",
                               insertbackground="white", relief="flat", font=(APP_FONT_FAMILY, 11),
                               highlightthickness=1, highlightbackground=PALETTE["panel_border"])
        name_entry.pack(fill="x", ipady=4)

        W = 480
        legendary_slot = {"v": None}

        def theme_color_values_for(slot):
            def getter():
                ls = legendary_slot["v"]
                return COLOR_LIST if (ls is None or ls == slot) else [c for c in COLOR_LIST if c != "Legendary"]
            return getter

        lfield(body, "Primary Color")
        pc_wrap, pc_var, pc_refresh = make_search_select(body, theme_color_values_for("P"),
                                                          initial=theme.get("p_color", COLOR_LIST[0]),
                                                          height=3, width=W)
        pc_wrap.pack(fill="x")

        lfield(body, "Secondary Color")
        sc_wrap, sc_var, sc_refresh = make_search_select(body, theme_color_values_for("S"),
                                                          initial=theme.get("s_color", COLOR_LIST[0]),
                                                          height=3, width=W)
        sc_wrap.pack(fill="x")

        lfield(body, "Tertiary Color")
        tc_wrap, tc_var, tc_refresh = make_search_select(body, theme_color_values_for("T"),
                                                          initial=theme.get("t_color", COLOR_LIST[0]),
                                                          height=3, width=W)
        tc_wrap.pack(fill="x")

        def enforce_theme_legendary(*_args):
            for slot, var in (("P", pc_var), ("S", sc_var), ("T", tc_var)):
                if var.get() == "Legendary":
                    legendary_slot["v"] = slot
                    break
            else:
                legendary_slot["v"] = None
            for rf in (pc_refresh, sc_refresh, tc_refresh):
                rf()

        pc_var.trace_add("write", enforce_theme_legendary)
        sc_var.trace_add("write", enforce_theme_legendary)
        tc_var.trace_add("write", enforce_theme_legendary)
        enforce_theme_legendary()

        lfield(body, "Primary Material")
        pm_wrap, pm_var, _ = make_search_select(body, MATERIAL_LIST, initial=theme.get("p_material", MATERIAL_LIST[0]), height=3, width=W)
        pm_wrap.pack(fill="x")

        lfield(body, "Secondary Material")
        sm_wrap, sm_var, _ = make_search_select(body, MATERIAL_LIST, initial=theme.get("s_material", MATERIAL_LIST[0]), height=3, width=W)
        sm_wrap.pack(fill="x")

        lfield(body, "Tertiary Material")
        tm_wrap, tm_var, _ = make_search_select(body, MATERIAL_LIST, initial=theme.get("t_material", MATERIAL_LIST[0]), height=3, width=W)
        tm_wrap.pack(fill="x")

        lfield(body, "Cosmetic Trait")
        ct_wrap, ct_var, _ = make_search_select(body, COSMETIC_TRAIT_LIST, initial=theme.get("cosmetic_trait", "None"), height=3, width=W)
        ct_wrap.pack(fill="x")

        def save_theme():
            n = name_var.get().strip()
            if not n:
                messagebox.showwarning("Missing name", "Enter a theme name.", parent=dlg)
                return
            current_themes[theme_id] = {
                "name": n,
                "p_color": pc_var.get(), "s_color": sc_var.get(), "t_color": tc_var.get(),
                "p_material": pm_var.get(), "s_material": sm_var.get(), "t_material": tm_var.get(),
                "cosmetic_trait": ct_var.get(),
            }
            save_themes(current_account, current_themes)
            refresh_list()
            messagebox.showinfo("Saved", f'Theme "{n}" saved!', parent=dlg)

        save_btn = tk.Button(edit_frame, text="Save Theme", command=save_theme,
                              bg=PALETTE["bar_fill"], fg="#16330F", relief="flat",
                              font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), pady=6)
        save_btn.pack(fill="x", pady=(8, 0))

        try:
            edit_frame.update_idletasks()
        except Exception:
            pass

    def refresh_list():
        sel = lb.curselection()
        lb.delete(0, "end")
        for tid, t in current_themes.items():
            lb.insert("end", f"  {t.get('name', tid)}")
            lb.itemconfig("end", fg=PALETTE["title_fill"])
        if sel and sel[0] < lb.size():
            lb.selection_set(sel[0])

    def on_select(_e=None):
        sel = lb.curselection()
        if not sel:
            return
        tid = list(current_themes.keys())[sel[0]]
        build_editor(tid)

    def new_theme():
        tid = uuid.uuid4().hex[:8]
        current_themes[tid] = {
            "name": "New Theme",
            "p_color": COLOR_LIST[0], "s_color": COLOR_LIST[0], "t_color": COLOR_LIST[0],
            "p_material": MATERIAL_LIST[0], "s_material": MATERIAL_LIST[0], "t_material": MATERIAL_LIST[0],
            "cosmetic_trait": "None",
        }
        save_themes(current_account, current_themes)
        refresh_list()
        lb.selection_set(lb.size() - 1)
        build_editor(tid)

    def delete_theme():
        sel = lb.curselection()
        if not sel:
            return
        tid = list(current_themes.keys())[sel[0]]
        name = current_themes[tid].get("name", "this theme")
        if not messagebox.askyesno("Delete", f'Delete "{name}"?', parent=dlg):
            return
        del current_themes[tid]
        save_themes(current_account, current_themes)
        refresh_list()
        empty_label.pack(expand=True)
        edit_frame.pack_forget()

    new_btn.config(command=new_theme)
    del_btn.config(command=delete_theme)
    lb.bind("<<ListboxSelect>>", on_select)
    refresh_list()


def sidebar_font_size(w, base_w=350, base_size=13, min_size=9, max_size=17):
    return max(min_size, min(max_size, round(base_size * w / base_w)))


def compact_btn_width(text, w, base_size, has_icon, icon_h, full_w):
    if not global_settings.get("CompactMode", False):
        return full_w
    TWO_CARD_WIDTH = 150 * 2 + 8 * 3
    return min(full_w, TWO_CARD_WIDTH)


def flex_button_canvas(parent, height, draw_fn, pady=(0, 4), padx=14):
    c = tk.Canvas(parent, height=height, bg=PALETTE["lair_bg"], highlightthickness=0)
    c.pack(fill="x", padx=padx, pady=pady)

    def _redraw(_e=None):
        w = c.winfo_width()
        if w > 4:
            draw_fn(c, w)

    c.bind("<Configure>", _redraw)
    return c


def open_lair(root, account):
    switch_account(account)
    root.withdraw()

    win = tk.Toplevel()
    win.title(f"The Lair — {account}")
    win.configure(bg=PALETTE["lair_bg"])
    _compact_at_open = global_settings.get("CompactMode", False)
    if _compact_at_open:
        center(win, 830, 880)
        win.minsize(640, 460)
    else:
        center(win, 1170, 850)
        win.minsize(760, 520)

    def back_to_accounts():
        win.destroy()
        root.deiconify()

    win.protocol("WM_DELETE_WINDOW", back_to_accounts)

    active_tab = {"id": None}

    win.columnconfigure(0, weight=(0 if _compact_at_open else 1), minsize=(350 if _compact_at_open else 340))
    win.columnconfigure(1, weight=2)
    win.rowconfigure(0, weight=1)

    left = tk.Frame(win, bg=PALETTE["lair_bg"])
    left.grid(row=0, column=0, sticky="nsew")

    tk.Label(left, text=f"Logged in as {account}", fg=PALETTE["label_text"],
             bg=PALETTE["lair_bg"], font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(pady=(12, 2))

    flex_button_canvas(left, 38, lambda c, w: (
        c.delete("all"),
        rounded_button_with_icon(c, 2, 2, compact_btn_width("\u2190 Switch Account", w, 13, False, 0, w - 4), 36, "Quick Add",
                                  os.path.join(MENUICONS_DIR, "quickadd.png"),
                                  lambda: open_quick_add(win, render), r=12,
                                  fill=PALETTE["card_fill"], outline=PALETTE["panel_border"],
                                  font=(APP_FONT_FAMILY, sidebar_font_size(w, base_size=11), APP_FONT_WEIGHT),
                                  text_align=("left" if global_settings.get("CompactMode") else "center"))
    ), pady=(2, 0))

    flex_button_canvas(left, 34, lambda c, w: (
        c.delete("all"),
        rounded_button(c, 2, 2, compact_btn_width("\u2190 Switch Account", w, 13, False, 0, w - 4), 32,
                        "\u2190 Switch Account", back_to_accounts, r=12,
                        fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"],
                        font=(APP_FONT_FAMILY, sidebar_font_size(w, base_size=13), APP_FONT_WEIGHT))
    ), pady=(2, 0))

    tab_area = tk.Frame(left, bg=PALETTE["lair_bg"])
    tab_area.pack(fill="x", padx=14, pady=(10, 0))

    tab_scroll_canvas = tk.Canvas(tab_area, bg=PALETTE["lair_bg"], highlightthickness=0, height=36)
    tab_scroll_canvas.pack(side="top", fill="x")

    tab_hscroll = tk.Scrollbar(tab_area, orient="horizontal", command=tab_scroll_canvas.xview)
    tab_hscroll.pack(side="top", fill="x")
    tab_scroll_canvas.configure(xscrollcommand=tab_hscroll.set)

    tab_inner = tk.Frame(tab_scroll_canvas, bg=PALETTE["lair_bg"])
    tab_scroll_canvas.create_window((0, 0), window=tab_inner, anchor="nw")

    def _tab_hscroll(event):
        tab_scroll_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    tab_scroll_canvas.bind("<Enter>", lambda _e: tab_scroll_canvas.bind_all("<MouseWheel>", _tab_hscroll))
    tab_scroll_canvas.bind("<Leave>", lambda _e: tab_scroll_canvas.unbind_all("<MouseWheel>"))

    search_var = tk.StringVar()
    search_box = tk.Frame(left, bg=PALETTE["lair_bg"])
    if global_settings.get("CompactMode", False):
        search_box.configure(width=324, height=44)
        search_box.pack_propagate(False)
        search_box.pack(anchor="w", padx=14, pady=(8, 6))
    else:
        search_box.pack(fill="x", padx=14, pady=(8, 6))
    search_canvas = tk.Canvas(search_box, height=40, bg=PALETTE["lair_bg"], highlightthickness=0)
    search_canvas.pack(fill="both", expand=True)
    search = tk.Entry(search_canvas, textvariable=search_var,
                       bg=PALETTE["tag_fill"], fg="white",
                       insertbackground="white", relief="flat",
                       font=(APP_FONT_FAMILY, 11))
    search_entry_window = search_canvas.create_window(2, 20, window=search, anchor="w")

    def _redraw_search(_e=None):
        w = search_canvas.winfo_width()
        if w <= 4:
            return
        search_canvas.delete("searchbg")
        round_rect(search_canvas, 2, 2, w - 2, 38, r=14,
                    fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"], width=2, tags="searchbg")
        search_canvas.tag_lower("searchbg")
        search_canvas.coords(search_entry_window, 12, 20)
        search_canvas.itemconfig(search_entry_window, width=max(60, w - 24))
        search.configure(font=(APP_FONT_FAMILY, sidebar_font_size(w, base_size=11)))

    search_canvas.bind("<Configure>", _redraw_search)
    _redraw_search()

    sort_wrap = tk.Frame(left, bg=PALETTE["lair_bg"])
    if global_settings.get("CompactMode", False):
        sort_wrap.configure(width=324, height=48)
        sort_wrap.pack_propagate(False)
        sort_wrap.pack(anchor="w", padx=14, pady=(0, 10))
    else:
        sort_wrap.pack(fill="x", padx=14, pady=(0, 10))
    tk.Label(sort_wrap, text="Sort by", fg=PALETTE["label_text"], bg=PALETTE["lair_bg"],
             font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT)).pack(anchor="w")
    sort_var = tk.StringVar(value="Nickname")
    sort_combo = ttk.Combobox(sort_wrap, textvariable=sort_var,
                               values=["Nickname", "Species", "Level", "Gender"],
                               state="readonly", style="Dragon.TCombobox", font=(APP_FONT_FAMILY, 10))
    sort_combo.pack(fill="x")

    add_dragon_window = {"win": None}

    def open_add_dragon():
        existing = add_dragon_window["win"]
        if existing is not None and existing.winfo_exists():
            existing.lift()
            existing.focus_force()
            return
        add_dragon_window["win"] = open_dragon_form(win, render)

    flex_button_canvas(left, 44, lambda c, w: (
        c.delete("all"),
        rounded_button(c, 2, 2, compact_btn_width("\u2190 Switch Account", w, 13, False, 0, w - 4), 42, "+ Add Dragon",
                        open_add_dragon, r=14,
                        fill=PALETTE["badge_fill"], outline=PALETTE["badge_border"],
                        text_fill="#3A2A06",
                        font=(APP_FONT_FAMILY, sidebar_font_size(w, base_size=13), APP_FONT_WEIGHT))
    ), pady=(0, 10))

    sub_on = account_settings.get("Subscription", False)
    sub_state = {"on": sub_on}
    sub_canvas = tk.Canvas(left, height=36, bg=PALETTE["lair_bg"], highlightthickness=0)
    sub_canvas.pack(fill="x", padx=14, pady=(0, 4))

    def draw_sub_btn(_e=None):
        w = sub_canvas.winfo_width()
        if w <= 4:
            return
        sub_canvas.delete("all")
        on = sub_state["on"]
        lbl = "\u2714 Subscription (ON)" if on else "Subscription (OFF)"
        fill = PALETTE["bar_fill"] if on else PALETTE["tag_fill"]
        tf = "#16330F" if on else "white"
        rounded_button(sub_canvas, 2, 2, compact_btn_width("\u2190 Switch Account", w, 13, False, 0, w - 4), 34, lbl,
                        toggle_sub, r=12, fill=fill, outline=PALETTE["panel_border"], text_fill=tf,
                        font=(APP_FONT_FAMILY, sidebar_font_size(w, base_size=12), APP_FONT_WEIGHT))

    def toggle_sub():
        sub_state["on"] = not sub_state["on"]
        account_settings["Subscription"] = sub_state["on"]
        save_account_settings(current_account, account_settings)
        draw_sub_btn()

    sub_canvas.bind("<Configure>", draw_sub_btn)

    if global_settings.get("EnableSDA", True):
        flex_button_canvas(left, 36, lambda c, w: (
            c.delete("all"),
            rounded_button_with_icon(c, 2, 2, compact_btn_width("\u2190 Switch Account", w, 13, False, 0, w - 4), 34, "SDA Tracker",
                                      os.path.join(MENUICONS_DIR, "SDA.png"),
                                      lambda: open_sda_tracker(win), r=12,
                                      fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"],
                                      font=(APP_FONT_FAMILY, sidebar_font_size(w, base_size=11), APP_FONT_WEIGHT),
                                      text_align=("left" if global_settings.get("CompactMode") else "center"))
        ))

    if global_settings.get("EnableElemental", True):
        flex_button_canvas(left, 36, lambda c, w: (
            c.delete("all"),
            rounded_button_with_icon(c, 2, 2, compact_btn_width("\u2190 Switch Account", w, 13, False, 0, w - 4), 34, "Elemental",
                                      os.path.join(MENUICONS_DIR, "elemental.png"),
                                      lambda: open_elemental_tracker(win), r=12,
                                      fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"],
                                      font=(APP_FONT_FAMILY, sidebar_font_size(w, base_size=13), APP_FONT_WEIGHT),
                                      text_align=("left" if global_settings.get("CompactMode") else "center"))
        ))

    flex_button_canvas(left, 36, lambda c, w: (
        c.delete("all"),
        rounded_button_with_icon(c, 2, 2, compact_btn_width("\u2190 Switch Account", w, 13, False, 0, w - 4), 34, "Themes",
                                  os.path.join(MENUICONS_DIR, "themes.png"),
                                  lambda: open_theme_manager(win), r=12,
                                  fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"],
                                  font=(APP_FONT_FAMILY, sidebar_font_size(w, base_size=11), APP_FONT_WEIGHT),
                                  text_align=("left" if global_settings.get("CompactMode") else "center"))
    ))

    select_mode = {"on": False}
    selected_ids = set()

    sel_canvas = tk.Canvas(left, height=36, bg=PALETTE["lair_bg"], highlightthickness=0)
    sel_canvas.pack(fill="x", padx=14, pady=(0, 4))

    def draw_sel_btn(_e=None):
        w = sel_canvas.winfo_width()
        if w <= 4:
            return
        sel_canvas.delete("all")
        fsz = sidebar_font_size(w, base_size=11)
        talign = "left" if global_settings.get("CompactMode") else "center"
        if select_mode["on"]:
            rounded_button_with_icon(sel_canvas, 2, 2, compact_btn_width("\u2190 Switch Account", w, 13, False, 0, w - 4), 34,
                                      "Select Mode  (on)",
                                      os.path.join(MENUICONS_DIR, "select.png"),
                                      lambda: toggle_select_mode(), r=12,
                                      fill=PALETTE["badge_fill"], outline=PALETTE["badge_border"],
                                      text_fill="#3A2A06", font=(APP_FONT_FAMILY, fsz, APP_FONT_WEIGHT),
                                      text_align=talign)
        else:
            rounded_button_with_icon(sel_canvas, 2, 2, compact_btn_width("\u2190 Switch Account", w, 13, False, 0, w - 4), 34,
                                      "Select Mode",
                                      os.path.join(MENUICONS_DIR, "select.png"),
                                      lambda: toggle_select_mode(), r=12,
                                      fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"],
                                      font=(APP_FONT_FAMILY, fsz, APP_FONT_WEIGHT),
                                      text_align=talign)

    sel_canvas.bind("<Configure>", draw_sel_btn)

    del_canvas = tk.Canvas(left, height=36, bg=PALETTE["lair_bg"], highlightthickness=0)
    move_canvas = tk.Canvas(left, height=36, bg=PALETTE["lair_bg"], highlightthickness=0)

    def refresh_del_button(_e=None):
        w = del_canvas.winfo_width()
        if w <= 4:
            return
        del_canvas.delete("all")
        n = len(selected_ids)
        rounded_button(del_canvas, 2, 2, w - 4, 34,
                        f"Delete Selected ({n})",
                        lambda: batch_delete(), r=12,
                        fill="#7A2020" if n else PALETTE["row_fill"],
                        outline="#4A1010" if n else PALETTE["panel_border"],
                        font=(APP_FONT_FAMILY, sidebar_font_size(w, base_size=12), APP_FONT_WEIGHT))

        w2 = move_canvas.winfo_width()
        if w2 <= 4:
            return
        move_canvas.delete("all")
        rounded_button(move_canvas, 2, 2, w2 - 4, 34,
                        f"Move Selected ({n})",
                        lambda: batch_move(), r=12,
                        fill=PALETTE["tag_fill"] if n else PALETTE["row_fill"],
                        outline=PALETTE["panel_border"],
                        font=(APP_FONT_FAMILY, sidebar_font_size(w2, base_size=12), APP_FONT_WEIGHT))

    del_canvas.bind("<Configure>", refresh_del_button)
    move_canvas.bind("<Configure>", refresh_del_button)

    def toggle_select_mode():
        select_mode["on"] = not select_mode["on"]
        selected_ids.clear()
        draw_sel_btn()
        if select_mode["on"]:
            move_canvas.pack(fill="x", padx=14, pady=(0, 4))
            del_canvas.pack(fill="x", padx=14, pady=(0, 4))
            refresh_del_button()
        else:
            del_canvas.pack_forget()
            move_canvas.pack_forget()
        render(search_var.get())

    def batch_delete():
        if not selected_ids:
            return
        n = len(selected_ids)
        names = ", ".join(dragons[i]["Nickname"] for i in selected_ids if i in dragons)
        if not messagebox.askyesno("Delete dragons",
                                    f"Permanently delete {n} dragon(s)?\n{names}"):
            return
        for did in list(selected_ids):
            dragons.pop(did, None)
            for tab in current_tabs.values():
                if did in tab.get("members", []):
                    tab["members"].remove(did)
        selected_ids.clear()
        persist()
        for w in right.winfo_children():
            w.destroy()
        toggle_select_mode()

    def batch_move():
        if not selected_ids:
            return
        other_accounts = [a for a in all_accounts_data.keys() if a != current_account]
        if not other_accounts:
            messagebox.showinfo("No other accounts",
                                "Create another account first from the Account Select screen.")
            return
        dlg = tk.Toplevel(win)
        dlg.title("Move Selected To")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 300, min(60 + len(other_accounts) * 46, 420))
        n = len(selected_ids)
        tk.Label(dlg, text=f"Move {n} selected dragon(s) to:",
                 fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                 font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(16, 8))

        def make_click(dest=None):
            def click():
                if not messagebox.askyesno("Confirm move",
                                            f'Move {n} dragon(s) to "{dest}"?',
                                            parent=dlg):
                    return
                for did in list(selected_ids):
                    move_dragon_to_account(did, dest)
                dlg.destroy()
                for w in right.winfo_children():
                    w.destroy()
                toggle_select_mode()
            return click

        for acc in other_accounts:
            tk.Button(dlg, text=acc, command=make_click(acc),
                       bg=PALETTE["card_fill"], fg="white", relief="flat",
                       font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT),
                       width=24).pack(pady=4)

    MAX_GRID_HEIGHT = 560

    canvas_holder = tk.Frame(left, bg=PALETTE["lair_bg"])
    canvas_holder.pack(fill="x")

    grid_canvas = tk.Canvas(canvas_holder, bg=PALETTE["lair_bg"], highlightthickness=0, height=1)
    grid_canvas.pack(side="left", fill="x", expand=True)

    scrollbar = tk.Scrollbar(canvas_holder, command=grid_canvas.yview)
    scrollbar.pack(side="right", fill="y")
    grid_canvas.configure(yscrollcommand=scrollbar.set)

    list_frame = tk.Frame(grid_canvas, bg=PALETTE["lair_bg"])
    list_window_id = grid_canvas.create_window((0, 0), window=list_frame, anchor="nw")
    grid_canvas.bind("<Configure>", lambda e: grid_canvas.itemconfig(list_window_id, width=e.width))

    _resize_job = {"id": None}

    def _on_grid_resize(_e=None):
        if _resize_job["id"] is not None:
            win.after_cancel(_resize_job["id"])
        _resize_job["id"] = win.after(150, lambda: render(search_var.get()))

    grid_canvas.bind("<Configure>", _on_grid_resize, add="+")

    right_outer = tk.Frame(win, bg=PALETTE["lair_bg"])
    right_outer.grid(row=0, column=1, sticky="nsew")
    right_outer.rowconfigure(0, weight=1)
    right_outer.columnconfigure(0, weight=1)

    right_canvas = tk.Canvas(right_outer, bg=PALETTE["lair_bg"], highlightthickness=0)
    right_canvas.grid(row=0, column=0, sticky="nsew")
    right_vscroll = tk.Scrollbar(right_outer, orient="vertical", command=right_canvas.yview)
    right_vscroll.grid(row=0, column=1, sticky="ns")
    right_canvas.configure(yscrollcommand=right_vscroll.set)
    bind_mousewheel(right_canvas)

    right = tk.Frame(right_canvas, bg=PALETTE["lair_bg"])
    right_window_id = right_canvas.create_window((0, 0), window=right, anchor="nw")

    def _sync_right_width(_e=None):
        canvas_w = right_canvas.winfo_width()
        right_canvas.itemconfig(right_window_id, width=canvas_w)
        right_canvas.configure(scrollregion=right_canvas.bbox("all"))

    right_canvas.bind("<Configure>", _sync_right_width)
    right.bind("<Configure>", _sync_right_width)

    def rebuild_tab_bar():
        for w in tab_inner.winfo_children():
            w.destroy()

        def make_tab_btn(tab_id, label, is_all=False):
            is_active = active_tab["id"] == tab_id
            fill = PALETTE["badge_fill"] if is_active else PALETTE["tag_fill"]
            text_color = "#3A2A06" if is_active else "white"
            btn_w = max(70, len(label) * 9 + 24)

            wrapper = tk.Frame(tab_inner, bg=PALETTE["lair_bg"])
            wrapper.pack(side="left", padx=(0, 4))

            c = tk.Canvas(wrapper, width=btn_w, height=30, bg=PALETTE["lair_bg"], highlightthickness=0)
            c.pack(side="left")
            round_rect(c, 1, 1, btn_w - 1, 29, r=10, fill=fill, outline=PALETTE["panel_border"], width=2)
            c.create_text(btn_w // 2, 15, text=label,
                          fill=text_color, font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT))
            c.bind("<Button-1>", lambda _e: select_tab(tab_id))

            if not is_all:
                ren = tk.Label(wrapper, text="✎", fg="#CCC", bg=PALETTE["card_fill"],
                                font=(APP_FONT_FAMILY, 8, APP_FONT_WEIGHT), cursor="hand2",
                                padx=2, pady=0, height=1)
                ren.pack(side="left", padx=(1, 0))
                ren.bind("<Button-1>", lambda _e, t=tab_id, n=label: open_rename_tab(t, n))

                dlt = tk.Label(wrapper, text="✕", fg="#FF8888", bg=PALETTE["card_fill"],
                                font=(APP_FONT_FAMILY, 8, APP_FONT_WEIGHT), cursor="hand2",
                                padx=2, pady=0, height=1)
                dlt.pack(side="left", padx=(1, 0))
                dlt.bind("<Button-1>", lambda _e, t=tab_id: confirm_delete_tab(t))

        make_tab_btn(None, "All Dragons", is_all=True)
        for tab_id, tab in current_tabs.items():
            make_tab_btn(tab_id, tab["name"])

        new_c = tk.Canvas(tab_inner, width=80, height=30, bg=PALETTE["lair_bg"], highlightthickness=0)
        new_c.pack(side="left", padx=(0, 4))
        round_rect(new_c, 1, 1, 79, 29, r=10, fill=PALETTE["card_fill"],
                    outline=PALETTE["panel_border"], width=2)
        new_c.create_text(40, 15, text="+ New Tab", fill=PALETTE["label_text"],
                           font=(APP_FONT_FAMILY, 8, APP_FONT_WEIGHT))
        new_c.bind("<Button-1>", lambda _e: open_new_tab_dialog())

        tab_inner.update_idletasks()
        tab_scroll_canvas.configure(scrollregion=tab_scroll_canvas.bbox("all"))

    def select_tab(tab_id):
        active_tab["id"] = tab_id
        rebuild_tab_bar()
        render(search_var.get())

    def confirm_delete_tab(tab_id):
        name = current_tabs.get(tab_id, {}).get("name", "this tab")
        if messagebox.askyesno("Delete tab", f'Delete "{name}"? Dragons won\'t be removed.'):
            if active_tab["id"] == tab_id:
                active_tab["id"] = None
            delete_tab(tab_id)
            rebuild_tab_bar()
            render(search_var.get())

    def open_rename_tab(tab_id, current_name):
        dlg = tk.Toplevel(win)
        dlg.title("Rename Tab")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 320, 170)
        tk.Label(dlg, text="New name (max 22 chars):", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                 font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(18, 4))
        var = tk.StringVar(value=current_name)
        e = tk.Entry(dlg, textvariable=var, bg=PALETTE["tag_fill"], fg="white",
                      insertbackground="white", relief="flat", font=(APP_FONT_FAMILY, 11))
        e.pack(fill="x", padx=20)
        e.config(validate="key", validatecommand=(dlg.register(lambda s: len(s) <= 22), "%P"))
        def save():
            n = var.get().strip()
            if not n:
                return
            if len(n) > 22:
                messagebox.showwarning("Too long", "Tab name must be 22 characters or less.", parent=dlg)
                return
            rename_tab(tab_id, n)
            rebuild_tab_bar()
            dlg.destroy()
        tk.Button(dlg, text="Save", command=save, bg=PALETTE["bar_fill"], fg="#16330F",
                   relief="flat", font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(pady=14)
        e.bind("<Return>", lambda _e: save())
        e.focus_set()

    def open_new_tab_dialog():
        dlg = tk.Toplevel(win)
        dlg.title("New Tab")
        dlg.configure(bg=PALETTE["bg_outer"])
        center(dlg, 320, 170)
        tk.Label(dlg, text="Tab name (max 22 chars):", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                 font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(18, 4))
        var = tk.StringVar()
        e = tk.Entry(dlg, textvariable=var, bg=PALETTE["tag_fill"], fg="white",
                      insertbackground="white", relief="flat", font=(APP_FONT_FAMILY, 11))
        e.pack(fill="x", padx=20)
        e.config(validate="key", validatecommand=(dlg.register(lambda s: len(s) <= 22), "%P"))
        def create():
            n = var.get().strip()
            if not n:
                return
            if len(n) > 22:
                messagebox.showwarning("Too long", "Tab name must be 22 characters or less.", parent=dlg)
                return
            new_id = create_tab(n)
            rebuild_tab_bar()
            select_tab(new_id)
            dlg.destroy()
        tk.Button(dlg, text="Create", command=create, bg=PALETTE["bar_fill"], fg="#16330F",
                   relief="flat", font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(pady=14)
        e.bind("<Return>", lambda _e: create())
        e.focus_set()

    def matches(d, ft):
        if not ft:
            return True
        haystack = [d.get("Nickname", ""), d.get("Species", ""),
                    d.get("CosmeticTrait", ""), d.get("Element", "")]
        haystack.extend(d.get("Colors", {}).values())
        return any(ft in str(h).lower() for h in haystack)

    def sort_key(item):
        _id, dd = item
        mode = sort_var.get()
        if mode == "Level":
            try:
                return (0, float(dd.get("Level", 0)))
            except (TypeError, ValueError):
                return (1, str(dd.get("Level", "")).lower())
        if mode == "Species":
            return (0, dd.get("Species", "").lower())
        if mode == "Gender":
            return (0, dd.get("Gender", "").lower())
        return (0, dd.get("Nickname", "").lower())

    def render(filter_text=""):
        for w in list_frame.winfo_children():
            w.destroy()

        tab_id = active_tab["id"]
        tab_members = set(current_tabs[tab_id]["members"]) if tab_id else None

        ft = filter_text.lower()
        all_items = [(i, d) for i, d in dragons.items() if matches(d, ft)]
        if tab_members is not None:
            all_items = [(i, d) for i, d in all_items if i in tab_members]
        all_items.sort(key=sort_key)

        CARD_FOOTPRINT = 150 + 2 * 8
        avail_w = grid_canvas.winfo_width()
        cols = max(1, avail_w // CARD_FOOTPRINT) if avail_w > 1 else 2

        row = col = 0
        for dragon_id, d in all_items:
            if select_mode["on"]:
                card = make_dragon_card(list_frame, dragon_id, d, lambda _n: None)
                card.grid(row=row, column=col, padx=8, pady=8)
                is_sel = dragon_id in selected_ids
                card.delete("sel_overlay")
                box_c = PALETTE["badge_fill"] if is_sel else PALETTE["tag_fill"]
                box_outline = PALETTE["badge_border"] if is_sel else PALETTE["panel_border"]
                bx, by, bsz = 6, 6, 18
                round_rect(card, bx, by, bx + bsz, by + bsz, r=4,
                            fill=box_c, outline=box_outline, width=2)
                if is_sel:
                    card.create_text(bx + bsz // 2, by + bsz // 2, text="\u2714",
                                      fill="white", font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT))

                def make_toggle(did=dragon_id, c=card):
                    def toggle(_event=None):
                        if did in selected_ids:
                            selected_ids.discard(did)
                        else:
                            selected_ids.add(did)
                        refresh_del_button()
                        render(search_var.get())
                    return toggle

                card.bind("<Button-1>", make_toggle())
            else:
                card = make_dragon_card(list_frame, dragon_id, d,
                                         lambda n=dragon_id: show_details(win, right, n, render, active_tab))
                card.grid(row=row, column=col, padx=8, pady=8)

                if tab_id is not None:
                    rem = tk.Label(card, text="✕", fg="#FF8888", bg=PALETTE["lair_bg"],
                                    font=(APP_FONT_FAMILY, 8, APP_FONT_WEIGHT), cursor="hand2")
                    rem.place(x=card.winfo_reqwidth() - 14, y=2)
                    rem.bind("<Button-1>", lambda _e, did=dragon_id, tid=tab_id: (
                        remove_dragon_from_tab(tid, did), render(search_var.get())))

            col += 1
            if col >= cols:
                col = 0
                row += 1

        if not all_items:
            tab_name = current_tabs.get(tab_id, {}).get("name", "") if tab_id else ""
            if ft:
                msg = "No dragons match your search"
            elif tab_id:
                msg = f'No dragons in "{tab_name}" yet\nOpen a dragon\'s card and tap + to add'
            else:
                msg = "No dragons yet —\ntap + Add Dragon to add one"
            tk.Label(list_frame, text=msg, fg=PALETTE["label_text"], bg=PALETTE["lair_bg"],
                     font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT), justify="center",
                     wraplength=320).pack(pady=50)

        list_frame.update_idletasks()
        content_h = max(1, list_frame.winfo_reqheight())
        grid_canvas.configure(height=min(content_h, MAX_GRID_HEIGHT))
        grid_canvas.configure(scrollregion=grid_canvas.bbox("all"))

    search_var.trace_add("write", lambda *_: render(search_var.get()))
    sort_var.trace_add("write", lambda *_: render(search_var.get()))
    rebuild_tab_bar()
    render()

    bind_mousewheel(grid_canvas)


def element_icon_path(element):
    return os.path.join(ICON_DIR, f"{element.lower().replace(' ', '_')}.png")


def legendary_shift_path(element):
    return os.path.join(LEGENDARY_SHIFT_DIR, f"{element.lower().replace(' ', '_')}.png")


def gender_icon_path(gender):
    return os.path.join(MISC_DIR, f"{gender.lower()}.png")


def custom_dragon_image_path(dragon_id):
    return os.path.join(DRAGON_IMAGES_DIR, f"{dragon_id}.png")


def import_dragon_custom_image(source, dragon_id):
    try:
        img = source if isinstance(source, Image.Image) else Image.open(source)
        img = img.convert("RGBA")
        img = autocrop_to_content(img)
        img.thumbnail((200, 200), Image.LANCZOS)
        dest = custom_dragon_image_path(dragon_id)
        img.save(dest, "PNG", optimize=True)
        return dest
    except Exception as e:
        print(f"[custom icon] Failed to import {source!r}: {e}")
        return None


def cosmetic_trait_icon_path(trait):
    import re as _re
    safe = _re.sub(r'[\\/:*?"<>|]', '', trait)
    base = safe.lower().replace(" ", "_")
    base_nospace = safe.lower().replace(" ", "")
    candidates = [
        f"{base}_icon.png",
        f"{base}.png",
        f"{base_nospace}_icon.png",
        f"{base_nospace}.png",
    ]
    try:
        existing = {f.lower(): f for f in os.listdir(COSMETIC_TRAIT_ICON_DIR)}
    except Exception:
        existing = {}
    for candidate in candidates:
        match = existing.get(candidate.lower())
        if match:
            return os.path.join(COSMETIC_TRAIT_ICON_DIR, match)
    return os.path.join(COSMETIC_TRAIT_ICON_DIR, candidates[0])


def make_element_picker(parent, initial=None):
    wrap_outer = tk.Frame(parent, bg=PALETTE["bg_outer"])
    selected = {"value": initial or (ELEMENT_LIST[0] if ELEMENT_LIST else None)}
    cells = {}

    search_holder, filter_var = styled_entry(wrap_outer, width=400, height=30,
                                              default=selected["value"] or "")
    search_holder.pack(pady=(0, 6))

    grid_holder = tk.Frame(wrap_outer, bg=PALETTE["bg_outer"])
    grid_holder.pack()

    GRID_W, GRID_H, COLS = 360, 220, 4
    CELL_W, CELL_H = 80, 78

    grid_canvas = tk.Canvas(grid_holder, width=GRID_W, height=GRID_H, bg=PALETTE["bg_outer"], highlightthickness=0)
    grid_canvas.pack(side="left")
    grid_scroll = tk.Scrollbar(grid_holder, command=grid_canvas.yview)
    grid_scroll.pack(side="left", fill="y")
    grid_canvas.configure(yscrollcommand=grid_scroll.set)
    bind_mousewheel(grid_canvas)

    inner = tk.Frame(grid_canvas, bg=PALETTE["bg_outer"])
    grid_canvas.create_window((0, 0), window=inner, anchor="nw")

    def refresh_highlight():
        for el, (_cell, border_id) in cells.items():
            is_sel = (el == selected["value"])
            _cell.itemconfig(border_id, outline=PALETTE["title_fill"] if is_sel else PALETTE["bg_outer"])

    def render_grid(filter_text=""):
        for w in inner.winfo_children():
            w.destroy()
        cells.clear()

        ft = filter_text.lower()
        col = row = 0
        for el in ELEMENT_LIST:
            if ft and ft not in el.lower():
                continue

            cell = tk.Canvas(inner, width=CELL_W, height=CELL_H,
                              bg=PALETTE["bg_outer"], highlightthickness=0)
            cell.grid(row=row, column=col, padx=2, pady=2)
            cell._refs = []

            border_id = round_rect(cell, 1, 1, CELL_W - 1, CELL_H - 1, r=10,
                                    fill="", outline=PALETTE["bg_outer"], width=3)

            try:
                img = Image.open(element_icon_path(el)).convert("RGBA")
                img = autocrop_to_content(img)
                img = fit_contain(img, 40, 40)
                photo = ImageTk.PhotoImage(img)
                cell._refs.append(photo)
                cell.create_image(CELL_W / 2, 26, image=photo)
            except Exception:
                draw_orb(cell, CELL_W / 2, 26, 16, get_element_color(el))

            cell.create_text(CELL_W / 2, 58, text=el, fill=PALETTE["label_text"],
                              font=(APP_FONT_FAMILY, 7, APP_FONT_WEIGHT), width=CELL_W - 6, justify="center")

            def select(_event=None, el=el):
                selected["value"] = el
                filter_var.set(el)
                refresh_highlight()

            cell.bind("<Button-1>", select)
            cells[el] = (cell, border_id)

            col += 1
            if col >= COLS:
                col = 0
                row += 1

        inner.update_idletasks()
        grid_canvas.configure(scrollregion=grid_canvas.bbox("all"))
        refresh_highlight()

    filter_var.trace_add("write", lambda *_: render_grid(filter_var.get()))
    render_grid()

    return wrap_outer, selected


def styled_entry(parent, width=420, height=34, default=""):
    holder = tk.Canvas(parent, width=width, height=height, bg=PALETTE["bg_outer"], highlightthickness=0)
    round_rect(holder, 2, 2, width - 2, height - 2, r=12,
                fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"], width=2)
    var = tk.StringVar(value=default)
    entry = tk.Entry(holder, textvariable=var, bg=PALETTE["tag_fill"], fg="white",
                      insertbackground="white", relief="flat", font=(APP_FONT_FAMILY, 11))
    holder.create_window(width / 2, height / 2, window=entry, width=width - 24)
    return holder, var


def labeled_field(parent, label_text):
    wrap = tk.Frame(parent, bg=PALETTE["bg_outer"])
    wrap.pack(fill="x", padx=20, pady=(10, 2))
    tk.Label(wrap, text=label_text, fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(anchor="w")
    return wrap


def labeled_entry(parent, label_text, default=""):
    wrap = labeled_field(parent, label_text)
    holder, var = styled_entry(wrap, width=420, height=34, default=default)
    holder.pack()
    return var


def labeled_spinbox(parent, label_text, from_, to, default=1):
    wrap = labeled_field(parent, label_text)
    var = tk.IntVar(value=max(from_, min(to, default)))
    spin = tk.Spinbox(wrap, from_=from_, to=to, textvariable=var,
                       bg=PALETTE["tag_fill"], fg="white",
                       insertbackground="white", relief="flat",
                       buttonbackground=PALETTE["card_fill"],
                       font=(APP_FONT_FAMILY, 11), justify="center")
    spin.pack(fill="x", pady=(2, 0), ipady=4)
    return var


def labeled_birthday_picker(parent, label_text, default_enabled=False, default_value=None):
    wrap = labeled_field(parent, label_text)

    current_year = date.today().year
    year_choices = [str(y) for y in range(current_year, BIRTHDAY_MIN_YEAR - 1, -1)]

    def_day, def_month, def_year = 1, 1, current_year
    if default_value:
        try:
            dt = date.fromisoformat(default_value)
            def_day, def_month, def_year = dt.day, dt.month, dt.year
        except Exception:
            pass

    enabled_var = tk.BooleanVar(value=default_enabled)
    tk.Checkbutton(wrap, text="Set a birthday", variable=enabled_var,
                    bg=PALETTE["bg_outer"], fg="white", selectcolor=PALETTE["tag_fill"],
                    activebackground=PALETTE["bg_outer"], activeforeground="white",
                    font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT),
                    command=lambda: set_enabled_state()).pack(anchor="w", pady=(2, 4))

    row = tk.Frame(wrap, bg=PALETTE["bg_outer"])
    row.pack(fill="x")

    day_var = tk.StringVar(value=str(def_day))
    month_var = tk.StringVar(value=MONTH_NAMES[def_month - 1])
    year_var = tk.StringVar(value=str(def_year))

    day_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    day_col.pack(side="left", padx=(0, 5))
    tk.Label(day_col, text="Day", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    day_combo = ttk.Combobox(day_col, textvariable=day_var, width=5, state="readonly",
                              style="Dragon.TCombobox", font=(APP_FONT_FAMILY, 10))
    day_combo.pack()

    month_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    month_col.pack(side="left", padx=5)
    tk.Label(month_col, text="Month", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    month_combo = ttk.Combobox(month_col, textvariable=month_var, values=MONTH_NAMES,
                                width=11, state="readonly", style="Dragon.TCombobox",
                                font=(APP_FONT_FAMILY, 10))
    month_combo.pack()

    year_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    year_col.pack(side="left", padx=(5, 0))
    tk.Label(year_col, text="Year", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    year_combo = ttk.Combobox(year_col, textvariable=year_var, values=year_choices,
                               width=7, state="readonly", style="Dragon.TCombobox",
                               font=(APP_FONT_FAMILY, 10))
    year_combo.pack()

    def refresh_day_options(*_args):
        try:
            m = MONTH_NAMES.index(month_var.get()) + 1
            y = int(year_var.get())
        except (ValueError, IndexError):
            m, y = 1, current_year
        days_in_month = calendar.monthrange(y, m)[1]
        day_combo["values"] = [str(d) for d in range(1, days_in_month + 1)]
        if int(day_var.get() or 1) > days_in_month:
            day_var.set(str(days_in_month))

    month_var.trace_add("write", refresh_day_options)
    year_var.trace_add("write", refresh_day_options)
    refresh_day_options()

    def set_enabled_state():
        state = "readonly" if enabled_var.get() else "disabled"
        for combo in (day_combo, month_combo, year_combo):
            combo.configure(state=state)

    set_enabled_state()

    def get_iso_or_none():
        if not enabled_var.get():
            return None
        try:
            m = MONTH_NAMES.index(month_var.get()) + 1
            return date(int(year_var.get()), m, int(day_var.get())).isoformat()
        except Exception:
            return None

    return enabled_var, day_var, month_var, year_var, get_iso_or_none


def labeled_trait_row(parent, label_text, trait_list, trait_default=None, tier_default=1):
    wrap = labeled_field(parent, label_text)
    row = tk.Frame(wrap, bg=PALETTE["bg_outer"])
    row.pack(fill="x", pady=(2, 0))

    trait_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    trait_col.pack(side="left", fill="x", expand=True, padx=(0, 5))
    tk.Label(trait_col, text="Trait", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    trait_var = tk.StringVar(value=trait_default if trait_default in trait_list else trait_list[0])
    trait_combo = ttk.Combobox(trait_col, textvariable=trait_var, values=trait_list, state="readonly",
                                style="Dragon.TCombobox", font=(APP_FONT_FAMILY, 10))
    trait_combo.pack(fill="x")

    tier_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    tier_col.pack(side="left", padx=(5, 0))
    tk.Label(tier_col, text="Tier", fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    tier_var = tk.IntVar(value=max(TRAIT_TIER_MIN, min(TRAIT_TIER_MAX, tier_default or TRAIT_TIER_MIN)))
    tk.Spinbox(tier_col, from_=TRAIT_TIER_MIN, to=TRAIT_TIER_MAX, textvariable=tier_var, width=4,
               bg=PALETTE["tag_fill"], fg="white", insertbackground="white", relief="flat",
               buttonbackground=PALETTE["card_fill"], font=(APP_FONT_FAMILY, 10), justify="center").pack()

    return trait_var, tier_var, trait_combo


def make_search_select(parent, values_or_getter, initial=None, height=5, width=420):
    def get_base():
        return values_or_getter() if callable(values_or_getter) else values_or_getter

    base_now = get_base()
    if initial in base_now:
        start_value = initial
    elif initial:
        start_value = next((b for b in base_now if b.lower() == str(initial).lower()), None) \
                      or (base_now[0] if base_now else "")
    else:
        start_value = base_now[0] if base_now else ""
    var = tk.StringVar(value=start_value)

    wrap = tk.Frame(parent, bg=PALETTE["bg_outer"])

    search_holder, search_var = styled_entry(wrap, width=width, height=32, default=start_value)
    search_holder.pack()

    search_entry = None
    for child in search_holder.winfo_children():
        if isinstance(child, tk.Entry):
            search_entry = child
            break

    if search_entry:
        search_entry.config(fg=PALETTE["title_fill"])

    list_holder = tk.Frame(wrap, bg=PALETTE["bg_outer"])
    list_holder.pack(fill="x", pady=(4, 0))
    listbox = tk.Listbox(list_holder, height=height, bg=PALETTE["tag_fill"], fg="white",
                          selectbackground=PALETTE["card_fill"], selectforeground="white",
                          relief="flat", font=(APP_FONT_FAMILY, 10), highlightthickness=1,
                          highlightbackground=PALETTE["panel_border"], exportselection=False,
                          activestyle="none")
    listbox.pack(side="left", fill="both", expand=True)
    scroll = tk.Scrollbar(list_holder, command=listbox.yview)
    scroll.pack(side="right", fill="y")
    listbox.configure(yscrollcommand=scroll.set)

    _typing = {"v": False}

    def on_focus_in(_e=None):
        if not _typing["v"]:
            search_var.set("")
            if search_entry:
                search_entry.config(fg="white")

    def on_focus_out(_e=None):
        if not search_var.get().strip():
            search_var.set(var.get())
            if search_entry:
                search_entry.config(fg=PALETTE["title_fill"])
            _typing["v"] = False

    def refresh(*_args):
        typed = search_var.get().strip().lower()
        base = get_base()
        if typed and typed != var.get().lower():
            _typing["v"] = True
            filtered = [v for v in base if typed in v.lower()]
        else:
            _typing["v"] = False
            filtered = base
        listbox.delete(0, "end")
        for v in filtered:
            listbox.insert("end", v)
        if var.get() in filtered:
            listbox.selection_set(filtered.index(var.get()))

    def on_pick(_event=None):
        sel = listbox.curselection()
        if sel:
            var.set(listbox.get(sel[0]))
            search_var.set(var.get())
            if search_entry:
                search_entry.config(fg=PALETTE["title_fill"])
            _typing["v"] = False

    if search_entry:
        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)

    search_var.trace_add("write", refresh)
    listbox.bind("<<ListboxSelect>>", on_pick)
    refresh()

    return wrap, var, refresh


def labeled_search_select(parent, label_text, values_or_getter, default=None, height=5):
    wrap = labeled_field(parent, label_text)
    field, var, refresh = make_search_select(wrap, values_or_getter, initial=default, height=height, width=420)
    field.pack()
    return var, refresh


def labeled_double_search(parent, label_text, left_label, left_values, right_label, right_values,
                           left_default=None, right_default=None, height=4):
    wrap = labeled_field(parent, label_text)
    row = tk.Frame(wrap, bg=PALETTE["bg_outer"])
    row.pack(fill="x", pady=(2, 0))

    left_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    left_col.pack(side="left", fill="both", expand=True, padx=(0, 5))
    tk.Label(left_col, text=left_label, fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    lfield, lvar, lrefresh = make_search_select(left_col, left_values, initial=left_default,
                                                 height=height, width=190)
    lfield.pack(fill="x")

    right_col = tk.Frame(row, bg=PALETTE["bg_outer"])
    right_col.pack(side="left", fill="both", expand=True, padx=(5, 0))
    tk.Label(right_col, text=right_label, fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w")
    rfield, rvar, rrefresh = make_search_select(right_col, right_values, initial=right_default,
                                                 height=height, width=190)
    rfield.pack(fill="x")

    return lvar, rvar, lrefresh, rrefresh


def labeled_combo(parent, label_text, values, default=None):
    wrap = labeled_field(parent, label_text)
    var = tk.StringVar(value=default if default is not None else (values[0] if values else ""))
    combo = ttk.Combobox(wrap, textvariable=var, values=values, state="readonly",
                          style="Dragon.TCombobox", font=(APP_FONT_FAMILY, 11))
    combo.pack(fill="x", pady=(2, 0))
    return var, combo


def open_dragon_form(parent_win, refresh_callback, dragon_id=None):
    editing = dragon_id is not None
    d = dragons.get(dragon_id, {}) if editing else {}
    pending_id = dragon_id if editing else uuid.uuid4().hex[:10]

    form = tk.Toplevel(parent_win)
    form.title("Edit Dragon" if editing else "Add New Dragon")
    form.configure(bg=PALETTE["bg_outer"])
    center(form, 480, 700)

    _traces = []

    def _traced(var, mode, cb):
        tid = var.trace_add(mode, cb)
        _traces.append((var, mode, tid))
        return tid

    def _cleanup_traces():
        for v, m, tid in _traces:
            try:
                v.trace_remove(m, tid)
            except Exception:
                pass

    form.bind("<Destroy>", lambda _e: _cleanup_traces())

    outer_canvas = tk.Canvas(form, bg=PALETTE["bg_outer"], highlightthickness=0)
    outer_canvas.pack(side="left", fill="both", expand=True)
    vscroll = tk.Scrollbar(form, command=outer_canvas.yview)
    vscroll.pack(side="right", fill="y")
    outer_canvas.configure(yscrollcommand=vscroll.set)

    body = tk.Frame(outer_canvas, bg=PALETTE["bg_outer"])
    outer_canvas.create_window((0, 0), window=body, anchor="nw", width=460)
    body.bind("<Configure>", lambda _e: outer_canvas.configure(scrollregion=outer_canvas.bbox("all")))

    def _form_scroll_route(event):
        w = event.widget
        cur = w
        while cur:
            if isinstance(cur, tk.Listbox):
                cur.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return "break"
            cur = getattr(cur, "master", None)
        outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def _bind_form_scroll(_e=None):
        form.bind_all("<MouseWheel>", _form_scroll_route)

    def _unbind_form_scroll(_e=None):
        form.unbind_all("<MouseWheel>")

    outer_canvas.bind("<Enter>", _bind_form_scroll)
    outer_canvas.bind("<Leave>", _unbind_form_scroll)
    form.bind("<Destroy>", lambda _e: (_unbind_form_scroll(), None), add=True)

    tk.Label(body, text="Edit Dragon" if editing else "Add New Dragon",
             fg=PALETTE["title_fill"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 18, APP_FONT_WEIGHT)).pack(pady=(16, 4))

    img_row = tk.Frame(body, bg=PALETTE["bg_outer"])
    img_row.pack(pady=10)
    preview_canvas = tk.Canvas(img_row, width=100, height=100, bg=PALETTE["bg_outer"], highlightthickness=0)
    preview_canvas.pack(side="left", padx=(0, 12))

    has_custom_icon = {"val": os.path.exists(custom_dragon_image_path(pending_id))}

    def update_preview():
        preview_canvas.delete("all")
        round_rect(preview_canvas, 2, 2, 98, 98, r=14, fill="#2A2143",
                    outline=PALETTE["panel_border"], width=2)
        try:
            if has_custom_icon["val"] and dragon_id:
                icon_path = custom_dragon_image_path(dragon_id)
            else:
                icon_path = species_icon_path(species_var.get())
            photo = make_rounded_photo(icon_path, 90, 90, radius=12)
            preview_canvas._ref = photo
            preview_canvas.create_image(50, 50, image=photo)
        except Exception:
            preview_canvas.create_text(50, 50, text="No\nIcon", fill="#9B8FCC",
                                        font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), justify="center")

    icon_btn_col = tk.Frame(img_row, bg=PALETTE["bg_outer"])
    icon_btn_col.pack(side="left")

    def browse_custom_icon():
        from tkinter import filedialog as _tkfd
        path = _tkfd.askopenfilename(
            title="Choose a custom dragon icon",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if not path:
            return
        temp_id = pending_id
        result = import_dragon_custom_image(path, temp_id)
        if result:
            has_custom_icon["val"] = True
            update_preview()
            custom_label.config(text="Custom icon set")

    def paste_custom_icon(_event=None):
        if _event is not None:
            focused = img_row.winfo_toplevel().focus_get()
            if isinstance(focused, (tk.Entry, tk.Text)):
                return
        try:
            clip = ImageGrab.grabclipboard()
        except Exception as e:
            messagebox.showwarning("Paste failed", f"Couldn't read the clipboard: {e}", parent=img_row.winfo_toplevel())
            return
        if clip is None:
            messagebox.showinfo("Nothing to paste",
                                 "No image found on the clipboard. Copy an image "
                                 "(e.g. a screenshot, or an image from a browser) first.",
                                 parent=img_row.winfo_toplevel())
            return
        if isinstance(clip, list):
            if not clip:
                messagebox.showinfo("Nothing to paste", "No image found on the clipboard.",
                                     parent=img_row.winfo_toplevel())
                return
            clip = clip[0]
            if isinstance(clip, str) and os.path.isfile(clip):
                temp_id = pending_id
                result = import_dragon_custom_image(clip, temp_id)
                if result:
                    has_custom_icon["val"] = True
                    update_preview()
                    custom_label.config(text="Custom icon set")
                return
        temp_id = pending_id
        result = import_dragon_custom_image(clip, temp_id)
        if result:
            has_custom_icon["val"] = True
            update_preview()
            custom_label.config(text="Custom icon set")

    def clear_custom_icon():
        p = custom_dragon_image_path(pending_id)
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass
        has_custom_icon["val"] = False
        update_preview()
        custom_label.config(text="Using species default")

    tk.Button(icon_btn_col, text="Upload Icon…", command=browse_custom_icon,
               bg=PALETTE["tag_fill"], fg="white", relief="flat",
               font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), pady=4).pack(fill="x", pady=(0, 4))
    tk.Button(icon_btn_col, text="Paste Icon (Ctrl+V)", command=paste_custom_icon,
               bg=PALETTE["tag_fill"], fg="white", relief="flat",
               font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), pady=4).pack(fill="x", pady=(0, 4))
    tk.Button(icon_btn_col, text="Clear Custom", command=clear_custom_icon,
               bg=PALETTE["row_fill"], fg="white", relief="flat",
               font=(APP_FONT_FAMILY, 9, APP_FONT_WEIGHT), pady=4).pack(fill="x")
    custom_label = tk.Label(icon_btn_col,
                             text="Custom icon set" if has_custom_icon["val"] else "Using species default",
                             fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                             font=(APP_FONT_FAMILY, 8), wraplength=120, justify="left")
    custom_label.pack(anchor="w", pady=(6, 0))
    _paste_toplevel = img_row.winfo_toplevel()
    _paste_toplevel.bind("<Control-v>", paste_custom_icon)
    _paste_toplevel.bind("<Control-V>", paste_custom_icon)

    nickname_var = labeled_entry(body, "Nickname", default=d.get("Nickname", ""))

    species_var, _species_refresh = labeled_search_select(body, "Species", SPECIES_LIST,
                                                            default=d.get("Species"), height=5)

    rarity_var = tk.StringVar(value=d.get("Rarity", "Common"))

    def sync_rarity_to_species(*_args):
        known_rarity = SPECIES_RARITY.get(species_var.get())
        if known_rarity:
            rarity_var.set(known_rarity)

    _traced(species_var, "write", sync_rarity_to_species)
    _traced(species_var, "write", lambda *_: update_preview())
    sync_rarity_to_species()
    update_preview()

    gender_var, _gender_combo = labeled_combo(body, "Gender", GENDER_LIST, default=d.get("Gender", GENDER_LIST[0]))

    soulbound_wrap = labeled_field(body, "Soulbound")
    soulbound_var = tk.BooleanVar(value=bool(d.get("Soulbound", False)))
    tk.Checkbutton(soulbound_wrap, text="This dragon is soulbound", variable=soulbound_var,
                    bg=PALETTE["bg_outer"], fg="white", selectcolor=PALETTE["tag_fill"],
                    activebackground=PALETTE["bg_outer"], activeforeground="white",
                    font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT)).pack(anchor="w", pady=(2, 0))

    bday_enabled, bday_day, bday_month, bday_year, get_birthday_iso = labeled_birthday_picker(
        body, "Birthday (optional)",
        default_enabled=bool(d.get("Birthday")), default_value=d.get("Birthday"))

    owner_enabled_wrap = labeled_field(body, "Original Owner (optional)")
    owner_enabled_var = tk.BooleanVar(value=bool(d.get("OriginalOwner")))
    owner_text_var = tk.StringVar(value=d.get("OriginalOwner", ""))

    tk.Checkbutton(owner_enabled_wrap, text="Track original owner", variable=owner_enabled_var,
                    bg=PALETTE["bg_outer"], fg="white", selectcolor=PALETTE["tag_fill"],
                    activebackground=PALETTE["bg_outer"], activeforeground="white",
                    font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT),
                    command=lambda: set_owner_state()).pack(anchor="w", pady=(2, 4))

    owner_holder = tk.Canvas(owner_enabled_wrap, width=420, height=34,
                              bg=PALETTE["bg_outer"], highlightthickness=0)
    owner_holder.pack()
    round_rect(owner_holder, 2, 2, 418, 32, r=12,
                fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"], width=2)
    owner_entry_widget = tk.Entry(owner_holder, textvariable=owner_text_var,
                                   bg=PALETTE["tag_fill"], fg="white",
                                   insertbackground="white", relief="flat",
                                   font=(APP_FONT_FAMILY, 11))
    owner_holder.create_window(210, 17, window=owner_entry_widget, width=396)

    def set_owner_state():
        owner_entry_widget.configure(state="normal" if owner_enabled_var.get() else "disabled")

    set_owner_state()

    _level_raw = d.get("Level", 1)
    level_default = int(_level_raw) if str(_level_raw).isdigit() else 1
    level_var = labeled_spinbox(body, "Level (1-50)", 1, 50, default=level_default)
    generation_var = labeled_entry(body, "Generation", default=str(d.get("Generation", "1")))
    rebirths_var = labeled_spinbox(body, "Rebirths", 0, 99, default=int(d.get("Rebirths", 0)))
    age_default = d.get("Age") if d.get("Age") in AGE_LIST else AGE_LIST[0]
    age_var, _age_combo = labeled_combo(body, "Age", AGE_LIST, default=age_default)

    d_colors = d.get("Colors", {})
    d_materials = d.get("Materials", {})

    color_vars = []

    def color_values_for(slot_index):
        def getter():
            legendary_slot = next((i for i, v in enumerate(color_vars) if v.get() == "Legendary"), None)
            non_legendary = [c for c in COLOR_LIST if c != "Legendary"]
            return COLOR_LIST if (legendary_slot is None or legendary_slot == slot_index) else non_legendary
        return getter

    if current_themes:
        theme_wrap = labeled_field(body, "Apply Theme")
        theme_var = tk.StringVar(value="— select a theme —")
        theme_names = ["— select a theme —"] + [t["name"] for t in current_themes.values()]
        theme_ids = [None] + list(current_themes.keys())
        theme_combo = ttk.Combobox(theme_wrap, textvariable=theme_var, values=theme_names,
                                    state="readonly", style="Dragon.TCombobox",
                                    font=(APP_FONT_FAMILY, 10))
        theme_combo.pack(fill="x", pady=(2, 0))

        _cosmetic_ref = {}

        def apply_theme(*_args):
            idx = theme_names.index(theme_var.get()) if theme_var.get() in theme_names else 0
            if idx == 0:
                return
            tid = theme_ids[idx]
            t = current_themes.get(tid, {})
            if t.get("p_color"): p_color.set(t["p_color"])
            if t.get("s_color"): s_color.set(t["s_color"])
            if t.get("t_color"): t_color.set(t["t_color"])
            if t.get("p_material"): p_material.set(t["p_material"])
            if t.get("s_material"): s_material.set(t["s_material"])
            if t.get("t_material"): t_material.set(t["t_material"])
            cv = _cosmetic_ref.get("var")
            if cv and t.get("cosmetic_trait") and t["cosmetic_trait"] != "None":
                cv.set(t["cosmetic_trait"])

        theme_var.trace_add("write", apply_theme)

    p_color, p_material, p_color_refresh, p_material_refresh = labeled_double_search(
        body, "Primary Coat", "Color", color_values_for(0), "Material", MATERIAL_LIST,
        left_default=d_colors.get("P"), right_default=d_materials.get("P"))
    s_color, s_material, s_color_refresh, s_material_refresh = labeled_double_search(
        body, "Secondary Coat", "Color", color_values_for(1), "Material", MATERIAL_LIST,
        left_default=d_colors.get("S"), right_default=d_materials.get("S"))
    t_color, t_material, t_color_refresh, t_material_refresh = labeled_double_search(
        body, "Tertiary Coat", "Color", color_values_for(2), "Material", MATERIAL_LIST,
        left_default=d_colors.get("T"), right_default=d_materials.get("T"))

    color_vars.extend([p_color, s_color, t_color])
    color_refreshes = [p_color_refresh, s_color_refresh, t_color_refresh]

    def enforce_single_legendary(*_args):
        for refresh in color_refreshes:
            refresh()

    for var in color_vars:
        _traced(var, "write", enforce_single_legendary)
    enforce_single_legendary()

    mutations_var, _mutations_combo = labeled_combo(body, "Mutations", [str(i) for i in range(MUTATION_CAP + 1)],
                                                      default=str(d.get("Mutations", MUTATION_CAP)))
    cosmetic_var, _cosmetic_refresh = labeled_search_select(body, "Cosmetic Trait", COSMETIC_TRAIT_LIST,
                                                              default=d.get("CosmeticTrait", "None"), height=5)
    try:
        _cosmetic_ref["var"] = cosmetic_var
    except NameError:
        pass
    pupil_var, _pupil_combo = labeled_combo(body, "Pupil", PUPIL_LIST, default=d.get("Pupil"))

    elem_wrap = labeled_field(body, "Element")
    element_row, element_selected = make_element_picker(elem_wrap, initial=d.get("Element", ELEMENT_LIST[0]))
    element_row.pack(anchor="w")

    element2_var = None
    if account_settings.get("Subscription", False):
        e2_choices = ["None"] + list(ELEMENT_LIST)
        element2_var, _e2_refresh = labeled_search_select(
            body, "Element 2 (Subscription — optional)",
            e2_choices, default=d.get("Element2") or "None", height=4)

    tk.Label(body, text="Genetic Traits", fg=PALETTE["title_fill"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 16, APP_FONT_WEIGHT)).pack(pady=(20, 0))

    d_positive = d.get("PositiveTraits", [])
    d_negative = d.get("NegativeTraits", [])

    positive_trait_vars = []
    positive_trait_combos = []
    for i in range(MAX_POSITIVE_TRAITS):
        existing = d_positive[i] if i < len(d_positive) else {}
        tvar, nvar, tcombo = labeled_trait_row(body, f"Positive Trait {i + 1}", POSITIVE_TRAIT_LIST,
                                                trait_default=existing.get("Trait", "None"),
                                                tier_default=existing.get("Tier", 1))
        positive_trait_vars.append((tvar, nvar))
        positive_trait_combos.append((tvar, tcombo))

    negative_trait_vars = []
    negative_trait_combos = []
    for i in range(MAX_NEGATIVE_TRAITS):
        existing = d_negative[i] if i < len(d_negative) else {}
        tvar, nvar, tcombo = labeled_trait_row(body, f"Negative Trait {i + 1}", NEGATIVE_TRAIT_LIST,
                                                trait_default=existing.get("Trait", "None"),
                                                tier_default=existing.get("Tier", 1))
        negative_trait_vars.append((tvar, nvar))
        negative_trait_combos.append((tvar, tcombo))

    def sync_trait_options(*_args):
        sp = species_var.get()
        pos_base = available_positive_traits(sp)
        neg_base = available_negative_traits(sp)

        chosen_pos = {var.get() for var, _ in positive_trait_combos if var.get() != "None"}
        for var, combo in positive_trait_combos:
            mine = var.get()
            if mine != "None" and mine not in pos_base:
                var.set("None")
                mine = "None"
            avail = [t for t in pos_base if t == "None" or t == mine or t not in chosen_pos]
            combo["values"] = avail

        for var, combo in negative_trait_combos:
            mine = var.get()
            if mine != "None" and mine not in neg_base:
                var.set("None")
            combo["values"] = neg_base

    _traced(species_var, "write", sync_trait_options)
    for tvar, _ in positive_trait_combos:
        _traced(tvar, "write", sync_trait_options)
    sync_trait_options()

    def save_dragon():
        nickname = nickname_var.get().strip() or species_var.get()
        if len(nickname) > 20:
            messagebox.showwarning("Nickname too long",
                                    f"Nickname must be 20 characters or less (currently {len(nickname)}).")
            return

        if bday_enabled.get() and not get_birthday_iso():
            messagebox.showwarning("Invalid birthday",
                                    "Birthday is enabled but the selected date isn't valid. "
                                    "Pick a Day, Month, and Year, or turn the birthday off.")
            return

        owner_value = owner_text_var.get().strip()
        if owner_enabled_var.get() and not owner_value:
            messagebox.showwarning("Missing owner",
                                    "Original Owner is enabled but no username was entered. "
                                    "Type a username, or turn this off.")
            return

        new_id = pending_id
        gen_text = generation_var.get().strip()
        if gen_text.lstrip("-").isdigit():
            generation = max(1, int(gen_text))
        else:
            generation = gen_text or "-"
        try:
            level = max(1, min(50, int(level_var.get())))
        except (TypeError, ValueError, tk.TclError):
            level = 1
        age = age_var.get()

        def collect_traits(trait_vars):
            collected = []
            for trait_var, tier_var in trait_vars:
                trait_name = trait_var.get()
                if trait_name and trait_name != "None":
                    try:
                        tier = max(TRAIT_TIER_MIN, min(TRAIT_TIER_MAX, int(tier_var.get())))
                    except (TypeError, ValueError, tk.TclError):
                        tier = TRAIT_TIER_MIN
                    collected.append({"Trait": trait_name, "Tier": tier})
            return collected

        dragons[new_id] = {
            "Nickname": nickname,
            "Species": species_var.get(),
            "Rarity": rarity_var.get(),
            "Gender": gender_var.get(),
            "Soulbound": soulbound_var.get(),
            "Birthday": get_birthday_iso() if bday_enabled.get() else None,
            "OriginalOwner": owner_value if owner_enabled_var.get() else None,
            "Level": level,
            "Colors": {"P": p_color.get(), "S": s_color.get(), "T": t_color.get()},
            "Materials": {"P": p_material.get(), "S": s_material.get(), "T": t_material.get()},
            "Mutations": int(mutations_var.get()),
            "MaxMutations": MUTATION_CAP,
            "CosmeticTrait": cosmetic_var.get(),
            "Element": element_selected["value"],
            "Element2": (element2_var.get() if element2_var and element2_var.get() != "None" else None),
            "Pupil": pupil_var.get(),
            "Generation": generation,
            "Rebirths": int(rebirths_var.get()) if rebirths_var else 0,
            "Age": age,
            "PositiveTraits": collect_traits(positive_trait_vars),
            "NegativeTraits": collect_traits(negative_trait_vars),
        }
        persist()
        if refresh_callback:
            refresh_callback()
        form.destroy()

    button_row = tk.Canvas(body, width=420, height=50, bg=PALETTE["bg_outer"], highlightthickness=0)
    button_row.pack(pady=24)
    rounded_button(button_row, 0, 0, 200, 50, "Cancel", form.destroy, r=16,
                    fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"])
    rounded_button(button_row, 220, 0, 200, 50, "Save Changes" if editing else "Save Dragon",
                    save_dragon, r=16,
                    fill=PALETTE["bar_fill"], outline=PALETTE["bar_border"], text_fill="#16330F")

    return form


def open_add_account_dialog(root, refresh_callback):
    dialog = tk.Toplevel(root)
    dialog.title("Add Account")
    dialog.configure(bg=PALETTE["bg_outer"])
    center(dialog, 360, 350)

    tk.Label(dialog, text="New Account Name", fg=PALETTE["title_fill"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 16, APP_FONT_WEIGHT)).pack(pady=(22, 4))

    name_var = labeled_entry(dialog, "Username")

    toggle_frame = tk.Frame(dialog, bg=PALETTE["bg_outer"])
    toggle_frame.pack(fill="x", padx=30, pady=(14, 0))
    tk.Label(toggle_frame, text="These apply app-wide, for every account:",
             fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 9)).pack(anchor="w", pady=(0, 4))

    sda_var = tk.BooleanVar(value=global_settings.get("EnableSDA", True))
    elemental_var = tk.BooleanVar(value=global_settings.get("EnableElemental", True))

    def on_sda_toggle():
        global_settings["EnableSDA"] = sda_var.get()
        save_global_settings(global_settings)

    def on_elemental_toggle():
        global_settings["EnableElemental"] = elemental_var.get()
        save_global_settings(global_settings)

    tk.Checkbutton(toggle_frame, text="Enable SDA Tracker button", variable=sda_var,
                    command=on_sda_toggle, fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                    selectcolor=PALETTE["tag_fill"], activebackground=PALETTE["bg_outer"],
                    font=(APP_FONT_FAMILY, 10)).pack(anchor="w")
    tk.Checkbutton(toggle_frame, text="Enable Elemental Tracker button", variable=elemental_var,
                    command=on_elemental_toggle, fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                    selectcolor=PALETTE["tag_fill"], activebackground=PALETTE["bg_outer"],
                    font=(APP_FONT_FAMILY, 10)).pack(anchor="w")

    def create_account():
        name = name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Please enter an account name.")
            return
        if " " in name:
            messagebox.showwarning("Invalid name", "Account names cannot contain spaces.")
            return
        if len(name) > 20:
            messagebox.showwarning("Name too long",
                                    f"Account names must be 20 characters or less (currently {len(name)}).")
            return
        if name in all_accounts_data:
            messagebox.showwarning("Already exists", f'An account named "{name}" already exists.')
            return
        all_accounts_data[name] = {}
        save_all_accounts(all_accounts_data)
        refresh_callback()
        dialog.destroy()

    btn_row = tk.Canvas(dialog, width=300, height=50, bg=PALETTE["bg_outer"], highlightthickness=0)
    btn_row.pack(pady=20)
    rounded_button(btn_row, 0, 0, 140, 50, "Cancel", dialog.destroy, r=14,
                    fill=PALETTE["tag_fill"], outline=PALETTE["panel_border"])
    rounded_button(btn_row, 160, 0, 140, 50, "Create", create_account, r=14,
                    fill=PALETTE["bar_fill"], outline=PALETTE["bar_border"], text_fill="#16330F")


def _version_tuple(v):
    try:
        return tuple(int(x) for x in v.lstrip("v").split("."))
    except Exception:
        return (0,)


def _clean_tag(raw_tag):
    import re as _re
    cleaned = raw_tag.strip()
    cleaned = _re.sub(r'(?i)^lairkeeper[\s_-]*(api[\s_-]*)?', '', cleaned)
    cleaned = cleaned.lstrip('vV')
    return cleaned


def fetch_latest_release():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    req = urllib.request.Request(url, headers={"User-Agent": f"Lairkeeper/{APP_VERSION}"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        raw_tag = data.get("tag_name", "")
        tag = _clean_tag(raw_tag)
        assets = data.get("assets", [])
        print(f"[update] assets found: {[a['name'] for a in assets]}")
        dl_url = next(
            (a["browser_download_url"] for a in assets
             if a["name"].lower() == "lairkeeper.exe"),
            None,
        )
        if dl_url is None:
            dl_url = next(
                (a["browser_download_url"] for a in assets
                 if a["name"].lower().endswith(".zip")),
                None,
            )
        if dl_url is None:
            dl_url = next(
                (a["browser_download_url"] for a in assets
                 if a["name"].lower().endswith(".exe")),
                None,
            )
        print(f"[update] raw tag: {raw_tag!r}  →  parsed: {tag!r}  local: {APP_VERSION}")
        print(f"[update] download url: {dl_url}")
        return tag, dl_url
    except Exception as e:
        print(f"[update] fetch failed: {e}")
        return None, None


def check_for_updates_async(parent_win, on_result):
    def _worker():
        tag, dl_url = fetch_latest_release()
        newer = bool(tag) and _version_tuple(tag) > _version_tuple(APP_VERSION)
        print(f"[update] newer={newer}  remote={_version_tuple(tag) if tag else '?'}  local={_version_tuple(APP_VERSION)}")
        parent_win.after(0, lambda: on_result(tag, dl_url, newer))
    threading.Thread(target=_worker, daemon=True).start()


def perform_update(parent_win, dl_url):
    if not getattr(sys, "frozen", False):
        messagebox.showinfo(
            "Script mode",
            "Auto-update only works when running the compiled Lairkeeper.exe.\n"
            "To update the script version, download the latest code.py from GitHub.",
            parent=parent_win)
        return

    exe_path = sys.executable
    exe_dir = os.path.dirname(exe_path)
    tmp_exe = os.path.join(exe_dir, "Lairkeeper_update.exe")
    updater_bat = os.path.join(exe_dir, "_lk_updater.bat")

    dlg = tk.Toplevel(parent_win)
    dlg.title("Updating Lairkeeper")
    dlg.configure(bg=PALETTE["bg_outer"])
    center(dlg, 360, 120)
    dlg.resizable(False, False)
    status_var = tk.StringVar(value="Connecting…")
    tk.Label(dlg, textvariable=status_var, fg="white", bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 11, APP_FONT_WEIGHT)).pack(pady=(24, 8))
    prog_canvas = tk.Canvas(dlg, width=300, height=14, bg=PALETTE["tag_fill"],
                             highlightthickness=1, highlightbackground=PALETTE["panel_border"])
    prog_canvas.pack()
    prog_bar = prog_canvas.create_rectangle(0, 0, 0, 14, fill=PALETTE["bar_fill"], outline="")
    dlg.update()

    def _set_status(text, pct=None):
        status_var.set(text)
        if pct is not None:
            prog_canvas.coords(prog_bar, 0, 0, 300 * pct, 14)
        try:
            dlg.update_idletasks()
        except Exception:
            pass

    def _download():
        try:
            print(f"[update] downloading from: {dl_url}")
            req = urllib.request.Request(dl_url, headers={"User-Agent": f"Lairkeeper/{APP_VERSION}"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                total = int(resp.headers.get("Content-Length") or 0)
                downloaded = 0
                chunks = []
                while True:
                    block = resp.read(65536)
                    if not block:
                        break
                    chunks.append(block)
                    downloaded += len(block)
                    if total:
                        pct = downloaded / total
                        parent_win.after(0, lambda p=pct: _set_status(f"Downloading… {int(p*100)}%", p))
                    else:
                        parent_win.after(0, lambda b=downloaded: _set_status(f"Downloading… {b // 1024} KB"))

            data = b"".join(chunks)
            print(f"[update] download complete: {len(data)} bytes")

            if dl_url.lower().endswith(".zip"):
                import io as _io
                tmp_dir = os.path.join(exe_dir, "_lk_update_tmp")
                if os.path.exists(tmp_dir):
                    import shutil as _sh
                    _sh.rmtree(tmp_dir, ignore_errors=True)
                os.makedirs(tmp_dir, exist_ok=True)
                with zipfile.ZipFile(_io.BytesIO(data)) as zf:
                    print(f"[update] zip contents: {zf.namelist()}")
                    zf.extractall(tmp_dir)
                entries = os.listdir(tmp_dir)
                if len(entries) == 1 and os.path.isdir(os.path.join(tmp_dir, entries[0])):
                    src_dir = os.path.join(tmp_dir, entries[0])
                else:
                    src_dir = tmp_dir
                print(f"[update] source dir: {src_dir}")
                parent_win.after(0, lambda sd=src_dir, td=tmp_dir: _swap(sd, td))
            else:
                with open(tmp_exe, "wb") as f:
                    f.write(data)
                parent_win.after(0, lambda: _swap(None, None))
        except Exception as e:
            print(f"[update] download error: {e}")
            parent_win.after(0, lambda err=str(e): (
                dlg.destroy(),
                messagebox.showerror("Update failed", f"Download error:\n{err}", parent=parent_win),
            ))

    def _swap(src_dir, tmp_dir):
        try:
            _set_status("Installing…", 1.0)
            exe_name = os.path.basename(exe_path)
            if src_dir:
                bat = (
                    "@echo off\n"
                    ":waitloop\n"
                    f'tasklist /FI "IMAGENAME eq {exe_name}" 2>NUL | find /I "{exe_name}" >NUL\n'
                    'if "%ERRORLEVEL%"=="0" (\n'
                    "    timeout /t 1 /nobreak >nul\n"
                    "    goto waitloop\n"
                    ")\n"
                    f'xcopy /E /I /Y "{src_dir}\\*" "{exe_dir}."\n'
                    f'rmdir /S /Q "{tmp_dir}"\n'
                    f'start "" "{exe_path}"\n'
                    'del "%~f0"\n'
                )
            else:
                bat = (
                    "@echo off\n"
                    ":waitloop\n"
                    f'tasklist /FI "IMAGENAME eq {exe_name}" 2>NUL | find /I "{exe_name}" >NUL\n'
                    'if "%ERRORLEVEL%"=="0" (\n'
                    "    timeout /t 1 /nobreak >nul\n"
                    "    goto waitloop\n"
                    ")\n"
                    f'move /Y "{tmp_exe}" "{exe_path}"\n'
                    f'start "" "{exe_path}"\n'
                    'del "%~f0"\n'
                )
            with open(updater_bat, "w") as f:
                f.write(bat)
            subprocess.Popen(
                f'cmd /c "{updater_bat}"',
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                close_fds=True,
            )
            parent_win.after(800, parent_win.destroy)
        except Exception as e:
            print(f"[update] swap error: {e}")
            dlg.destroy()
            messagebox.showerror("Update failed", f"Could not install update:\n{e}", parent=parent_win)

    threading.Thread(target=_download, daemon=True).start()


def open_update_dialog(parent_win, tag, dl_url):
    dlg = tk.Toplevel(parent_win)
    dlg.title("Update Available")
    dlg.configure(bg=PALETTE["bg_outer"])
    center(dlg, 380, 180)
    dlg.resizable(False, False)
    tk.Label(dlg, text=f"A new version is available!",
             fg=PALETTE["title_fill"], bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 14, APP_FONT_WEIGHT)).pack(pady=(20, 4))
    tk.Label(dlg, text=f"Current: Lairkeeper v{APP_VERSION}     →     New: Lairkeeper v{tag}",
             fg="white", bg=PALETTE["bg_outer"],
             font=(APP_FONT_FAMILY, 10)).pack(pady=(0, 16))
    btn_row = tk.Frame(dlg, bg=PALETTE["bg_outer"])
    btn_row.pack()
    tk.Button(btn_row, text="Update Now", command=lambda: (dlg.destroy(), perform_update(parent_win, dl_url)),
               bg=PALETTE["bar_fill"], fg="#16330F", relief="flat",
               font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), padx=18, pady=6).pack(side="left", padx=8)
    tk.Button(btn_row, text="Not Now", command=dlg.destroy,
               bg=PALETTE["tag_fill"], fg="white", relief="flat",
               font=(APP_FONT_FAMILY, 10, APP_FONT_WEIGHT), padx=18, pady=6).pack(side="left", padx=8)


def _dlog(msg):
    import datetime
    line = f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}] {msg}"
    try:
        _dlog._file.write(line + "\n")
        _dlog._file.flush()
    except Exception:
        pass


def _init_debug_log():
    import sys
    log_path = os.path.join(SCRIPT_DIR, "lairkeeper_debug.log")
    try:
        _dlog._file = open(log_path, "w", encoding="utf-8", buffering=1)
    except Exception:
        _dlog._file = None
    _dlog(f"=== Lairkeeper Debug Log ===")
    _dlog(f"Version: {APP_VERSION}")
    _dlog(f"Python: {sys.version}")
    _dlog(f"Frozen: {getattr(sys, 'frozen', False)}")
    _dlog(f"SCRIPT_DIR: {SCRIPT_DIR}")
    try:
        import ctypes as _ct
        _dlog(f"Primary monitor: {_ct.windll.user32.GetSystemMetrics(0)}x{_ct.windll.user32.GetSystemMetrics(1)}")
        _dlog(f"Virtual desktop: {_ct.windll.user32.GetSystemMetrics(78)}x{_ct.windll.user32.GetSystemMetrics(79)}")
    except Exception as e:
        _dlog(f"Monitor info unavailable: {e}")


def start():

    splash = tk.Tk()
    splash.title("Lairkeeper")
    splash.geometry("380x150")
    splash.resizable(False, False)
    splash.configure(bg=PALETTE["bg_outer"])

    try:
        sw = splash.winfo_screenwidth()
        sh = splash.winfo_screenheight()
        splash.geometry(f"380x150+{(sw - 380) // 2}+{(sh - 150) // 2}")
    except Exception:
        pass
    splash.lift()
    splash.attributes("-topmost", True)
    splash.after(500, lambda: splash.attributes("-topmost", False))
    set_window_icon(splash)

    panel = tk.Frame(splash, bg=PALETTE["panel_fill"], highlightbackground=PALETTE["panel_border"],
                      highlightthickness=2)
    panel.pack(expand=True, fill="both", padx=14, pady=14)

    text_row = tk.Frame(panel, bg=PALETTE["panel_fill"])
    text_row.pack(pady=(22, 6))
    tk.Label(text_row, text="Lairkeeper is loading", font=("Segoe UI", 12, "bold"),
              bg=PALETTE["panel_fill"], fg=PALETTE["label_text"]).pack(side="left")

    happy_icon_label = tk.Label(text_row, text=" :)", font=("Segoe UI", 12, "bold"),
                                 bg=PALETTE["panel_fill"], fg=PALETTE["label_text"])
    happy_icon_label.pack(side="left")
    splash._happy_icon_ref = None

    def try_show_happy_icon():
        if splash._happy_icon_ref is not None:
            return
        path = os.path.join(MISC_DIR, "happy_icon.png")
        if not os.path.exists(path):
            return
        try:
            img = Image.open(path).convert("RGBA")
            img.thumbnail((40, 40), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            splash._happy_icon_ref = photo
            happy_icon_label.config(image=photo, text="")
        except Exception:
            pass

    try_show_happy_icon()

    label = tk.Label(panel, text="Fetching data from the wiki...",
                      font=("Segoe UI", 10), wraplength=330, justify="center",
                      bg=PALETTE["panel_fill"], fg=PALETTE["label_text"])
    label.pack(expand=True, padx=20, pady=(0, 20))
    splash.update()

    def poll_data():
        try_show_happy_icon()
        if _WIKI_BG["thread"].is_alive():
            splash.after(100, poll_data)
            return
        global MATERIAL_LIST, ELEMENT_LIST, SPECIES_LIST, SPECIES_RARITY
        global PUPIL_LIST, COSMETIC_TRAIT_LIST, POSITIVE_TRAIT_LIST, NEGATIVE_TRAIT_LIST
        global SDA_EXCLUDED, COLOR_LIST, ELEMENTAL_POTIONS
        real = _WIKI_BG["data"] or {}
        MATERIAL_LIST = real.get("MATERIAL_LIST") or MATERIAL_LIST
        ELEMENT_LIST = real.get("ELEMENT_LIST") or ELEMENT_LIST
        SPECIES_LIST = real.get("SPECIES_LIST") or SPECIES_LIST
        SPECIES_RARITY = {**SPECIES_RARITY_FALLBACK, **(real.get("SPECIES_RARITY") or {})}
        PUPIL_LIST = real.get("PUPIL_LIST") or PUPIL_LIST
        COLOR_LIST = real.get("COLOR_LIST") or COLOR_LIST
        COSMETIC_TRAIT_LIST = ["None"] + (real.get("COSMETIC_TRAIT_LIST") or COSMETIC_TRAIT_LIST[1:])
        POSITIVE_TRAIT_LIST = ["None"] + (real.get("POSITIVE_TRAIT_LIST") or [])
        NEGATIVE_TRAIT_LIST = ["None"] + (real.get("NEGATIVE_TRAIT_LIST") or [])
        SDA_EXCLUDED = SDA_EXCLUDED_FALLBACK | (real.get("SDA_EXCLUDED") or set())
        ELEMENTAL_POTIONS = real.get("ELEMENTAL_POTIONS") or ELEMENTAL_POTIONS

        label.config(text="Downloading icons...")
        splash.update()

        icon_thread_box = {}
        progress_box = {"done": 0, "total": 0}

        def on_icon_progress(done, total):
            progress_box["done"] = done
            progress_box["total"] = total

        def fetch_icons():
            try:
                import wiki_icons
                wiki_icons.download_all_icons(
                    icon_dir=ICON_DIR,
                    dragon_icons_dir=DRAGON_ICONS_DIR,
                    cosmetic_trait_icon_dir=COSMETIC_TRAIT_ICON_DIR,
                    species_list=SPECIES_LIST,
                    elements=ELEMENT_LIST,
                    traits=COSMETIC_TRAIT_LIST,
                    verbose=True,
                    on_progress=on_icon_progress,
                )
                wiki_icons.download_legendary_shift_icons(
                    LEGENDARY_SHIFT_DIR,
                    elements=ELEMENT_LIST,
                    verbose=True,
                )
                wiki_icons.download_potion_icons(
                    POTION_ICON_DIR,
                    potions=ELEMENTAL_POTIONS,
                    verbose=True,
                )
            except Exception as e:
                print(f"[wiki_icons] icon fetch skipped: {e}")

        icon_thread_box["thread"] = threading.Thread(target=fetch_icons, daemon=True)
        icon_thread_box["thread"].start()

        def poll_icons():
            try_show_happy_icon()
            total = progress_box["total"]
            done = progress_box["done"]
            if total:
                label.config(text=f"Downloading icons... {done}/{total}")
            if icon_thread_box["thread"].is_alive():
                splash.after(100, poll_icons)
                return
            for widget in splash.winfo_children():
                widget.destroy()
            _start_main_app(splash)

        poll_icons()

    poll_data()
    splash.mainloop()


def _start_main_app(root):
    _init_debug_log()
    _dlog("Reusing splash's Tk root for the main window (avoids a second")
    _dlog("tk.Tk() instance, which is what caused the window icon to")
    _dlog("revert to Python's default on some Windows setups)...")
    root.title("Accounts")
    root.resizable(True, True)
    _dlog("Setting window icon...")
    set_window_icon(root)
    _dlog("Loading fonts...")
    load_custom_fonts()
    _dlog("Setting up ttk style...")
    setup_ttk_style(root)
    _dlog("Centering window...")
    center(root, 440, 600)
    root.update_idletasks()
    _dlog(f"Geometry: {root.winfo_geometry()}")
    root.lift()
    root.attributes("-topmost", True)
    root.after(200, lambda: root.attributes("-topmost", False))
    _dlog("Building account screen...")

    bg_canvas = tk.Canvas(root, bg=PALETTE["bg_outer"], highlightthickness=0)
    bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

    def redraw_bg(_e=None):
        bg_canvas.delete("bgpanel")
        w = max(bg_canvas.winfo_width(), 440)
        h = max(bg_canvas.winfo_height(), 600)
        round_rect(bg_canvas, w * 0.034, h * 0.025, w * 0.966, h * 0.975, r=26,
                   fill=PALETTE["panel_fill"], outline=PALETTE["panel_border"], width=5,
                   tags="bgpanel")
        round_rect(bg_canvas, w * 0.182, h * 0.047, w * 0.818, h * 0.130, r=22,
                   fill=PALETTE["card_fill"], outline=PALETTE["panel_border"], width=3,
                   tags="bgpanel")
        outline_text(bg_canvas, w * 0.5, h * 0.088, "Select Account",
                     (APP_FONT_FAMILY, 22, APP_FONT_WEIGHT),
                     PALETTE["title_fill"], PALETTE["title_outline"], tags="bgpanel")

    _bg_resize_job = {"id": None}

    def _on_bg_resize(_e=None):
        if _bg_resize_job["id"] is not None:
            root.after_cancel(_bg_resize_job["id"])
        _bg_resize_job["id"] = root.after(80, redraw_bg)

    bg_canvas.bind("<Configure>", _on_bg_resize)
    redraw_bg()

    MAX_LIST_HEIGHT = 375

    list_holder = tk.Frame(root, bg=PALETTE["panel_fill"])
    list_holder.place(relx=30 / 440, rely=95 / 600, relwidth=380 / 440, relheight=375 / 600)

    list_canvas = tk.Canvas(list_holder, bg=PALETTE["panel_fill"], highlightthickness=0, height=1)
    list_canvas.pack(side="left", fill="x", expand=True, anchor="n")
    list_scroll = tk.Scrollbar(list_holder, command=list_canvas.yview)
    list_scroll.pack(side="right", fill="y")
    list_canvas.configure(yscrollcommand=list_scroll.set)
    bind_mousewheel(list_canvas)

    rows_frame = tk.Frame(list_canvas, bg=PALETTE["panel_fill"])
    rows_window_id = list_canvas.create_window((0, 0), window=rows_frame, anchor="nw")
    list_canvas.bind("<Configure>", lambda e: list_canvas.itemconfig(rows_window_id, width=e.width))

    def render_accounts():
        for w in rows_frame.winfo_children():
            w.destroy()

        if not all_accounts_data:
            tk.Label(rows_frame, text="No accounts yet —\ntap + Add Account below",
                     fg=PALETTE["label_text"], bg=PALETTE["panel_fill"],
                     font=(APP_FONT_FAMILY, 12, APP_FONT_WEIGHT), justify="center").pack(pady=60)

        for acc in list(all_accounts_data.keys()):
            row = tk.Canvas(rows_frame, width=350, height=56, bg=PALETTE["panel_fill"], highlightthickness=0)
            row.pack(pady=6)
            round_rect(row, 2, 2, 348, 54, r=14,
                        fill=PALETTE["card_fill"], outline=PALETTE["card_border"], width=2)
            rounded_button(row, 6, 6, 270, 44, acc,
                            lambda r=root, u=acc: open_lair(r, u), r=10,
                            fill=PALETTE["card_fill"], outline="")

            def make_delete(u=acc):
                def _delete():
                    if messagebox.askyesno("Delete account",
                                            f'Delete "{u}" and all its dragons? This can\'t be undone.'):
                        all_accounts_data.pop(u, None)
                        try:
                            shutil.rmtree(_account_dir(u), ignore_errors=True)
                        except Exception:
                            pass
                        render_accounts()
                return _delete

            rounded_button(row, 282, 6, 62, 44, "\u2715", make_delete(), r=10,
                            fill="#7A2020", outline="#4A1010")

        rows_frame.update_idletasks()
        content_h = max(1, rows_frame.winfo_reqheight())
        list_canvas.configure(height=min(content_h, MAX_LIST_HEIGHT))
        list_canvas.configure(scrollregion=list_canvas.bbox("all"))

    render_accounts()

    add_canvas = tk.Canvas(root, bg=PALETTE["bg_outer"], highlightthickness=0)
    add_canvas.place(relx=30 / 440, rely=485 / 600, relwidth=380 / 440, height=50)

    def redraw_add_btn(_e=None):
        add_canvas.delete("addbtn")
        w = max(add_canvas.winfo_width(), 380)
        ids = rounded_button(add_canvas, 0, 0, w, 50, "+ Add Account",
                              lambda: open_add_account_dialog(root, render_accounts), r=14,
                              fill=PALETTE["badge_fill"], outline=PALETTE["badge_border"],
                              text_fill="#3A2A06")
        for item_id in ids:
            add_canvas.addtag_withtag("addbtn", item_id)

    add_canvas.bind("<Configure>", redraw_add_btn)
    redraw_add_btn()

    footer = tk.Frame(root, bg=PALETTE["bg_outer"])
    footer.place(relx=30 / 440, rely=544 / 600, relwidth=380 / 440)
    version_label = tk.Label(footer, text=f"Lairkeeper v{APP_VERSION}", fg=PALETTE["label_text"],
                              bg=PALETTE["bg_outer"], font=(APP_FONT_FAMILY, 9))
    version_label.pack(side="left")

    compact_var = tk.BooleanVar(value=global_settings.get("CompactMode", False))

    def on_compact_toggle():
        global_settings["CompactMode"] = compact_var.get()
        save_global_settings(global_settings)

    tk.Checkbutton(footer, text="Compact Mode", variable=compact_var, command=on_compact_toggle,
                    fg=PALETTE["label_text"], bg=PALETTE["bg_outer"],
                    selectcolor=PALETTE["tag_fill"], activebackground=PALETTE["bg_outer"],
                    font=(APP_FONT_FAMILY, 9)).pack(side="left", padx=(12, 0))

    update_btn_var = tk.StringVar(value="Check for Updates")
    update_btn = tk.Button(footer, textvariable=update_btn_var,
                            command=lambda: _check_updates_clicked(),
                            bg=PALETTE["tag_fill"], fg="white", relief="flat",
                            font=(APP_FONT_FAMILY, 9), padx=10, pady=3,
                            cursor="hand2")
    update_btn.pack(side="right")

    def _check_updates_clicked():
        update_btn.configure(state="disabled")
        update_btn_var.set("Checking…")

        def on_result(tag, dl_url, is_newer):
            update_btn.configure(state="normal")
            if tag is None:
                update_btn_var.set("No connection")
                root.after(3000, lambda: update_btn_var.set("Check for Updates"))
            elif is_newer:
                update_btn_var.set(f"Lairkeeper v{tag} available!")
                open_update_dialog(root, tag, dl_url)
            else:
                update_btn_var.set(f"Up to date (v{tag}) ✓")
                root.after(3000, lambda: update_btn_var.set("Check for Updates"))

        check_for_updates_async(root, on_result)

    _dlog("Entering mainloop — app should be visible now")
    try:
        _dlog._file.close()
    except Exception:
        pass
    root.mainloop()


if __name__ == "__main__":
    start()





