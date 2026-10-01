# 🌱 Smart Food Waste Management System
### Python & Streamlit Coursework / Student Assignment Submission

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smartfoodwastemanagerapp.streamlit.app/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/sinduvr-cmd/smart-food-waste-manager-app)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

🌐 **Live Streamlit App**: [https://smartfoodwastemanagerapp.streamlit.app/](https://smartfoodwastemanagerapp.streamlit.app/)  
📂 **GitHub Source Code**: [https://github.com/sinduvr-cmd/smart-food-waste-manager-app](https://github.com/sinduvr-cmd/smart-food-waste-manager-app)  
🚀 **1-Click Community Cloud Deploy**: [Deploy on Streamlit Cloud](https://share.streamlit.io/deploy?repository=sinduvr-cmd/smart-food-waste-manager-app&branch=main&mainModule=app.py)

A responsive, sustainability-focused **Streamlit web application** that connects food donors (restaurants, hotels, catering venues, event organizers, and households) with NGOs, community kitchens, and volunteers before surplus food expires.

> **Project Mission**: Aligning with **UN Sustainable Development Goal 2 (Zero Hunger)** and **UN SDG 12 (Responsible Consumption & Production)** to reduce methane emissions from landfills and feed communities in need through automated, transparent surplus food logistics.

---

## 🎓 Python Concepts Demonstrated (Academic Checklist)

This project has been deliberately architected for a **student assignment submission**, emphasizing core Python concepts, clean code structure, modular programming, defensive error handling, and standard type hints.

| # | Python Concept | Implementation in Code | Where to Find in Code (`app.py`) |
|---|----------------|------------------------|-----------------------------------|
| **1** | **Variables** | Primitives: `int`, `float`, `str`, `bool`. Global constants for file paths and category lists. | Constants: `FOOD_LISTINGS_FILE`, `FOOD_CATEGORIES`. Metrics: `total_food_listings: int`, `weight_kg: float`. |
| **2** | **Lists** | Dynamic lists, `.append()`, `len()`, list slicing, and list comprehensions. | `meals_donated_list = []`, `validation_errors: list[str] = []`, `[char for char in phone if char.isdigit()]`. |
| **3** | **Dictionaries** | Structured key-value donation records, dictionary access with `.get(key, default)`, nested dicts. | `new_listing = {"id": ..., "food_item": ..., "servings": ...}`, `claim_info = item.get("claim_info", {})`. |
| **4** | **Functions** | Reusable, modular functions with single responsibilities and PEP 257 docstrings. | `load_donations()`, `save_donations()`, `generate_unique_id()`, `calculate_impact_metrics()`, `validate_*()`. |
| **5** | **Loops (`for` & `while`)** | `for` loops for aggregation & card rendering; `while` loop for generating guaranteed collision-free IDs. | `for listing in all_listings: ...`, `while candidate_id in existing_ids: counter += 1`. |
| **6** | **If / Else Conditions** | Multi-way branching (`if`, `elif`, `else`) for input validation rules and urgency tiers. | Freshness tiers (`delta_hours <= 24` vs `48` vs `>48`), empty-state checks (`if not donations:`). |
| **7** | **Input Validation** | 6 dedicated validator functions verifying name, item, positive quantity, future dates, address, phone. | `validate_donor_name()`, `validate_quantity()`, `validate_expiry_date()`, `validate_contact_number()`. |
| **8** | **File Handling with JSON** | Reading & writing to `food_listings.json` with `json.load()` and `json.dump()`. Safe context managers (`with`). | `with open(file_path, "r", encoding="utf-8") as f: data = json.load(f)` in `load_donations()`. |
| **9** | **Exception Handling** | Multi-tier `try...except` blocks handling `FileNotFoundError`, `json.JSONDecodeError`, `ValueError`, `IOError`. | Graceful fallbacks in `load_donations()`, `save_donations()`, `validate_quantity()`, `get_expiry_details()`. |
| **10** | **Basic Type Hints** | Clear PEP 484 annotations on parameters and return values across all functions. | `def validate_donor_name(name: str) -> tuple[bool, str]:`, `def load_donations() -> list[dict[str, Any]]:`. |

---

### Detailed Code Examples of Required Concepts

#### 1. Variables & Constants
```python
FOOD_LISTINGS_FILE: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "food_listings.json")
total_food_listings: int = 0
co2_saved_kg: float = round(total_kg * 2.5, 1)
is_valid: bool = True
```

#### 2. Lists & List Comprehensions
```python
# List comprehension to extract numeric digits from phone numbers
digits: list[str] = [char for char in contact_number if char.isdigit()]

# Dynamic lists for accumulator calculations
meals_donated_list: list[int] = []
meals_collected_list: list[int] = []
```

#### 3. Dictionaries & Safe Key Access
```python
# Constructing a structured surplus food record
new_listing: dict[str, Any] = {
    "id": new_id,
    "donor_name": donor_name.strip(),
    "food_item": food_item.strip(),
    "category": category,
    "servings": int(servings),
    "status": "Available"
}

# Safe key access with default fallback
food_title = listing.get("food_item") or listing.get("title") or "Surplus Food"
```

#### 4. Loops (`for` and `while`)
```python
# For Loop: Accumulating meal quantities from extracted lists
total_estimated_meals = 0
for meal in meals_donated_list:
    total_estimated_meals += meal

# While Loop: Guaranteeing collision-free unique IDs for new donations
while candidate_id in existing_ids:
    counter += 1
    candidate_id = f"{prefix}-{counter}"
```

#### 5. Input Validation with If/Else Conditions
```python
def validate_quantity(servings: Any) -> tuple[bool, str]:
    try:
        val: float = float(servings)
        if val <= 0:
            return False, "Estimated servings/meals quantity must be above zero."
        return True, ""
    except (ValueError, TypeError):
        return False, "Estimated servings/meals must be a valid number above zero."
```

#### 6. File Handling with JSON & Exception Handling
```python
def load_donations(file_path: str = FOOD_LISTINGS_FILE) -> list[dict[str, Any]]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return generate_seed_data()
            return data
    except (FileNotFoundError, json.JSONDecodeError, IOError) as error:
        st.error(f"Error loading file: {error}")
        return generate_seed_data()
```

---

## ✨ Application Features & Page Walkthrough

### 1. 📊 Impact Dashboard
- **Real-Time Sustainability KPI Cards**:
  - 🍱 **Active Food Listings**: Total batches awaiting rescue.
  - 🍲 **Estimated Meals Available**: Real-time wholesome meal portions ready.
  - 🚨 **Urgent Pickups (< 6h)**: Critical attention indicator for meals needing rapid rescue.
  - 🌿 **CO₂e Emissions Averted**: Carbon emissions kept out of municipal landfills.
- **🔄 Three-Step “How It Works” Guide**:
  1. *Donors list surplus food*: Fast 2-minute listing with portions, dietary labels, and safe holding criteria.
  2. *NGOs/volunteers find nearby food*: Real-time discovery, urgency filters, and automated verification codes.
  3. *Food is collected and waste is reduced*: Safe thermal transport, community nourishment, and carbon reduction.
- **⚡ Priority Pickup Cards**:
  - Highlights listings expiring today (🔴 Urgent) or within 48 hours (🟡 Priority).
  - Displays portions, holding conditions, pickup address, contact number, and inline claim forms.
  - Clean empty state when no urgent items require action.

### 2. 🔍 Find Food (Active Food Marketplace)
- **Direct Load from `food_listings.json`**: Loads active surplus listings (`status == "Available"`).
- **Search & Category Filtering**:
  - Filter by category: `Cooked meals`, `Fruits & vegetables`, `Bakery`, `Dairy`, `Packaged food`, `Other`.
  - Search by food item name, donor name, or location.
- **Color-Coded Freshness Status**:
  - 🔴 **Red (Collect Today)**: Batches expiring within 24 hours.
  - 🟠 **Orange (Expires within 2 Days)**: Batches with 24 to 48 hours remaining.
  - 🟢 **Green (Available for >2 Days)**: Batches with more than 48 hours remaining.
- **“Mark Collected” Workflow**:
  - One-click button updates status from `Available` to `Collected` in `food_listings.json`.
  - Refreshes the page and automatically updates all impact statistics.

### 3. ➕ Donate Food (Donor Portal with Input Validation)
- **Form Fields**:
  - Organisation/Donor name, Contact phone number, Food item name, Category, Estimated servings, Best before date & time, Pickup location, Dietary classification, Packaging type, and Optional safety/allergen notes.
- **Strict Validation Rules**:
  - Name and food item must contain at least 2 characters.
  - Quantity must be strictly above zero.
  - Expiry date & time cannot be in the past.
  - Pickup address must contain at least 3 characters.
  - Contact number must contain at least 10 numeric digits.
- **Instant Persistence**:
  - Generates unique ID (`DON-100X`) via `while` loop.
  - Persists record directly into `food_listings.json` and displays a celebratory confirmation card.

### 4. 📈 Impact Report (Python Loops & Lists Engine)
- **Explicit Loop & List Calculations**:
  - Iterates through listings to calculate:
    1. **Total food listings**
    2. **Total estimated meals donated**
    3. **Meals redistributed/collected**
    4. **Meals awaiting collection**
- **Metrics Display**: 4 responsive metric containers.
- **Audit Registry Table**: Displays exactly: `Food name`, `Quantity`, `Donor`, `Expiry date`, and `Status`. Includes interactive status filtering and keyword search.
- **Helpful Empty State**: Friendly sustainability empty-state card rendered when zero listings exist.

### 5. 📋 Manage Listings & Handover Verification
- **Claims Verification Tab**: Donors and volunteers can confirm unique 6-character claim codes and complete handovers.
- **Master Registry**: Filterable table of all donations with inline permanent deletion for test cleanup.
- **Audit Data Export**: One-click download of the complete dataset in **JSON (`food_listings.json`)** or **CSV (`food_waste_donations.csv`)** format.

### 6. 🛡️ Food Safety & Handling Guidelines
- **Temperature Danger Zone Guide**: Visual guide to cold holding (< 4°C), danger zone (4°C–60°C), and hot holding (> 60°C).
- **Checklists**: Donor pre-listing guidelines and volunteer thermal transport standards.
- **Safety FAQ**: Legal protections (Good Samaritan acts) and food hygiene FAQs.

---

## 🚀 Installation & Running Instructions

### 1. Prerequisites
- **Python**: Version 3.9 or higher (Python 3.9, 3.10, 3.11, 3.12, 3.13, or 3.14).
- **Package Manager**: `pip` (included with standard Python installations).
- **Web Browser**: Any modern browser (Chrome, Firefox, Edge, Safari).

### 2. Step-by-Step Setup

#### Step 1: Open Terminal in Project Directory
Navigate to the root directory containing `app.py`:
```bash
cd "c:\Users\SINDHU SURAJ\Downloads\test"
```

#### Step 2: (Optional but Recommended) Create a Virtual Environment
```bash
# Windows (PowerShell or Command Prompt)
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Required Dependencies
Install the required packages using the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```
*Required packages:*
- `streamlit>=1.31.0`
- `pandas>=2.0.0`

#### Step 4: Run the Application
Launch the Streamlit development server:
```bash
python -m streamlit run app.py
```
*(Or simply `streamlit run app.py` if Streamlit is in your system PATH).*

#### Step 5: View the App in Your Browser
The terminal will display the local URL. Open:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 📁 Project Structure

```
test/
├── app.py                   # Main Streamlit web application & Python logic
├── requirements.txt         # Package dependencies (streamlit, pandas)
├── README.md                # Project documentation & assignment concept mapping
├── food_listings.json       # JSON file storage for all surplus food records
├── .streamlit/
│   └── config.toml          # Streamlit sustainability theme & server settings
└── data/
    └── food_donations.json  # Synchronized backup data store
```

---

## 🎨 Design Theme & Aesthetics

- **Sustainability Palette**: Emerald Green (`#059669`), Forest Green (`#064E3B`), Mint Tint (`#F0FDF4`), and Crisp White (`#FFFFFF`).
- **Typography**: Modern fonts loaded from Google Fonts (*Outfit* for bold headings, *Plus Jakarta Sans* for body text).
- **Icons**: Food waste and environmental icons used across banners, metrics, and cards (🥗, 🍲, 🍞, 🍱, 🌿, 🌱, ⏳, 🚨).
- **Defensive States**: Informative empty-state cards, loading spinners, and validation banners ensure an intuitive user experience.

---

## 🧪 Testing & Verification Guide for Evaluators

1. **Test Input Validation**:
   - Navigate to **"➕ Donate Food"**.
   - Leave fields blank or enter an invalid phone number (`12345`) or 0 servings. Click **Publish Food Listing**.
   - Notice the precise error messages generated by Python validation functions.
2. **Test While-Loop ID Generation & JSON File Persistence**:
   - Fill out valid details and submit.
   - Observe the success confirmation card with a newly generated ID (`DON-100X`).
   - Open `food_listings.json` to verify the record was saved to disk.
3. **Test Status Updates**:
   - Go to **"🔍 Find Food"** and click **"Mark Collected"** on any card.
   - The status updates to `Collected`, and it vanishes from active food listings.
4. **Test Loop/List Impact Computations**:
   - Go to **"📈 Impact Report"**.
   - Review the 4 metrics and the full table with columns: `Food name`, `Quantity`, `Donor`, `Expiry date`, and `Status`.
   - The values match the loop aggregations computed in `calculate_impact_metrics()`.
5. **Test Empty States**:
   - Filter by a status with zero matches or search for non-existent keywords to verify graceful empty-state handling.

---

## 📄 License & Academic Integrity
This project was developed for educational and academic coursework purposes. Free to use and adapt under the **MIT License**.
