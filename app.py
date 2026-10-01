"""
Smart Food Waste Management System
===================================
A responsive Streamlit web application connecting surplus food donors (restaurants,
hotels, event caterers, and households) with NGOs, community kitchens, and volunteers
before surplus food expires.

================================================================================
🎓 STUDENT ASSIGNMENT SUBMISSION METADATA & PYTHON CONCEPTS DEMONSTRATED
================================================================================
This application was engineered to demonstrate proficiency in core Python programming:

1. VARIABLES:
   - Primitive Types: int (counts, portions), float (weights, carbon savings),
     str (titles, donor names, locations), bool (validation flags).
   - Global Constants: UPPERCASE configuration variables (FOOD_LISTINGS_FILE, DATA_DIR).

2. LISTS:
   - Dynamic Collections: Appending, filtering, slicing, and calculating length with len().
   - List Comprehensions: Extracting digits from phone strings, filtering records by category.

3. DICTIONARIES:
   - Key-Value Structures: Structured surplus food donation records, claim tracking objects.
   - Safe Retrieval: Using .get(key, default) for fault-tolerant property access.

4. FUNCTIONS:
   - Modular Architecture: Pure validation functions, utility helpers, and page renderers.
   - Reusability: calculate_impact_metrics(), generate_unique_id(), get_freshness_status().

5. LOOPS:
   - For Loops: Iterating through lists to aggregate meals, compute totals, and render cards.
   - While Loops: Generating guaranteed unique sequential donation IDs without collision.

6. IF / ELSE CONDITIONS:
   - Conditional Branching: Validating inputs, categorizing urgency tiers (Red/Orange/Green),
     and rendering empty-state messages when lists are empty.

7. INPUT VALIDATION:
   - Defensive Programming: 6 dedicated Python functions validating name length, positive
     servings, future expiry date/time, address length, and 10-digit phone numbers.

8. FILE HANDLING WITH JSON:
   - Persistent Storage: Reading and writing to 'food_listings.json' with standard json.load()
     and json.dump(). Context managers ('with open(...)') guarantee proper resource cleanup.

9. EXCEPTION HANDLING:
   - Robust Error Recovery: Multi-level try...except blocks catching FileNotFoundError,
     json.JSONDecodeError, ValueError, TypeError, and IOError with helpful user feedback.

10. BASIC TYPE HINTS:
    - PEP 484 Annotations: Clear type hints on all function parameters and return types
      (str, int, float, bool, list[dict], tuple[bool, str], dict[str, Any]).
================================================================================
"""

import os
import json
import uuid
import datetime
from datetime import datetime as dt, timedelta
from typing import Any, Optional, Union
import pandas as pd
import streamlit as st

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Smart Food Waste Management System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Green & White Sustainability Theme
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1f2937;
}

/* Green Brand Gradient Headers */
.app-header {
    background: linear-gradient(135deg, #064e3b 0%, #047857 50%, #059669 100%);
    color: white;
    padding: 2.2rem 2.5rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.15);
}

.app-header h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 2.3rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.02em;
    color: #ffffff !important;
}

.app-header p {
    font-size: 1.05rem;
    margin: 0.5rem 0 0 0;
    color: #d1fae5;
    font-weight: 400;
}

.badge-pill-header {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 4px 14px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.75rem;
    color: #ecfdf5;
}

/* Sustainability Metric Cards */
.metric-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.25rem;
    margin-bottom: 2rem;
}

.metric-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.4rem 1.25rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px -2px rgba(0, 0, 0, 0.04);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px -3px rgba(5, 150, 105, 0.12);
    border-color: #10b981;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #10b981, #34d399);
}

.metric-icon-wrap {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 0.75rem;
    background: #f0fdf4;
    border: 1px solid #dcfce7;
}

.metric-val {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #064e3b;
    line-height: 1.1;
}

.metric-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #4b5563;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 0.35rem;
}

.metric-sub {
    font-size: 0.78rem;
    color: #059669;
    margin-top: 0.25rem;
    font-weight: 500;
}

/* Food Listing Cards */
.food-card {
    background: #ffffff;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    padding: 1.4rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease-in-out;
}

.food-card:hover {
    box-shadow: 0 12px 24px -4px rgba(5, 150, 105, 0.1);
    border-color: #a7f3d0;
}

.food-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
    gap: 8px;
}

.food-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #064e3b;
    margin: 0;
}

/* Badges */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.badge-urgent {
    background-color: #fef2f2;
    color: #b91c1c;
    border: 1px solid #fecaca;
}

.badge-moderate {
    background-color: #fffbeb;
    color: #b45309;
    border: 1px solid #fde68a;
}

.badge-safe {
    background-color: #f0fdf4;
    color: #15803d;
    border: 1px solid #bbf7d0;
}

.badge-dietary-veg {
    background-color: #ecfdf5;
    color: #047857;
    border: 1px solid #a7f3d0;
}

.badge-dietary-vegan {
    background-color: #f0fdf4;
    color: #166534;
    border: 1px solid #86efac;
}

.badge-dietary-nonveg {
    background-color: #fff1f2;
    color: #be123c;
    border: 1px solid #fecdd3;
}

.badge-status-available {
    background-color: #d1fae5;
    color: #065f46;
    border: 1px solid #6ee7b7;
}

.badge-status-claimed {
    background-color: #e0f2fe;
    color: #0369a1;
    border: 1px solid #7dd3fc;
}

.badge-status-completed {
    background-color: #f3f4f6;
    color: #4b5563;
    border: 1px solid #d1d5db;
}

/* Card details grid */
.food-meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0.75rem;
    padding: 0.85rem 0;
    margin: 0.6rem 0;
    border-top: 1px solid #f3f4f6;
    border-bottom: 1px solid #f3f4f6;
}

.meta-item {
    font-size: 0.84rem;
    color: #374151;
}

.meta-item strong {
    color: #111827;
    font-weight: 600;
}

.donor-info-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
    font-size: 0.85rem;
    color: #4b5563;
    margin-top: 0.5rem;
}

/* Clean Form Styling */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    border: none;
    box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #047857 0%, #064e3b 100%);
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(5, 150, 105, 0.35);
}

/* Eco Tips Banner */
.eco-banner {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    color: #14532d;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 14px;
}

/* Section Headings */
.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: #064e3b;
    margin: 1.5rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Footer */
.custom-footer {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem 1rem;
    color: #6b7280;
    font-size: 0.85rem;
    border-top: 1px solid #e5e7eb;
    margin-top: 3rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# SECTION 1: GLOBAL CONSTANTS & FILE STORAGE CONFIGURATION
# Demonstrates: Variables (Constants, Strings, File Paths) and Data Setup
# ==============================================================================
FOOD_LISTINGS_FILE: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "food_listings.json")
DATA_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE: str = FOOD_LISTINGS_FILE
LEGACY_BACKUP_FILE: str = os.path.join(DATA_DIR, "food_donations.json")

# Standard food categories list used for validation, forms, and filtering
FOOD_CATEGORIES: list[str] = [
    "Cooked meals",
    "Fruits & vegetables",
    "Bakery",
    "Dairy",
    "Packaged food",
    "Other"
]

