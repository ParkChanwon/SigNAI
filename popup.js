document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript(
    {
      target: { tabId: tab.id },
      func: () => document.body.innerText,
    },
    async (results) => {
      if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError.message);
        document.getElementById("result").innerText = "❌ 텍스트 추출 실패";
        return;
      }

      const extractedText = results[0].result;
      const score = await analyzeWithDetectGPT(extractedText);
      const resultBox = document.getElementById("result");

      if (score === null) {
        resultBox.innerText = "❌ 분석 실패";
        return;
      }

      drawBar(score); // 점수로 시각화
    }
  );
});

async function analyzeWithDetectGPT(text) {
  try {
    const response = await fetch("http://localhost:8000/detect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    const result = await response.json();
    return result.score;
  } catch (error) {
    console.error("API 호출 실패:", error);
    return null;
  }
}

// 점수를 막대그래프로 시각화
function drawBar(score) {
  const resultBox = document.getElementById("result");
  const percent = Math.min(Math.max(score * 100, 0), 100); // 0~100%로 변환
  const color = percent >= 50 ? "red" : "green";

  resultBox.innerHTML = `
    <p><strong>GPT 유사도 점수: ${percent.toFixed(1)}%</strong></p>
    <div style="width: 100%; background: #eee; height: 18px; border-radius: 9px; overflow: hidden;">
      <div style="width: ${percent}%; background: ${color}; height: 100%; transition: width 0.5s;"></div>
    </div>
  `;
}