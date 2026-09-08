# FLARE의 두 가지 방법 비교 이미지 생성 프롬프트

이 문서는 이미지 생성 모델에 그대로 입력할 수 있는 제작 명세다. 목표는 논문 *Active Retrieval Augmented Generation*에서 제안한 두 구현 방식인 **FLAREinstruct**와 **FLAREdirect**의 차이를 한 장의 교육용 인포그래픽으로 정확하게 보여주는 것이다.

> 참고: 논문의 기여 전체가 오직 두 알고리즘만이라는 뜻은 아니다. 논문은 active retrieval을 `when to retrieve`와 `what to retrieve`의 문제로 일반화하고, 이를 구현하는 두 가지 FLARE 방법을 제안한다. 이 이미지는 그중 두 방법의 비교에 초점을 맞춘다.

---

## 이미지 생성 모델에 입력할 최종 프롬프트

```text
Use case: scientific-educational
Asset type: Korean technical blog infographic, a single landscape figure explaining two methods from the FLARE paper

Primary request:
Create a polished, publication-quality educational infographic comparing the two forward-looking active retrieval methods proposed in the paper "Active Retrieval Augmented Generation": FLAREinstruct and FLAREdirect. The core message must be immediately understandable: both methods repeatedly interleave generation and retrieval, but they decide WHEN and WHAT to retrieve in different ways.

Canvas and layout:
- 16:9 landscape canvas, 1920 x 1080 or equivalent high resolution.
- White or very light warm-gray background.
- Use a clean academic vector-infographic style, not a photorealistic scene.
- Large title at the top, a small shared-principle strip below it, and two equal-width vertical panels beneath.
- Left panel: FLAREinstruct, blue accent color.
- Right panel: FLAREdirect, orange accent color.
- Place a narrow common conclusion strip across the bottom.
- Maintain generous whitespace, consistent alignment, rounded rectangular nodes, thin arrows, and readable typography.
- Reading direction is top-to-bottom inside each panel.
- Use solid arrows for the normal forward path and a single curved loop-back arrow to indicate repetition.

Exact title text, render verbatim:
"FLARE: 미래 생성을 보고 검색하는 두 가지 방법"

Exact subtitle text, render verbatim:
"Active Retrieval = 언제 검색할까? (WHEN) + 무엇을 검색할까? (WHAT)"

Shared input block centered above the two panels:
- Label: "현재 생성 상태"
- Inside the block show: "사용자 입력 x" and "지금까지의 출력 y<t"
- From this block, split one arrow toward each method panel.

LEFT PANEL — FLAREinstruct:
- Panel heading, exact text: "1. FLAREinstruct"
- Small panel subtitle, exact text: "LM이 검색 명령을 직접 생성"
- Use blue accents: navy blue headings, pale blue nodes, blue arrows.

Draw the following pipeline as five vertically arranged stages:

Stage I-1:
- Node label: "Retrieval instruction + task examples"
- Small Korean annotation: "검색 방법과 과업을 few-shot prompt로 지시"
- Add a small prompt/document icon.

Stage I-2:
- Node label: "LM이 답변을 생성"
- Show a short example text stream containing the exact inline marker:
  "… [Search(Joe Biden university)] …"
- The `[Search(query)]` marker must be visually prominent in a darker blue monospace capsule.

Stage I-3:
- Diamond decision node with exact text:
  "[Search(query)]를 생성했는가?"
- Branch labels must be exact Korean text: "아니오" and "예"
- "아니오" continues ordinary answer generation.
- "예" goes to the retriever.

Stage I-4, yes branch:
- Stop/pause generation at the search marker.
- A magnifying-glass node labeled: "query로 관련 문서 검색"
- Then a small document stack labeled: "검색 문서 Dq"

Stage I-5:
- Node label: "문서를 입력 앞에 붙이고 생성 재개"
- Small formula-like line, render exactly:
  "LM([Dq, x, y<t])"
- Draw a curved loop arrow back toward answer generation with the label: "다음 검색 명령 또는 종료까지 반복"

Add a concise blue callout box at the bottom of the left panel:
- Heading: "판단 기준"
- Text: "WHEN: LM이 [Search(...)]를 출력할 때"
- Text: "WHAT: [Search(...)] 안의 query"
- Text: "특징: 직관적이지만 black-box LM의 검색 명령이 불안정할 수 있음"

RIGHT PANEL — FLAREdirect:
- Panel heading, exact text: "2. FLAREdirect"
- Small panel subtitle, exact text: "다음 문장의 확률로 검색을 결정"
- Use orange accents: dark burnt-orange headings, pale orange nodes, orange arrows.

Draw the following pipeline as seven vertically arranged stages:

Stage D-1:
- Node label: "검색 문서 없이 임시 다음 문장 생성"
- Render this equation exactly and clearly:
  "ŝt = LM([x, y<t])"
- The temporary sentence must be gray and italic to show that it is not committed yet.
- Example temporary sentence:
  "Joe Biden attended the University of Pennsylvania."
- Underline "University of Pennsylvania" in red and add a tiny red label: "low confidence"

Stage D-2:
- Show token probability bars or small probability badges beneath the temporary sentence.
- Most tokens are green and above the threshold; at least one uncertain token is red and below the threshold.
- Diamond decision node with exact text:
  "모든 token의 P(w) ≥ θ ?"

Stage D-3, high-confidence branch:
- Branch label: "예"
- Green check node labeled: "임시 문장 ŝt를 그대로 채택"
- Small annotation: "검색하지 않음"

Stage D-4, low-confidence branch:
- Branch label: "아니오"
- Red-orange node labeled: "검색 실행"
- Small annotation: "하나라도 P(w) < θ"

Stage D-5, query formulation:
- Split into two small side-by-side query options, clearly shown as alternatives rather than sequential steps.
- Option A heading: "Implicit query"
- Option A text: "β보다 낮은 token을 masking"
- Option A example: "Joe Biden attended the _____."
- Option A equation: "qt = mask(ŝt)"
- Option B heading: "Explicit query"
- Option B text: "low-confidence span을 묻는 질문 생성"
- Option B example: "Which university did Joe Biden attend?"
- Option B equation: "qt = qgen(ŝt)"
- Put a small label between them: "or"

Stage D-6:
- Magnifying-glass node labeled: "qt로 관련 문서 검색"
- Then a document stack labeled: "현재 단계의 검색 문서 Dqt"

Stage D-7:
- Node label: "검색 문서를 근거로 다음 문장 재생성"
- Render the equation exactly:
  "st = LM([Dqt, x, y<t])"
- Add an emphasized note with exact text:
  "임시 문장 ŝt는 폐기하고, 재생성한 st만 채택"
- Draw a curved loop arrow back to temporary next-sentence generation with the label: "문장 단위로 반복"

Add a concise orange callout box at the bottom of the right panel:
- Heading: "판단 기준"
- Text: "WHEN: 임시 문장에 P(w) < θ인 token이 있을 때"
- Text: "WHAT: 임시 미래 문장을 masking하거나 질문으로 변환"
- Text: "특징: LM의 명시적 검색 명령 대신 token confidence를 사용"

BOTTOM COMMON STRIP:
- Heading, exact text: "두 방법의 공통점"
- Show three compact items connected from left to right:
  1. "미래에 생성할 내용을 반영해 검색"
  2. "Generation ↔ Retrieval을 반복"
  3. "현재 검색 문서만 다음 생성에 사용"
- Beneath item 3 add a smaller exact note:
  "이전 단계의 검색 문서는 누적하지 않음"
- Add one final centered conclusion in bold:
  "FLAREinstruct는 검색 의도를 명시적으로 출력하고, FLAREdirect는 불확실성을 관찰해 검색을 촉발한다."

Visual encoding rules:
- Blue always means FLAREinstruct.
- Orange always means FLAREdirect.
- Green means confident/accepted/no retrieval.
- Red means low confidence/retrieval trigger/discarded temporary content.
- Gray italic text means temporary generation that is not yet part of the final answer.
- Document stacks mean retrieved external context.
- Use visually different icons for LM, retriever, documents, decision, and accepted output.
- Keep all arrows unambiguous and avoid crossing arrows.
- Make the yes/no branches visually obvious.
- Equations should be typeset like clean mathematical notation, with subscripts where possible.

Typography:
- Use a modern Korean sans-serif typeface similar to Pretendard, Noto Sans KR, or SUIT.
- Use a compatible math/serif face only for equations.
- Preserve the exact capitalization and spelling of "FLAREinstruct", "FLAREdirect", "WHEN", "WHAT", "Implicit query", "Explicit query", "Search", "LM", and token symbols.
- All Korean text must be crisp, correctly spelled, and fully legible at blog width.

Scientific accuracy constraints:
- Do not depict FLAREinstruct as using token probabilities or θ. Its trigger is the LM-generated `[Search(query)]` marker.
- Do not depict FLAREdirect as requiring the LM to emit `[Search(query)]`.
- In FLAREdirect, always generate the temporary sentence before checking token confidence.
- In FLAREdirect, accept the temporary sentence directly only on the high-confidence branch.
- On the low-confidence branch, never append the uncertain temporary sentence to the answer; use it to formulate the query, retrieve documents, regenerate the sentence, and commit only the regenerated sentence.
- Show masking and question generation as two alternative query-formulation variants inside FLAREdirect.
- Do not confuse θ and β: θ triggers retrieval; β selects which low-confidence tokens/spans are masked or converted into questions.
- Retrieved context is temporary for the current generation step; do not draw an ever-growing permanent conversation-memory database.
- Both methods operate repeatedly during long-form generation rather than retrieving only once at the beginning.

Avoid:
- No 3D render, no photorealistic people, no decorative AI brain, no robots, no neon cyberpunk style.
- No dense background patterns, gradients that reduce readability, excessive shadows, or tiny text.
- No extra algorithms, no baseline methods, no benchmark scores, and no unrelated RAG architecture.
- No spelling errors, malformed Korean, duplicated nodes, invented formulas, crossed arrows, or ambiguous loops.
- No company logos, watermarks, citations fabricated inside the artwork, or paper-like aged texture.
- Do not label masking and question generation as FLAREinstruct; both belong under FLAREdirect query formulation.

Quality target:
The result should look like a carefully designed figure for a Korean machine-learning engineering blog: academically precise, visually balanced, easy to scan in under 20 seconds, but detailed enough that a reader can reconstruct both algorithms from the flowchart.
```

