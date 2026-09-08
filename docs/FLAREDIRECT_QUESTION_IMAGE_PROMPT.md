# FLAREdirect - Generated Question 이미지 생성 프롬프트 (3/3)

아래 코드 블록 전체를 이미지 생성 모델에 한 번에 입력한다. 앞의 masking 방식과 confidence 기반 검색 판단은 같지만, low-confidence span을 답으로 하는 명시적 질문을 별도의 LM 호출로 생성한다.

```text
Use case: scientific-educational
Asset type: Korean machine-learning blog infographic, image 3 of a three-image series

Create a polished Korean technical infographic explaining FLAREdirect with generated-question explicit query formulation. Use the same King Sejong execution scenario as the other images. Clearly show that token confidence first triggers retrieval, then low-confidence spans are extracted, and a separate LM call generates a question whose answer is that span. The generated question becomes the retrieval query.

CANVAS AND STYLE
- 16:9 landscape, 1920 x 1080.
- Match images 1/3 and 2/3 exactly in visual system: white background, navy-to-blue title bar, six horizontal numbered cards, bottom context panel, lower-right formula box, thick loop arrow.
- Academic Korean AI engineering slide style.
- Pale blue for LM generation, gray italic for temporary text, red/orange for low confidence, violet for question generation, green for documents and accepted output.
- Modern Korean sans-serif font, serif math font for equations, crisp vector icons, thin borders, minimal shadows.

TOP BAR
- Exact title: "FLAREdirect - Generated Question을 explicit query로 사용하는 방식"
- Subtitle line 1: "다음 문장의 low-confidence span을 찾고, 그 span이 답이 되는 질문을 생성하여 검색합니다."
- Subtitle line 2: "명시적인 질문으로 정보 요구를 표현한 뒤, 검색 문서를 근거로 임시 문장을 다시 생성합니다."
- Top-right badge: "3/3"

STEP 1 CARD
- Number: "1"
- Heading: "사용자 입력 및 최초 검색"
- Input, exact text: "세종대왕은 몇년도에 태어났으며 어떤 업적이 있어?"
- Equations: "q_1 = x" and "D_q1 = ret(q_1)"
- Green badge: "documents found: 3"
- Note: "최초에는 사용자 입력을 query로 사용"

STEP 2 CARD
- Number: "2"
- Heading: "검색 문서로 첫 문장 생성"
- LM icon.
- Model input: "LM([D_q1, x])"
- Accepted sentence, exact text:
  "세종대왕은 1397년에 태어났으며, 훈민정음을 창제하고 과학 기술과 농업 발전에 기여한 업적이 있습니다."
- Green check: "확정된 출력 y_<t에 추가"

STEP 3 CARD
- Number: "3"
- Heading: "임시 다음 문장 생성"
- Equation: "ŝ_t = LM([x, y_<t])"
- Note: "검색 문서 없이 미래 문장을 예측"
- Gray italic temporary sentence, exact text:
  "세종대왕의 업적은 오늘날에도 많은 이들에게 존경받고 있습니다."
- Show token probability badges and underline an uncertain span in red.
- Exact metric: "minimum token probability = 0.2076"
- Decision: "min P(w) < θ → retrieval triggered"

STEP 4 CARD
- Number: "4"
- Heading: "Low-confidence span 추출"
- Use a red selection/highlight icon.
- Show the temporary sentence again with the uncertain phrase highlighted.
- Extracted span label:
  "z = '세종대왕의 업적'"
- Add this universal prompt template in a small code-style box:
  "위 passage를 바탕으로, 'z'가 답이 되는 질문을 작성하라."
- Role note:
  "β보다 낮은 token이 포함된 연속 span을 추출"
- Formula: "z ∈ low-confidence spans(ŝ_t, β)"

STEP 5 CARD
- Number: "5"
- Heading: "질문 생성 후 검색"
- Divide into two sub-blocks.
- Sub-block A uses a small LM icon with a question-mark bubble.
- Label: "별도의 question-generation LM 호출"
- Generated explicit question, exact text:
  "세종대왕의 주요 업적에는 무엇이 있나요?"
- Equation: "q_t,z = qgen(x, y_≤t, z)"
- If multiple spans exist, add a tiny note:
  "span마다 질문을 하나씩 생성"
- Sub-block B uses a magnifying-glass icon.
- Retriever equation: "D_qt,z = ret(q_t,z)"
- Three schematic results:
  "문서 1  훈민정음 창제"
  "문서 2  측우기·앙부일구 등 과학 기술"
  "문서 3  농사직설과 농업 발전"
- Tiny note: "여러 질문의 검색 결과는 하나의 ranking list로 interleave"

STEP 6 CARD
- Number: "6"
- Heading: "검색 문서로 문장 재생성"
- LM icon.
- Model input equation: "s_t = LM([D_qt, x, y_<t])"
- Context blocks:
  1. Green: "질문 검색 결과 D_qt"
  2. Blue: "사용자 입력 x"
  3. Purple: "확정된 이전 출력 y_<t"
- Show the original temporary sentence in gray with a discard icon:
  "ŝ_t: 세종대왕의 업적은 오늘날에도 많은 이들에게 존경받고 있습니다."
- Label: "임시 문장 폐기"
- Regenerated sentence in green, exact text:
  "세종대왕은 훈민정음을 창제하고 측우기와 앙부일구 제작을 장려했으며, 농업 발전을 위해 농사직설을 편찬했습니다."
- Green check: "s_t만 최종 출력에 추가"

LOOP ARROW
- Thick blue arrow from Step 6 back to Step 3.
- Label: "다음 문장을 위해 Step 3부터 반복"
- Second line: "임시 생성 → confidence 검사 → span 질문 생성 → 검색"

BOTTOM CONTEXT PANEL
- Heading: "Context 및 문장 상태 관리 (FLAREdirect - Question Generation)"
- Rows:
  1. "사용자 입력 x - 항상 유지"
  2. "확정된 출력 y_<t - 계속 누적"
  3. "임시 문장 ŝ_t - span 추출 후 폐기"
  4. "검색 문서 D_qt - 현재 재생성 단계에서만 사용"
- Bullets:
  - "θ는 검색 발생 여부를 결정합니다."
  - "β는 질문으로 바꿀 low-confidence span을 선택합니다."
  - "각 span z에 대해 z가 답이 되는 질문 q_t,z를 생성합니다."
  - "여러 질문의 검색 결과를 합쳐 현재 문장을 재생성합니다."
  - "이전 검색 문서는 누적하지 않습니다."

BOTTOM FORMULA BOX
- Heading: "Explicit query 생성"
- Render:
  "z = spans with P(w) < β"
  "q_t,z = qgen(x, y_≤t, z)"
  "D_qt,z = ret(q_t,z)"
  "s_t = LM([D_qt, x, y_<t])"
- Small distinction label:
  "WHEN: min P(w) < θ"
  "WHAT: z가 답이 되는 generated question"

SCIENTIFIC ACCURACY CONSTRAINTS
- This is FLAREdirect, so retrieval is first triggered by token probability below θ, not by the LM emitting `[Search(query)]`.
- Extract low-confidence spans using β only after retrieval has been triggered.
- Generate a question that can be answered by each extracted span z.
- Question generation is an additional LM call; do not portray it as simple masking or string deletion.
- If there are multiple spans, generate multiple questions, retrieve for each, and interleave returned documents into one ranking list.
- Use the generated question, not the raw temporary sentence, as the explicit retrieval query.
- Discard the uncertain temporary sentence and append only the document-conditioned regenerated sentence.
- Do not permanently accumulate retrieved documents.
- Keep θ and β visually and semantically distinct.

AVOID
- No `[Search(query)]` marker and no FLAREinstruct behavior.
- No masked sentence as the final query in this image.
- Do not make the question-generation step happen before confidence checking.
- No photorealistic historical scene, decorative AI brain, 3D render, benchmark scores, logos, watermark, crossed arrows, malformed Korean, or invented formulas.

TEXT REQUIREMENT
Render every Korean phrase, equation, `ŝ_t`, `s_t`, `z`, `q_t,z`, `D_qt`, `P(w)`, `θ`, and `β` exactly and legibly. Prioritize information hierarchy and text correctness over decoration.
```

## 검수 체크리스트

- [ ] 우측 상단이 `3/3`인가?
- [ ] confidence 검사 후 low-confidence span `z`를 추출하는가?
- [ ] `z`가 답이 되는 명시적 질문을 별도 LM 호출로 생성하는가?
- [ ] 질문이 검색 query로 들어가는가?
- [ ] masking 결과가 query로 사용되지 않는가?
- [ ] 임시 문장을 폐기하고 문서 기반 재생성 문장만 채택하는가?
- [ ] 여러 span일 때 검색 결과를 interleave한다는 설명이 있는가?
