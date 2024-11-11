import asyncio
import ollama

# Define tool functions for products, services, and sales
def products_tool():
    print("Products function called")
    return "Product details are available. Please check our catalog."

def services_tool():
    print("Services function called")
    return "Here are the details about our services."

def sales_tool():
    print("Sales function called")
    return "We have several sales offerings. Let's discuss your needs."

# Function to log client information (for now, just printing to console)
def log_client_info(name, email, phone, interest):
    print(f"Client Information - Name: {name}, Email: {email}, Phone: {phone}, Interest: {interest}")

# Function to collect user details
def collect_user_details(interest):
    print(f"Please provide your details to assist you with {interest}:")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")

    log_client_info(name, email, phone, interest)
    return {'name': name, 'email': email, 'phone': phone, 'interest': interest}

# Main function for interacting with the model
async def run(model: str):
    # Initialize Ollama client
    client = ollama.AsyncClient()

    print("Chatbot is ready! (Type 'exit' to end the conversation)")
    
    while True:
        # Ask the user for their query
        query = input("You: ").lower()
        print(f"Debug: User Query: {query}")  # Debugging query content

        # Exit the loop if the user types "exit"
        if query == "exit":
            print("Goodbye!")
            break

        # Define the messages to send to the model
        messages = [{'role': 'user', 'content': query}]
        
        # Check if the query relates to products, services, or sales
        if 'products' in query:
            print("Bot: Sure, I can help with product details.")
            user_details = collect_user_details('products')
            print("Bot:", products_tool())  # Call the products tool
        elif 'services' in query:
            print("Bot: Sure, I can help with service details.")
            user_details = collect_user_details('services')
            print("Bot:", services_tool())  # Call the services tool
        elif 'sales' in query:
            print("Bot: Sure, I can help with sales details.")
            user_details = collect_user_details('sales')
            print("Bot:", sales_tool())  # Call the sales tool
        else:
            # If the query is unrelated to the allowed topics
            print("Bot: I can only assist with product, service, and sales inquiries.")
            response = await client.chat(model=model, messages=messages)
            print("Bot:", response['message']['content'])

# Execute the async function
asyncio.run(run('qugates_chatbot:latest'))
