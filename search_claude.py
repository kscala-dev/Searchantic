import json

with open(r"C:\Users\Kathl\Downloads\conversations-000\conversations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Claude Conversation Search")
print("Type 'quit' to exit\n")

while True:
    search_term = input("Search: ").lower()
    if search_term == "quit":
        break

    results = 0
    for conversation in data:
        matches = []
        for message in conversation["chat_messages"]:
            content = message.get("content", "")
            if isinstance(content, list):
                text = " ".join(c.get("text", "") for c in content if c.get("type") == "text")
            else:
                text = str(content)
            if search_term in text.lower():
                index = text.lower().find(search_term)
                start = max(0, index - 100)
                end = min(len(text), index + 200)
                snippet = text[start:end].strip()
                matches.append(snippet)
        if matches:
            results += 1
            print(f"\nFound in: {conversation['name']}")
            print(f"Date: {conversation['created_at'][:10]}")
            print(f"Matches: {len(matches)}")
            for i, snippet in enumerate(matches, 1):
                print(f"\n  [{i}] ...{snippet}...")
            print("-" * 50)

    print(f"\n{results} conversation(s) found for '{search_term}'\n")
    