import streamlit as st
import httpx

FASTAPI_URL = "http://localhost:8000/query"

st.set_page_config(
    page_title="Citi Latam Research Q&A",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ Citi Latam Internal Research Q&A")
st.markdown("Semantic search engine for Latam Corporate Strategy, FX, Credit, and Rates.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about Latam Markets..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare request to FastAPI backend
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Searching documents and synthesizing answer... 🔍")
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    FASTAPI_URL,
                    json={"query": prompt, "top_k": 3}
                )
                
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer provided.")
                sources = data.get("sources", [])
                
                # Format the response
                formatted_response = f"{answer}\n\n**Sources:**\n"
                
                # Deduplicate sources primarily by filename+page
                seen_sources = set()
                source_bullets = []
                for idx, src in enumerate(sources):
                    doc_name = src.get('source_file', src.get('source', 'Unknown Document'))
                    page = src.get('page', 'N/A')
                    date = src.get('date', 'Unknown Date')
                    identifier = f"{doc_name}_{page}"
                    
                    if identifier not in seen_sources:
                        seen_sources.add(identifier)
                        source_bullets.append(f"- *{doc_name}* (Page {page}, Date: {date})")
                
                if source_bullets:
                    formatted_response += "\n".join(source_bullets)
                else:
                    formatted_response += "- No direct sources cited in metadata."
                
                message_placeholder.markdown(formatted_response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": formatted_response})
                
            else:
                error_msg = f"Error from backend: {response.status_code} - {response.text}"
                message_placeholder.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
        except Exception as e:
            error_msg = f"Failed to connect to backend: {e}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
