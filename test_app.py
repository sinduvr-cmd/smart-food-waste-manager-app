"""
Unit Test Suite for Smart Food Waste Management System
======================================================
Academic Coursework Assessment & Rubric Verification:
- Section 10: Student Implementation Tasks (Tasks 1 to 11)
- Section 13: Submission Deliverables (Unit Tests & Test-Case Evidence)

Testing Quadrants Covered:
1. Valid Inputs
2. Invalid Inputs
3. Boundary Inputs
4. Empty Inputs
"""

import unittest
from datetime import datetime as dt, timedelta
from typing import Any

# Import modular business functions and validators from app.py
from app import (
    add_food_item,
    search_inventory,
    update_item_quantity,
    delete_food_item,
    calculate_expiry_status,
    generate_inventory_summary,
    check_duplicate_id,
    validate_date_string,
    validate_donor_name,
    validate_food_item,
    validate_quantity,
    validate_contact_number,
    validate_location,
    load_donations,
    generate_unique_id,
    run_automated_tests,
    add_item,
    validate_date,
    calculate_status,
    view_inventory,
    search_item,
    update_quantity,
    remove_item,
    generate_summary,
    get_assignment_sample_inventory,
    export_inventory_to_csv,
    init_sqlite_db,
    sync_to_sqlite,
    load_from_sqlite,
    generate_daily_expiry_report,
    is_item_expired,
    get_effective_status,
    sync_expired_statuses,
    get_freshness_status
)


