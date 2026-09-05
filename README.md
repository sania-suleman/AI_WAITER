# AI Waiter - Restaurant Ordering Bot

## Project Description

AI Waiter is a conversational restaurant ordering chatbot built using Python, LangChain, LangGraph, and Google Gemini.

The chatbot acts like a virtual waiter. It allows customers to view the restaurant menu, add items to their order, remove items, modify their order, check the current cart, and calculate the final total.

## Technologies Used

- Python
- LangChain
- LangGraph
- Google Gemini
- Python-dotenv
- Short-term memory using LangGraph MemorySaver

## Features

- Displays the restaurant menu
- Adds food items to the cart
- Removes food items
- Remembers the running order
- Handles order corrections
- Calculates the current total
- Handles unavailable items
- Handles allergy requests
- Prevents invented menu items
- Confirms the final order

## Menu

The project uses the exact menu stored in `menu.txt`.

## Short-Term Memory

The chatbot uses LangGraph `MemorySaver` with a conversation thread ID.

This allows the chatbot to remember the conversation and maintain the customer's order during the session.

## Edge Cases

### 1. Out-of-stock item

If an item becomes unavailable, the chatbot marks it as out of stock and does not allow the customer to order it.

### 2. Allergy substitution

The provided menu does not specify approved allergy substitutions. Therefore, the chatbot does not invent a substitution and informs the customer.

### 3. Order correction

The customer can say things such as:

"Actually remove the cheesecake."

The chatbot removes the item from the current cart.

## How to Run

Install the required packages:

```bash
python -m pip install langchain langchain-google-genai langgraph python-dotenv