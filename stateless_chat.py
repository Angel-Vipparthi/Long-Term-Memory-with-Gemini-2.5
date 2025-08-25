#!/usr/bin/env python3
"""
Milestone 1: Basic Stateless Chatbot
Goal: Verify Gemini API works for basic interaction and demonstrate its stateless nature.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def main():
    # Load environment variables
    load_dotenv()
    
    # Configure Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in .env file")
        return
    
    genai.configure(api_key=api_key)
    
    # Initialize the model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("🤖 Basic Stateless Chatbot (Milestone 1)")
    print("=" * 50)
    
    # Test 1: Ask for book recommendations
    print("\n📚 Test 1: Asking for book recommendations")
    user_input_1 = "Can you recommend some good books to read?"
    print(f"You: {user_input_1}")
    
    try:
        response_1 = model.generate_content(user_input_1)
        print(f"Gemini: {response_1.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n" + "-" * 50)
    
    # Test 2: Follow-up question (demonstrating stateless nature)
    print("\n📖 Test 2: Follow-up question about fiction books")
    user_input_2 = "What about that fiction book you mentioned? Tell me more about it."
    print(f"You: {user_input_2}")
    
    try:
        response_2 = model.generate_content(user_input_2)
        print(f"Gemini: {response_2.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n" + "=" * 50)
    print("📋 MILESTONE 1 ANALYSIS:")
    print("✅ First response: Gemini provided book recommendations")
    print("❌ Second response: Gemini doesn't remember the previous conversation")
    print("🔍 This demonstrates the STATELESS nature of basic LLM interactions")
    print("📈 Next: We'll add memory to solve this problem!")

if __name__ == "__main__":
    main()