from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import random

# ---------------------------
# 1. 모델 로드 (서버 시작 시 1회만 실행)
# ---------------------------
print("[INFO] GPT-2 모델 로딩 중...")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
model.eval()
print("[INFO] 모델 로딩 완료!")

# ---------------------------
# 2. FastAPI 인스턴스 및 데이터 모델 정의
# ---------------------------
app = FastAPI()

class TextInput(BaseModel):
    text: str

# ---------------------------
# 3. 로그 확률 계산 함수
# ---------------------------
def compute_log_prob(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
    # log-prob = -loss * sequence length
    return -outputs.loss.item() * inputs["input_ids"].size(1)

# ---------------------------
# 4. 텍스트 변형 (간단하게 [MASK]를 랜덤 단어에 삽입)
# ---------------------------
def perturb_text(text, num_perturbations=10):
    words = text.split()
    if len(words) < 2:
        return [text] * num_perturbations  # 너무 짧으면 복제만
    perturbed_texts = []
    for _ in range(num_perturbations):
        perturbed = words.copy()
        idx = random.randint(0, len(words) - 1)
        perturbed[idx] = "[MASK]"
        perturbed_texts.append(" ".join(perturbed))
    return perturbed_texts

# ---------------------------
# 5. Detect-GPT 스타일 판별 함수
# ---------------------------
def detect_gpt(text, threshold=0.5):
    original_log_prob = compute_log_prob(text)
    perturbed_texts = perturb_text(text)
    perturbed_log_probs = [compute_log_prob(pt) for pt in perturbed_texts]
    avg_perturbed_log_prob = sum(perturbed_log_probs) / len(perturbed_log_probs)
    discrepancy = original_log_prob - avg_perturbed_log_prob

    print(f"[DEBUG] 원본 log-prob: {original_log_prob:.3f}")
    print(f"[DEBUG] 변형 평균 log-prob: {avg_perturbed_log_prob:.3f}")
    print(f"[DEBUG] Discrepancy: {discrepancy:.3f}")

    return discrepancy > threshold

# ---------------------------
# 6. FastAPI 엔드포인트
# ---------------------------
@app.post("/detect")
async def detect_endpoint(input: TextInput):
    original_log_prob = compute_log_prob(input.text)
    perturbed_texts = perturb_text(input.text)
    perturbed_log_probs = [compute_log_prob(pt) for pt in perturbed_texts]
    avg_perturbed_log_prob = sum(perturbed_log_probs) / len(perturbed_log_probs)
    discrepancy = original_log_prob - avg_perturbed_log_prob

    return {
        "input_text": input.text,
        "score": discrepancy  # float 값 반환
    }