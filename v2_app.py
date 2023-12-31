# -*- coding: utf-8 -*-
"""v2_chat with PDF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yx42ZJDmhf_mUVPYtQ3t9XIcF3ar8lfL
"""

## https://medium.com/@johnthuo/chat-with-your-pdf-using-langchain-f-a-i-s-s-and-openai-to-query-pdfs-e7bfde086155
## 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

#pip install python-dotenv PyPDF2 streamlit langchain openai tiktoken faiss-cpu

##from dotenv import load_dotenv
from dotenv import load_dotenv,find_dotenv
import os
from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import openai


# Load environment variables
load_dotenv()

openai.api_key="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"
os.environ["OPENAI_API_KEY"] = "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"

openai.api_key="sk-"

def process_text(text):
    # Split the text into chunks using Langchain's CharacterTextSplitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Convert the chunks of text into embeddings to form a knowledge base
    embeddings = OpenAIEmbeddings()
    knowledgeBase = FAISS.from_texts(chunks, embeddings)

    return knowledgeBase

# Commented out IPython magic to ensure Python compatibility.
#  %%writefile /content/my_app.py


from dotenv import load_dotenv,find_dotenv
import os
from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import openai

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = "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"

def main():
      st.title("Load your PDF Document 💬")

      pdf = st.file_uploader('Upload your PDF Document', type='pdf')

      if pdf is not None:
          pdf_reader = PdfReader(pdf)
          # Text variable will store the pdf text
          text = ""
          for page in pdf_reader.pages:
              text += page.extract_text()


          def process_text(text):
            openai.api_key="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"
            # Split the text into chunks using Langchain's CharacterTextSplitter
            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text)

            # Convert the chunks of text into embeddings to form a knowledge base
            embeddings = OpenAIEmbeddings()
            knowledgeBase = FAISS.from_texts(chunks, embeddings)

            return knowledgeBase

          # Create the knowledge base object
          knowledgeBase = process_text(text)
          query = st.text_input('Ask a question to the PDF')
          cancel_button = st.button('Cancel')

          if cancel_button:
              st.stop()

          if query:
              docs = knowledgeBase.similarity_search(query)
              llm = OpenAI()
              chain = load_qa_chain(llm, chain_type='stuff')

              with get_openai_callback() as cost:
                  response = chain.run(input_documents=docs, question=query)
                  print(cost)

              st.write(response)
if __name__ == "__main__":
   main()