---

## 이미지 모델이 한글을 자주 틀릴 때 사용할 영문판 프롬프트

한글 텍스트 정확도가 낮은 이미지 모델에는 위 프롬프트의 레이아웃과 제약을 유지하면서 화면 안의 문구만 아래처럼 교체한다.

```text
Title: "FLARE: Two Ways to Look Forward and Retrieve"
Subtitle: "Active Retrieval = WHEN to retrieve + WHAT to retrieve"

Shared state:
"User input x" + "Output so far y<t"

Left panel:
"1. FLAREinstruct"
"The LM explicitly emits a search command"
"Retrieval instruction + task examples"
"Generate the answer"
"Did the LM emit [Search(query)]?"
"Pause generation"
"Retrieve documents Dq"
"Prepend documents and resume generation"
"WHEN: the LM emits [Search(...)]"
"WHAT: the query inside [Search(...)]"

Right panel:
"2. FLAREdirect"
"Token confidence determines retrieval"
"Generate a temporary next sentence without retrieved documents"
"Are all token probabilities P(w) ≥ θ?"
"Accept ŝt without retrieval"
"Trigger retrieval if any P(w) < θ"
"Implicit query: mask tokens below β"
"Explicit query: generate questions for low-confidence spans"
"Retrieve documents Dqt"
"Regenerate the next sentence"
"Discard temporary ŝt; commit only regenerated st"
"WHEN: any token has P(w) < θ"
"WHAT: mask or question generation based on the temporary future sentence"

Bottom strip:
"Both methods anticipate future content"
"Interleave Generation ↔ Retrieval"
"Use only the current step's retrieved documents"
"Previously retrieved documents are not accumulated"
```