def ensure_data_directory():
    """Ensure the data folder exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def generate_seed_data():
    """Generate realistic seed donations with dynamic timestamps relative to right now."""
    now = dt.now()
    return [
        {
            "id": "DON-1001",
            "title": "Royal Hyderabadi Veg Dum Biryani & Mirchi Salan",
            "category": "Cooked Meals",
            "dietary": "Vegetarian",
            "portions": 65,
            "weight_kg": 26.0,
            "donor_name": "Grand Palace Banquet Hall",
            "donor_type": "Hotel / Catering",
            "contact_person": "Rajesh Varma (Banquet Mgr)",
            "contact_phone": "+91 98450 12345",
            "contact_email": "banquets@grandpalace.org",
            "pickup_address": "88 Emerald Avenue, MG Road, Central Area",
            "city_area": "Central City",
            "storage_condition": "Insulated Heat Box (>60°C)",
            "prepared_at": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "expires_at": (now + timedelta(hours=2, minutes=15)).strftime("%Y-%m-%d %H:%M"),
            "notes": "Packed in food-grade insulated aluminum foil containers. Freshly prepared for corporate event lunch.",
            "status": "Available",
            "created_at": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "claim_info": None
        },
        {
            "id": "DON-1002",
            "title": "Fresh Artisan Sourdough Breads & French Baguettes",
            "category": "Bakery & Pastries",
            "dietary": "Vegan",
            "portions": 40,
            "weight_kg": 14.5,
            "donor_name": "The Rustic Crumb Artisan Bakery",
            "donor_type": "Bakery / Cafe",
            "contact_person": "Claire Dupont",
            "contact_phone": "+91 98230 45678",
            "contact_email": "hello@rusticcrumb.com",
            "pickup_address": "12 Baker's Street, 4th Block, Green Garden Area",
            "city_area": "Northside",
            "storage_condition": "Dry / Room Temperature",
            "prepared_at": (now - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"),
            "expires_at": (now + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"),
            "notes": "Baked this morning with natural sourdough fermentation. 100% vegan, clean paper bag packaging.",
            "status": "Available",
            "created_at": (now - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
            "claim_info": None
        },
        {
            "id": "DON-1003",
            "title": "Homestyle Paneer Butter Masala, Dal Makhani & Rotis",
            "category": "Cooked Meals",
            "dietary": "Vegetarian",
            "portions": 25,
            "weight_kg": 11.0,
            "donor_name": "Sharma Family (Community Wedding)",
            "donor_type": "Household / Family Event",
            "contact_person": "Sunita Sharma",
            "contact_phone": "+91 98765 89012",
            "contact_email": "sunita.sharma@example.com",
            "pickup_address": "Flat 402, Lotus Greens, Sector 7",
            "city_area": "South Suburb",
            "storage_condition": "Refrigerated (3°C - 4°C)",
            "prepared_at": (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
            "expires_at": (now + timedelta(hours=1, minutes=20)).strftime("%Y-%m-%d %H:%M"),
            "notes": "Untouched surplus from a housewarming reception. Packed in stainless steel containers (bring transfer vessels).",
            "status": "Available",
            "created_at": (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
            "claim_info": None
        },
        {
            "id": "DON-1004",
            "title": "Organic Farm Apples, Oranges & Bananas Crates",
            "category": "Fresh Fruits & Produce",
            "dietary": "Vegan",
            "portions": 80,
            "weight_kg": 35.0,
            "donor_name": "EarthHarvest Organic Mart",
            "donor_type": "Supermarket / Grocery",
            "contact_person": "Karthik Nair",
            "contact_phone": "+91 97110 33445",
            "contact_email": "supply@earthharvest.com",
            "pickup_address": "Plot 15, Warehouse Hub, Ring Road",
            "city_area": "East Industrial",
            "storage_condition": "Chilled / Ventilated",
            "prepared_at": (now - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"),
            "expires_at": (now + timedelta(hours=22)).strftime("%Y-%m-%d %H:%M"),
            "notes": "Slight cosmetic blemishes on skins, perfectly ripe, nutritious and sweet. Great for shelter breakfast.",
            "status": "Available",
            "created_at": (now - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S"),
            "claim_info": None
        },
        {
            "id": "DON-1005",
            "title": "Grilled Chicken Rice Bowls & Steamed Veggies",
            "category": "Cooked Meals",
            "dietary": "Non-Vegetarian",
            "portions": 35,
            "weight_kg": 15.0,
            "donor_name": "FitBites Healthy Kitchen",
            "donor_type": "Restaurant",
            "contact_person": "Chef Anand",
            "contact_phone": "+91 98334 77665",
            "contact_email": "kitchen@fitbites.com",
            "pickup_address": "Shop 4, Commercial Plaza, Tech Park Blvd",
            "city_area": "Tech Corridor",
            "storage_condition": "Chilled Cooler (4°C)",
            "prepared_at": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "expires_at": (now + timedelta(hours=3, minutes=45)).strftime("%Y-%m-%d %H:%M"),
            "notes": "Hygienically meal-prepped bowls, sealed with tamper-evident lids. High protein nutritious meals.",
            "status": "Available",
            "created_at": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "claim_info": None
        },
        {
            "id": "DON-1006",
            "title": "South Indian Tiffin: Idlis, Vadas & Sambar",
            "category": "Cooked Meals",
            "dietary": "Vegetarian",
            "portions": 50,
            "weight_kg": 20.0,
            "donor_name": "Sri Krishna Bhavan",
            "donor_type": "Restaurant",
            "contact_person": "Murugan Swamy",
            "contact_phone": "+91 94441 55667",
            "contact_email": "skbhavan@example.com",
            "pickup_address": "22 Temple Road, Gandhi Bazaar",
            "city_area": "Old Town",
            "storage_condition": "Insulated Hot Cans",
            "prepared_at": (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
            "expires_at": (now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "notes": "Claimed by Robin Hood Army volunteer team. Pick-up vehicle en route.",
            "status": "Claimed",
            "created_at": (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
            "claim_info": {
                "claim_code": "PICK-7821",
                "claimed_by": "Rohan Deshmukh",
                "organization": "Robin Hood Army (Chapter Central)",
                "recipient_type": "Registered NGO",
                "phone": "+91 98220 99881",
                "eta": "Within 45 mins",
                "purpose": "Distributing to construction worker settlement in Ward 14",
                "claimed_at": (now - timedelta(minutes=25)).strftime("%Y-%m-%d %H:%M")
            }
        },
        {
            "id": "DON-1007",
            "title": "Corporate Conference High-Tea Sandwiches & Cakes",
            "category": "Bakery & Pastries",
            "dietary": "Vegetarian",
            "portions": 70,
            "weight_kg": 22.0,
            "donor_name": "Summit Tech Conference 2026",
            "donor_type": "Event Organizer",
            "contact_person": "Priya Sen",
            "contact_phone": "+91 99001 22334",
            "contact_email": "events@summittech.io",
            "pickup_address": "Convention Center, Gate 3, Airport Road",
            "city_area": "Northside",
            "storage_condition": "Room Temperature / Dry",
            "prepared_at": (now - timedelta(hours=7)).strftime("%Y-%m-%d %H:%M"),
            "expires_at": (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
            "notes": "Successfully picked up and distributed to St. Mary's Shelter.",
            "status": "Completed",
            "created_at": (now - timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S"),
            "claim_info": {
                "claim_code": "PICK-4490",
                "claimed_by": "Sister Theresa",
                "organization": "St. Mary's Community Shelter",
                "recipient_type": "Shelter Home",
                "phone": "+91 94800 11223",
                "eta": "Picked up",
                "purpose": "Evening snack for 65 shelter residents",
                "claimed_at": (now - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"),
                "completed_at": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
            }
        }
    ]

# ==============================================================================
# SECTION 2: FILE HANDLING WITH JSON & EXCEPTION HANDLING
# Demonstrates: File handling with JSON (open, load, dump) and Exception Handling (try...except)
# ==============================================================================
def load_donations(file_path: str = FOOD_LISTINGS_FILE) -> list[dict[str, Any]]:
    """
    Load food donation records from a JSON file. Auto-initialize with seed data if absent.
    
    Demonstrates:
    - File Handling with JSON: json.load(), open(), context manager ('with')
    - Exception Handling: FileNotFoundError, json.JSONDecodeError, OSError
    - If/Else Conditions: Checking file existence and verifying list type
    - Basic Type Hints: file_path: str -> list[dict[str, Any]]
    
    Parameters:
        file_path (str): Path to the food listings JSON file.
        
    Returns:
        list[dict[str, Any]]: List of donation dictionaries loaded from storage.
    """
    ensure_data_directory()
    target_file = file_path if os.path.exists(file_path) else LEGACY_BACKUP_FILE
    
    # If the file does not exist on disk, create default seed data
    if not os.path.exists(target_file):
        seed_data: list[dict[str, Any]] = generate_seed_data()
        save_donations(seed_data, file_path)
        return seed_data
    
    try:
        # File Handling: Open the JSON file safely with a context manager
        with open(target_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # If/Else Condition: verify that the JSON structure is a list
            if not isinstance(data, list):
                st.warning("⚠️ Invalid data format in JSON file (expected a list). Reinitializing seed data.")
                seed_data = generate_seed_data()
                save_donations(seed_data, file_path)
                return seed_data
                
            # Keep food_listings.json synchronized if reading from legacy backup
            if target_file != FOOD_LISTINGS_FILE or not os.path.exists(FOOD_LISTINGS_FILE):
                with open(FOOD_LISTINGS_FILE, "w", encoding="utf-8") as out_f:
                    json.dump(data, out_f, indent=2, ensure_ascii=False)
                    
            return data
            
    # Exception Handling: specific exceptions for file and JSON issues
    except FileNotFoundError:
        st.info("ℹ️ Listings file not found. Generating default seed database.")
        seed_data = generate_seed_data()
        save_donations(seed_data, file_path)
        return seed_data
    except json.JSONDecodeError as json_err:
        st.error(f"⚠️ JSON parsing error in '{target_file}': {json_err}. Restoring seed database.")
        seed_data = generate_seed_data()
        save_donations(seed_data, file_path)
        return seed_data
    except (IOError, OSError) as io_err:
        st.error(f"⚠️ Filesystem read error: {io_err}. Loading empty listing list.")
        return []


def save_donations(data: list[dict[str, Any]], file_path: str = FOOD_LISTINGS_FILE) -> bool:
    """
    Write donation records to the JSON file and keep the backup file synchronized.
    
    Demonstrates:
    - File Handling with JSON: json.dump() with indenting and UTF-8 encoding
    - Exception Handling: IOError, OSError, TypeError
    - Basic Type Hints: data: list[dict[str, Any]], file_path: str -> bool
    
    Parameters:
        data (list[dict[str, Any]]): List of food donation dictionaries to persist.
        file_path (str): Destination file path.
        
    Returns:
        bool: True if saving succeeded, False otherwise.
    """
    ensure_data_directory()
    try:
        # File Handling: Write data formatted as clean indented JSON
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        # Also sync backup file if saving the primary listings file
        if file_path == FOOD_LISTINGS_FILE:
            try:
                with open(LEGACY_BACKUP_FILE, "w", encoding="utf-8") as backup_f:
                    json.dump(data, backup_f, indent=2, ensure_ascii=False)
            except (IOError, OSError):
                pass
            
        return True
    except (IOError, OSError, TypeError) as save_err:
        # Exception Handling: Display error to user without crashing the app
        st.error(f"❌ Failed to save food donations to '{file_path}': {save_err}")
        return False


# ==============================================================================
# SECTION 3: CORE LOGIC, METRIC CALCULATIONS & LOOPS
# Demonstrates: Functions, Loops (While & For), Lists, Dictionaries & Type Hints
# ==============================================================================
def generate_unique_id(existing_donations: list[dict[str, Any]], prefix: str = "DON") -> str:
    """
    Generate a guaranteed unique identifier for a new food listing.
    
    Demonstrates:
    - Loops: While loop for sequence generation and collision avoidance
    - Collections: Set for O(1) membership lookup
    - Variables: String formatting and integer counting
    - Basic Type Hints: existing_donations: list[dict[str, Any]], prefix: str -> str
    
    Parameters:
        existing_donations (list[dict[str, Any]]): Currently existing donation dictionaries.
        prefix (str): Prefix string for the identifier (default: 'DON').
        
    Returns:
        str: Guaranteed unique identifier string (e.g. 'DON-1009').
    """
    existing_ids: set[str] = {item.get("id") for item in existing_donations if "id" in item}
    counter: int = len(existing_donations) + 1001
    candidate_id: str = f"{prefix}-{counter}"
    
    # Loop: While loop increments counter until a completely non-colliding ID is found
    while candidate_id in existing_ids:
        counter += 1
        candidate_id = f"{prefix}-{counter}"
        
    return candidate_id


def calculate_impact_metrics(donations_list: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Calculate platform sustainability metrics using explicit Python loops and lists.
    
    Demonstrates:
    - Variables: Counters (int), totals (int), weights (float)
    - Lists: Separate lists for meal quantities and categorized listings
    - Loops: For loops iterating over dictionaries and accumulating values
    - If/Else Conditions: Status classification (Collected vs Awaiting)
    - Dictionaries: Returning structured metric summary
    - Basic Type Hints: donations_list: list[dict[str, Any]] -> dict[str, Any]
    
    Parameters:
        donations_list (list[dict[str, Any]]): Master list of surplus food donation records.
        
    Returns:
        dict[str, Any]: Dictionary containing computed metrics and environmental equivalencies.
    """
    # Variables: Counter initialized to zero
    total_food_listings: int = 0
    all_listings: list[dict[str, Any]] = list(donations_list) if donations_list else []
    
    # Loop: For loop to count total listings
    for _ in all_listings:
        total_food_listings += 1
        
    # Lists: Initialize lists to store individual meal counts
    meals_donated_list: list[int] = []
    meals_collected_list: list[int] = []
    meals_awaiting_list: list[int] = []
    
    # Loop: For loop through each food donation dictionary
    for listing in all_listings:
        # Safely extract meal portions with fallbacks
        qty_raw = listing.get("servings")
        if qty_raw is None:
            qty_raw = listing.get("portions")
        if qty_raw is None:
            qty_raw = listing.get("quantity", 0)
            
        try:
            qty_int: int = int(qty_raw)
            if qty_int < 0:
                qty_int = 0
        except (ValueError, TypeError):
            qty_int = 0
            
        # Append to master donated meals list
        meals_donated_list.append(qty_int)
        
        status_str: str = str(listing.get("status", "Available")).strip()
        
        # If/Else Condition: categorize based on status
        if status_str in ["Collected", "Completed"]:
            meals_collected_list.append(qty_int)
        else:
            # "Available", "Claimed"
            meals_awaiting_list.append(qty_int)
            
    # Loop: Accumulate totals using for loops over the extracted lists
    total_estimated_meals: int = 0
    for meal in meals_donated_list:
        total_estimated_meals += meal
        
    meals_redistributed: int = 0
    for meal in meals_collected_list:
        meals_redistributed += meal
        
    meals_awaiting: int = 0
    for meal in meals_awaiting_list:
        meals_awaiting += meal
        
    # Variables: Floating-point environmental equivalency metrics
    total_kg: float = round(total_estimated_meals * 0.4, 1)
    co2_saved_kg: float = round(total_kg * 2.5, 1)
    fulfillment_pct: float = (meals_redistributed / total_estimated_meals * 100) if total_estimated_meals > 0 else 0.0
    
    # Dictionary: Return structured key-value results
    return {
        "total_food_listings": total_food_listings,
        "total_estimated_meals": total_estimated_meals,
        "meals_redistributed": meals_redistributed,
        "meals_awaiting": meals_awaiting,
        "total_kg": total_kg,
        "co2_saved_kg": co2_saved_kg,
        "fulfillment_pct": fulfillment_pct
    }


