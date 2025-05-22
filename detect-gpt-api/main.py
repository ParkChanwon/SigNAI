from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import random
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List

# ---------------------------
# 1. 모델 로드 (서버 시작 시 1회만 실행)
# ---------------------------
print("[INFO] GPT-2 모델 로딩 중...")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
model.eval()
print("[INFO] 모델 로딩 완료!")

# ---------------------------
# 2. FastAPI 인스턴스 및 설정
# ---------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프론트엔드에서 접근 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

# ---------------------------
# 3. 로그 확률 계산 함수
# ---------------------------
def compute_log_prob(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
    return -outputs.loss.item() * inputs["input_ids"].size(1)

# ---------------------------
# 4. 텍스트 변형 함수
# ---------------------------
def perturb_text(text, num_perturbations=10):
    words = text.split()
    if len(words) < 2:
        return [text] * num_perturbations
    perturbed_texts = []
    for _ in range(num_perturbations):
        perturbed = words.copy()
        idx = random.randint(0, len(words) - 1)
        perturbed[idx] = "[MASK]"
        perturbed_texts.append(" ".join(perturbed))
    return perturbed_texts

# ---------------------------
# 5. 메인 API 엔드포인트 (/api/analyze)
# ---------------------------
@app.post("/api/analyze")
async def detect_endpoint(input: TextInput):
    original_log_prob = compute_log_prob(input.text)
    perturbed_texts = perturb_text(input.text)
    perturbed_log_probs = [compute_log_prob(pt) for pt in perturbed_texts]
    avg_perturbed_log_prob = sum(perturbed_log_probs) / len(perturbed_log_probs)
    discrepancy = original_log_prob - avg_perturbed_log_prob

    return JSONResponse({
        "input_text": input.text,
        "score": round(discrepancy, 4)  # 점수만 반환
    })

# ---------------------------
# 6. 질문 예시 제공 엔드포인트 (선택 사항)
# ---------------------------
def generate_questions(text: str) -> List[str]:
    questions = []
    if "이름" in text:
        questions.append("이 이름이 본인의 실명인가요?")
    if "안녕하세요" in text:
        questions.append("이 인사는 어떤 맥락에서 사용되었나요?")
    questions.append("이 문장을 다른 표현으로 바꿀 수 있다면 어떻게 표현할 수 있나요?")
    questions.append("이 문장의 목적은 무엇인가요?")
    return questions

# 기존 라우터 교체
@app.get("/api/questions")
async def get_questions(text: str):
    return { "questions": generate_questions(text) }
