#!/usr/bin/env python3
"""
Milestone 3: Store Predefined Memories
Goal: Populate the memory system with pre-existing conversational data to build a base of 
long-term memories for a specific user.
"""

import os
import json
from datetime import datetime, timedelta
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
    
    def add_conversation(self, messages, user_id="default_user", timestamp=None):
        """Add a conversation to memory storage."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
            
        conversation = {
            "user_id": user_id,
            "timestamp": timestamp,
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
    
    def add_memory(self, memory_text, user_id="default_user", timestamp=None):
        """Add a processed memory."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
            
        memory = {
            "user_id": user_id,
            "memory": memory_text,
            "timestamp": timestamp
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
    
    def clear_all_data(self):
        """Clear all stored data (for fresh start)."""
        with open(self.memory_file, 'w') as f:
            json.dump([], f)
        with open(self.conversations_file, 'w') as f:
            json.dump([], f)

def populate_predefined_memories(memory, user_id="john"):
    """Populate memory with predefined conversations to simulate conversation history."""
    
    print("📝 Populating memory with predefined conversations...")
    
    # Clear existing data for fresh start
    memory.clear_all_data()
    
    # Predefined conversations (simulating past chat history)
    base_time = datetime.now() - timedelta(days=7)  # 7 days ago
    
    # Conversation 1: Personal introduction
    conv1 = [
        {"role": "user", "content": "Hi! I'm John, I live in Nuremberg, Germany."},
        {"role": "assistant", "content": "Nice to meet you John! Nuremberg is a beautiful city with rich history. How do you like living there?"},
        {"role": "user", "content": "I love it here! The old town is amazing, and I enjoy walking around the castle area."},
        {"role": "assistant", "content": "That's wonderful! The Nuremberg Castle is indeed spectacular. Do you have any hobbies or interests?"}
    ]
    
    # Conversation 2: Hobbies discussion
    conv2 = [
        {"role": "user", "content": "I'm really into mountain climbing and hiking. Just got back from the Bavarian Alps."},
        {"role": "assistant", "content": "Mountain climbing sounds exciting! The Bavarian Alps must offer some amazing trails. What was your favorite part of the trip?"},
        {"role": "user", "content": "The view from Zugspitze was breathtaking! I also love the physical challenge."},
        {"role": "assistant", "content": "Zugspitze is Germany's highest peak! That's quite an accomplishment. Do you climb regularly?"}
    ]
    
    # Conversation 3: Work/interests discussion  
    conv3 = [
        {"role": "user", "content": "I work in tech, specifically AI and machine learning. Always fascinated by how AI can solve complex problems."},
        {"role": "assistant", "content": "AI and ML are fascinating fields! What kind of projects do you work on?"},
        {"role": "user", "content": "Mostly computer vision and natural language processing. I'm particularly interested in how AI can understand human behavior."},
        {"role": "assistant", "content": "That's cutting-edge work! Computer vision and NLP are revolutionizing so many industries."}
    ]
    
    # Conversation 4: Local knowledge about Nuremberg
    conv4 = [
        {"role": "user", "content": "Do you know any good places to cool down in Nuremberg during summer?"},
        {"role": "assistant", "content": "Yes! Nuremberg has several great spots for hot weather. The Dutzendteich lake is perfect for swimming, and there are many beer gardens like Schönweiss with shaded areas."},
        {"role": "user", "content": "I've been to Dutzendteich! The swimming area is great. Any other recommendations?"},
        {"role": "assistant", "content": "The Wöhrder See is another beautiful lake option, and the old town has many fountains where you can cool off. The Hauptkirche area stays cooler due to the stone buildings."}
    ]
    
    # Store conversations with different timestamps
    conversations = [
        (conv1, base_time + timedelta(days=0)),
        (conv2, base_time + timedelta(days=1)),
        (conv3, base_time + timedelta(days=3)),
        (conv4, base_time + timedelta(days=5))
    ]
    
    stored_conversations = []
    for i, (conv, timestamp) in enumerate(conversations):
        conv_id = memory.add_conversation(conv, user_id, timestamp.isoformat())
        stored_conversations.append(conv_id)
        print(f"✅ Stored conversation {i+1} (ID: {conv_id})")
    
    # Create processed memories from conversations (simulate memory extraction)
    predefined_memories = [
        "John lives in Nuremberg, Germany and loves the old town and castle area",
        "John is passionate about mountain climbing and hiking, especially in the Bavarian Alps",
        "John has climbed Zugspitze (Germany's highest peak) and enjoys physical challenges",
        "John works in tech, specifically AI and machine learning with focus on computer vision and NLP",
        "John is interested in how AI can understand human behavior",
        "John knows about local Nuremberg spots like Dutzendteich lake, Wöhrder See, and beer gardens",
        "John has been swimming at Dutzendteich lake during hot weather"
    ]
    
    stored_memories = []
    for i, memory_text in enumerate(predefined_memories):
        memory_id = memory.add_memory(memory_text, user_id, (base_time + timedelta(days=i)).isoformat())
        stored_memories.append(memory_id)
        print(f"✅ Stored memory {i+1}: {memory_text[:50]}...")
    
    return stored_conversations, stored_memories

def main():
    # Load environment variables
    load_dotenv()
    
    # Configure Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in .env file")
        return
    
    genai.configure(api_key=api_key)
    
    print("📚 Milestone 3: Store Predefined Memories")
    print("=" * 60)
    
    try:
        # Initialize memory system
        print("🔄 Initializing memory system...")
        memory = SimpleMemory()
        print("✅ Memory system initialized")
        
        # Populate with predefined memories
        conv_ids, mem_ids = populate_predefined_memories(memory, user_id="john")
        
        print(f"\n📊 POPULATION COMPLETE:")
        print(f"✅ Stored {len(conv_ids)} conversations")
        print(f"✅ Stored {len(mem_ids)} memories")
        
        # Verify stored data
        print(f"\n🔍 VERIFICATION:")
        john_conversations = memory.get_conversations(user_id="john", limit=20)
        john_memories = memory.get_memories(user_id="john")
        stats = memory.get_stats()
        
        print(f"📋 Retrieved conversations: {len(john_conversations)}")
        print(f"📋 Retrieved memories: {len(john_memories)}")
        print(f"📋 System stats: {stats}")
        
        # Display sample memories
        print(f"\n💭 SAMPLE STORED MEMORIES:")
        for i, memory in enumerate(john_memories[:3]):
            print(f"{i+1}. {memory['memory']}")
        
        print(f"\n📝 SAMPLE CONVERSATION TOPICS:")
        topics = [
            "Personal introduction (Nuremberg resident)",
            "Hobbies discussion (mountain climbing, Alps)",
            "Work interests (AI, ML, computer vision)",
            "Local knowledge (cooling spots in Nuremberg)"
        ]
        for i, topic in enumerate(topics):
            print(f"{i+1}. {topic}")
        
        print("\n" + "=" * 60)
        print("📋 MILESTONE 3 ANALYSIS:")
        print("✅ Successfully populated memory with conversation history")
        print("✅ Created comprehensive user profile for 'john'")
        print("✅ Stored both raw conversations and processed memories")
        print("✅ Memory includes personal info, hobbies, work, and local knowledge")
        print("✅ Data is persistent and can be retrieved across sessions")
        print("📈 Next: We'll integrate this memory into chatbot responses!")
        
        return memory
        
    except Exception as e:
        print(f"❌ Error during memory population: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()