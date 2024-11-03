import streamlit as st
from routers import primary_router, secondary_router, department_router
from system_messages import department_messages
from utils import openrouter_completion

# Streamlit App Title
st.title("MegaMart Conversational Assistant")
st.write("Ask questions about MegaMart products and services!")

# User Input
user_input = st.text_input("Enter your question:")

if st.button("Submit") and user_input:
    # Determine the appropriate model
    model = primary_router(user_input)
    
    # Choose system message based on model or department
    if model == "llama3-70b-8192":
        system_message = secondary_router(user_input, model="code")
    elif model == "llama-3.1-70b-versatile":
        system_message = secondary_router(user_input, model="complex")
    elif model == "gemma-7b-it":
        system_message = secondary_router(user_input, model="simple")
    else:
        department = department_router(user_input)
        system_message = department_messages.get(department, "General customer service.")
        st.write(f"Connecting you to the {department.replace('_', ' ').title()} department.")

    # Generate response
    response = openrouter_completion(model, user_input, system_message)
    
    # Display response
    st.write("**Assistant:**", response)