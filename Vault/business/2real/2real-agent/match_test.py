#!/usr/bin/env python3
import json
from pathlib import Path
from difflib import SequenceMatcher
JIJI_TITLES = [
  "Flopro 8 Head Hose Spray Gun",
  "Vtech Frozen Learning Tablet",
  "Makita 6280d 14,4v Drill Driver Plus Charger 1 Battery",
  "Silverline Plane 41x1mm Sheet Metal Block",
  "Gorilla Tack Reusable Tapes",
  "Poker Chip Set 300 Pieces",
  "Stanley Torch 600 Lumens",
  "Day Plus 130w Detail Palm Sander Qd6301",
  "Parkside 20v Cordless Drill Driver With Battery and Charger",
  "Portable CD Player",
  "Adidas F50 Size 43 Unisex From Uk",
  "Rust Oleum Peel Coat Orange",
  "Kids and Adults Neck Pillow",
  "Slimlime LED Under Cabinet Light Kit",
  "Weber 7183 Premium Barbecue Grill Cover",
  "Desktop Hard Drive 2tb 3.5inch Hard Drive 3.5inch",
  "Original Gillette Mach3 Men's Razor Handle With Two Blade Refills Uk",
  "Xbox One Assassin's Creed Origins From UK",
  "Assassin's Creed: Brotherhood (DVD-ROM) for Windows",
  "Lg Digital 42 Inches Tv",
]

ITEMS = [
  ("Hydraulic Bottle Jack HBJ602", 450.0, 1),
  ("30m Fiberglass Measuring Tape HFMT8330", 160.0, 7),
  ("Hack Saw Frame HHF3088", 170.0, 5),
  ("Acetic Silicone Sealant Black HASS03", 50.0, 22),
  ("Lithium-Ion aspirator blower CABLI2001", 645.0, 1),
  ("Lithium-Ion battery pack 20V FBLI20011", 370.0, 2),
  ("Angle Square HAS123002", 100.0, 3),
  ("HGVP01 PVC Gloves 32cm", 17.0, 11),
  ("HGVC01 Leather Gloves 10.5", 52.0, 10),
  ("HDCP08168 Diagonal cutting pliers", 47.0, 4),
  ("HTSN0110S Aviation Snip", 84.0, 4),
  ("HCG0309 Caulking Gun", 39.0, 11),
  ("HSMT08525 Steel measuring tape 5M", 46.0, 9),
  ("HSMT08825 Steel measuring tape 8M", 71.0, 9),
  ("Bi-Metal Hacksaw Blade Set HSBKT12185", 80.0, 50),
]

def norm(s):
    return " ".join(str(s).lower().replace("'","").replace("-"," ").split())

def match(q):
    qn = norm(q)
    for t in JIJI_TITLES:
        if SequenceMatcher(None, qn, norm(t)).ratio() > 0.65:
            return ("JIJI", t)
    best, bscore, bsrc = None, 0.0, None
    for name, price, stock in ITEMS:
        score = SequenceMatcher(None, qn, norm(name)).ratio()
        words = set(qn.split()) & set(norm(name).split())
        score = max(score, len(words)/max(len(qn.split()),1))
        if score > bscore:
            bscore, best, bsrc = score, (name,price,stock), "ZOBaZE"
    if best and bscore >= 0.55:
        return ("ZOBaZE", best)
    return None

if __name__ == "__main__":
    queries = [
        "Flopro hose spray gun",
        "Makita 6280d drill",
        "Desktop Hard Drive 2tb",
        "Assassin's Creed",
        "PORTABLE CD PLAYER",
        "Rust Oleum Peel Coat",
        "Poker Chip Set 300",
        "Stanley Torch",
        "some random phone xyz",
    ]
    for q in queries:
        print(f"Q: {q}")
        print(f"-> {match(q)}")
        print()
