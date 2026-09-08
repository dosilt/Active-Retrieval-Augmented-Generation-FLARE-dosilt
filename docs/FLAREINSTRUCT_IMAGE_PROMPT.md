# FLAREinstruct 이미지 생성 프롬프트 (1/3)

아래 코드 블록 전체를 이미지 생성 모델에 한 번에 입력한다. 다른 두 이미지와 한 세트로 사용할 수 있도록 16:9 강의 슬라이드형 디자인을 명시했다.

```text
Use case: scientific-educational
Asset type: Korean machine-learning blog infographic, image 1 of a three-image series

Create a polished Korean technical infographic explaining FLAREinstruct from the paper "Active Retrieval Augmented Generation". The image must explain that the language model itself explicitly generates `[Search(query)]` when it decides that more information is needed. Use the King Sejong example specified below.

CANVAS AND STYLE
- 16:9 landscape, 1920 x 1080, crisp high resolution.
- White background with a dark navy-to-blue title bar.
- Six tall rounded process cards arranged horizontally, connected by blue right arrows.
- Wide context-management panel across the lower left and center.
- Compact formula box in the lower right.
- Thick blue loop arrow from Step 6 back to Step 3.
- Academic vector infographic, similar to a carefully designed Korean AI engineering lecture slide.
- Modern Korean sans-serif font similar to Pretendard or Noto Sans KR; serif math font for equations only.
- Pale blue LM cards, pale purple search-instruction card, pale green retrieval card.
- Consistent numbered circles, thin borders, minimal shadows, generous padding.

TOP BAR
- Exact title: "FLAREinstruct - 모델이 직접 [Search(query)]를 생성하는 방식"
- Exact subtitle line 1: "추가 정보가 필요하다고 판단하면 검색 지시를 직접 출력하고, 검색 문서를 context에 추가하여 생성을 이어갑니다."
- Exact subtitle line 2: "새 검색이 발생하면 이전 검색 문서는 누적하지 않고 현재 검색 결과로 교체합니다."
- Top-right rounded badge: "1/3"

STEP 1 CARD
- Number: "1"
- Heading: "사용자 입력 x"
- User icon.
- Speech box, exact text: "세종대왕은 몇년도에 태어났으며 어떤 업적이 있어?"
- Math label below: "x"

STEP 2 CARD
- Number: "2"
- Heading: "현재 context로 생성 시작"
- Robot icon labeled "Language Model (Instruct-tuned LM)".
- Model input equation: "y_t = LM([x, y_<t])"
- Initial-state note: "y_<t = ∅, D_q = ∅"
- Model output example: "세종대왕은 조선의 제4대 왕으로, ..."
- Bottom note: "아직 검색 문서 없음"

STEP 3 CARD
- Number: "3"
- Heading: "추가 정보 필요 → 검색 지시 생성"
- Same LM icon.
- Model output example on two lines:
  "세종대왕은 조선의 제4대 왕으로,"
  "[Search(세종대왕 출생 연도와 주요 업적)]"
- Render `[Search(세종대왕 출생 연도와 주요 업적)]` in vivid blue monospace text inside the generated text stream.
- Explanation: "모델이 추가 정보가 필요하다고 판단하면 [Search(query)]를 직접 출력"
- Formula: "q_t = 모델이 직접 생성한 Search query"
- Make it visually clear that generation pauses at this marker.

STEP 4 CARD
- Number: "4"
- Heading: "검색 수행"
- Large magnifying-glass icon labeled "검색 시스템 (e.g., Web Search)".
- Query box, exact text: "q_t = '세종대왕 출생 연도와 주요 업적'"
- Result equation: "D_qt = ret(q_t)"
- Three schematic document rows:
  "문서 1  세종대왕 - 1397년 출생"
  "문서 2  훈민정음 창제"
  "문서 3  측우기·농사직설 등 과학과 농업"
- These are schematic snippets, not literal quotations.

STEP 5 CARD
- Number: "5"
- Heading: "검색 결과를 context에 추가하여 생성 재개"
- LM icon.
- Model input equation: "y_t = LM([D_qt, x, y_<t])"
- Three stacked context blocks:
  1. Green: "검색된 문서 D_qt - 이번 검색 결과"
  2. Blue: "사용자 입력 x"
  3. Purple: "이전까지의 생성 결과 y_<t"
- Model output example, exact text:
  "세종대왕은 1397년에 태어났으며, 훈민정음을 창제하고 과학 기술과 농업 발전에 기여했습니다."

STEP 6 CARD
- Number: "6"
- Heading: "생성 계속"
- LM icon.
- Output example:
  "... 측우기와 앙부일구 제작을 장려하고, 농사직설 편찬을 통해 농업 발전에도 기여했습니다."
- Pale-red notice:
  "추가 정보가 필요하면 다시 [Search(query)] 생성"
- Smaller note:
  "또는 생성이 끝날 때까지 현재 검색 결과를 사용"

LOOP ARROW
- Draw a thick blue arrow from Step 6 downward, leftward, and upward into Step 3.
- Label: "추가 정보가 필요하면 다시 Step 3으로"
- Second line: "새로운 [Search(query)] 생성"

BOTTOM CONTEXT PANEL
- Heading: "Context 및 메모리 관리 (FLAREinstruct)"
- Four compact rows:
  1. "사용자 입력 x - 항상 유지"
  2. "지금까지의 생성 결과 y_<t - 계속 누적"
  3. "검색 문서 D_qt - 현재 검색 결과만 유지"
  4. "새 검색 발생 - 이전 D_qt를 버리고 D_q(t+1)로 교체"
- Add this note: "검색 문서는 다음 [Search(query)]가 생성되거나 생성이 종료될 때까지 사용"

BOTTOM FORMULA BOX
- Heading: "전체 생성 과정"
- Equations:
  "D_qt = ret(q_t)"
  "y_t = LM([D_qt, x, y_<t])"
- Note: "q_t는 LM이 [Search(query)] 형태로 직접 생성"

VISUAL SEMANTICS
- Blue means LM generation and control flow.
- Purple means the explicit `[Search(query)]` marker.
- Green means retrieved documents.
- The search marker is generated model text, not an external button.
- The final natural-language answer must not retain the control marker.

SCIENTIFIC ACCURACY CONSTRAINTS
- Do not use token probability, low-confidence tokens, θ, β, masking, a temporary next sentence, or a confidence decision diamond.
- Retrieval is triggered only when the LM emits `[Search(query)]`.
- Text inside `[Search(...)]` becomes q_t.
- A new retrieval replaces the previous retrieved-document context; do not show permanent accumulation of documents.
- User input x and accepted answer history y_<t remain available.
- Show repeated generation and retrieval, not one-time RAG.

AVOID
- No FLAREdirect elements.
- No photorealistic King Sejong portrait, palace scene, decorative AI brain, 3D robot, neon style, benchmark scores, logos, or watermark.
- No crossed arrows, malformed Korean, duplicated cards, invented formulas, tiny labels, or ambiguous loops.

TEXT REQUIREMENT
Render every Korean phrase, equation, subscript, and `[Search(query)]` string exactly and legibly. Prioritize textual accuracy over decoration.
```

## 검수 체크리스트

- [ ] 우측 상단이 `1/3`인가?
- [ ] `[Search(query)]`가 LM 출력으로 표현됐는가?
- [ ] 검색 query가 `세종대왕 출생 연도와 주요 업적`인가?
- [ ] `θ`, `β`, masking, token probability가 전혀 등장하지 않는가?
- [ ] 새 검색 시 이전 검색 문서가 교체되는가?
- [ ] Step 6에서 Step 3으로 돌아가는 loop가 보이는가?
