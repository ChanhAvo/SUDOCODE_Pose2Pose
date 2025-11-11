from retriever import VSLKnowledgeBase
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from typing import List, Dict, Tuple
from langchain_classic.chains import RetrievalQA
from langchain_classic.docstore.document import Document
class VietnameseSignLanguageChatbot:
    def __init__(self, knowledge_base: VSLKnowledgeBase):
        self.knowledge_base = knowledge_base
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.retriever = knowledge_base.retriever
        self.vectorstore = knowledge_base.vectorstore
        self.relevance_threshold = 0.7

        template = """
        Bạn là trợ lý chuyên về Ngôn ngữ Ký hiệu Việt Nam (VSL).
        Chỉ sử dụng thông tin trong ngữ cảnh dưới đây để trả lời.
        KHÔNG tự suy luận hay thêm thông tin không có trong dữ liệu.

        Ngữ cảnh:
        {context}

        Câu hỏi của người dùng:
        {question}
        

        Yêu cầu trả lời:
        - Chỉ dựa vào dữ liệu trên.
        - Trình bày các thông tin theo định dạng:
          1. **Từ**:
          2. **Mô tả (Nghĩa)**:
          3. **Từ loại**:
          4. **Mã video**:
        - Nếu có các từ trùng lặp với nhau, liệt kê tất cả và đánh số thứ tự.
        - Nếu không tìm thấy thông tin phù hợp, trả lời: "Tôi không tìm thấy thông tin cho từ này trong cơ sở dữ liệu."
        
        """
        

        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=template
        )
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": self.prompt}
        )

        # Keywords for in-domain detection
        self.allowed_keywords = ["vsl", "ngôn ngữ ký hiệu", "ký hiệu", "vietnamese sign language", "từ", "tay", "cử chỉ", "diễn tả"]

    def is_in_domain(self, query: str) -> bool:
        q_lower = query.lower()
        return any(keyword in q_lower for keyword in self.allowed_keywords)
    

    def ask(self, query: str):
        if not self.is_in_domain(query):
            return "Tôi không thể trả lời các câu hỏi không liên quan. Vui lòng hỏi về Ngôn ngữ Ký hiệu Việt Nam (VSL)."

        docs_with_scores: List[Tuple[Document, float]] = self.vectorstore.similarity_search_with_relevance_scores(query, k=3)
        # Check relevance
        if not docs_with_scores or docs_with_scores[0][1] < self.relevance_threshold:
            print("Low relevance or no docs. Using n-gram keyword fallback.")
            #Keyword fallback
            kb_results = self.knowledge_base.keyword_search(query, n=2, top_k=3)
            if not kb_results:
                return "Tôi không tìm thấy thông tin cho từ này trong cơ sở dữ liệu."
            grouped = {}
            for overlap, row in kb_results:
                word = row.get("word", "")
                grouped.setdefault(word, []).append(row)

            #Context for LLM
            context_parts = []
            for word, rows in grouped.items():
                for i, row in enumerate(rows, 1):
                    context_parts.append(
                        f"{i}. **Từ**: {row.get('word', '')}\n"
                        f"**Mô tả (Nghĩa)**: {row.get('description', '')}\n"
                        f"**Từ loại**: {row.get('tl', '')}\n"
                        f"**Mã video**: {row.get('_id', '')}"
                    )
            context = "\n\n".join(context_parts)
            final_prompt = self.prompt.format(context=context, question=query)
            response = self.llm.invoke(final_prompt).content
        else:
            # Use chain 
            response = self.chain.run(query)
        if not response or "không tìm thấy" in response.lower():
            return "Tôi không tìm thấy thông tin cho từ này trong cơ sở dữ liệu."
        return response