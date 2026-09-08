# FLAREdirect - Masked Sentence 이미지 생성 프롬프트 (2/3)

아래 코드 블록 전체를 이미지 생성 모델에 한 번에 입력한다. 사용자가 제공한 실제 실행 로그의 Step 4를 중심 예시로 사용한다.

```text
Use case: scientific-educational
Asset type: Korean machine-learning blog infographic, image 2 of a three-image series

Create a polished Korean technical infographic explaining FLAREdirect with masked-sentence implicit query formulation. Use the supplied real execution trace about King Sejong. Show initial retrieval, temporary next-sentence generation, token-confidence checking, no-retrieval acceptance, masking, retrieval, disposal of the uncertain temporary sentence, and regeneration with current documents.

CANVAS AND STYLE
- 16:9 landscape, 1920 x 1080.
- Match image 1/3: white background, dark navy-to-blue title bar, six horizontal numbered cards, bottom context panel, lower-right formula box, thick loop arrow.
- Academic vector infographic with modern Korean typography.
- Pale blue for LM generation, gray italic for temporary sentences, red/orange for uncertainty, green for retrieved documents and accepted output.
- Crisp icons, thin borders, subtle shadows, generous padding, no decorative clutter.

TOP BAR
- Exact title: "FLAREdirect - Masked Sentence를 implicit query로 사용하는 방식"
- Subtitle line 1: "다음 문장을 임시로 생성한 뒤, 하나라도 확률이 낮은 token이 있으면 해당 token을 제거해 검색합니다."
- Subtitle line 2: "검색 분기에서는 임시 문장을 폐기하고, 현재 검색 문서를 근거로 문장을 다시 생성합니다."
- Top-right badge: "2/3"

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
- Input: "LM([D_q1, x])"
- Accepted sentence, exact text:
  "세종대왕은 1397년에 태어났으며, 훈민정음을 창제하고 과학 기술과 농업 발전에 기여한 업적이 있습니다."
- Green check: "확정된 출력 y_<t에 추가"

STEP 3 CARD
- Number: "3"
- Heading: "임시 다음 문장 생성 및 검사"
- Equation: "ŝ_t = LM([x, y_<t])"
- Label: "검색 문서 없이 미래 문장을 예측"
- Gray italic temporary sentence, exact text:
  "또한, 그는 음악과 의학 분야에서도 많은 발전을 이끌었습니다."
- Green condition: "모든 token의 P(w) ≥ θ"
- Green result: "no retrieval → ŝ_t 채택"
- Small second example, exact text:
  "그의 통치 아래에서 백성의 삶의 질이 크게 향상되었습니다."
- Small green label: "step 3: no retrieval"

STEP 4 CARD
- Number: "4"
- Heading: "Low-confidence token 감지"
- Warning icon.
- Gray italic temporary sentence, exact text:
  "세종대왕의 업적은 오늘날에도 많은 이들에게 존경받고 있습니다."
- Draw small probability badges under tokens; underline uncertain tokens in red.
- Exact metric: "minimum token probability = 0.2076"
- Decision: "min P(w) < θ"
- Bold result: "retrieval triggered"
- Small parameter box: "예시 설정: θ = 0.4, β = 0.4"

STEP 5 CARD
- Number: "5"
- Heading: "Masking 후 검색"
- Formula: "q_t = mask_β(ŝ_t)"
- Explain: "P(w) < β인 token을 임시 문장에서 제거"
- Show the actual implementation query verbatim, preserving the awkward spacing:
  "세종대왕의 업적은 오늘날에도 많은들에게경받고 있습니다."
- Label: "실제 masked search query"
- Retriever equation: "D_qt = ret(q_t)"
- Green badge: "documents found: 3"
- Role box:
  "θ: 검색할지 결정"
  "β: query에서 제거할 token 결정"

STEP 6 CARD
- Number: "6"
- Heading: "검색 문서로 문장 재생성"
- Equation: "s_t = LM([D_qt, x, y_<t])"
- Three context blocks:
  1. Green: "현재 검색 문서 D_qt"
  2. Blue: "사용자 입력 x"
  3. Purple: "확정된 이전 출력 y_<t"
- Show the temporary sentence in gray with a red strikethrough/discard icon:
  "ŝ_t: 세종대왕의 업적은 오늘날에도 많은 이들에게 존경받고 있습니다."
- Label: "임시 문장 폐기"
- Show regenerated sentence in a green accepted box, exact text:
  "세종대왕은 또한 국방과 정치 개혁에도 많은 기여를 하여 조선의 국력을 강화했습니다."
- Green check: "s_t만 최종 출력에 추가"

LOOP ARROW
- Thick blue arrow from Step 6 back to Step 3.
- Label: "다음 문장을 위해 Step 3부터 반복"
- Second line: "임시 생성 → confidence 검사 → 필요할 때만 검색"

BOTTOM CONTEXT PANEL
- Heading: "Context 및 문장 상태 관리 (FLAREdirect - Masking)"
- Rows:
  1. "사용자 입력 x - 항상 유지"
  2. "확정된 출력 y_<t - 계속 누적"
  3. "임시 문장 ŝ_t - 검사 후 채택 또는 폐기"
  4. "검색 문서 D_qt - 현재 재생성 단계에서만 사용"
- Bullets:
  - "모든 token이 θ 이상이면 검색 없이 ŝ_t를 확정합니다."
  - "하나라도 θ보다 낮으면 mask_β(ŝ_t)를 query로 검색합니다."
  - "검색 분기에서는 ŝ_t를 답변에 넣지 않고 재생성한 s_t만 확정합니다."
  - "이전 검색 문서는 누적하지 않습니다."

BOTTOM FORMULA BOX
- Heading: "문장 선택 규칙"
- Piecewise rule:
  "y_t = ŝ_t,  if all P(w) ≥ θ"
  "y_t = s_t = LM([D_qt, x, y_<t]),  otherwise"
- Query formula: "q_t = mask_β(ŝ_t)"

SCIENTIFIC ACCURACY CONSTRAINTS
- Initial retrieval uses q_1 = x.
- Later temporary sentences are generated without retrieved documents: ŝ_t = LM([x, y_<t]).
- θ triggers retrieval; β determines which tokens are removed from the query.
- If all probabilities are at least θ, accept ŝ_t without retrieval.
- On the low-confidence branch, use the masked temporary sentence only as a query, discard ŝ_t, retrieve D_qt, regenerate s_t, and append only s_t.
- Never append both ŝ_t and s_t.
- Do not feed ŝ_t into accepted conversation history before regeneration.
- Retrieved documents are current-step context, not permanent memory.
- The malformed-looking masked query is intentional and must not be corrected.

AVOID
- No `[Search(query)]`, no FLAREinstruct, and no generated-question path.
- Do not depict retrieval on every sentence; show the two no-retrieval examples.
- No photorealistic historical scene, decorative AI brain, 3D render, logos, watermark, benchmark score, crossed arrows, or invented formulas.

TEXT REQUIREMENT
Render all Korean text, `ŝ_t`, `s_t`, `q_t`, `D_qt`, `P(w)`, `θ`, and `β` exactly and legibly.
```

## 검수 체크리스트

- [ ] 우측 상단이 `2/3`인가?
- [ ] 실제 Step 4의 임시 문장과 `0.2076`이 보이는가?
- [ ] 실제 masked query의 붙어 있는 글자까지 그대로인가?
- [ ] `θ`와 `β`의 역할이 구분됐는가?
- [ ] 임시 문장 `ŝ_t`를 폐기하고 재생성한 `s_t`만 채택하는가?
- [ ] `[Search(query)]`와 question generation이 등장하지 않는가?

