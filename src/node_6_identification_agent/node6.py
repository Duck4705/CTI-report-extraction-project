from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder
from prompt.prompt import Prompt_Identification_AT
from tool.Call_LLM import call_LLM
import json
import re
from datetime import datetime
import os

base_llm = call_LLM()
CHROMA_DIR = "./chroma_mitre_mpnet"
EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
OUTPUT_DIR = "./output"  # Thư mục lưu kết quả

# Load embedding model và vector database
print("🔹 [Node6] Đang tải embedding model và Chroma DB...")
embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding_model)

# Load reranker model
print("🔹 [Node6] Đang tải reranker model...")
reranker = CrossEncoder(RERANK_MODEL)

def clean_html(text):
    """Xóa tag HTML cho mô tả MITRE"""
    return re.sub(r"<.*?>", "", text or "")

def get_candidate_techniques(query, top_k=5):
    """
    Truy vấn vector database để lấy top_k kỹ thuật AT,
    sau đó rerank lại và trả về danh sách các kỹ thuật phù hợp nhất.
    
    Returns:
        str: Chuỗi JSON chứa thông tin các kỹ thuật AT candidate
    """
    # Retrieval: lấy top_k kết quả từ embedding similarity
    results = vectordb.similarity_search_with_score(query, k=top_k)
    
    if not results:
        return "[]"
    
    candidates = [(doc.page_content, doc.metadata, score) for doc, score in results]
    
    # Tính điểm rerank (cross-encoder) - chạy từng cặp một
    pairs = [[query, c[0]] for c in candidates]
    rerank_scores = [float(reranker.predict([pair])[0]) for pair in pairs]
    
    # Tạo danh sách kỹ thuật với điểm số
    techniques_info = []
    for i, (text, meta, emb_score) in enumerate(candidates):
        technique_id = meta.get('technique_id', 'Unknown')
        description = clean_html(text).replace("\n", " ").strip()
        
        techniques_info.append({
            "technique_id": technique_id,
            "description": description,
            "rerank_score": rerank_scores[i]
        })
    
    # Sắp xếp theo điểm rerank giảm dần
    techniques_info.sort(key=lambda x: x["rerank_score"], reverse=True)
    
    return json.dumps(techniques_info, ensure_ascii=False, indent=2)

def Node6(state: dict):
    mapped_sentences = state['mapped_sentences']
    all_AT = []
    results_simple = []  # Lưu kết quả đơn giản
    
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for idx, sentence in enumerate(mapped_sentences):
        # Lấy top 10 kỹ thuật AT từ vector database và rerank
        candidate_techniques = get_candidate_techniques(sentence, top_k=10)
        
        # Tạo prompt với thông tin các kỹ thuật candidate
        messages_system = SystemMessage(content=Prompt_Identification_AT)
        
        # Thêm thông tin các kỹ thuật candidate vào user message
        user_content = f"""Sentence to analyze:
{sentence}

Candidate MITRE ATT&CK Techniques (retrieved and reranked from vector database):
{candidate_techniques}

Based on the sentence and the candidate techniques above, identify which technique(s) best match the described behavior."""
        
        messages_user = HumanMessage(content=user_content)

        messages = [
            messages_system,
            messages_user
        ]
        
        identified_techniques = []
        try:
            response = base_llm.invoke(messages)
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            # Parse response - kỳ vọng là list hoặc "None"
            if response_content.strip().lower() != "none":
                # Thử parse JSON nếu là list
                try:
                    parsed = json.loads(response_content)
                    if isinstance(parsed, list) and len(parsed) > 0:
                        identified_techniques = parsed
                        all_AT.append(parsed)
                except:
                    # Nếu không parse được, thử extract từ text
                    # Tìm các pattern T#### trong response
                    techniques = re.findall(r'T\d{4}', response_content)
                    if techniques:
                        identified_techniques = techniques
                        all_AT.append(techniques)
            
            # Lưu kết quả đơn giản: chỉ id, sentence và AT
            results_simple.append({
                "id": idx + 1,
                "sentence": sentence,
                "AT": identified_techniques
            })
            
        except Exception as e:
            print(f"Error processing sentence {idx+1}: {e}")
            results_simple.append({
                "id": idx + 1,
                "sentence": sentence,
                "AT": [],
                "link": state['input']
            })
    
    # Tìm số thứ tự file tiếp theo
    existing_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('_AT_result.json')]
    if existing_files:
        # Lấy số lớn nhất từ tên file
        numbers = []
        for f in existing_files:
            match = re.match(r'(\d+)_AT_result\.json', f)
            if match:
                numbers.append(int(match.group(1)))
        next_number = max(numbers) + 1 if numbers else 1
    else:
        next_number = 1
    
    # Ghi kết quả ra file với số thứ tự
    output_file = os.path.join(OUTPUT_DIR, f"{next_number:02d}_AT_result.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_simple, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 [Node6] Kết quả đã được lưu vào: {output_file}")
            
    return {"AT": all_AT}
    