def get_expiry_details(expires_at_str: str) -> dict[str, Any]:
    """
    Parse an expiry datetime string and calculate remaining time and urgency.
    
    Demonstrates:
    - Exception Handling: try...except for robust datetime string parsing
    - If/Else Conditions: multi-tiered urgency evaluation (<2h, <6h, >6h)
    - Dictionaries: returning structured outcome with status, label, delta_hours
    - Basic Type Hints: expires_at_str: str -> dict[str, Any]
    
    Parameters:
        expires_at_str (str): Datetime string in '%Y-%m-%d %H:%M' or ISO format.
        
    Returns:
        dict[str, Any]: Dictionary containing status, label, delta_hours, badge_class, and urgency.
    """
    try:
        expires_dt = dt.strptime(expires_at_str, "%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        try:
            expires_dt = dt.fromisoformat(expires_at_str)
        except (ValueError, TypeError):
            return {"status": "Unknown", "label": "No expiry set", "delta_hours": 999, "badge_class": "badge-safe"}

    now = dt.now()
    diff = expires_dt - now
    total_seconds = diff.total_seconds()

    if total_seconds <= 0:
        mins_ago = int(abs(total_seconds) // 60)
        hours_ago = mins_ago // 60
        mins_rem = mins_ago % 60
        ago_str = f"{hours_ago}h {mins_rem}m" if hours_ago > 0 else f"{mins_rem}m"
        return {
            "status": "Expired",
            "label": f"Expired ({ago_str} ago)",
            "delta_hours": -abs(total_seconds) / 3600,
            "badge_class": "badge-urgent",
            "urgency": "Expired"
        }
    
    hours = int(total_seconds // 3600)
    mins = int((total_seconds % 3600) // 60)

    if total_seconds < 7200:  # Less than 2 hours: CRITICAL
        return {
            "status": "Urgent",
            "label": f"🚨 {hours}h {mins}m remaining (Urgent)",
            "delta_hours": total_seconds / 3600,
            "badge_class": "badge-urgent",
            "urgency": "Urgent"
        }
    elif total_seconds < 21600:  # 2 to 6 hours: MODERATE
        return {
            "status": "Moderate",
            "label": f"⏳ {hours}h {mins}m remaining",
            "delta_hours": total_seconds / 3600,
            "badge_class": "badge-moderate",
            "urgency": "Moderate"
        }
    else:  # More than 6 hours: SAFE
        days = hours // 24
        rem_h = hours % 24
        time_text = f"{days}d {rem_h}h" if days > 0 else f"{hours}h {mins}m"
        return {
            "status": "Safe",
            "label": f"🌿 {time_text} remaining",
            "delta_hours": total_seconds / 3600,
            "badge_class": "badge-safe",
            "urgency": "Safe"
        }


def get_freshness_status(expires_at_str: str) -> dict[str, Any]:
    """
    Calculate freshness tier based on expiry deadline:
    - Red: collect today (delta_hours <= 24)
    - Orange: expires within 2 days (24 < delta_hours <= 48)
    - Green: available for more than 2 days (delta_hours > 48)
    
    Demonstrates:
    - Functions & Basic Type Hints: expires_at_str: str -> dict[str, Any]
    - If/Elif/Else Conditions: multi-range categorization
    - Exception Handling: fallback when date string is missing or malformed
    
    Parameters:
        expires_at_str (str): The best-before expiry timestamp string.
        
    Returns:
        dict[str, Any]: Dictionary with tier, color, label, and badge_html.
    """
    try:
        expires_dt = dt.strptime(expires_at_str, "%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        try:
            expires_dt = dt.fromisoformat(expires_at_str)
        except (ValueError, TypeError):
            return {
                "tier": "Green",
                "color": "green",
                "label": "🟢 Available for >2 days",
                "badge_html": '<span style="background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; font-weight: 700; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px;">🟢 Available for >2 days</span>'
            }

    now = dt.now()
    diff = expires_dt - now
    total_seconds = diff.total_seconds()
    delta_hours = total_seconds / 3600

    if delta_hours <= 24:
        hours = max(0, int(total_seconds // 3600))
        mins = max(0, int((total_seconds % 3600) // 60))
        time_text = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
        urgency_label = f"🔴 Collect Today ({time_text} left)" if delta_hours > 0 else "🔴 Collect Today (Immediate)"
        return {
            "tier": "Red",
            "color": "red",
            "label": urgency_label,
            "badge_html": f'<span style="background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; font-weight: 700; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px;">{urgency_label}</span>'
        }
    elif delta_hours <= 48:
        hours = int(total_seconds // 3600)
        return {
            "tier": "Orange",
            "color": "orange",
            "label": f"🟠 Expires within 2 days ({hours}h left)",
            "badge_html": f'<span style="background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; font-weight: 700; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px;">🟠 Expires within 2 days ({hours}h left)</span>'
        }
    else:
        days = int(delta_hours // 24)
        return {
            "tier": "Green",
            "color": "green",
            "label": f"🟢 Available for more than 2 days ({days}d left)",
            "badge_html": f'<span style="background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; font-weight: 700; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px;">🟢 Available for >2 days ({days}d left)</span>'
        }



# ==============================================================================
# SECTION 4: INPUT VALIDATION FUNCTIONS
# Demonstrates: Modular Functions, Basic Type Hints, If/Else Conditions & List Comprehensions
# ==============================================================================
def validate_donor_name(name: str) -> tuple[bool, str]:
    """
    Validate that the donor or organisation name has at least 2 characters.
    
    Demonstrates:
    - Basic Type Hints: name: str -> tuple[bool, str]
    - String manipulation: .strip() and len()
    - If/Else Conditions: boundary length check
    
    Parameters:
        name (str): Donor or organization name entered in form.
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not name or len(name.strip()) < 2:
        return False, "Organisation or donor name must have at least 2 characters."
    return True, ""


def validate_food_item(food_item: str) -> tuple[bool, str]:
    """
    Validate that the food item name has at least 2 characters.
    
    Demonstrates:
    - Basic Type Hints: food_item: str -> tuple[bool, str]
    - If/Else Conditions: verifying minimum character requirement
    
    Parameters:
        food_item (str): Name or title of the surplus food batch.
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not food_item or len(food_item.strip()) < 2:
        return False, "Food item name must have at least 2 characters."
    return True, ""


def validate_quantity(servings: Any) -> tuple[bool, str]:
    """
    Validate that quantity (estimated servings/meals) is strictly above zero.
    
    Demonstrates:
    - Exception Handling: try...except catching ValueError and TypeError
    - If/Else Conditions: boundary comparison (> 0)
    - Basic Type Hints: servings: Any -> tuple[bool, str]
    
    Parameters:
        servings (Any): Value entered for number of servings/meals.
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    try:
        val: float = float(servings)
        if val <= 0:
            return False, "Estimated servings/meals quantity must be above zero."
        return True, ""
    except (ValueError, TypeError):
        return False, "Estimated servings/meals must be a valid number above zero."


def validate_expiry_date(expiry_date: datetime.date, expiry_time: Optional[datetime.time] = None) -> tuple[bool, str]:
    """
    Validate that the expiry date and time cannot be in the past.
    
    Demonstrates:
    - Datetime arithmetic: comparing selected date against current system clock
    - Optional parameters with default None
    - If/Else Conditions: nested time comparison
    - Basic Type Hints: expiry_date: datetime.date, expiry_time: Optional[datetime.time] -> tuple[bool, str]
    
    Parameters:
        expiry_date (datetime.date): Expiry date.
        expiry_time (Optional[datetime.time]): Expiry time of day.
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not expiry_date:
        return False, "Best before date is required."
    now: dt = dt.now()
    if expiry_time:
        exp_dt: dt = dt.combine(expiry_date, expiry_time)
        if exp_dt < now:
            return False, "Best before date and time cannot be in the past."
    else:
        if expiry_date < now.date():
            return False, "Best before date cannot be in the past."
    return True, ""


def validate_location(location: str) -> tuple[bool, str]:
    """
    Validate that the pickup location address has at least 3 characters.
    
    Demonstrates:
    - String manipulation: .strip() and len()
    - Basic Type Hints: location: str -> tuple[bool, str]
    
    Parameters:
        location (str): Pickup address or area description.
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not location or len(location.strip()) < 3:
        return False, "Pickup location must have at least 3 characters."
    return True, ""


def validate_contact_number(contact_number: str) -> tuple[bool, str]:
    """
    Validate that the contact phone number includes at least 10 digits.
    
    Demonstrates:
    - List Comprehension: filtering numeric characters from phone string
    - Lists: counting length of extracted digits
    - If/Else Conditions: checking minimum 10-digit threshold
    - Basic Type Hints: contact_number: str -> tuple[bool, str]
    
    Parameters:
        contact_number (str): Raw phone number string entered by user.
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not contact_number:
        return False, "Contact number is required."
    digits: list[str] = [c for c in contact_number if c.isdigit()]
    if len(digits) < 10:
        return False, f"Contact number must include at least 10 digits (currently has {len(digits)})."
    return True, ""


def validate_donation_form_fields(
    donor_name: str,
    contact_number: str,
    food_item: str,
    servings: Any,
    expiry_date: datetime.date,
    location: str,
    expiry_time: Optional[datetime.time] = None
) -> list[str]:
    """
    Validate all required fields using core Python validation functions.
    
    Demonstrates:
    - Lists: building a list of validation check tuples and accumulating error messages
    - Loops: iterating through checks using a for loop
    - Functions: calling multiple modular helper functions
    - Basic Type Hints: typed parameters and list[str] return type
    
    Returns:
        list[str]: List of validation error messages (empty if all fields valid).
    """
    errors: list[str] = []
    checks: list[tuple[bool, str]] = [
        validate_donor_name(donor_name),
        validate_contact_number(contact_number),
        validate_food_item(food_item),
        validate_quantity(servings),
        validate_expiry_date(expiry_date, expiry_time),
        validate_location(location)
    ]
    # Loop: Check each validation result and collect error strings
    for is_valid, error_msg in checks:
        if not is_valid:
            errors.append(error_msg)
    return errors


# ==============================================================================
# SECTION 5: UI & PAGE RENDERING FUNCTIONS
# Demonstrates: Functions, Basic Type Hints & Streamlit Components
# ==============================================================================
def render_header() -> None:
    """Render the global hero header banner with sustainability branding."""
    st.markdown("""
    <div class="app-header">
        <div class="badge-pill-header">
            <span>🌱</span> ZERO HUNGER • ZERO FOOD WASTE • SUSTAINABILITY IN ACTION
        </div>
        <h1>Smart Food Waste Management System</h1>
        <p>Connecting surplus food from restaurants, hotels, homes, and events with NGOs, community kitchens, and people in need before it expires.</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# SIDEBAR NAVIGATION & QUICK ACTIONS
# ==========================================
def render_sidebar(donations: list[dict[str, Any]]) -> str:
    """
    Render the sidebar navigation, live sustainability stats, and data reset tools.
    
    Demonstrates:
    - Lists: sum() iterations over donation status attributes
    - Basic Type Hints: donations: list[dict[str, Any]] -> str
    - Dictionaries: .get() property extraction
    """
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 0.5rem;">
            <div style="font-size: 3rem; margin-bottom: 0.25rem;">🥗 ➔ 🤝 ➔ 🍲</div>
            <h3 style="color: #064e3b; margin: 0; font-family: 'Outfit', sans-serif;">Food Rescue Hub</h3>
            <p style="font-size: 0.8rem; color: #059669; margin-top: 0.25rem;">Clean Food, Cleaner Planet</p>
        </div>
        """, unsafe_allow_html=True)

        page = st.radio(
            "Navigate Platform",
            [
                "📊 Impact Dashboard",
                "🔍 Find Food",
                "➕ Donate Food",
                "📈 Impact Report",
                "📋 Manage Listings & Claims",
                "🛡️ Safety & Handling Guidelines"
            ],
            index=0
        )

        st.markdown("---")

        # Quick stats snapshot in sidebar
        active_count = sum(1 for d in donations if d.get("status") == "Available")
        claimed_count = sum(1 for d in donations if d.get("status") == "Claimed")
        completed_count = sum(1 for d in donations if d.get("status") in ["Completed", "Collected"])
        total_kg = sum(d.get("weight_kg", 0) for d in donations if d.get("status") in ["Claimed", "Completed", "Collected"])
        co2_saved = round(total_kg * 2.5, 1)

        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #d1fae5; border-radius: 12px; padding: 1rem; margin-top: 0.5rem;">
            <div style="font-size: 0.78rem; font-weight: 700; color: #047857; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
                🌿 Quick Sustainability Pulse
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.4rem;">
                <span style="color: #4b5563;">Active Listings:</span>
                <strong style="color: #059669;">{active_count} ready</strong>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.4rem;">
                <span style="color: #4b5563;">In Pickup / Transit:</span>
                <strong style="color: #0284c7;">{claimed_count} claims</strong>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.4rem;">
                <span style="color: #4b5563;">Completed Rescues:</span>
                <strong style="color: #10b981;">{completed_count} done</strong>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px dashed #d1fae5;">
                <span style="color: #064e3b; font-weight: 600;">CO₂ Diverted:</span>
                <strong style="color: #047857;">{co2_saved} kg CO₂e</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        with st.expander("⚙️ System Storage Tools"):
            st.caption("JSON Storage File:")
            st.code(DATA_FILE, language="text")
            if st.button("🔄 Reset Demo Seed Data", use_container_width=True):
                new_seed = generate_seed_data()
                save_donations(new_seed)
                st.success("Sample seed database refreshed with current timestamps!")
                st.rerun()

        st.caption("v1.2 • Zero Waste Platform • Python & Streamlit")

    return page


# ==========================================
# PAGE 1: IMPACT DASHBOARD
# ==========================================
def render_dashboard(donations: list[dict[str, Any]]) -> None:
    """
    Render the real-time operational and sustainability impact dashboard.
    
    Demonstrates:
    - Lists: Filtering donations by status using list comprehensions
    - Loops: Iterating over listings to calculate urgent (<6h) and priority (<48h) batches
    - Dictionaries: Accessing nested and flat dictionary attributes
    - If/Else Conditions: Threshold checking and rendering clean empty states
    - Basic Type Hints: donations: list[dict[str, Any]] -> None
    """
    render_header()

    # Sustainability & Data Computations
    total_listings = len(donations)
    active_donations = [d for d in donations if d.get("status") == "Available"]
    claimed_donations = [d for d in donations if d.get("status") == "Claimed"]
    completed_donations = [d for d in donations if d.get("status") in ["Completed", "Collected"]]

    rescued_items = claimed_donations + completed_donations

    active_count = len(active_donations)
    available_meals = sum(d.get("portions", 0) for d in active_donations)
    available_weight = sum(d.get("weight_kg", 0.0) for d in active_donations)

    total_meals_saved = sum(d.get("portions", 0) for d in rescued_items)
    total_kg_rescued = sum(d.get("weight_kg", 0.0) for d in rescued_items)

    co2_averted_kg = round(total_kg_rescued * 2.5, 1)
    water_saved_liters = round(total_kg_rescued * 1000)

    # Calculate Urgent Pickups (< 6h) and Priority Expiring (Today or within 2 days / 48h)
    urgent_items = []
    priority_two_days_items = []

    for d in active_donations:
        info = get_expiry_details(d.get("expires_at", ""))
        delta_h = info.get("delta_hours", 999)
        
        # Priority: Expiring today or within 2 days (0 < delta_h <= 48 hours)
        if 0 < delta_h <= 48:
            is_today = delta_h <= 24
            priority_two_days_items.append((d, info, is_today))

        # Urgent pickups: < 6 hours remaining
        if 0 < delta_h <= 6:
            urgent_items.append((d, info))

    # Sort priority items: most urgent first (shortest time remaining)
    priority_two_days_items.sort(key=lambda x: x[1].get("delta_hours", 999))
    urgent_count = len(urgent_items)

    # ----------------------------------------------------
    # 1. STREAMLIT METRICS SECTION (COLUMNS & CONTAINERS)
    # ----------------------------------------------------
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        with st.container(border=True):
            st.metric(
                label="🍱 Active Food Listings",
                value=f"{active_count}",
                delta=f"{total_listings} Total Tracked",
                delta_color="normal"
            )
            st.caption("Active surplus batches awaiting pickup")

    with col_m2:
        with st.container(border=True):
            st.metric(
                label="🍲 Estimated Meals Available",
                value=f"{available_meals:,}",
                delta=f"~{available_weight:.1f} kg surplus",
                delta_color="normal"
            )
            st.caption("Fresh, wholesome meal portions ready")

    with col_m3:
        with st.container(border=True):
            st.metric(
                label="🚨 Urgent Pickups (< 6h)",
                value=f"{urgent_count}",
                delta="Critical Window" if urgent_count > 0 else "All Clear",
                delta_color="inverse" if urgent_count > 0 else "off"
            )
            st.caption("Require priority volunteer collection")

    with col_m4:
        with st.container(border=True):
            st.metric(
                label="🌿 CO₂e Emissions Averted",
                value=f"{co2_averted_kg} kg",
                delta=f"{total_meals_saved} meals saved",
                delta_color="normal"
            )
            st.caption("Diverted from municipal landfills")

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # 2. “HOW IT WORKS” SECTION (3 CLEAR STEPS)
    # ----------------------------------------------------
    st.markdown('<div class="section-title">🔄 How It Works</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #4b5563; margin-top: -0.4rem; margin-bottom: 1.1rem; font-size: 0.95rem;'>Our automated surplus food routing bridges food businesses with community responders in three seamless steps:</p>", unsafe_allow_html=True)

    hw_col1, hw_col2, hw_col3 = st.columns(3)

    with hw_col1:
        with st.container(border=True):
            st.markdown("""
            <div style="padding: 0.4rem 0.2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <span style="background: #ecfdf5; color: #047857; font-weight: 700; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px; border: 1px solid #a7f3d0;">
                        STEP 1
                    </span>
                    <span style="font-size: 2rem;">🏢 ➔ 📋</span>
                </div>
                <h4 style="color: #064e3b; margin: 0 0 0.5rem 0; font-family: 'Outfit', sans-serif;">1. Donors list surplus food</h4>
                <p style="color: #4b5563; font-size: 0.88rem; line-height: 1.55; margin: 0;">
                    Restaurants, hotels, caterers, banquet organizers, and households log unserved surplus food in under 2 minutes. They specify meal portions, dietary category (Veg, Non-Veg, Vegan), storage state, and safe expiry window.
                </p>
                <div style="margin-top: 0.85rem; padding-top: 0.5rem; border-top: 1px dashed #d1fae5; font-size: 0.78rem; color: #059669; font-weight: 600;">
                    ✓ Food-grade packaging & safe holding
                </div>
            </div>
            """, unsafe_allow_html=True)

    with hw_col2:
        with st.container(border=True):
            st.markdown("""
            <div style="padding: 0.4rem 0.2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <span style="background: #e0f2fe; color: #0369a1; font-weight: 700; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px; border: 1px solid #bae6fd;">
                        STEP 2
                    </span>
                    <span style="font-size: 2rem;">📍 ➔ 🔍</span>
                </div>
                <h4 style="color: #064e3b; margin: 0 0 0.5rem 0; font-family: 'Outfit', sans-serif;">2. NGOs/volunteers find nearby food</h4>
                <p style="color: #4b5563; font-size: 0.88rem; line-height: 1.55; margin: 0;">
                    Verified NGOs, shelters, and community volunteers browse live listings filtered by neighborhood, diet, and time urgency. They claim batches with an estimated pickup ETA and receive a secure Pickup Verification Code.
                </p>
                <div style="margin-top: 0.85rem; padding-top: 0.5rem; border-top: 1px dashed #bae6fd; font-size: 0.78rem; color: #0284c7; font-weight: 600;">
                    ✓ Automated Pickup Verification Code
                </div>
            </div>
            """, unsafe_allow_html=True)

    with hw_col3:
        with st.container(border=True):
            st.markdown("""
            <div style="padding: 0.4rem 0.2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <span style="background: #f0fdf4; color: #15803d; font-weight: 700; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px; border: 1px solid #bbf7d0;">
                        STEP 3
                    </span>
                    <span style="font-size: 2rem;">🚚 ➔ 🥗</span>
                </div>
                <h4 style="color: #064e3b; margin: 0 0 0.5rem 0; font-family: 'Outfit', sans-serif;">3. Food is collected and waste is reduced</h4>
                <p style="color: #4b5563; font-size: 0.88rem; line-height: 1.55; margin: 0;">
                    Volunteers collect food using insulated temperature carriers and distribute wholesome meals directly to vulnerable families. Organic food is kept out of landfills, eliminating methane and CO₂ emissions.
                </p>
                <div style="margin-top: 0.85rem; padding-top: 0.5rem; border-top: 1px dashed #bbf7d0; font-size: 0.78rem; color: #16a34a; font-weight: 600;">
                    ✓ Zero hunger impact & real-time CO₂ logs
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # 3. PRIORITY PICKUP CARDS (EXPIRING TODAY OR WITHIN 2 DAYS)
    # ----------------------------------------------------
    st.markdown('<div class="section-title">⚡ Priority Pickups: Expiring Today or Within Two Days</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #4b5563; margin-top: -0.4rem; margin-bottom: 1.1rem; font-size: 0.95rem;'>High-priority surplus food batches requiring immediate collection to ensure safe consumption and prevent waste:</p>", unsafe_allow_html=True)

    if not priority_two_days_items:
        # Clear Empty State
        with st.container(border=True):
            st.markdown("""
            <div style="text-align: center; padding: 2.2rem 1.5rem;">
                <div style="font-size: 3.2rem; margin-bottom: 0.5rem;">🌿 🥗 ✨</div>
                <h3 style="color: #065f46; font-family: 'Outfit', sans-serif; margin-bottom: 0.35rem;">No Imminent Food Waste at Risk!</h3>
                <p style="color: #4b5563; max-width: 580px; margin: 0 auto 1.25rem auto; font-size: 0.95rem; line-height: 1.55;">
                    There are currently no active surplus food listings expiring today or within the next 48 hours. All existing donations are either safely stored or have already been collected by volunteers.
                </p>
            </div>
            """, unsafe_allow_html=True)
            e_c1, e_c2 = st.columns(2)
            with e_c1:
                st.info("💡 **Have extra food to share?** Restaurants, caterers, and households can post surplus meals anytime in the **Donate Food** portal.")
            with e_c2:
                st.success("🤝 **Want to explore all surplus food?** Check out the complete marketplace under **Browse Surplus Food** to plan upcoming pickups.")
    else:
        # Render priority cards in columns
        priority_cols = st.columns(2)
        for idx, (item, expiry_info, is_today) in enumerate(priority_two_days_items):
            target_col = priority_cols[idx % 2]
            with target_col:
                with st.container(border=True):
                    # Dietary class
                    dietary = item.get("dietary", "Vegetarian")
                    dietary_class = "badge-dietary-veg"
                    if dietary == "Vegan":
                        dietary_class = "badge-dietary-vegan"
                    elif dietary == "Non-Vegetarian":
                        dietary_class = "badge-dietary-nonveg"

                    # Urgency tag
                    if is_today:
                        urgency_badge = "🔴 EXPIRING TODAY"
                        urgency_style = "background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca;"
                    else:
                        urgency_badge = "🟡 EXPIRING WITHIN 48H"
                        urgency_style = "background: #fffbeb; color: #b45309; border: 1px solid #fde68a;"

                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 6px;">
                        <div>
                            <span style="{urgency_style} font-weight: 700; font-size: 0.75rem; padding: 3px 10px; border-radius: 9999px;">
                                {urgency_badge}
                            </span>
                            <span class="badge {dietary_class}" style="margin-left: 4px;">{dietary}</span>
                            <span class="badge {expiry_info['badge_class']}">{expiry_info['label']}</span>
                        </div>
                        <span style="font-size: 0.78rem; font-weight: 700; color: #6b7280;">ID: {item.get('id')}</span>
                    </div>
                    <h4 style="color: #064e3b; margin: 0.4rem 0 0.2rem 0; font-family: 'Outfit', sans-serif;">{item.get('title')}</h4>
                    <div style="font-size: 0.88rem; color: #047857; font-weight: 600; margin-bottom: 0.6rem;">
                        🏢 {item.get('donor_name')} &bull; <span style="color: #4b5563; font-weight: 400;">{item.get('donor_type')}</span>
                    </div>
                    <div style="background: #f8fafc; border: 1px solid #f1f5f9; border-radius: 8px; padding: 0.65rem 0.85rem; margin-bottom: 0.75rem; font-size: 0.84rem; display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
                        <div>📦 <strong>Portions:</strong> {item.get('portions')} (~{item.get('weight_kg')} kg)</div>
                        <div>❄️ <strong>Storage:</strong> {item.get('storage_condition')}</div>
                        <div>📍 <strong>Area:</strong> {item.get('city_area')}</div>
                        <div>⏱️ <strong>Best Before:</strong> {item.get('expires_at')}</div>
                    </div>
                    <div style="font-size: 0.82rem; color: #374151; margin-bottom: 0.65rem;">
                        <strong>Pickup:</strong> {item.get('pickup_address')}<br>
                        <strong>Contact:</strong> {item.get('contact_person')} ({item.get('contact_phone')})
                    </div>
                    """, unsafe_allow_html=True)

                    # Quick pickup claim expander
                    with st.expander(f"🤝 Claim Priority Pickup ({item.get('id')})", expanded=False):
                        with st.form(key=f"dash_claim_{item.get('id')}"):
                            st.caption("Reserve this priority batch for immediate collection:")
                            dc_org = st.text_input("NGO / Volunteer Organization *", placeholder="e.g. Robin Hood Army / Community Shelter")
                            dc_name = st.text_input("Volunteer Name *", placeholder="Your full name")
                            dc_phone = st.text_input("Contact Mobile *", placeholder="+91 98765 00000")
                            dc_eta = st.selectbox("Estimated Pickup Arrival", ["Within 30 mins", "Within 1 hour", "Within 2 hours", "Within 3 hours"], key=f"eta_{item.get('id')}")
                            dc_submit = st.form_submit_button("⚡ Reserve Priority Pickup", type="primary", use_container_width=True)

                            if dc_submit:
                                if not dc_org or not dc_name or not dc_phone:
                                    st.error("Please enter Organization, Volunteer Name, and Phone.")
                                else:
                                    claim_code = f"PICK-{uuid.uuid4().hex[:6].upper()}"
                                    item["status"] = "Claimed"
                                    item["claim_info"] = {
                                        "claim_code": claim_code,
                                        "claimed_by": dc_name,
                                        "organization": dc_org,
                                        "recipient_type": "Priority Rescue Volunteer",
                                        "phone": dc_phone,
                                        "eta": dc_eta,
                                        "purpose": "Priority rescue of expiring batch",
                                        "claimed_at": dt.now().strftime("%Y-%m-%d %H:%M")
                                    }
                                    save_donations(donations)
                                    st.success(f"🎉 Reserved! Verification Code: **{claim_code}**")
                                    st.balloons()
                                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # 4. VISUAL FOOD FLOW & SUSTAINABILITY INSIGHTS
    # ----------------------------------------------------
    st.markdown('<div class="section-title">📊 Visual Food Flow & Sustainability Insights</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🍱 Food Rescued by Category")
        if donations:
            cat_data = {}
            for d in donations:
                cat = d.get("category", "Other")
                cat_data[cat] = cat_data.get(cat, 0) + d.get("portions", 0)
            
            df_cat = pd.DataFrame(list(cat_data.items()), columns=["Category", "Portions"])
            st.bar_chart(df_cat.set_index("Category"), color="#059669")
        else:
            st.info("No donation data available yet.")

    with col2:
        st.subheader("🏢 Donor Network Breakdown")
        if donations:
            donor_types = {}
            for d in donations:
                dtype = d.get("donor_type", "Other")
                donor_types[dtype] = donor_types.get(dtype, 0) + 1
            
            df_donors = pd.DataFrame(list(donor_types.items()), columns=["Donor Type", "Total Listings"])
            st.bar_chart(df_donors.set_index("Donor Type"), color="#10b981")
        else:
            st.info("No donor data available.")

    # ----------------------------------------------------
    # 5. REAL-WORLD ENVIRONMENTAL EQUIVALENCIES
    # ----------------------------------------------------
    st.markdown('<div class="section-title">🌍 Real-World Environmental Equivalency</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        km_driven = round(co2_averted_kg * 4.2, 1)  # approx ~0.24 kg CO2/km driven
        with st.container(border=True):
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem 0;">
                <div style="font-size: 2.2rem; margin-bottom: 0.4rem;">🚗</div>
                <h3 style="margin: 0; color: #064e3b; font-size: 1.6rem; font-family: 'Outfit', sans-serif;">{km_driven:,} km</h3>
                <p style="color: #6b7280; font-size: 0.85rem; margin-top: 0.25rem;">Standard passenger car emissions avoided</p>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        homes_powered = round(co2_averted_kg * 0.12, 1)
        with st.container(border=True):
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem 0;">
                <div style="font-size: 2.2rem; margin-bottom: 0.4rem;">💡</div>
                <h3 style="margin: 0; color: #064e3b; font-size: 1.6rem; font-family: 'Outfit', sans-serif;">{homes_powered:,} Days</h3>
                <p style="color: #6b7280; font-size: 0.85rem; margin-top: 0.25rem;">Clean electricity equivalent conserved</p>
            </div>
            """, unsafe_allow_html=True)

    with c3:
        people_fed = total_meals_saved
        with st.container(border=True):
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem 0;">
                <div style="font-size: 2.2rem; margin-bottom: 0.4rem;">🤝</div>
                <h3 style="margin: 0; color: #064e3b; font-size: 1.6rem; font-family: 'Outfit', sans-serif;">{people_fed:,} People</h3>
                <p style="color: #6b7280; font-size: 0.85rem; margin-top: 0.25rem;">Nutritious meals delivered to community</p>
            </div>
            """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # 6. RECENT RESCUE OPERATIONS ACTIVITY LOG
    # ----------------------------------------------------
    st.markdown('<div class="section-title">⏱️ Recent Food Rescue Operations</div>', unsafe_allow_html=True)
    recent = sorted(donations, key=lambda x: x.get("created_at", ""), reverse=True)[:5]
    
    if not recent:
        st.info("No activity recorded yet.")
    else:
        for item in recent:
            status = item.get("status", "Available")
            status_color = "#10b981" if status == "Available" else ("#0284c7" if status == "Claimed" else "#6b7280")
            st.markdown(f"""
            <div style="background: #ffffff; border: 1px solid #f1f5f9; border-left: 4px solid {status_color}; border-radius: 8px; padding: 0.85rem 1.2rem; margin-bottom: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{item.get('title')}</strong> • <span style="color: #6b7280; font-size: 0.85rem;">{item.get('portions')} portions ({item.get('weight_kg')} kg)</span><br>
                    <span style="font-size: 0.8rem; color: #059669;">📍 {item.get('donor_name')} ({item.get('city_area')})</span>
                </div>
                <div>
                    <span style="background: #f8fafc; border: 1px solid #e2e8f0; color: {status_color}; font-weight: 700; font-size: 0.78rem; padding: 4px 10px; border-radius: 9999px;">
                        {status.upper()}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# PAGE 2: FIND FOOD
# ==========================================
def render_find_food_page(donations: list[dict[str, Any]]) -> None:
    """
    Render the active surplus food discovery marketplace with filters and search.
    
    Demonstrates:
    - Lists: Filtering active listings by category and search keywords
    - Loops: Enumerating over listings to build a 2-column card layout
    - If/Else Conditions: Matching search criteria and checking for empty results
    - File Handling with JSON: Modifying listing status to 'Collected' and saving to disk
    - Basic Type Hints: donations: list[dict[str, Any]] -> None
    """
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h2 style="color: #064e3b; font-family: 'Outfit', sans-serif; margin-bottom: 0.25rem;">🔍 Find Food</h2>
        <p style="color: #4b5563; font-size: 0.95rem;">
            Browse real-time active surplus food listings loaded directly from <code>food_listings.json</code>. Filter by category, search by food name, donor, or location, and mark items as collected to eliminate food waste.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Freshness Status Legend
    st.markdown("""
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 0.8rem 1.2rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
        <div style="font-size: 0.82rem; font-weight: 700; color: #064e3b; text-transform: uppercase; letter-spacing: 0.04em;">
            ⏱️ Freshness Status Legend:
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <span style="background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; font-weight: 700; font-size: 0.78rem; padding: 3px 10px; border-radius: 9999px;">
                🔴 Red: Collect today (&le; 24h)
            </span>
            <span style="background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; font-weight: 700; font-size: 0.78rem; padding: 3px 10px; border-radius: 9999px;">
                🟠 Orange: Expires within 2 days (24–48h)
            </span>
            <span style="background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; font-weight: 700; font-size: 0.78rem; padding: 3px 10px; border-radius: 9999px;">
                🟢 Green: Available for &gt;2 days
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filters: Search & Category Dropdown
    search_col, cat_col = st.columns([3, 2])
    with search_col:
        search_query = st.text_input(
            "🔍 Search Food Name, Donor Name, or Location",
            placeholder="e.g. Biryani, Bread, Sharma, Indiranagar, Grand Palace..."
        )
    with cat_col:
        categories = ["All Categories", "Cooked meals", "Fruits & vegetables", "Bakery", "Dairy", "Packaged food", "Other"]
        selected_category = st.selectbox("📦 Filter by Category", categories)

    # Active Listings Filter from food_listings.json
    active_items = []
    for item in donations:
        # Load active listings only
        if item.get("status") != "Available":
            continue

        item_food = item.get("food_item") or item.get("title") or ""
        item_donor = item.get("donor_name") or ""
        item_location = item.get("location") or item.get("pickup_address") or item.get("city_area") or ""
        item_category = item.get("category") or "Other"

        # Category Filter
        if selected_category != "All Categories":
            if item_category.lower() != selected_category.lower():
                continue

        # Search Query Filter
        if search_query:
            query = search_query.lower()
            text_corpus = f"{item_food} {item_donor} {item_location}".lower()
            if query not in text_corpus:
                continue

        # Freshness Status Calculation
        expiry_str = item.get("best_before") or item.get("expires_at") or ""
        freshness = get_freshness_status(expiry_str)
        active_items.append((item, freshness))

    # Header counter
    st.markdown(f"**Showing {len(active_items)} active food listings** ready for pickup:")
    st.markdown("<br>", unsafe_allow_html=True)

    # Clear Empty State
    if not active_items:
        with st.container(border=True):
            st.markdown("""
            <div style="text-align: center; padding: 2.5rem 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔍 🥗 ✨</div>
                <h3 style="color: #065f46; font-family: 'Outfit', sans-serif; margin-bottom: 0.35rem;">No Active Food Listings Found</h3>
                <p style="color: #4b5563; max-width: 540px; margin: 0 auto 1.25rem auto; font-size: 0.95rem; line-height: 1.55;">
                    There are no available food listings matching your selected category and search terms. All items may have already been collected or you can try resetting your search filters.
                </p>
            </div>
            """, unsafe_allow_html=True)
            e1, e2 = st.columns(2)
            with e1:
                st.info("💡 **Have food to share?** Post surplus meals anytime using the **Donate Food** portal.")
            with e2:
                st.success("🔄 Try selecting **All Categories** or clearing the search query.")
        return

    # Render Food Listing Cards in 2 Columns
    c_left, c_right = st.columns(2)
    for idx, (item, freshness) in enumerate(active_items):
        target_col = c_left if idx % 2 == 0 else c_right
        with target_col:
            with st.container(border=True):
                # Fields
                food_title = item.get("food_item") or item.get("title") or "Surplus Food"
                category_name = item.get("category") or "Cooked meals"
                servings = item.get("servings") or item.get("portions") or "N/A"
                donor = item.get("donor_name") or "Community Donor"
                loc = item.get("location") or item.get("pickup_address") or "City Area"
                contact = item.get("contact_number") or item.get("contact_phone") or "Not provided"
                safety = item.get("safety_notes") or item.get("notes") or "Standard hygiene and safe packaging observed."
                expiry_date = item.get("best_before") or item.get("expires_at") or "Not specified"

                # Card Header with Badges
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 6px;">
                    <div>
                        {freshness['badge_html']}
                        <span style="background: #f1f5f9; color: #475569; font-weight: 600; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px; border: 1px solid #cbd5e1; margin-left: 4px;">
                            {category_name}
                        </span>
                    </div>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #94a3b8;">ID: {item.get('id')}</span>
                </div>
                <h3 style="color: #064e3b; margin: 0.35rem 0 0.2rem 0; font-family: 'Outfit', sans-serif; font-size: 1.25rem;">
                    {food_title}
                </h3>
                <div style="font-size: 0.88rem; color: #047857; font-weight: 600; margin-bottom: 0.6rem;">
                    🏢 <strong>Donor:</strong> {donor}
                </div>
                <div style="background: #f8fafc; border: 1px solid #f1f5f9; border-radius: 10px; padding: 0.75rem 0.85rem; margin-bottom: 0.75rem; font-size: 0.85rem; display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
                    <div>📦 <strong>Quantity:</strong> {servings} Servings / Meals</div>
                    <div>⏱️ <strong>Best Before:</strong> {expiry_date}</div>
                    <div>📍 <strong>Location:</strong> {loc}</div>
                    <div>📞 <strong>Contact:</strong> {contact}</div>
                </div>
                <div style="font-size: 0.82rem; color: #4b5563; background: #fafafa; border: 1px dashed #e2e8f0; border-radius: 8px; padding: 0.6rem 0.8rem; margin-bottom: 0.85rem;">
                    🛡️ <strong>Safety Notes:</strong> {safety}
                </div>
                """, unsafe_allow_html=True)

                # "Mark Collected" Button
                if st.button(f"✅ Mark Collected", key=f"mark_collected_{item.get('id')}", type="primary", use_container_width=True):
                    # Update status in JSON file from Available to Collected
                    item["status"] = "Collected"
                    item["collected_at"] = dt.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_donations(donations)
                    st.success(f"🎉 '{food_title}' marked as Collected!")
                    st.rerun()

# Backward compatibility alias
render_browse_and_claim = render_find_food_page


# ==========================================
# PAGE 3: DONATE FOOD (DONOR PORTAL)
# ==========================================
def render_donate_page(donations: list[dict[str, Any]]) -> None:
    """
    Render the validated food donor portal form for registering surplus food.
    
    Demonstrates:
    - Input Validation: 6 dedicated validation functions verifying all required fields
    - Loops (While Loop): Calling generate_unique_id() to ensure unique sequential IDs
    - Dictionaries: Constructing new food listing record with diverse key-value pairs
    - Lists: Appending the new record to the master donations list
    - File Handling with JSON: Persisting new donation to 'food_listings.json'
    - Basic Type Hints: donations: list[dict[str, Any]] -> None
    """
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #064e3b; font-family: 'Outfit', sans-serif; margin-bottom: 0.25rem;">➕ Donate Food</h2>
        <p style="color: #4b5563; font-size: 0.95rem;">
            List surplus food from restaurants, hotels, event organizers, caterers, or households to connect with nearby NGOs and volunteers before it expires.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Guidelines callout
    st.markdown("""
    <div class="eco-banner">
        <div style="font-size: 1.8rem;">🌿</div>
        <div>
            <strong>Safe Food Donation Standards:</strong> Ensure food is untouched, prepared in clean sanitary conditions, and packaged securely for temperature-safe transport.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 📝 Surplus Food Listing Form")
        st.caption("All fields marked with an asterisk (*) are validated by Python functions.")

        with st.form("donate_food_form", clear_on_submit=False):
            # 1. Donor & Contact Information
            st.markdown("#### 1. Donor & Contact Details")
            c_d1, c_d2 = st.columns(2)
            with c_d1:
                donor_name = st.text_input(
                    "Organisation or donor name *",
                    placeholder="e.g. Green Leaf Bistro, Hyatt Regency, Sharma Family",
                    help="Must have at least 2 characters"
                )
            with c_d2:
                contact_number = st.text_input(
                    "Contact number *",
                    placeholder="e.g. +91 98765 43210 (at least 10 digits)",
                    help="Must contain at least 10 digits"
                )

            st.markdown("---")

            # 2. Food Item Details
            st.markdown("#### 2. Food Specifications")
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                food_item = st.text_input(
                    "Food item name *",
                    placeholder="e.g. 50 Packs Veg Dum Biryani, Fresh Sourdough Bread, Organic Fruit Crates",
                    help="Must have at least 2 characters"
                )
            with c_f2:
                category = st.selectbox(
                    "Food category *",
                    ["Cooked meals", "Fruits & vegetables", "Bakery", "Dairy", "Packaged food", "Other"]
                )

            # 3. Servings and Expiry
            c_q1, c_q2, c_q3 = st.columns(3)
            with c_q1:
                servings = st.number_input(
                    "Estimated servings/meals *",
                    min_value=0,
                    value=30,
                    step=1,
                    help="Quantity must be strictly above zero"
                )
            with c_q2:
                best_before_date = st.date_input(
                    "Best before date *",
                    min_value=dt.now().date(),
                    value=dt.now().date(),
                    help="Expiry date cannot be in the past"
                )
            with c_q3:
                best_before_time = st.time_input(
                    "Best before time *",
                    value=(dt.now() + timedelta(hours=4)).time(),
                    help="Target safe consumption cutoff time"
                )

            st.markdown("---")

            # 4. Pickup Location
            st.markdown("#### 3. Pickup Logistics")
            location = st.text_area(
                "Pickup location *",
                placeholder="Full pickup address, street, building/floor, gate number, loading dock instructions (at least 3 characters)",
                help="Must have at least 3 characters"
            )

            st.markdown("---")

            # 5. Optional Safety Notes & Handling
            st.markdown("#### 4. Optional Safety & Handling Notes")
            c_s1, c_s2 = st.columns(2)
            with c_s1:
                dietary = st.selectbox(
                    "Vegetarian / Non-Vegetarian / Dietary",
                    ["Vegetarian", "Vegan", "Non-Vegetarian", "Egg Only", "Other / Not Specified"]
                )
            with c_s2:
                packing_details = st.selectbox(
                    "Packing Details",
                    [
                        "Sealed Food-Grade Containers / Trays",
                        "Clean Paper / Bakery Bags",
                        "Insulated Thermal Boxes",
                        "Original Sealed Packaged Goods",
                        "Transfer Vessels Required (Bring Crates/Pots)",
                        "Other"
                    ]
                )

            safety_notes = st.text_area(
                "Optional safety notes (Allergens, ingredients, storage & handling instructions)",
                placeholder="e.g. Contains dairy & nuts. Kept in warm insulated box (>60°C). Disposable food containers."
            )

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🌱 Submit Food Listing", type="primary", use_container_width=True)

            if submitted:
                # Validate all fields with Python functions
                validation_errors = validate_donation_form_fields(
                    donor_name=donor_name,
                    contact_number=contact_number,
                    food_item=food_item,
                    servings=servings,
                    expiry_date=best_before_date,
                    location=location,
                    expiry_time=best_before_time
                )

                if validation_errors:
                    st.error("⚠️ **Please correct the following errors before submitting:**")
                    for err in validation_errors:
                        st.markdown(f"- ❌ {err}")
                else:
                    # Successful validation: Generate unique ID using while loop
                    new_id: str = generate_unique_id(donations)
                    expires_datetime = dt.combine(best_before_date, best_before_time).strftime("%Y-%m-%d %H:%M")
                    
                    new_listing = {
                        "id": new_id,
                        "donor_name": donor_name.strip(),
                        "contact_number": contact_number.strip(),
                        "contact_phone": contact_number.strip(),  # cross-compatibility
                        "contact_person": donor_name.strip(),    # cross-compatibility
                        "food_item": food_item.strip(),
                        "title": food_item.strip(),              # cross-compatibility
                        "category": category,
                        "servings": int(servings),
                        "portions": int(servings),               # cross-compatibility
                        "weight_kg": round(float(servings) * 0.4, 1),
                        "best_before_date": str(best_before_date),
                        "best_before": expires_datetime,
                        "expires_at": expires_datetime,          # cross-compatibility
                        "prepared_at": dt.now().strftime("%Y-%m-%d %H:%M"),
                        "location": location.strip(),
                        "pickup_address": location.strip(),      # cross-compatibility
                        "city_area": location.strip().split(",")[0].strip(),
                        "dietary": dietary,
                        "packing_details": packing_details,
                        "safety_notes": safety_notes.strip() if safety_notes else "No specific allergens reported.",
                        "notes": f"Diet: {dietary}. Packing: {packing_details}. {safety_notes.strip() if safety_notes else ''}".strip(),
                        "status": "Available",
                        "created_at": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "claim_info": None
                    }

                    # Add and save to food_listings.json
                    donations.append(new_listing)
                    save_donations(donations)

                    # Display success message
                    st.success("✅ **Food listing successfully submitted and saved to `food_listings.json`!**")
                    st.balloons()

                    # Summary card
                    st.markdown(f"""
                    <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 14px; padding: 1.4rem; margin-top: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                            <h4 style="color: #065f46; margin: 0;">🎉 Listing Published: {food_item.strip()}</h4>
                            <span style="background: #d1fae5; color: #065f46; font-weight: 700; font-size: 0.82rem; padding: 4px 12px; border-radius: 9999px;">
                                ID: {new_id}
                            </span>
                        </div>
                        <div style="margin-top: 0.75rem; font-size: 0.9rem; color: #166534; line-height: 1.6;">
                            • <strong>Organisation/Donor:</strong> {donor_name.strip()} ({contact_number.strip()})<br>
                            • <strong>Category:</strong> {category} &bull; <strong>Estimated Servings:</strong> {servings} meals (~{float(servings) * 0.4:.1f} kg)<br>
                            • <strong>Best Before Date:</strong> {expires_datetime}<br>
                            • <strong>Pickup Location:</strong> {location.strip()}<br>
                            • <strong>Dietary & Packing:</strong> {dietary} &bull; {packing_details}<br>
                            • <strong>Safety Notes:</strong> {safety_notes.strip() if safety_notes else 'None provided'}<br>
                        </div>
                        <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px dashed #86efac; font-size: 0.85rem; color: #047857; font-weight: 600;">
                            🌿 Potential Impact: Prevents ~{float(servings) * 0.4 * 2.5:.1f} kg of CO₂e emissions! Volunteers and NGOs have been notified.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


# ==========================================
# PAGE 4: IMPACT REPORT
# ==========================================
def render_impact_report_page(donations: list[dict[str, Any]]) -> None:
    """
    Render the transparency impact report page calculating metrics via Python loops and lists.
    
    Demonstrates:
    - Variables: Primitive types (int, float, str)
    - Lists: Separate lists for meal quantities and tabular rows
    - Loops: Explicit for-loops iterating over dictionaries and accumulating values
    - If/Else Conditions: Status classification (Collected vs Awaiting) and empty check
    - Dictionaries: Constructing audit table rows with exact schema keys
    - Basic Type Hints: donations: list[dict[str, Any]] -> None
    """
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div class="badge-pill-header" style="background: rgba(5, 150, 105, 0.15); border-color: #a7f3d0; color: #065f46;">
            🌱 TRANSPARENCY & COMMUNITY METRICS
        </div>
        <h2 style="color: #064e3b; font-family: 'Outfit', sans-serif; margin-bottom: 0.25rem;">
            📈 Surplus Food Impact Report
        </h2>
        <p style="color: #4b5563; font-size: 0.95rem;">
            Real-time audit of registered surplus food listings, estimated meals donated, volunteer redistributions, and live collection statuses.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # CALCULATE VALUES USING PYTHON LOOPS AND LISTS (CORE PYTHON)
    # -------------------------------------------------------------
    all_listings_list = list(donations) if donations else []

    # 1. Total food listings calculated via Python loop
    total_food_listings = 0
    for _ in all_listings_list:
        total_food_listings += 1

    # Python lists for storing extracted individual meal values and table records
    meals_donated_list = []
    meals_collected_list = []
    meals_awaiting_list = []
    table_rows_list = []

    for item in all_listings_list:
        # Extract estimated servings / meals safely
        servings_val = item.get("servings")
        if servings_val is None:
            servings_val = item.get("portions")
        if servings_val is None:
            servings_val = item.get("quantity", 0)

        try:
            qty_int = int(servings_val)
            if qty_int < 0:
                qty_int = 0
        except (ValueError, TypeError):
            qty_int = 0

        # Append to meals donated list
        meals_donated_list.append(qty_int)

        status_str = str(item.get("status", "Available")).strip()

        # Categorize into redistributed/collected vs awaiting collection
        if status_str in ["Collected", "Completed"]:
            meals_collected_list.append(qty_int)
        else:
            # "Available", "Claimed", etc.
            meals_awaiting_list.append(qty_int)

        # Extract table columns: Food name, quantity, donor, expiry date, and status
        food_name = item.get("food_item") or item.get("title") or "Surplus Food"
        donor_name = item.get("donor_name") or "Community Donor"
        expiry_date = item.get("best_before") or item.get("best_before_date") or item.get("expires_at") or "Not specified"

        table_rows_list.append({
            "Food name": food_name,
            "Quantity": f"{qty_int} meals",
            "Donor": donor_name,
            "Expiry date": expiry_date,
            "Status": status_str,
            "_raw_qty": qty_int
        })

    # Accumulate totals using Python loops over the extracted lists
    total_estimated_meals = 0
    for meals in meals_donated_list:
        total_estimated_meals += meals

    meals_redistributed = 0
    for meals in meals_collected_list:
        meals_redistributed += meals

    meals_awaiting = 0
    for meals in meals_awaiting_list:
        meals_awaiting += meals

    # -------------------------------------------------------------
    # METRICS DISPLAY (STREAMLIT COLUMNS & METRIC CARDS)
    # -------------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.metric(
                label="📦 Total Food Listings",
                value=f"{total_food_listings:,}",
                help="Total surplus food donation batches registered in the system"
            )
            st.caption("Active & past surplus batches")

    with col2:
        with st.container(border=True):
            st.metric(
                label="🍲 Total Estimated Meals Donated",
                value=f"{total_estimated_meals:,}",
                help="Cumulative estimated meals contributed across all listings"
            )
            st.caption("Meals contributed by all donors")

    with col3:
        with st.container(border=True):
            pct_collected = (meals_redistributed / total_estimated_meals * 100) if total_estimated_meals > 0 else 0.0
            st.metric(
                label="✅ Meals Redistributed/Collected",
                value=f"{meals_redistributed:,}",
                delta=f"{pct_collected:.1f}% fulfilled" if total_food_listings > 0 else None,
                delta_color="normal",
                help="Meals successfully collected and delivered to beneficiaries"
            )
            st.caption("Rescued & distributed to people")

    with col4:
        with st.container(border=True):
            pct_awaiting = (meals_awaiting / total_estimated_meals * 100) if total_estimated_meals > 0 else 0.0
            st.metric(
                label="⏳ Meals Awaiting Collection",
                value=f"{meals_awaiting:,}",
                delta=f"{pct_awaiting:.1f}% pending" if total_food_listings > 0 else None,
                delta_color="off",
                help="Meals currently available or claimed awaiting volunteer pickup"
            )
            st.caption("Ready for pickup right now")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # EMPTY-STATE DISPLAY (WHEN THERE ARE NO LISTINGS)
    # -------------------------------------------------------------
    if total_food_listings == 0:
        with st.container(border=True):
            st.markdown("""
            <div style="text-align: center; padding: 2.75rem 1.5rem;">
                <div style="font-size: 3.5rem; margin-bottom: 0.75rem;">🌱 🍱 ✨</div>
                <h3 style="color: #065f46; font-family: 'Outfit', sans-serif; font-size: 1.45rem; margin-bottom: 0.5rem;">
                    No Food Listings Recorded Yet
                </h3>
                <p style="color: #4b5563; max-width: 580px; margin: 0 auto 1.5rem auto; font-size: 0.98rem; line-height: 1.6;">
                    The impact registry is currently clean with zero recorded food listings. When food donors, restaurants, event organizers, or households post surplus food, live metrics and verified donation records will appear here.
                </p>
                <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 1.1rem 1.25rem; max-width: 600px; margin: 0 auto; text-align: left; font-size: 0.9rem; color: #166534;">
                    <strong>💡 How to create an impact:</strong>
                    <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0; line-height: 1.6;">
                        <li><strong>Food Donors:</strong> Share excess meals from kitchens, buffets, or pantries using the <strong>Donate Food</strong> portal.</li>
                        <li><strong>Volunteers & NGOs:</strong> Check the <strong>Find Food</strong> tab to claim and collect active listings.</li>
                        <li><strong>Zero Waste:</strong> Every meal rescued prevents landfill methane and feeds community members in need.</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        return

    # -------------------------------------------------------------
    # FOOD LISTINGS TABLE DISPLAY
    # Columns: Food name, quantity, donor, expiry date, status
    # -------------------------------------------------------------
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 8px;">
        <div>
            <h3 style="color: #064e3b; font-family: 'Outfit', sans-serif; margin: 0;">📋 Food Listings & Status Registry</h3>
            <p style="color: #4b5563; font-size: 0.9rem; margin: 0.2rem 0 0 0;">
                Detailed audit log of all registered surplus food batches, quantities, donors, expiry dates, and current fulfillment statuses.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Search & Filter Controls for the Table
    tbl_col1, tbl_col2 = st.columns([1, 2])
    with tbl_col1:
        status_filter = st.selectbox(
            "Filter Registry by Status",
            ["All Listings", "Available", "Claimed", "Collected / Completed"],
            key="impact_tbl_status"
        )
    with tbl_col2:
        search_kw = st.text_input(
            "Search Table",
            placeholder="Search by food name, donor, or expiry date...",
            key="impact_tbl_search"
        )

    # Filter rows based on user input
    filtered_table_rows = []
    for row in table_rows_list:
        # Status filter
        if status_filter == "Available" and row["Status"] != "Available":
            continue
        elif status_filter == "Claimed" and row["Status"] != "Claimed":
            continue
        elif status_filter == "Collected / Completed" and row["Status"] not in ["Collected", "Completed"]:
            continue

        # Search keyword filter
        if search_kw.strip():
            kw = search_kw.strip().lower()
            match_found = (
                kw in row["Food name"].lower()
                or kw in row["Donor"].lower()
                or kw in row["Expiry date"].lower()
                or kw in row["Status"].lower()
            )
            if not match_found:
                continue

        # Clean display dict with exact required column names
        filtered_table_rows.append({
            "Food name": row["Food name"],
            "Quantity": row["Quantity"],
            "Donor": row["Donor"],
            "Expiry date": row["Expiry date"],
            "Status": row["Status"]
        })

    if filtered_table_rows:
        df_impact_table = pd.DataFrame(filtered_table_rows)

        # Display the required table
        st.dataframe(
            df_impact_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Food name": st.column_config.TextColumn("Food name", width="medium"),
                "Quantity": st.column_config.TextColumn("Quantity", width="small"),
                "Donor": st.column_config.TextColumn("Donor", width="medium"),
                "Expiry date": st.column_config.TextColumn("Expiry date", width="medium"),
                "Status": st.column_config.TextColumn("Status", width="small"),
            }
        )
        st.caption(f"Showing {len(filtered_table_rows)} of {total_food_listings} total food listings.")
    else:
        st.info("ℹ️ No listings match your selected status or search filter.")

    # -------------------------------------------------------------
    # ENVIRONMENTAL & SOCIAL IMPACT SUMMARY CARD
    # -------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    total_kg_diverted = round(total_estimated_meals * 0.4, 1)
    co2e_saved_kg = round(total_kg_diverted * 2.5, 1)

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%); border: 1px solid #86efac; border-radius: 16px; padding: 1.4rem 1.6rem; margin-top: 0.5rem;">
        <h4 style="color: #065f46; margin: 0 0 0.5rem 0; font-family: 'Outfit', sans-serif;">
            🌍 Environmental Impact Summary
        </h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 0.75rem;">
            <div>
                <span style="font-size: 0.85rem; color: #047857; font-weight: 600;">Landfill Waste Diverted:</span>
                <div style="font-size: 1.4rem; font-weight: 800; color: #064e3b;">~{total_kg_diverted:,} kg</div>
                <div style="font-size: 0.78rem; color: #166534;">Based on ~0.4 kg average wholesome portion</div>
            </div>
            <div>
                <span style="font-size: 0.85rem; color: #047857; font-weight: 600;">CO₂e Emissions Averted:</span>
                <div style="font-size: 1.4rem; font-weight: 800; color: #064e3b;">~{co2e_saved_kg:,} kg CO₂e</div>
                <div style="font-size: 0.78rem; color: #166534;">Equivalent to ~{co2e_saved_kg * 4:.0f} km driven by passenger car</div>
            </div>
            <div>
                <span style="font-size: 0.85rem; color: #047857; font-weight: 600;">Fulfillment Success Rate:</span>
                <div style="font-size: 1.4rem; font-weight: 800; color: #064e3b;">{(meals_redistributed / total_estimated_meals * 100) if total_estimated_meals > 0 else 0:.1f}%</div>
                <div style="font-size: 0.78rem; color: #166534;">{meals_redistributed} of {total_estimated_meals} meals collected</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE 5: MANAGE LISTINGS & HANDOVERS
# ==========================================
def render_manage_listings(donations: list[dict[str, Any]]) -> None:
    """
    Render donation management, volunteer handover claims, and data backup tools.
    
    Demonstrates:
    - Lists: Filtering claims and deleting listings
    - File Handling with JSON: Exporting complete registry to JSON and CSV
    - Basic Type Hints: donations: list[dict[str, Any]] -> None
    """
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #064e3b; font-family: 'Outfit', sans-serif; margin-bottom: 0.25rem;">📋 Manage Donations & Handover Verification</h2>
        <p style="color: #4b5563; font-size: 0.95rem;">Track live claims, confirm volunteer pickups, review historical distributions, and export system audit data.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🚚 Active Claims & Verification", "📦 All Surplus Listings", "📥 Data Export & Backup"])

    # TAB 1: Claims & Verification
    with tab1:
        claimed_items = [d for d in donations if d.get("status") == "Claimed"]
        st.subheader(f"Pending Pickups ({len(claimed_items)})")
        
        if not claimed_items:
            st.info("No pending pickups at this moment. When a volunteer or NGO claims food, it will appear here for handover confirmation.")
        else:
            for item in claimed_items:
                c_info = item.get("claim_info", {})
                with st.container():
                    st.markdown(f"""
                    <div style="background: #ffffff; border: 1px solid #93c5fd; border-left: 6px solid #0284c7; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                            <h4 style="color: #0369a1; margin: 0;">🍱 {item.get('title')}</h4>
                            <span style="background: #e0f2fe; color: #0284c7; font-weight: 700; padding: 4px 12px; border-radius: 9999px; font-size: 0.85rem;">
                                CODE: {c_info.get('claim_code')}
                            </span>
                        </div>
                        <div style="font-size: 0.85rem; color: #4b5563; margin-top: 0.5rem;">
                            <strong>Donor:</strong> {item.get('donor_name')} &bull; <strong>Portions:</strong> {item.get('portions')} ({item.get('weight_kg')} kg) &bull; <strong>Location:</strong> {item.get('city_area')}
                        </div>
                        <div style="background: #f0f9ff; border: 1px dashed #7dd3fc; border-radius: 8px; padding: 0.75rem; margin-top: 0.75rem; font-size: 0.85rem;">
                            <strong>Claimed By:</strong> {c_info.get('organization')} &bull; <strong>Volunteer:</strong> {c_info.get('claimed_by')} ({c_info.get('phone')})<br>
                            <strong>ETA:</strong> {c_info.get('eta')} &bull; <strong>Claimed At:</strong> {c_info.get('claimed_at')}<br>
                            <strong>Plan:</strong> {c_info.get('purpose', 'N/A')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    btn_c1, btn_c2 = st.columns([1, 1])
                    with btn_c1:
                        if st.button(f"✅ Confirm Handover Complete ({item.get('id')})", key=f"complete_{item.get('id')}", type="primary", use_container_width=True):
                            item["status"] = "Completed"
                            if "claim_info" in item and item["claim_info"]:
                                item["claim_info"]["completed_at"] = dt.now().strftime("%Y-%m-%d %H:%M")
                            save_donations(donations)
                            st.success(f"Listing {item.get('id')} marked as Successfully Completed!")
                            st.rerun()

                    with btn_c2:
                        if st.button(f"❌ Cancel Claim / Re-open ({item.get('id')})", key=f"cancel_{item.get('id')}", use_container_width=True):
                            item["status"] = "Available"
                            item["claim_info"] = None
                            save_donations(donations)
                            st.warning(f"Claim cancelled. Listing {item.get('id')} is now Available again.")
                            st.rerun()

    # TAB 2: All Surplus Listings Table
    with tab2:
        st.subheader("Master Donation Registry")
        status_filter = st.radio("Filter By Status", ["All", "Available", "Claimed", "Completed"], horizontal=True)

        display_list = donations
        if status_filter != "All":
            display_list = [d for d in donations if d.get("status") == status_filter]

        table_rows = []
        for d in display_list:
            table_rows.append({
                "ID": d.get("id"),
                "Title": d.get("title"),
                "Category": d.get("category"),
                "Dietary": d.get("dietary"),
                "Portions": d.get("portions"),
                "Weight (kg)": d.get("weight_kg"),
                "Donor": d.get("donor_name"),
                "Area": d.get("city_area"),
                "Expires": d.get("expires_at"),
                "Status": d.get("status")
            })

        if table_rows:
            df_table = pd.DataFrame(table_rows)
            st.dataframe(df_table, use_container_width=True, hide_index=True)
        else:
            st.info("No records matching the selected status.")

        # Quick Delete / Cancel Listing
        st.markdown("---")
        with st.expander("🗑️ Cancel or Remove a Listing"):
            item_ids = [d.get("id") for d in donations]
            selected_del_id = st.selectbox("Select Listing ID to remove", item_ids)
            if st.button("Delete Listing Permanently", type="secondary"):
                donations = [d for d in donations if d.get("id") != selected_del_id]
                save_donations(donations)
                st.success(f"Listing {selected_del_id} removed.")
                st.rerun()

    # TAB 3: Data Export & Backup
    with tab3:
        st.subheader("Data Export & Sustainability Reporting")
        st.write("Export full registry in standard JSON or CSV format for audit trails, reporting, or municipal waste management records.")

        c_exp1, c_exp2 = st.columns(2)
        with c_exp1:
            json_str = json.dumps(donations, indent=2)
            st.download_button(
                label="📥 Download Full food_listings.json",
                data=json_str,
                file_name="food_listings.json",
                mime="application/json",
                use_container_width=True
            )

        with c_exp2:
            df_export = pd.DataFrame(donations)
            csv_str = df_export.to_csv(index=False)
            st.download_button(
                label="📊 Download CSV Spreadsheet",
                data=csv_str,
                file_name="food_waste_donations.csv",
                mime="text/csv",
                use_container_width=True
            )


# ==========================================
# PAGE 5: SAFETY & HANDLING GUIDELINES
# ==========================================
def render_safety_guidelines():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="color: #064e3b; font-family: 'Outfit', sans-serif; margin-bottom: 0.25rem;">🛡️ Food Safety & Hygiene Protocol</h2>
        <p style="color: #4b5563; font-size: 0.95rem;">Surplus food donation must adhere strictly to food hygiene standards to guarantee that rescued meals are wholesome and safe for vulnerable communities.</p>
    </div>
    """, unsafe_allow_html=True)

    # Temperature Danger Zone
    st.markdown("""
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem;">
        <h3 style="color: #064e3b; font-family: 'Outfit', sans-serif; margin-top: 0;">🌡️ The Critical Temperature Danger Zone</h3>
        <p style="color: #4b5563; font-size: 0.9rem;">Bacteria multiply most rapidly between <strong>4°C (40°F) and 60°C (140°F)</strong>. Keep food either safely cold or piping hot:</p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 12px; padding: 1rem; text-align: center;">
                <div style="font-size: 1.8rem;">❄️ Cold Holding</div>
                <h4 style="color: #166534; margin: 0.5rem 0 0.25rem 0;">Below 4°C (40°F)</h4>
                <p style="font-size: 0.8rem; color: #15803d; margin: 0;">Refrigerated storage for cooked items, dairy, and salads.</p>
            </div>
            <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 12px; padding: 1rem; text-align: center;">
                <div style="font-size: 1.8rem;">⚠️ Danger Zone</div>
                <h4 style="color: #991b1b; margin: 0.5rem 0 0.25rem 0;">4°C to 60°C</h4>
                <p style="font-size: 0.8rem; color: #b91c1c; margin: 0;">Do NOT leave cooked food in this zone for > 2 hours.</p>
            </div>
            <div style="background: #fff7ed; border: 1px solid #fed7aa; border-radius: 12px; padding: 1rem; text-align: center;">
                <div style="font-size: 1.8rem;">🔥 Hot Holding</div>
                <h4 style="color: #9a3412; margin: 0.5rem 0 0.25rem 0;">Above 60°C (140°F)</h4>
                <p style="font-size: 0.8rem; color: #c2410c; margin: 0;">Maintain in insulated thermal boxes until recipient pickup.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Pillars of Safe Food Donation
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 1.25rem; height: 100%;">
            <h4 style="color: #047857; margin-top: 0;">👨‍🍳 Donor Checklist: Pre-Listing Protocol</h4>
            <ul style="font-size: 0.88rem; color: #374151; line-height: 1.6; padding-left: 1.2rem;">
                <li><strong>Untouched Food Only:</strong> Food served on self-service buffet tables after customer access cannot be donated. Kitchen-held unserved surplus only.</li>
                <li><strong>Food-Grade Packaging:</strong> Pack in clean, non-toxic, sealed containers (aluminum foil trays, food-safe plastic containers).</li>
                <li><strong>Label Date & Time:</strong> Clearly specify the exact time food was cooked and the target safe consumption window.</li>
                <li><strong>Allergen Declaration:</strong> Mention if food contains peanuts, dairy, tree nuts, gluten, or eggs.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 1.25rem; height: 100%;">
            <h4 style="color: #047857; margin-top: 0;">🚚 Volunteer & NGO Transport Protocol</h4>
            <ul style="font-size: 0.88rem; color: #374151; line-height: 1.6; padding-left: 1.2rem;">
                <li><strong>Thermal Transport:</strong> Use insulated delivery bags or cooler boxes with ice gel packs for chilled items.</li>
                <li><strong>Direct Route:</strong> Transport directly from donor to distribution location without unneeded stops.</li>
                <li><strong>Sensory Inspection:</strong> Check aroma, visual appearance, and seal integrity before distribution.</li>
                <li><strong>Immediate Distribution:</strong> Aim to deliver hot food within 90 minutes of pickup.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Safety FAQ Accordion
    st.markdown("#### ❓ Frequently Asked Food Safety Questions")
    with st.expander("Can households donate leftover food from private dinners?"):
        st.write("Yes, provided the surplus food was segregated prior to dining, cooled promptly, refrigerated in clean containers, and donated within 24 hours of preparation.")

    with st.expander("What foods are NOT acceptable for donation?"):
        st.write("Expired canned goods past 'use-by' dates, opened dairy containers, food left at ambient temperature for over 4 hours, and items with compromised seals or foul odor.")

    with st.expander("Are donors protected from liability for donating surplus food in good faith?"):
        st.write("In many jurisdictions (such as the US Bill Emerson Good Samaritan Act and national food rescue regulations), donors who donate food in good faith to non-profit organizations without gross negligence are shielded from civil and criminal liability.")


# ==========================================
# FOOTER
# ==========================================
def render_footer() -> None:
    """Render the global application footer with UN SDG mission goals."""
    st.markdown("""
    <div class="custom-footer">
        <strong>Smart Food Waste Management System</strong> &bull; Zero Hunger (UN SDG 2) &bull; Responsible Consumption (UN SDG 12)<br>
        Empowering communities, feeding families, and reducing greenhouse gas emissions through intelligent surplus food rescue.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# MAIN APPLICATION ROUTING
# ==========================================
def main() -> None:
    """
    Main application routing controller.
    
    Demonstrates:
    - File Handling with JSON: Invoking load_donations() to load dataset on launch
    - If/Elif/Else Conditions: Routing execution flow to the appropriate page renderer
    - Function Composition: Modular top-level application orchestration
    """
    # Load dataset
    donations = load_donations()

    # Sidebar Navigation
    current_page = render_sidebar(donations)

    # Page Router
    if current_page == "📊 Impact Dashboard":
        render_dashboard(donations)
    elif current_page in ["🔍 Find Food", "🍱 Browse Surplus Food"]:
        render_find_food_page(donations)
    elif current_page in ["➕ Donate Food", "➕ Donate Food (Donor Portal)"]:
        render_donate_page(donations)
    elif current_page in ["📈 Impact Report", "Impact Report"]:
        render_impact_report_page(donations)
    elif current_page in ["📋 Manage Listings & Claims", "📋 Manage Listings & Handovers"]:
        render_manage_listings(donations)
    elif current_page == "🛡️ Safety & Handling Guidelines":
        render_safety_guidelines()

    # Footer
    render_footer()

if __name__ == "__main__":
    main()
