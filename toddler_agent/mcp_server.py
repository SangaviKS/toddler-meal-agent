from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Toddler Nutrition Server")

@mcp.tool()
def get_age_appropriate_foods(age_months: int) -> dict:
    """
    Returns age-appropriate foods and textures for a toddler
    based on their age in months.
    """
    if age_months < 12:
        return {
            "age_months": age_months,
            "texture": "pureed or mashed",
            "appropriate_foods": [
                "pureed vegetables", "mashed banana", 
                "pureed chicken", "iron-fortified cereals"
            ],
            "foods_to_avoid": [
                "honey", "whole nuts", "hard raw vegetables",
                "whole grapes", "popcorn", "added salt or sugar"
            ]
        }
    elif age_months < 18:
        return {
            "age_months": age_months,
            "texture": "soft, small pieces",
            "appropriate_foods": [
                "sliced bananas", "soft cooked pasta",
                "scrambled eggs", "soft cooked vegetables",
                "small pieces of soft chicken", "yogurt",
                "soft cheese cubes", "avocado slices"
            ],
            "foods_to_avoid": [
                "honey", "whole nuts", "popcorn",
                "whole grapes", "hard raw vegetables",
                "large chunks of meat"
            ]
        }
    elif age_months < 24:
        return {
            "age_months": age_months,
            "texture": "chopped, soft pieces",
            "appropriate_foods": [
                "chopped fruits", "cooked vegetables",
                "whole grain crackers", "cheese",
                "beans", "soft cooked fish",
                "scrambled eggs", "yogurt"
            ],
            "foods_to_avoid": [
                "whole nuts", "popcorn",
                "hard candy", "large pieces of raw vegetables"
            ]
        }
    else:
        return {
            "age_months": age_months,
            "texture": "most textures appropriate",
            "appropriate_foods": [
                "most fruits and vegetables",
                "whole grain bread", "lean proteins",
                "dairy products", "legumes"
            ],
            "foods_to_avoid": [
                "hard candy", "excessive sugar or salt"
            ]
        }


@mcp.tool()
def get_weekly_meal_plan(
    age_months: int,
    allergies: list[str],
    preferred_foods: list[str]
) -> dict:
    """
    Generates a 7-day meal and snack plan for a toddler
    based on age, allergies, and food preferences.
    """
    # Base meal templates filtered by age
    if age_months < 18:
        breakfasts = [
            "Mashed banana with yogurt",
            "Scrambled eggs with soft toast",
            "Oatmeal with mashed berries",
            "Soft pancakes with fruit puree",
            "Yogurt with soft fruit pieces",
            "Whole grain cereal with warm milk",
            "Avocado toast fingers"
        ]
        snacks = [
            "Sliced banana",
            "Soft cheese cubes",
            "Yogurt",
            "Soft cooked carrot sticks",
            "Rice cakes",
            "Avocado slices",
            "Soft pear pieces"
        ]
        lunches = [
            "Soft pasta with veggie sauce",
            "Mashed sweet potato with chicken",
            "Lentil soup with soft bread",
            "Avocado and egg mash",
            "Soft fish with mashed peas",
            "Cheese quesadilla strips",
            "Veggie and rice bowl"
        ]
        dinners = [
            "Soft chicken with mashed vegetables",
            "Fish with sweet potato mash",
            "Lentil dal with rice",
            "Soft tofu stir fry with rice",
            "Pasta with meat sauce",
            "Bean and veggie soup",
            "Egg fried rice with vegetables"
        ]
    else:
        breakfasts = [
            "Chopped fruit with yogurt",
            "Whole grain toast with avocado",
            "Oatmeal with banana slices",
            "Scrambled eggs with cheese",
            "Mini whole grain pancakes",
            "Yogurt parfait with soft fruit",
            "Whole grain cereal with milk"
        ]
        snacks = [
            "Apple slices with cheese",
            "Whole grain crackers",
            "Hummus with soft pita",
            "Yogurt cup",
            "Banana with cheese",
            "Soft dried mango pieces",
            "Cucumber sticks with cream cheese"
        ]
        lunches = [
            "Pasta with veggie sauce and cheese",
            "Bean and cheese quesadilla",
            "Vegetable soup with bread",
            "Tuna and avocado on crackers",
            "Grilled cheese sandwich strips",
            "Lentil soup with rice",
            "Chicken and vegetable wrap"
        ]
        dinners = [
            "Baked chicken with roasted vegetables",
            "Salmon with mashed potatoes",
            "Beef and vegetable stew",
            "Pasta with bolognese sauce",
            "Bean tacos with soft tortilla",
            "Stir fry tofu with rice",
            "Lentil curry with naan"
        ]

    # Filter out allergens
    def is_safe(meal: str) -> bool:
        return not any(
            allergen.lower() in meal.lower()
            for allergen in allergies
        )

    # Prioritize preferred foods
    def has_preference(meal: str) -> bool:
        return any(
            pref.lower() in meal.lower()
            for pref in preferred_foods
        )

    safe_breakfasts = [m for m in breakfasts if is_safe(m)]
    safe_snacks = [m for m in snacks if is_safe(m)]
    safe_lunches = [m for m in lunches if is_safe(m)]
    safe_dinners = [m for m in dinners if is_safe(m)]

    # Build 7-day plan
    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
    plan = {}
    for i, day in enumerate(days):
        plan[day] = {
            "breakfast": safe_breakfasts[i % len(safe_breakfasts)],
            "morning_snack": safe_snacks[i % len(safe_snacks)],
            "lunch": safe_lunches[i % len(safe_lunches)],
            "afternoon_snack": safe_snacks[(i + 3) % len(safe_snacks)],
            "dinner": safe_dinners[i % len(safe_dinners)]
        }

    return {
        "age_months": age_months,
        "allergies_excluded": allergies,
        "weekly_plan": plan
    }


@mcp.tool()
def get_grocery_list(age_months: int, allergies: list[str]) -> dict:
    """
    Generates a grocery list for a toddler based on age and allergies.
    """
    base_items = {
        "Fruits": ["bananas", "pears", "avocados", "berries"],
        "Vegetables": ["sweet potato", "carrots", "peas", "cucumber"],
        "Protein": ["eggs", "chicken", "fish", "lentils", "tofu", "beans"],
        "Dairy": ["yogurt", "cheese", "milk"],
        "Grains": ["oatmeal", "whole grain bread", "pasta", "rice", "rice cakes"],
        "Pantry": ["olive oil", "cream cheese", "hummus"]
    }

    # Filter out allergens
    filtered = {}
    for category, items in base_items.items():
        safe_items = [
            item for item in items
            if not any(allergen.lower() in item.lower() for allergen in allergies)
        ]
        if safe_items:
            filtered[category] = safe_items

    return {"grocery_list": filtered, "allergies_excluded": allergies}


if __name__ == "__main__":
    mcp.run(transport="stdio")