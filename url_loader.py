
dhiki = "chiki"

if __name__ == "__main__":

    import os
    import openai

    openai.api_key  = os.environ['OPENAI_API_KEY']
    # _ = load_dotenv(find_dotenv()) # read local .env file

    knowledge_base_links = [
        'https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest/chapter-1/authority.html#a1_1_0',
        'https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest/chapter-1/qualifying-period.html#a1_2_0',
        'https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest/chapter-1/extend-qualifying-period.html#a1_3_0',
        'https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest/chapter-1/benefit-period-structure.html#a1_4_0',
        'https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest/chapter-1/extend-benefit-period.html#a1_5_0',
        'https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest/chapter-1/disqualification.html#a1_6_0',
        'https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest/chapter-1/disentitlement.html#a1_7_0',
        'https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest/chapter-1/waiting-period.html#a1_8_0',
        'https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest/chapter-1/payment-benefit.html#a1_9_0'
    ]

    from langchain.document_loaders import UnstructuredURLLoader
    loaders = UnstructuredURLLoader(urls=knowledge_base_links)
    data = loaders.load()

    # Text Splitter
    from langchain.text_splitter import CharacterTextSplitter

    text_splitter = CharacterTextSplitter(separator='\n', 
                                        chunk_size=1000, 
                                        chunk_overlap=200)


    docs = text_splitter.split_documents(data)

    import pickle
    import faiss
    from langchain.vectorstores import FAISS
    from langchain.embeddings import OpenAIEmbeddings

    embeddings = OpenAIEmbeddings()

    vectorStore_openAI = FAISS.from_documents(docs, embeddings)

    from langchain.chat_models import ChatOpenAI
    llm = ChatOpenAI(model_name='gpt-4', temperature=0)

    from langchain.chains import RetrievalQA
    qa_chain = RetrievalQA.from_chain_type(
                llm,
                retriever=vectorStore_openAI.as_retriever(),
                return_source_documents=True
                )

    question = "How long should I get the maternity benefits for?"
    question2 = "How long is the parental benefit period when child hospitalized?"

    result = qa_chain({"query": question2})
    print('Answer: ', result['result'])
    print('Source: ', result["source_documents"][0])