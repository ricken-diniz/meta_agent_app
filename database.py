import os
from dotenv import load_dotenv
load_dotenv()
# from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain.docstore.document import Document



class VectorDataBase:
    def __init__(self):
        api_key = os.getenv("GPT_KEY")
        self.embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small', openai_api_key=api_key)
        if not os.path.exists("./meu_banco"):
            print("O diretório './meu_banco' não existe... realizando a indexação")
            # divide_texto = divide_texto(texto_completo_lido)
            self.write('init')
        else:
            print("O diretório './meu_banco' já existe. Pulando a criação do banco vetorial.")
        
    # Cria o banco de dados vetorial, gerando os embeddings dos documentos
    def write(self, content):
        print(f">>> REALIZANDO INDEXAÇÃO DOS CHUNKS NO BANCO VETORIAL")
        document = [Document(page_content=content)]
        # Cria o banco de dados vetorial, gerando os embeddings dos documentos
        # Adicionar os chunks no banco em lote
        Chroma.from_documents(document, collection_name="nome_colecao", embedding=self.embeddings_model, persist_directory="./meu_banco")
        
    def conecta_banco_vetorial_pre_criado(self):
        vector_store_from_client = Chroma(
            persist_directory="./meu_banco",
            collection_name="nome_colecao",
            embedding_function=self.embeddings_model,
        )
        return vector_store_from_client