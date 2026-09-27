import streamlit as st
import json

st.title("Searchantic")
st.write("Search your Claude conversation history")

uploaded_file = st.file_uploader("Upload your conversations.json file", type="json")

if uploaded_file is not None:
    data = json.load(uploaded_file)
    st.write(f"Loaded {len(data)} conversations")

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
    
    else:
        st.write("Enter a search term above to begin.")

else:
    st.info("Please upload your conversations.json file to get started.")