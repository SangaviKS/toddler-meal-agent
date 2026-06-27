"""
Export tool for Toddler Meal Concierge Agent.
Generates a beautiful HTML meal plan file parents can save, print, or share.
"""

import os
from datetime import datetime


def export_meal_plan_html(
    child_age_months: int,
    allergies: list[str],
    weekly_plan: dict,
    grocery_list: dict
) -> dict:
    """
    Generates a formatted HTML meal plan file saved to the user's Downloads folder.
    Parents can open it in a browser, print it, or save it for reference.

    Args:
        child_age_months: Child's age in months
        allergies: List of allergens to exclude
        weekly_plan: Weekly meal plan from get_weekly_meal_plan tool
        grocery_list: Grocery list from get_grocery_list tool

    Returns:
        dict with success status and file path
    """
    try:
        plan = weekly_plan.get("weekly_plan", {})
        grocery = grocery_list.get("grocery_list", {})
        allergies_str = ", ".join(allergies) if allergies else "None"
        today = datetime.now().strftime("%B %d, %Y")
        filename = f"toddler_meal_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        output_path = os.path.join(
            os.path.expanduser("~"), "Downloads", filename
        )

        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]

        day_emojis = {
            "Monday": "🌟", "Tuesday": "🌈", "Wednesday": "🌻",
            "Thursday": "🦋", "Friday": "🎉", "Saturday": "🌸", "Sunday": "☀️"
        }

        category_emojis = {
            "Fruits": "🍎", "Vegetables": "🥕", "Protein": "🥚",
            "Dairy": "🥛", "Grains": "🌾", "Pantry": "🫙"
        }

        # Build day cards
        day_cards_html = ""
        for day in days:
            if day in plan:
                meals = plan[day]
                emoji = day_emojis.get(day, "📅")
                day_cards_html += f"""
                <div class="day-card">
                    <div class="day-header">{emoji} {day}</div>
                    <div class="meal-row">
                        <span class="meal-label">🌅 Breakfast</span>
                        <span class="meal-value">{meals.get('breakfast', '')}</span>
                    </div>
                    <div class="meal-row">
                        <span class="meal-label">🍎 Morning Snack</span>
                        <span class="meal-value">{meals.get('morning_snack', '')}</span>
                    </div>
                    <div class="meal-row">
                        <span class="meal-label">☀️ Lunch</span>
                        <span class="meal-value">{meals.get('lunch', '')}</span>
                    </div>
                    <div class="meal-row">
                        <span class="meal-label">🍌 Afternoon Snack</span>
                        <span class="meal-value">{meals.get('afternoon_snack', '')}</span>
                    </div>
                    <div class="meal-row">
                        <span class="meal-label">🌙 Dinner</span>
                        <span class="meal-value">{meals.get('dinner', '')}</span>
                    </div>
                </div>
                """

        # Build grocery categories
        grocery_html = ""
        for category, items in grocery.items():
            emoji = category_emojis.get(category, "•")
            items_html = "".join(
                f"<li>{item.capitalize()}</li>" for item in items
            )
            grocery_html += f"""
            <div class="grocery-category">
                <h3>{emoji} {category}</h3>
                <ul>{items_html}</ul>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weekly Meal Plan — {child_age_months}-Month-Old</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #FFF8F0;
            color: #333;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #FF8C00, #FFA500);
            color: white;
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2em; margin-bottom: 8px; }}
        .header p {{ opacity: 0.9; font-size: 1.1em; }}
        .badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 20px;
            margin: 4px;
            font-size: 0.9em;
        }}
        .section-title {{
            font-size: 1.5em;
            color: #FF8C00;
            margin: 30px 0 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #FFE0B2;
        }}
        .days-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 16px;
            margin-bottom: 30px;
        }}
        .day-card {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .day-header {{
            background: linear-gradient(135deg, #4CAF50, #66BB6A);
            color: white;
            padding: 12px 16px;
            font-weight: bold;
            font-size: 1.1em;
        }}
        .meal-row {{
            display: flex;
            padding: 10px 16px;
            border-bottom: 1px solid #F5F5F5;
            align-items: flex-start;
            gap: 10px;
        }}
        .meal-row:last-child {{ border-bottom: none; }}
        .meal-label {{
            color: #888;
            font-size: 0.85em;
            min-width: 130px;
            padding-top: 2px;
        }}
        .meal-value {{
            font-size: 0.95em;
            color: #333;
            flex: 1;
        }}
        .grocery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 16px;
        }}
        .grocery-category {{
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .grocery-category h3 {{
            color: #FF8C00;
            margin-bottom: 10px;
            font-size: 1em;
        }}
        .grocery-category ul {{
            list-style: none;
            padding: 0;
        }}
        .grocery-category li {{
            padding: 4px 0;
            border-bottom: 1px solid #F5F5F5;
            font-size: 0.9em;
            color: #555;
        }}
        .grocery-category li:last-child {{ border-bottom: none; }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #888;
            font-size: 0.85em;
        }}
        @media print {{
            body {{ background: white; }}
            .day-card, .grocery-category {{ box-shadow: none; border: 1px solid #ddd; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🍼 Weekly Meal Plan</h1>
        <p>Personalized for your <strong>{child_age_months}-month-old</strong></p>
        <div style="margin-top: 10px;">
            <span class="badge">Generated: {today}</span>
            <span class="badge">🚫 Excludes: {allergies_str}</span>
        </div>
    </div>

    <h2 class="section-title">📅 7-Day Meal Schedule</h2>
    <div class="days-grid">
        {day_cards_html}
    </div>

    <h2 class="section-title">🛒 Grocery List</h2>
    <div class="grocery-grid">
        {grocery_html}
    </div>

    <div class="footer">
        <p>🤖 Generated by Toddler Meal Concierge Agent</p>
        <p>Always consult your pediatrician for personalized nutritional advice.</p>
    </div>
</body>
</html>"""

        with open(output_path, "w") as f:
            f.write(html)

        return {
            "success": True,
            "message": f"Meal plan saved to your Downloads folder as {filename}. Open it in your browser to view or print it!",
            "file_path": output_path
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Could not save meal plan: {str(e)}"
        }