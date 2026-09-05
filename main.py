import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver


# =========================================================
# 1. LOAD API KEY
# =========================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")


# =========================================================
# 2. EXACT MENU FROM THE PROVIDED MENU
# =========================================================

MENU = {
    "grilled salmon": 18.99,
    "vegetable pad thai": 13.99,
    "mushroom risotto": 14.99,
    "grilled chicken": 12.99,
    "classic beef": 16.99,
    "eggplant parmesan": 15.99,

    "classic margarita": 3.99,
    "mango mocktail": 2.99,
    "iced caramel macchiato": 4.99,
    "green tea frappuccino": 3.99,
    "pineapple coconut smoothie": 5.99,
    "raspberry mojito": 3.99,
    "blackberry ginger sparkler": 2.99,

    "chocolate mousse": 5.99,
    "apple pie": 7.99,
    "strawberry shortcake": 6.99,
    "fruit tart": 5.99,
    "tiramisu": 8.99,
    "chocolate lava cake": 6.99,
    "cheesecake": 5.99,
}


# =========================================================
# 3. CART STATE
# =========================================================

cart = {}


# =========================================================
# 4. OUT-OF-STOCK ITEMS
# =========================================================

out_of_stock = set()


# =========================================================
# 5. ADD ITEM TOOL
# =========================================================

@tool
def add_item(item: str, quantity: int = 1) -> str:
    """Add a menu item to the customer's cart."""

    item = item.lower().strip()

    if item not in MENU:
        return (
            f"Sorry, '{item}' is not on our menu. "
            "Please choose an item from the available menu."
        )

    if item in out_of_stock:
        return f"Sorry, {item.title()} is currently out of stock."

    if quantity < 1:
        return "Quantity must be at least 1."

    if item in cart:
        cart[item] += quantity
    else:
        cart[item] = quantity

    total = MENU[item] * quantity

    return (
        f"Added {quantity} x {item.title()} to your order. "
        f"Item cost: ${total:.2f}."
    )


# =========================================================
# 6. REMOVE ITEM TOOL
# =========================================================

@tool
def remove_item(item: str, quantity: int = 1) -> str:
    """Remove a quantity of an item from the customer's cart."""

    item = item.lower().strip()

    if item not in cart:
        return f"{item.title()} is not currently in your cart."

    if quantity >= cart[item]:
        del cart[item]
        return f"Removed {item.title()} from your order."

    cart[item] -= quantity

    return (
        f"Removed {quantity} x {item.title()}. "
        f"{cart[item]} remaining."
    )


# =========================================================
# 7. SHOW CART TOOL
# =========================================================

@tool
def show_cart() -> str:
    """Show all items currently in the customer's cart."""

    if not cart:
        return "Your cart is currently empty."

    lines = ["Current order:"]

    total = 0

    for item, quantity in cart.items():
        price = MENU[item]
        item_total = price * quantity
        total += item_total

        lines.append(
            f"- {quantity} x {item.title()} = ${item_total:.2f}"
        )

    lines.append(f"Current total: ${total:.2f}")

    return "\n".join(lines)


# =========================================================
# 8. REMOVE EVERYTHING TOOL
# =========================================================

@tool
def clear_cart() -> str:
    """Clear the entire customer order."""

    cart.clear()

    return "Your entire order has been cleared."


# =========================================================
# 9. ALLERGY REQUEST TOOL
# =========================================================

@tool
def handle_allergy_request(item: str, allergy: str) -> str:
    """Handle an allergy request according to the menu rules."""

    return (
        f"Your allergy request for {item.title()} involving {allergy} "
        "cannot be approved because the provided menu does not specify "
        "an allergy substitution for this item. "
        "I will not invent a substitution."
    )


# =========================================================
# 10. OUT OF STOCK TOOL
# =========================================================

@tool
def mark_out_of_stock(item: str) -> str:
    """Mark a menu item as temporarily out of stock."""

    item = item.lower().strip()

    if item not in MENU:
        return f"{item.title()} is not a menu item."

    out_of_stock.add(item)

    if item in cart:
        del cart[item]
        return (
            f"{item.title()} is now out of stock. "
            "It has been removed from the current order."
        )

    return f"{item.title()} has been marked as out of stock."


