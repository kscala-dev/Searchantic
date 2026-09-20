import streamlit as st
import json

@st.cache_data
def load_data():
    with open(r"C:\Users\Kathl\Downloads\conversations-000\conversations.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

st.title("Claude Conversation Search")
st.write(f"Searching across {len(data)} conversations")

search_term = st.text_input("Search:")

if search_term:
    results = []
    for conversation in data:
        matches = []
        for message in conversation["chat_messages"]:
            content = message.get("content", "")
            if isinstance(content, list):
                text = " ".join(c.get("text", "") for c in content if c.get("type") == "text")
            else:
                text = str(content)
            if search_term.lower() in text.lower():
                index = text.lower().find(search_term.lower())
                start = max(0, index - 100)
                end = min(len(text), index + 200)
                snippet = text[start:end].strip()
                matches.append(snippet)
        if matches:
            results.append((conversation, matches))

    st.write(f"**{len(results)} conversation(s) found**")

    for conversation, matches in results:
        with st.expander(f"{conversation['name']} — {conversation['created_at'][:10]}"):
            for i, snippet in enumerate(matches, 1):
                st.markdown(f"**[{i}]** ...{snippet}...")