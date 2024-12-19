from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)

# create a chain of the model and prompt operations
chain = prompt | model

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def add_to_chat_history(question, answer):
    st.session_state.chat_history.append({'role': 'user', 'message': question})
    st.session_state.chat_history.append({'role': 'bot', 'message': answer})

def handle_conversation():
    st.title("Chat Interface")
    context = ""
    
    for entry in st.session_state.chat_history:
      print(entry)

    message = st.text_area("Message", placeholder="Ask something...")

    if st.button("Chat"):
        if not message.strip():
            st.error("Please enter a message")
            return
        
        try:
            with st.spinner("Running flow..."):
                prompt = message

            response = chain.invoke({"context": context, "question": prompt})

            st.markdown(f'<div style="text-align: right; background-color: #5eb1b7; border-radius: 10px; padding: 10px; margin: 5px 0;">You:</br>{prompt}</div>', unsafe_allow_html=True)
            
            st.markdown(f'<div style="text-align: left; background-color: #f1ab86; border-radius: 10px; padding: 10px; margin: 5px 0;">Bot:</br>{response}</div>', unsafe_allow_html=True)

            context += f"\nUser: {prompt}\nAI: {response}"
            add_to_chat_history(prompt, response)
        except Exception as e:
            st.error(str(e))
    ######################
    #context = ""
    #print("Welcome to the AI Chatbot! Type 'exit' to quit.")

    #while True: 
    #    user_input = input("You: ")
    #    if user_input.lower() == "exit":
    #        break

        #result = chain.invoke({"context": context, "question": user_input})
        #print("Bot: ", result)
        #context += f"\nUser: {user_input}\nAI: {result}"

if __name__ == "__main__":
    handle_conversation()