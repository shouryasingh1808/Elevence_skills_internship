import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db

st.title("CUSTOMER SERVICE CHATBOT 🤖")

btn = st.button("Create Knowledgebase")
if btn:
    with st.spinner("Knowledgebase ban raha hai..."):
        create_vector_db()
    st.success("Knowledgebase ready hai!")


# Chain ko baar-baar load na karna pade, isliye cache kar liya
@st.cache_resource
def load_chain():
    return get_qa_chain()


question = st.text_input("Question: ")

if question:
    try:
        chain = load_chain()
        response = chain.invoke({"query": question})

        st.header("Answer")
        st.write(response["result"])
    except Exception as e:
        st.error(f"Pehle 'Create Knowledgebase' button dabao. Error: {e}")