class TestStudentImplementationTasks(unittest.TestCase):
    """
    Formal unit tests validating Student Implementation Tasks 1 through 11.
    """

    def setUp(self):
        """Prepare an isolated in-memory test inventory for each test case."""
        self.now = dt.now()
        self.future_date = (self.now + timedelta(days=3)).strftime("%Y-%m-%d %H:%M")
        self.urgent_date = (self.now + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M")
        self.past_date = (self.now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")

        self.inventory: list[dict[str, Any]] = [
            {
                "id": "UNIT-1001",
                "title": "Fresh Paneer Rice",
                "food_item": "Fresh Paneer Rice",
                "category": "Cooked meals",
                "dietary": "Vegetarian",
                "portions": 30,
                "servings": 30,
                "weight_kg": 12.0,
                "donor_name": "Spice Delight",
                "contact_phone": "9876543210",
                "pickup_address": "12 Residency Road",
                "expires_at": self.urgent_date,
                "status": "Available"
            },
            {
                "id": "UNIT-1002",
                "title": "Whole Wheat Bagels",
                "food_item": "Whole Wheat Bagels",
                "category": "Bakery",
                "dietary": "Vegan",
                "portions": 40,
                "servings": 40,
                "weight_kg": 16.0,
                "donor_name": "Baker's Haven",
                "contact_phone": "9811223344",
                "pickup_address": "44 High Street",
                "expires_at": self.future_date,
                "status": "Available"
            }
        ]

    # -------------------------------------------------------------
    # TASK 1: INVENTORY DATA STRUCTURE (List of Dictionaries)
    # -------------------------------------------------------------
    def test_task1_inventory_data_structure(self):
        """Task 1: Verify inventory is a list of dictionaries with required schema keys."""
        self.assertIsInstance(self.inventory, list)
        self.assertTrue(len(self.inventory) > 0)
        for item in self.inventory:
            self.assertIsInstance(item, dict)
            self.assertIn("id", item)
            self.assertIn("category", item)
            self.assertIn("portions", item)
            self.assertIn("expires_at", item)
            self.assertIn("status", item)

    # -------------------------------------------------------------
    # TASK 4: DATE VALIDATION USING DATETIME MODULE
    # -------------------------------------------------------------
    def test_task4_valid_future_date(self):
        """Task 4: Valid future datetime string passes validation."""
        valid, msg, parsed = validate_date_string(self.future_date)
        self.assertTrue(valid)
        self.assertEqual(msg, "")
        self.assertIsNotNone(parsed)
        self.assertGreater(parsed, dt.now())

    def test_task4_past_date_rejected(self):
        """Task 4: Past datetime string is strictly rejected."""
        valid, msg, _ = validate_date_string(self.past_date)
        self.assertFalse(valid)
        self.assertIn("past", msg.lower())

    def test_task4_invalid_date_format_rejected(self):
        """Task 4 & 6: Malformed date text is caught via exception handling."""
        valid, msg, _ = validate_date_string("invalid-date-2026")
        self.assertFalse(valid)
        self.assertIn("invalid date format", msg.lower())

    # -------------------------------------------------------------
    # TASK 5: EXPIRY-STATUS CALCULATION
    # -------------------------------------------------------------
    def test_task5_expiry_status_tiers(self):
        """Task 5: Correct calculation of urgency tiers (Expired, Urgent, Moderate, Safe)."""
        # Expired
        exp_res = calculate_expiry_status(self.past_date)
        self.assertEqual(exp_res["status"], "Expired")
        self.assertTrue(exp_res["is_expired"])

        # Urgent (<= 24h)
        urg_date = (dt.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M")
        urg_res = calculate_expiry_status(urg_date)
        self.assertEqual(urg_res["status"], "Urgent")
        self.assertEqual(urg_res["tier"], "Red")
        self.assertTrue(urg_res["is_urgent"])

        # Moderate (24h - 48h)
        mod_date = (dt.now() + timedelta(hours=36)).strftime("%Y-%m-%d %H:%M")
        mod_res = calculate_expiry_status(mod_date)
        self.assertEqual(mod_res["status"], "Moderate")
        self.assertEqual(mod_res["tier"], "Orange")

        # Safe (> 48h)
        safe_date = (dt.now() + timedelta(hours=72)).strftime("%Y-%m-%d %H:%M")
        safe_res = calculate_expiry_status(safe_date)
        self.assertEqual(safe_res["status"], "Safe")
        self.assertEqual(safe_res["tier"], "Green")

    # -------------------------------------------------------------
    # TASK 6: EXCEPTION HANDLING FOR NUMERIC & DATE INPUTS
    # -------------------------------------------------------------
    def test_task6_non_numeric_quantity_exception_handling(self):
        """Task 6: Non-numeric quantity strings are caught safely without crashing."""
        valid, msg = validate_quantity("twenty_meals")
        self.assertFalse(valid)
        self.assertIn("valid number", msg.lower())

        valid_none, _ = validate_quantity(None)
        self.assertFalse(valid_none)

    # -------------------------------------------------------------
    # TASK 7: PREVENT DUPLICATE IDS AND NEGATIVE STOCK
    # -------------------------------------------------------------
    def test_task7_prevent_duplicate_ids(self):
        """Task 7: Duplicate ID assignment is detected and prevented."""
        self.assertTrue(check_duplicate_id(self.inventory, "UNIT-1001"))
        self.assertFalse(check_duplicate_id(self.inventory, "UNIT-9999"))

        # Attempt to add item with duplicate ID
        ok, msg, _ = add_food_item(
            self.inventory, "Extra Bread", "Bakery", 15,
            self.future_date, "Baker A", "9876543210", "12 High St",
            item_id="UNIT-1001", auto_save=False
        )
        self.assertFalse(ok)
        self.assertIn("duplicate id", msg.lower())

    def test_task7_prevent_negative_stock(self):
        """Task 7: Negative quantities are strictly prohibited in add and update."""
        # In validate_quantity
        ok_neg, _ = validate_quantity(-10)
        self.assertFalse(ok_neg)

        # In add_food_item
        ok_add, msg_add, _ = add_food_item(
            self.inventory, "Negative Meals", "Cooked meals", -5,
            self.future_date, "Donor X", "9876543210", "10 Elm St", auto_save=False
        )
        self.assertFalse(ok_add)
        self.assertIn("negative", msg_add.lower())

        # In update_item_quantity
        ok_upd, msg_upd = update_item_quantity(self.inventory, "UNIT-1001", -20, auto_save=False)
        self.assertFalse(ok_upd)
        self.assertIn("negative", msg_upd.lower())

    # -------------------------------------------------------------
    # TASK 8: SEARCH BY ITEM NAME AND CATEGORY
    # -------------------------------------------------------------
    def test_task8_search_by_name_and_category(self):
        """Task 8: Search filtering by name, category, and combination."""
        # By Keyword
        res_kw = search_inventory(self.inventory, keyword="Paneer")
        self.assertEqual(len(res_kw), 1)
        self.assertEqual(res_kw[0]["id"], "UNIT-1001")

        # By Category
        res_cat = search_inventory(self.inventory, category="Bakery")
        self.assertEqual(len(res_cat), 1)
        self.assertEqual(res_cat[0]["id"], "UNIT-1002")

        # Combination match
        res_both = search_inventory(self.inventory, keyword="Bagels", category="Bakery")
        self.assertEqual(len(res_both), 1)

        # Combination mismatch
        res_mismatch = search_inventory(self.inventory, keyword="Paneer", category="Bakery")
        self.assertEqual(len(res_mismatch), 0)

    # -------------------------------------------------------------
    # TASK 9: QUANTITY UPDATE AND DELETION
    # -------------------------------------------------------------
    def test_task9_quantity_update(self):
        """Task 9: Update quantity adjusts portions and recalculates weight."""
        ok, msg = update_item_quantity(self.inventory, "UNIT-1001", 50, auto_save=False)
        self.assertTrue(ok)
        item = next(i for i in self.inventory if i["id"] == "UNIT-1001")
        self.assertEqual(item["portions"], 50)
        self.assertEqual(item["weight_kg"], 20.0)

    def test_task9_deletion(self):
        """Task 9: Deletion removes the target item completely."""
        initial_len = len(self.inventory)
        ok, msg = delete_food_item(self.inventory, "UNIT-1002", auto_save=False)
        self.assertTrue(ok)
        self.assertEqual(len(self.inventory), initial_len - 1)
        self.assertFalse(any(i["id"] == "UNIT-1002" for i in self.inventory))

    # -------------------------------------------------------------
    # TASK 10: INVENTORY SUMMARY & OPERATIONAL ALERTS
    # -------------------------------------------------------------
    def test_task10_inventory_summary_and_alerts(self):
        """Task 10: Summary calculates totals and raises urgent operational alerts."""
        summary = generate_inventory_summary(self.inventory)
        self.assertEqual(summary["total_items"], 2)
        self.assertEqual(summary["total_servings"], 70)
        self.assertGreater(summary["alerts_count"], 0)

        # Check urgent alert exists for UNIT-1001 expiring within 4h
        alerts = summary["operational_alerts"]
        urgent_alerts = [a for a in alerts if a["type"] == "URGENT_EXPIRY"]
        self.assertTrue(len(urgent_alerts) > 0)

    # -------------------------------------------------------------
    # TASK 11: TESTING VALID, INVALID, BOUNDARY, AND EMPTY INPUTS
    # -------------------------------------------------------------
    def test_task11_boundary_inputs(self):
        """Task 11 Boundary: Boundary condition testing."""
        # Boundary: Zero servings in add (rejected)
        ok_zero, _, _ = add_food_item(
            self.inventory, "Zero Portions", "Other", 0,
            self.future_date, "Donor Z", "9876543210", "15 Lake Rd", auto_save=False
        )
        self.assertFalse(ok_zero)

        # Boundary: 1 serving (accepted as smallest positive)
        ok_one, _, rec_one = add_food_item(
            self.inventory, "Single Portion Meal", "Other", 1,
            self.future_date, "Donor Z", "9876543210", "15 Lake Rd", auto_save=False
        )
        self.assertTrue(ok_one)
        self.assertEqual(rec_one["portions"], 1)

        # Boundary: Name with exactly 2 characters (accepted)
        v_name2, _ = validate_donor_name("OK")
        self.assertTrue(v_name2)

        # Boundary: Name with 1 character (rejected)
        v_name1, _ = validate_donor_name("O")
        self.assertFalse(v_name1)

    def test_task11_empty_inputs(self):
        """Task 11 Empty: Empty strings, None values, and empty inventories."""
        # Empty string inputs
        v_food_empty, _ = validate_food_item("")
        self.assertFalse(v_food_empty)

        v_donor_empty, _ = validate_donor_name("   ")
        self.assertFalse(v_donor_empty)

        v_date_empty, _, _ = validate_date_string("")
        self.assertFalse(v_date_empty)

        # Operations on empty inventory list
        empty_search = search_inventory([], keyword="Anything")
        self.assertEqual(empty_search, [])

        empty_summary = generate_inventory_summary([])
        self.assertEqual(empty_summary["total_items"], 0)
        self.assertEqual(empty_summary["alerts_count"], 0)

        # Delete from empty list
        del_empty_ok, _ = delete_food_item([], "ID-1")
        self.assertFalse(del_empty_ok)

    def test_task11_automated_test_battery(self):
        """Task 11: Ensure run_automated_tests() reports 100% pass rate."""
        battery = run_automated_tests(self.inventory)
        self.assertEqual(battery["failed"], 0)
        self.assertTrue(battery["all_passed"])
        self.assertGreaterEqual(battery["total_tests"], 20)


class TestSection11MinimumTestScenarios(unittest.TestCase):
    """
    Direct verification of all 11 Minimum Test Scenarios specified in Section 11
    of the Coursework Specification, along with Section 9 metrics and Section 12 enhancements.
    """

    def setUp(self):
        """Prepare the standardized coursework baseline inventory."""
        self.operating_date = "2026-10-01"
        self.inventory: list[dict[str, Any]] = [
            {
                "id": "FD001",
                "name": "Milk",
                "category": "Dairy",
                "quantity": 12,
                "unit": "litres",
                "purchase_date": "2026-09-28",
                "expiry_date": "2026-09-30"
            },
            {
                "id": "FD002",
                "name": "Tomatoes",
                "category": "Produce",
                "quantity": 15,
                "unit": "kg",
                "purchase_date": "2026-09-29",
                "expiry_date": "2026-10-02"
            },
            {
                "id": "FD003",
                "name": "Rice",
                "category": "Grains",
                "quantity": 25,
                "unit": "kg",
                "purchase_date": "2026-09-20",
                "expiry_date": "2027-02-15"
            }
        ]

    def test_scenario_1_valid_food_item(self):
        """Scenario 1: Valid food item -> Record added successfully."""
        success, msg, rec = add_item(
            inventory=self.inventory,
            name="Fresh Paneer",
            category="Dairy",
            quantity=8,
            unit="kg",
            purchase_date="2026-09-30",
            expiry_date="2026-10-02",
            item_id="FD004",
            auto_save=False
        )
        self.assertTrue(success)
        self.assertIn("FD004", msg)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["name"], "Fresh Paneer")
        self.assertEqual(rec["quantity"], 8)
        self.assertEqual(len(self.inventory), 4)

    def test_scenario_2_duplicate_item_id(self):
        """Scenario 2: Duplicate item ID -> Reject record and display validation error."""
        success, msg, _ = add_item(
            inventory=self.inventory,
            name="Extra Milk",
            category="Dairy",
            quantity=5,
            unit="litres",
            purchase_date="2026-10-01",
            expiry_date="2026-10-04",
            item_id="FD001",
            auto_save=False
        )
        self.assertFalse(success)
        self.assertIn("duplicate", msg.lower())

    def test_scenario_3_negative_quantity(self):
        """Scenario 3: Negative quantity -> Reject input."""
        success, msg, _ = add_item(
            inventory=self.inventory,
            name="Apples",
            category="Fruit",
            quantity=-5,
            unit="kg",
            purchase_date="2026-10-01",
            expiry_date="2026-10-05",
            auto_save=False
        )
        self.assertFalse(success)
        self.assertTrue("greater than zero" in msg.lower() or "negative" in msg.lower())

    def test_scenario_4_zero_quantity(self):
        """Scenario 4: Zero quantity -> Reject input."""
        success, msg, _ = add_item(
            inventory=self.inventory,
            name="Apples",
            category="Fruit",
            quantity=0,
            unit="kg",
            purchase_date="2026-10-01",
            expiry_date="2026-10-05",
            auto_save=False
        )
        self.assertFalse(success)
        self.assertTrue("greater than zero" in msg.lower() or "zero" in msg.lower())

    def test_scenario_5_invalid_date_format(self):
        """Scenario 5: Invalid date format -> Display date validation error."""
        ok_slash, msg_slash, _ = validate_date("2026/10/01")
        self.assertFalse(ok_slash)
        self.assertIn("yyyy-mm-dd", msg_slash.lower())

        ok_bad, msg_bad, _ = validate_date("31-12-2026")
        self.assertFalse(ok_bad)

        ok_add, msg_add, _ = add_item(
            inventory=self.inventory,
            name="Bread",
            category="Bakery",
            quantity=2,
            unit="loaves",
            purchase_date="invalid-date",
            expiry_date="2026-10-05",
            auto_save=False
        )
        self.assertFalse(ok_add)
        self.assertIn("invalid", msg_add.lower())

    def test_scenario_6_expiry_before_purchase(self):
        """Scenario 6: Expiry before purchase -> Reject record."""
        success, msg, _ = add_item(
            inventory=self.inventory,
            name="Stale Bread",
            category="Bakery",
            quantity=2,
            unit="loaves",
            purchase_date="2026-09-30",
            expiry_date="2026-09-25",
            auto_save=False
        )
        self.assertFalse(success)
        self.assertIn("earlier than purchase", msg.lower())

    def test_scenario_7_expired_item(self):
        """Scenario 7: Expired item -> Status = EXPIRED."""
        status = calculate_status("2026-09-30", current_date=self.operating_date)
        self.assertEqual(status, "EXPIRED")

    def test_scenario_8_expiry_within_3_days(self):
        """Scenario 8: Expiry within 3 days -> Status = EXPIRING SOON."""
        stat_0 = calculate_status("2026-10-01", current_date=self.operating_date)
        self.assertEqual(stat_0, "EXPIRING SOON")

        stat_1 = calculate_status("2026-10-02", current_date=self.operating_date)
        self.assertEqual(stat_1, "EXPIRING SOON")

        stat_3 = calculate_status("2026-10-04", current_date=self.operating_date)
        self.assertEqual(stat_3, "EXPIRING SOON")

    def test_scenario_9_expiry_beyond_3_days(self):
        """Scenario 9: Expiry beyond 3 days -> Status = AVAILABLE."""
        stat_4 = calculate_status("2026-10-05", current_date=self.operating_date)
        self.assertEqual(stat_4, "AVAILABLE")

        stat_far = calculate_status("2027-02-15", current_date=self.operating_date)
        self.assertEqual(stat_far, "AVAILABLE")

    def test_scenario_10_reduce_stock_below_zero(self):
        """Scenario 10: Reduce stock below zero -> Reject transaction."""
        success, msg = update_quantity(self.inventory, "FD001", operation="reduce", quantity=20, auto_save=False)
        self.assertFalse(success)
        self.assertIn("negative", msg.lower())

    def test_scenario_11_unknown_item_id(self):
        """Scenario 11: Unknown item ID -> Display not-found message without crashing."""
        success, msg = remove_item(self.inventory, "NON-EXISTENT-ID-404", auto_save=False)
        self.assertFalse(success)
        self.assertIn("not found", msg.lower())

    def test_section_9_summary_and_metrics(self):
        """
        Verify Section 9 production sample output metrics with 4 canonical items
        on operating date 2026-10-01.
        """
        add_item(
            inventory=self.inventory,
            name="Fresh Paneer",
            category="Dairy",
            quantity=8,
            unit="kg",
            purchase_date="2026-09-30",
            expiry_date="2026-10-02",
            item_id="FD004",
            auto_save=False
        )
        summary = generate_summary(self.inventory, current_date=self.operating_date)
        self.assertEqual(summary["total_food_records"], 4)
        self.assertEqual(summary["total_quantity_records"], 60)
        self.assertEqual(summary["expired_items"], 1)
        self.assertEqual(summary["expiring_soon_items"], 2)
        self.assertEqual(summary["available_items"], 1)
        self.assertEqual(summary["attention_required_items"], 3)
        self.assertIn("disposal", summary["recommendation"].lower())

    def test_section_12_enhancements(self):
        """
        Verify Section 12 enhancements: CSV export, SQLite persistence, and daily report.
        """
        import os
        csv_file_path = export_inventory_to_csv(self.inventory)
        self.assertTrue(os.path.exists(csv_file_path))
        with open(csv_file_path, "r", encoding="utf-8") as f:
            csv_content = f.read()
        self.assertIn("FD001", csv_content)
        self.assertIn("Milk", csv_content)

        import tempfile
        import os
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_db:
            db_path = tmp_db.name

        try:
            conn = init_sqlite_db(db_path)
            conn.close()
            synced = sync_to_sqlite(self.inventory, db_path)
            self.assertTrue(synced)

            loaded_rows = load_from_sqlite(db_path)
            self.assertEqual(len(loaded_rows), len(self.inventory))
        finally:
            if os.path.exists(db_path):
                try:
                    os.remove(db_path)
                except OSError:
                    pass

        report = generate_daily_expiry_report(self.inventory, operating_date=self.operating_date)
        self.assertIn("DAILY FOOD EXPIRY", report)
        self.assertIn("Expired", report)
        self.assertIn("Expiring-Soon", report)


class TestFoodSafetyExpiryQuarantine(unittest.TestCase):
    """
    Verification of food safety quarantine protocols:
    - Items past expiry timestamp cannot be 'Available'
    - Effective status dynamically reclassifies to 'Expired'
    - get_freshness_status labels expired food with '🚨 Expired'
    - sync_expired_statuses quarantines all past-due items
    """

    def setUp(self):
        self.operating_date = "2026-10-05"
        self.past_item = {
            "id": "DON-1001",
            "name": "Royal Hyderabadi Veg Dum Biryani",
            "title": "Royal Hyderabadi Veg Dum Biryani",
            "category": "Cooked Meals",
            "portions": 65,
            "weight_kg": 26.0,
            "donor_name": "Grand Palace Banquet Hall",
            "prepared_at": "2026-10-01 16:51",
            "expires_at": "2026-10-01 21:06",
            "expiry_date": "2026-10-01",
            "status": "Available"
        }
        self.future_item = {
            "id": "DON-1008",
            "name": "Steamed Idli Breakfast Combos",
            "title": "Steamed Idli Breakfast Combos",
            "category": "Cooked Meals",
            "portions": 45,
            "weight_kg": 18.0,
            "donor_name": "Annapoorna Tiffin Center",
            "prepared_at": "2026-10-05 14:00",
            "expires_at": (dt.now() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"),
            "expiry_date": (dt.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "status": "Available"
        }
        self.completed_item = {
            "id": "DON-1007",
            "name": "High-Tea Sandwiches",
            "title": "High-Tea Sandwiches",
            "category": "Bakery",
            "portions": 70,
            "weight_kg": 22.0,
            "prepared_at": "2026-10-01 11:51",
            "expires_at": "2026-10-01 17:51",
            "status": "Completed"
        }

    def test_past_expiry_marked_expired_not_available(self):
        """Food past safe use-by/expiry date is strictly expired and never available."""
        self.assertTrue(is_item_expired(self.past_item, current_time=self.operating_date))
        effective = get_effective_status(self.past_item, current_time=self.operating_date)
        self.assertEqual(effective, "Expired")
        self.assertNotEqual(effective, "Available")

    def test_future_expiry_remains_available(self):
        """Uncollected food before expiry date remains available."""
        self.assertFalse(is_item_expired(self.future_item))
        effective = get_effective_status(self.future_item)
        self.assertEqual(effective, "Available")

    def test_completed_item_preserves_completed_status(self):
        """Food already completed/handed over remains 'Completed'."""
        effective = get_effective_status(self.completed_item, current_time=self.operating_date)
        self.assertEqual(effective, "Completed")

    def test_sync_expired_statuses_quarantines_inventory(self):
        """sync_expired_statuses updates stored status and flags quarantined=True."""
        inv = [dict(self.past_item), dict(self.future_item), dict(self.completed_item)]
        reclassified = sync_expired_statuses(inv, current_time=self.operating_date)
        self.assertEqual(reclassified, 1)
        self.assertEqual(inv[0]["status"], "Expired")
        self.assertTrue(inv[0].get("quarantined"))
        self.assertEqual(inv[1]["status"], "Available")
        self.assertEqual(inv[2]["status"], "Completed")

    def test_get_freshness_status_for_past_date(self):
        """get_freshness_status classifies elapsed dates as Expired tier."""
        freshness = get_freshness_status("2026-10-01 21:06")
        self.assertEqual(freshness["tier"], "Expired")
        self.assertTrue(freshness.get("is_expired"))
        self.assertIn("Expired", freshness["label"])
        self.assertNotIn("Collect Today", freshness["label"])


if __name__ == "__main__":
    unittest.main()
