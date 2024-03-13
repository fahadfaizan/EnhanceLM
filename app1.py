import streamlit as st 
import os 
from dotenv import load_dotenv
import google.generativeai as gen_ai
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.memory import ChatMessageHistory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from IPython.display import display
from IPython.display import Markdown
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
# st.set_page_config(
#     page_title="Chat with HOPE",
#     page_icon ="Brain",
#     layout="centered",
# )

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

gen_ai.configure(api_key = GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')



def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# def get_docs():
#     loader = CSVLoader(file_path ="psychological_conversations.xls",encoding = 'utf8')
#     documents = loader.load()
#     return documents

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    template =  """As a world-class therapist working in a college, your job is to be as friendly as possible to the students and engage in conversational interactions with them to learn more about them. To achieve this, please adhere to the following rules:

    1. Base your responses on similar text from the past that I provide you.
    2. If past texts are irrelevant, try and respond with a friendly relavant answer.
    3. Keep the conversation open by engaging interactively. Don't just listen; ask questions to keep the conversation going.
    4. Be supportive and take a realistic approach. Avoid saying negative things.
    5. Ask normal questions; avoid questions that require effort from the student to answer, such as 'What would you like to talk about?' or 'What do you want to do?'

    The chat should not feel like a therapy session but rather like talking to a friend.

    Here is the message from the student:
    {context}
    And here are the past text conversations:
    {question}

    """
    model = ChatGoogleGenerativeAI(model ='gemini-pro',temperature=0.3)
    prompt = PromptTemplate(template=template , input_variables=["context","question"])
    chain = load_qa_chain(model,chain_type="stuff",prompt=prompt)
    return chain

def user_input(user_question):
    new_db = FAISS.load_local("faiss_index",embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents":docs,"question":user_question}
        , return_only_outputs=True 
    )
    print(response)
    st.write("Reply :",response["output_text"])

def main():
    st.set_page_config("Chat PDF")
    st.header("Hope AI your daily companion💁")
    user_question = st.text_input("Ask a Question from the PDF Files")
    raw_text=get_pdf_text(['attention.pdf'])
    text_chunks=get_text_chunks(raw_text)
    get_vector_store(text_chunks)
    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")


if __name__ == "__main__":
    main()

# embeddings = GoogleGenerativeAIEmbeddings(model = 'models/embedding-001')
# db = FAISS.from_documents(documents,embedding = embeddings)  



# prompt = PromptTemplate(
#     input_variables = ["message","best_practice"],
#     template = template
# )

# llm = ChatGoogleGenerativeAI(model="gemini-pro")
# history = ChatMessageHistory()
# chain = LLMChain(llm = llm, prompt = prompt)



# def retrieve_info(query):
#     similar_response = db.similarity_search(query,3)
#     contents = [doc.page_content for doc in similar_response]
#     return contents


# def generate_response(message):
#     best_practice = retrieve_info(message)
#     response = chain.run(message = message, best_practice = best_practice)
#     history.add_user_message(message)
#     history.add_ai_message(response)
#     return response

# def translate_role_for_streamlit(user_role):
#     if user_role == "model":
#         return "assistant"
#     else:
#         return user_role


# if "chat_session" not in st.session_state:
#     st.session_state.chat_session = model.start_chat(history=[])


# st.title("Chat with HOPE")


# for message in st.session_state.chat_session.history:
#     with st.chat_message(translate_role_for_streamlit(message.role)):
#         st.markdown(message.parts[0].text)

# user_prompt = st.chat_input("Talk with Hope ...")
# if user_prompt:
#     st.chat_message("user").markdown(user_prompt)
#     # gemini_response = st.session_state.chat_session.send_message(user_prompt)
#     gemini_response = generate_response(user_prompt)
#     with st.chat_message('assistant'):
#         st.markdown(gemini_response)

