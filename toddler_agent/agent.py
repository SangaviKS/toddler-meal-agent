import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

load_dotenv()

def check_snack_safety(food_item: str, age_months: int, allergies: list[str]) -> dict:
    """
    Checks if a snack is safe for a toddler based on age and allergies.
    Returns safety status and reason.
    """
    choking_hazards = {
        12: ["grapes", "nuts", "raw carrots", "popcorn", "hard candy", "whole blueberries"],
        18: ["nuts", "popcorn", "hard candy"],
        24: ["popcorn", "hard candy"],
    }

    hazards = []
    for age_threshold, foods in choking_hazards.items():
        if age_months <= age_threshold:
            hazards.extend(foods)

    food_lower = food_item.lower()

    for hazard in hazards:
        if hazard in food_lower:
            return {
                "safe": False,
                "reason": f"{food_item} is a choking hazard for children under {age_months} months"
            }

    for allergy in allergies:
        if allergy.lower() in food_lower:
            return {
                "safe": False,
                "reason": f"{food_item} contains {allergy} which is in the allergy list"
            }

    return {"safe": True, "reason": f"{food_item} is safe for a {age_months}-month-old"}


# MCP Toolset connecting to local nutrition server
mcp_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="python",
        args=[
            "/Users/sangavisundaramoorthy/Downloads/Sangavi/Personal_Projects/toddler-meal-agent/toddler_agent/mcp_server.py"
        ],
    )
)

# Define the orchestrator agent
root_agent = Agent(
    name="toddler_meal_concierge",
    model="gemini-2.5-flash",
    description="A personal concierge agent that suggests safe, age-appropriate meals and snacks for toddlers.",
    instruction="""
        You are a caring and knowledgeable toddler meal planning assistant.
        
        You have access to these tools:
        - check_snack_safety: Always use this before suggesting any food
        - get_age_appropriate_foods: Use this to understand what textures and foods suit the child's age
        - get_weekly_meal_plan: Use this when a parent asks for a weekly or daily meal plan
        - get_grocery_list: Call with age_months and allergies to generate a shopping list
        
        When a parent asks for meal or snack suggestions:
        1. Ask for the child's age in months if not provided
        2. Ask about any known allergies
        3. Ask about foods the child enjoys
        4. Always call get_age_appropriate_foods first to understand age constraints
        5. Always call check_snack_safety before suggesting any specific food
        6. Explain WHY a food is appropriate for the child's age
        7. Keep suggestions practical and easy to prepare
        
        When a parent asks for a weekly plan:
        1. Call get_weekly_meal_plan with age, allergies, and preferences
        2. Then call get_grocery_list with the resulting plan
        3. Present both the plan and grocery list clearly
        
        Be warm, reassuring, and parent-friendly in your tone.
        Never suggest a food without checking its safety first.
        Always prioritize child safety above all else.
    """,
    tools=[check_snack_safety, mcp_toolset],
)