# =========================================================
# 11. MENU TOOL
# =========================================================

@tool
def show_menu() -> str:
    """Show the restaurant menu and prices."""

    sections = {
        "Main Dishes": [
            "grilled salmon",
            "vegetable pad thai",
            "mushroom risotto",
            "grilled chicken",
            "classic beef",
            "eggplant parmesan",
        ],
        "Beverages": [
            "classic margarita",
            "mango mocktail",
            "iced caramel macchiato",
            "green tea frappuccino",
            "pineapple coconut smoothie",
            "raspberry mojito",
            "blackberry ginger sparkler",
        ],
        "Desserts": [
            "chocolate mousse",
            "apple pie",
            "strawberry shortcake",
            "fruit tart",
            "tiramisu",
            "chocolate lava cake",
            "cheesecake",
        ],
    }

    result = []

    for section, items in sections.items():
        result.append(f"\n{section}")

        for item in items:
            status = ""

            if item in out_of_stock:
                status = " - OUT OF STOCK"

            result.append(
                f"{item.title()} - ${MENU[item]:.2f}{status}"
            )

    result.append(
        "\nSpecial rules: No combo discounts, "
        "spice-level options, or allergy substitutions "
        "are specified on the provided menu."
    )

    return "\n".join(result)


# =========================================================
# 12. TOTAL TOOL
# =========================================================

@tool
def calculate_total() -> str:
    """Calculate the customer's current order total."""

    if not cart:
        return "Your cart is empty. Total: $0.00"

    subtotal = 0

    for item, quantity in cart.items():
        subtotal += MENU[item] * quantity

    return f"Your current total is ${subtotal:.2f}."


# =========================================================
# 13. AI MODEL
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)


# =========================================================
# 14. SYSTEM INSTRUCTIONS
# =========================================================

SYSTEM_PROMPT = """
You are an AI Waiter for Paucek and Lage Restaurant.

Your job is to help customers order food.

IMPORTANT RULES:

1. ONLY use items and prices from the provided menu.
2. NEVER invent a food item or price.
3. Always use tools when adding, removing, or checking cart items.
4. Remember the customer's order during the conversation.
5. If the customer says "actually remove..." or changes an order,
   correctly update the cart.
6. If an item is unavailable, clearly tell the customer.
7. If the customer asks for an allergy substitution, do NOT invent
   a substitution because the provided menu does not specify approved
   allergy substitutions.
8. There are no combo discounts in the provided menu.
9. There are no spice-level options in the provided menu.
10. Calculate the final total accurately.
11. Before final confirmation, show all ordered items, quantities,
    individual prices, and the final total.
12. Be polite and concise like a real restaurant waiter.
13. If the user asks to see the menu, use the menu tool.
14. If the user asks to add an item, use add_item.
15. If the user asks to remove an item, use remove_item.
16. If the user asks for the current order, use show_cart.
17. If the user asks for the total, use calculate_total.
"""


# =========================================================
# 15. TOOLS
# =========================================================

tools = [
    show_menu,
    add_item,
    remove_item,
    show_cart,
    calculate_total,
    clear_cart,
    handle_allergy_request,
    mark_out_of_stock,
]


# =========================================================
# 16. SHORT-TERM MEMORY
# =========================================================

memory = MemorySaver()


# =========================================================
# 17. CREATE LANGCHAIN AGENT
# =========================================================

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory,
)


# =========================================================
# 18. CHAT LOOP
# =========================================================

print("\n====================================")
print("     AI WAITER - RESTAURANT BOT")
print("====================================")
print("Type 'exit' to stop.")
print("Type 'menu' to see the menu.")
print("====================================\n")


config = {
    "configurable": {
        "thread_id": "restaurant_customer_1"
    }
}


while True:

    user_input = input("Customer: ")

    if user_input.lower().strip() == "exit":
        print("AI Waiter: Thank you for visiting Paucek and Lage Restaurant!")
        break

    if user_input.lower().strip() == "menu":
        print("\n" + show_menu.invoke({}) + "\n")
        continue

    try:

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            },
            config=config
        )

        print("\nAI Waiter:", response["messages"][-1].text)
        print()

    except Exception as e:
        print("\nError:", e)
        print()
        # python main.py