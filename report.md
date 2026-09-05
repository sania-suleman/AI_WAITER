AI WAITER - RESTAURANT ORDERING BOT
PROJECT REPORT

1. INTRODUCTION

The AI Waiter is a conversational restaurant ordering chatbot that works like a virtual waiter. The customer can talk to the chatbot and place a food order.

The chatbot can add items, remove items, remember the customer's order, handle corrections, calculate the total price, and handle special situations such as out-of-stock items and allergy requests.

The system uses the restaurant menu provided for this project and does not invent menu items or prices.


2. SYSTEM ARCHITECTURE

The system has four main components:

1. Customer
2. AI Waiter
3. Menu and Cart Tools
4. Short-Term Memory

The customer sends a message to the AI Waiter. The AI understands the customer's request and selects the appropriate tool.

For example, when the customer says "add cheesecake", the chatbot uses the add_item tool.

When the customer says "remove cheesecake", the chatbot uses the remove_item tool.

The cart keeps the customer's current order and quantities.


3. MENU MODELING

The restaurant menu is stored separately in the menu.txt file.

Each menu item has a fixed price.

The chatbot checks the requested item against the available menu before adding it to the cart.

This prevents the chatbot from creating or inventing food items and prices that are not present in the menu.

The menu contains main dishes, beverages, and desserts.


4. CART STATE

The customer's order is stored using a Python dictionary.

For example:

cart = {
    "grilled chicken": 2,
    "cheesecake": 1
}

The item name is the key and the quantity is the value.

When the customer adds an item, its quantity is added to the cart.

When the customer removes an item, its quantity is reduced or the item is completely removed.

The cart is also used to calculate the current order total.


5. SHORT-TERM MEMORY

The system uses LangGraph MemorySaver for short-term conversation memory.

A conversation thread ID is used to maintain the conversation.

This allows the chatbot to remember what the customer has previously ordered during the conversation.

For example, if the customer says:

"Add cheesecake."

and later says:

"Actually remove the cheesecake."

the chatbot can understand that the customer wants to remove the previously added cheesecake.


6. TOOLS

The chatbot uses the following tools:

- show_menu
- add_item
- remove_item
- show_cart
- calculate_total
- clear_cart
- handle_allergy_request
- mark_out_of_stock

These tools allow the AI Waiter to perform actual actions on the customer's order.


7. ORDER CORRECTIONS

The chatbot can handle corrections made by the customer.

For example:

Customer: Add cheesecake.

Customer: Actually remove the cheesecake.

The chatbot removes the cheesecake from the cart and updates the order.

This makes the chatbot behave more like a real restaurant waiter.


8. EDGE CASE 1 - OUT OF STOCK

The system can handle an item becoming unavailable.

For example, during the live demonstration the instructor can say:

"The kitchen just ran out of grilled chicken."

The chatbot can mark grilled chicken as out of stock.

If the customer then tries to order grilled chicken, the chatbot informs the customer that the item is currently unavailable.

This allows the system to handle a real-time restaurant constraint.


9. EDGE CASE 2 - ALLERGY REQUEST

The provided menu does not specify approved allergy substitutions.

Therefore, the chatbot does not invent an allergy substitution.

If a customer asks for an allergy substitution, the chatbot explains that no approved substitution is specified in the menu.

This prevents the AI from providing unsupported information.


10. PRICE CALCULATION

The chatbot calculates the total using the fixed menu prices.

The calculation for each item is:

Item Total = Quantity × Item Price

The item totals are then added together to calculate the final order total.

No combo discount is applied because no combo discount is specified in the menu.


11. API USAGE

Google Gemini is used as the language model.

LangChain connects the language model with the available tools.

LangGraph MemorySaver provides short-term memory for the conversation.

The Google API key is stored in a .env file instead of being written directly inside the Python source code.


12. CONCLUSION

The AI Waiter demonstrates how an AI chatbot can be used for restaurant ordering.

The chatbot can understand customer requests, maintain a running cart, handle order corrections, calculate prices, and respond to special situations such as out-of-stock items and allergy requests.

The project can be improved in the future by adding a database, real-time restaurant inventory, online payment, and a graphical user interface.