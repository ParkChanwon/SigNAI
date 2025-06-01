
# 소프트웨어캡스톤디자인 — 생성형 AI 탐지를 위한 크롬 확장 프로그램
![image](https://github.com/user-attachments/assets/3893283b-57d1-4156-aef0-2d08e5f4fe7c)

---

##  프로젝트 소개

`생성형 AI 탐지를 위한 크롬 프로그램`은 소프트웨어캡스톤디자인을 수강하며 만든 **팀 프로젝트**입니다.  
핵심 목표는 

- 인간과 생성형 AI의 텍스트 차이 판별
- 간단한 접근성   
- 사용자의 편의성, 직관적인 UX/UI

---


![image](https://github.com/user-attachments/assets/222f9bf7-06cc-4e6b-87c0-c4968cbdde26)

초기 UX/UI 구상입니다.
크롬 확장 프로그램으로 하였기 때문에 작은 화면에서의 입력 중심 구조를 기반으로 하였습니다.  
</br>

![image](https://github.com/user-attachments/assets/bad95b1e-84e7-4028-bced-44769e903481)
![image](https://github.com/user-attachments/assets/750b6c52-f447-427e-9c95-925b3855fafb)
![image](https://github.com/user-attachments/assets/b8678002-36fe-4254-b1c7-5748b07cf4ec)

초기 구상된 이미지를 가지고 만들었던 UX/UI입니다. 
간단하게 검사할 문장을 입력하게 되면 AI 탐지 결과에서 AI 유사도를 보여주며 유사도에 따라 인간 혹은 AI일 가능성을 알려줍니다.
생성형 AI 기반으로 추가적인 검증 질문을 통해 텍스트에 대한 목적 등을 학습할 수 있습니다.

</br>

![image](https://github.com/user-attachments/assets/674572f6-143b-4d7b-bdb2-f7fe68ee3473)
![image](https://github.com/user-attachments/assets/a8e49c97-9d37-44b7-bb0e-d706796981e4)
![image](https://github.com/user-attachments/assets/92bf7d7d-00e5-42e0-982f-d029cbf873a9)
![image](https://github.com/user-attachments/assets/84e79754-9659-45c1-9957-925365977cd6)

최종 UX/UI이며 입력 -> 분석 -> 결과 -> 질문의 직관적인 단계를 구성하였고, 사용자를 위한 다크 모드, 드래그를 통한 분석 등의 편의 기능을 추가하였습니다.

</br>
![image](https://github.com/user-attachments/assets/1d7aac34-8ada-4c08-a466-dfaf0fdd4e5c)

이전에 분석했던 텍스트와 유사도, 시간이 남아있는 검사 기록을 확인해볼 수 있습니다.

## 핵심 API

---
![image](https://github.com/user-attachments/assets/afa5a045-2a7f-4ba8-8351-17f932eb006d)
![image](https://github.com/user-attachments/assets/bef9c54b-9cf2-4ba9-a3a9-515818b054a1)

</br>
Detect-GPT는 텍스트 분석 API로 문장을 분석하여 원문과 변형 문장의 로그 확률 차이를 계산하여 AI 유사도 점수를 산출해낼 수 있습니다.
정규화를 통해 문장의 AI 생성 가능성을 직관적인 수치로 표현하였습니다.

질문 생성을 하는 API로 AI 탐지 결과를 바탕으로 해당 문장을 검토할 수 있는 질문을 생성하고, 의도 정보 등을 점검하며 단순 점수만 확인하는 것이 아닌 추가적인 질문을 통해 사용자에게 사고를 유도하였습니다.

</br>

![image](https://github.com/user-attachments/assets/241fe916-3f5e-4dc9-8188-0b36e47bdd56)
로그 점수 기반의 유사도 분석 결과를 정규화를 통해 유사도를 나타내는 부분에서 점수가 0% 혹은 100%로만 출력되는 문제가 발생했고, 이에 원인을 찾아보니 정규화 기준이 명확하지 않아 범위를 너무 좁게 잡은 것이 문제인 것을 확인하였습니다.
</br>
![image](https://github.com/user-attachments/assets/58d3528b-79b5-4586-b6a5-ef5a87c0e620)
인간의 텍스트와 생성형 AI 텍스트를 반복적인 검사를 통해 Discrepancy가 어느정도에 포진해있는지 확인하여 분석할 수 있었으며 이를 통해 어느정도 신뢰도 있는 유사도를 제공할 수 있게 되었습니다.


##시연 영상
</br>
[![시연 영상](https://img.youtube.com/vi/6MWHkbroRoQ/0.jpg)](https://youtu.be/6MWHkbroRoQ)


