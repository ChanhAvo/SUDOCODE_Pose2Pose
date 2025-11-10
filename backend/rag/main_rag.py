import os
from preprocess import VietnameseSignLanguageData
from retriever import VSLKnowledgeBase
from chatbot import VietnameseSignLanguageChatbot
import config

os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
data_path = "VSL_DATA.json"  
chroma_path = "models/vsl_chroma_index"

data_handler = VietnameseSignLanguageData(data_path)
df = data_handler.load_data()
df = data_handler.prepare_data()
knowledge_base = VSLKnowledgeBase(df)


if os.path.exists(chroma_path) and os.listdir(chroma_path):
    print("Loading existing Chroma vectorstore...")
    knowledge_base.load(chroma_path)
else:
    print("Building Chroma vectorstore from scratch...")
    knowledge_base.build_vectorstore(chroma_path)
    
chatbot = VietnameseSignLanguageChatbot(knowledge_base)

print("\nVietnamese Sign Language Chatbot ready! Type 'exit' to quit.\n")

while True:
    user_input = input("Bạn: ").strip()
    if user_input.lower() in ["exit", "quit", "q"]:
        print("Tạm biệt!")
        break

    response = chatbot.ask(user_input)
    print(f"Bot: {response}\n")
