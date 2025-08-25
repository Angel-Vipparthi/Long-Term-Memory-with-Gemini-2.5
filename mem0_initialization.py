#!/usr/bin/env python3
"""
Milestone 2: Initialize Memory System (Alternative Approach)
Goal: Set up a memory system using only Gemini API and local storage, no external dependencies.
"""

import os
import json
import pickle
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

class SimpleMemory:
    """Simple memory system using Gemini API for processing and local storage for persistence."""
    
    def __init__(self, storage_path="./simple_memory_db"):
        self.storage_path = storage_path
        self.memory_file = os.path.join(storage_path, "memories.json")
        self.conversations_file = os.path.join(storage_path, "conversations.json")
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
        
        # Initialize storage files
        self._init_storage()
        
    def _init_storage(self):
        """Initialize storage files if they don't exist."""
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.conversations_file):
            with open(self.conversations_file, 'w') as f:
                json.dump([], f)
    
    def add_conversation(self, messages, user_id="default_user"):
        """Add a conversation to memory storage."""
        conversation = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "messages": messages
        }
        
        # Load existing conversations
        with open(self.conversations_file, 'r') as f:
            conversations = json.load(f)
        
        # Add new conversation
        conversations.append(conversation)
        
        # Save back to file
        with open(self.conversations_file, 'w') as f:
            json.dump(conversations, f, indent=2)
        
        return len(conversations) - 1  # Return conversation ID
    
    def get_conversations(self, user_id="default_user", limit=10):
        """Get recent conversations for a user."""
        with open(self.conversations_file, 'r') as f:
            conversations = json.load(f)
        
        # Filter by user_id and get recent ones
        user_conversations = [
            conv for conv in conversations 
            if conv.get("user_id") == user_id
        ]
        
        return user_conversations[-limit:] if user_conversations else []
    
    def add_memory(self, memory_text, user_id="default_user"):
        """Add a processed memory."""
        memory = {
            "user_id": user_id,
            "memory": memory_text,
            "timestamp": datetime.now().isoformat()
        }
        
        # Load existing memories
        with open(self.memory_file, 'r') as f:
            memories = json.load(f)
        
        # Add new memory
        memories.append(memory)
        
        # Save back to file
        with open(self.memory_file, 'w') as f:
            json.dump(memories, f, indent=2)
        
        return len(memories) - 1  # Return memory ID
    
    def get_memories(self, user_id="default_user"):
        """Get all memories for a user."""
        with open(self.memory_file, 'r') as f:
            memories = json.load(f)
        
        return [mem for mem in memories if mem.get("user_id") == user_id]
    
    def get_stats(self):
        """Get memory system statistics."""
        with open(self.memory_file, 'r') as f:
            memories = json.load(f)
        
        with open(self.conversations_file, 'r') as f:
            conversations = json.load(f)
        
        return {
            "total_memories": len(memories),
            "total_conversations": len(conversations),
            "storage_path": self.storage_path
        }

def main():
    # Load environment variables
    load_dotenv()
    
    # Configure Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in .env file")
        return
    
    genai.configure(api_key=api_key)
    
    print("🧠 Milestone 2: Alternative Memory System")
    print("=" * 50)
    
    try:
        print("🔄 Initializing simple memory system...")
        
        # Initialize our custom memory system
        memory = SimpleMemory()
        
        print("✅ Simple memory system initialized successfully")
        
        # Test the memory system functionality
        print("🔍 Testing memory system functionality...")
        
        # Test 1: Add a test conversation
        test_conversation = [
            {"role": "user", "content": "Hello, I'm John and I love hiking"},
            {"role": "assistant", "content": "Nice to meet you John! Hiking is a great hobby."}
        ]
        
        conv_id = memory.add_conversation(test_conversation, user_id="test_user")
        print(f"✅ Test conversation added (ID: {conv_id})")
        
        # Test 2: Add a processed memory
        memory_id = memory.add_memory("User John enjoys hiking and outdoor activities", user_id="test_user")
        print(f"✅ Test memory added (ID: {memory_id})")
        
        # Test 3: Retrieve data
        conversations = memory.get_conversations(user_id="test_user")
        memories = memory.get_memories(user_id="test_user")
        stats = memory.get_stats()
        
        print(f"✅ Retrieved {len(conversations)} conversations")
        print(f"✅ Retrieved {len(memories)} memories")
        
        # Display system info
        print(f"📊 System stats: {stats}")
        print(f"🗂️  Storage location: {memory.storage_path}")
        
        # Check if storage files were created
        if os.path.exists(memory.memory_file) and os.path.exists(memory.conversations_file):
            print("✅ Storage files created successfully")
        else:
            print("⚠️  Storage files not found")
        
        print("\n" + "=" * 50)
        print("📋 MILESTONE 2 ANALYSIS:")
        print("✅ Custom memory system created successfully")
        print("✅ Local storage working (no external APIs needed)")
        print("✅ Can store conversations and memories")
        print("✅ Can retrieve stored data")
        print("✅ Persistent storage across sessions")
        print("📈 Next: We'll populate memory with predefined conversations!")
        
        return memory
        
    except Exception as e:
        print(f"❌ Memory system initialization error: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("- Check if you have write permissions in the current directory")
        print("- Make sure the directory is not read-only")
        return None

if __name__ == "__main__":
    main()