---

## 생성 후 검수 체크리스트

- [ ] 좌측은 `[Search(query)]` 생성 여부로 분기하는가?
- [ ] 우측은 임시 문장 `ŝt` 생성 후 token probability를 검사하는가?
- [ ] `θ`는 검색 발생 판단, `β`는 masking/question 대상 선택으로 구분되어 있는가?
- [ ] FLAREdirect의 고신뢰 분기는 `ŝt`를 그대로 채택하는가?
- [ ] 저신뢰 분기는 `ŝt`를 폐기하고 문서 기반 `st`만 채택하는가?
- [ ] masking과 question generation이 FLAREdirect 내부의 대안 두 가지로 표현됐는가?
- [ ] 검색 문서가 영구 누적되는 것처럼 그려지지 않았는가?
- [ ] 두 패널 모두 생성과 검색이 반복되는 loop를 보여주는가?
- [ ] 수식과 기호 `x`, `y<t`, `ŝt`, `st`, `qt`, `Dqt`, `θ`, `β`가 서로 뒤바뀌지 않았는가?
- [ ] 한글, 영문, 수식이 확대 없이도 읽히는가?

## 논문 근거

- Jiang et al., *Active Retrieval Augmented Generation*, EMNLP 2023, Sections 2.3, 3.1, 3.2.
- Paper: https://aclanthology.org/2023.emnlp-main.495/
- Official implementation: https://github.com/jzbjyb/FLARE

