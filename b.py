import asyncio
import ollama
from pymongo import MongoClient

# MongoDB client setup (you can modify this according to your DB URI)
client = MongoClient("mongodb://localhost:27017")
db = client.qugates_chatbot
collection = db.client_details  # Collection to store client details

# Define tool functions for products, services, sales, and job applications
def products_tool():
    print("Products function called")
    return "Product details are available. Please check our catalog."

def services_tool():
    print("Services function called")
    return "Here are the details about our services."

def sales_tool():
    print("Sales function called")
    return "We have several sales offerings. Let's discuss your needs."

def job_application_tool():
    print("Job Application function called")
    return "We are currently hiring. Please submit your application details."

# Function to log client information to the database
def log_client_info_to_db(name, email, phone, interest):
    client_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "interest": interest
    }
    collection.insert_one(client_data)
    print(f"Client Information saved to DB: {client_data}")

# Function to collect user details
def collect_user_details(interest):
    print(f"Please provide your details to assist you with {interest}:")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")

    log_client_info_to_db(name, email, phone, interest)
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
        
        # Check if the query relates to products, services, sales, or job application
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
        elif 'job' in query or 'career' in query:
            print("Bot: Sure, I can help with job applications.")
            user_details = collect_user_details('job application')
            print("Bot:", job_application_tool())  # Call the job application tool
        else:
            # If the query is unrelated to the allowed topics
            print("Bot: I can only assist with product, service, sales, or job inquiries.")
            response = await client.chat(model=model, messages=messages)
            print("Bot:", response['message']['content'])

# Execute the async function
asyncio.run(run('qugates_chatbot:latest'))
