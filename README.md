# FLARE: Active Retrieval Augmented Generation — 코드로 읽기

논문 **Active Retrieval Augmented Generation**의 FLAREdirect 흐름을 수식과 Python 코드로 연결하는 학습용 저장소입니다. 블로그에서는 배경과 아이디어를 설명하고, 여기서는 각 수식이 어떤 함수로 실행되는지 따라갑니다.

- [논문 · EMNLP 2023](https://aclanthology.org/2023.emnlp-main.495/)
- [저자들의 공식 구현](https://github.com/jzbjyb/FLARE)
- 이 저장소는 개인 학습용 구현이며 공식 구현의 복제본이 아닙니다.
- 블로그 글 주소는 발행 후 이 위치에 연결할 예정입니다.

## 먼저 확인할 구현 범위

구현한 방법은 **FLAREdirect + masked sentence 기반 implicit query**입니다. FLAREinstruct와 질문 생성 방식의 explicit query는 구현하지 않았습니다.

| 항목 | 논문 | 현재 코드 |
|---|---|---|
| 생성 모델 | text-davinci-003 | gpt-4o-mini |
| Wikipedia 검색 | passage dump + BM25 | 한국어 Wikipedia API |
| 문장 추출 | 64토큰 생성 후 NLTK로 첫 문장 추출 | 한 문장 생성을 지시하고 응답 전체 사용, 최대 120토큰 |
| 전체 생성 제한 | 실험별 토큰 길이 제한 | 최대 6단계 및 단순 조기 종료 |
| 최초 검색 | 사용자 입력으로 검색 | 구현됨 |
| 이후 질의 | 임시 다음 문장으로 구성 | 저신뢰 토큰 제거, 질문 추가·표제어 폴백 없음 |
| 임계값 | 작업별 θ, β 설정 | 각각 기본 0.4, 별도 변경 가능 |

**이 코드로 논문의 성능 수치를 재현했다고 해석하면 안 됩니다.** 특히 현재 검색기는 무관한 문서나 빈 결과를 반환할 수 있습니다. 검색 결과 개수는 관련성을 보장하지 않습니다.

## 실행

Python 3.13의 Conda `rag` 환경에서 사용한 코드입니다. 기존 환경이 없다면 먼저 생성합니다.

```powershell
conda create -n rag python=3.13
conda activate rag
git clone --branch docs/flare-code-walkthrough https://github.com/dosilt/Active-Retrieval-Augmented-Generation-FLARE-dosilt.git
cd Active-Retrieval-Augmented-Generation-FLARE-dosilt
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

기존 `.env`가 있다면 복사 명령은 생략합니다. `.env`에 자신의 API 키를 입력합니다.

```dotenv
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

`main.py`의 `load_dotenv()`가 설정을 로드합니다. 이미 셸에 같은 환경변수가 있다면 그 값이 우선합니다. `.env`는 Git 추적에서 제외합니다. 실행하면 OpenAI API 사용료가 발생합니다.

```powershell
python main.py "세종대왕은 몇년도에 태어났으며 어떤 업적이 있어?" --verbose
```

| 옵션 | 기본값 | 역할 |
|---|---|---|
| `--model` | OPENAI_MODEL 또는 gpt-4o-mini | 생성 모델 |
| `--threshold` | 0.4 | θ: 검색 판단 |
| `--mask-threshold` | 0.4 | β: 검색어 토큰 제거 |
| `--max-sentences` | 6 | 최초 문장을 포함한 최대 단계 수 |
| `--language` | ko | Wikipedia 언어, 생성 언어 지정 옵션은 아님 |
| `--verbose` | 꺼짐 | 초안·검색어·문서 수·재생성 로그 |

θ=0은 논문에서 가능한 설정이지만 현재 생성자의 검증은 허용하지 않습니다. β=0은 허용하며 masking을 하지 않습니다. 기본 θ=β=0.4는 논문 Table 9의 StrategyQA 설정과 수치가 같지만, 같은 실험 조건이라는 뜻은 아닙니다.

## 코드 지도

| 파일 | 책임 |
|---|---|
| [main.py](main.py) | 환경변수와 CLI 인자를 읽고 생성기·검색기 연결 |
| [flare.py](flare.py) | 확률 판정, masking, 검색과 생성 반복 |
| [retriever.py](retriever.py) | Wikipedia API 호출 및 문서 자료형 |
| [requirements.txt](requirements.txt) | 실행 의존성 |

아래 코드는 설명에 필요한 발췌입니다. 함수 전체와 주변 조건은 링크된 소스에서 확인할 수 있습니다.

<a id="part-1"></a>
## Part 1. 수식과 변수 대응

| 기호 | 의미 | 코드 변수 |
|---|---|---|
| x | 사용자 입력 | question |
| y&lt;t | 이전까지 확정한 답변 | answer |
| ŝₜ | 임시 다음 문장 | draft |
| θ | 검색 임계값 | probability_threshold |
| β | masking 임계값 | mask_probability_threshold |
| qₜ | 검색 질의 | query |
| Dqₜ | 현재 검색 문서 | documents |
| yₜ | 현재 채택할 출력 | sentence |

핵심 진입점은 [FlareGenerator.generate()](flare.py)입니다. `answer`는 누적 상태이고 `draft`는 검색을 위해 폐기할 수 있는 임시 결과입니다.

<a id="part-2"></a>
## Part 2. 최초 검색 — q₁ = x

처음에는 누적 답변이 없으므로 사용자 질문으로 검색합니다.

$$
q_1=x,\qquad D_x=\operatorname{ret}(x)
$$

```python
initial_documents = self.retriever.search(question, self.search_results)
initial_evidence = (
    self._format_evidence(initial_documents) if initial_documents else None
)
first_sentence, _ = self._predict_next_sentence(
    question, answer, initial_evidence
)
```

첫 문장의 입력은 개념적으로 다음과 같습니다.

$$
\hat{s}_1=LM([D_x,x])
$$

현재 코드는 첫 문장을 바로 답변에 넣습니다. 초기 검색은 θ에 의한 이후 검색 판단과 구분합니다. 문서가 없으면 `evidence=None`으로 생성하는 예외가 있습니다.

<a id="part-3"></a>
## Part 3. 임시 다음 문장 — ŝₜ = LM([x, y&lt;t])

이후 반복에서는 이전 검색 문서 없이 다음 문장을 예측합니다.

$$
\hat{s}_t=LM([x,y_{<t}])
$$

```python
draft, scores = self._predict_next_sentence(question, answer)
```

이 호출에는 `evidence` 인자가 없습니다. 질문과 확정 답변을 매번 다시 전달합니다. 현재 프롬프트는 “다음 한 문장만 생성하라”고 지시하지만 문장 분리기로 검증하지는 않습니다.

`_predict_next_sentence()`는 `logprobs=True`로 응답을 요청하고, 생성된 토큰별 `logprob`를 `TokenScore`에 저장합니다.

$$
\ell_i=\log p_i,\qquad p_i=\exp(\ell_i)
$$

```python
@property
def probability(self) -> float:
    return math.exp(self.logprob)
```

여기서 pᵢ는 입력과 앞선 생성 토큰을 조건으로 해당 토큰에 부여한 확률입니다. **사실이 맞을 확률이나 문장 전체의 정확도 점수가 아닙니다.**

<a id="part-4"></a>
## Part 4. 검색 판단 — θ

논문의 조건은 확률이 θ보다 낮은 토큰의 존재 여부입니다.

$$
\operatorname{retrieve}_t=\mathbf{1}[\exists i:\ p_i<\theta]
$$

```python
meaningful = [score for score in scores if score.token.strip()]
return bool(meaningful) and any(
    score.logprob < self.logprob_threshold for score in meaningful
)
```

로그 함수가 단조 증가하므로 pᵢ < θ와 log pᵢ < log θ는 같은 판정입니다. 평균 확률을 구하지 않으며, 낮은 토큰 하나로도 검색이 발동합니다.

현재 구현은 공백만 있는 토큰을 제외합니다. 이는 모든 토큰에 대한 논문 조건식과 구분되는 구현 선택입니다. 확률 데이터가 비어 있어도 현재 함수는 False를 반환하므로, 이를 높은 확신으로 해석해서는 안 됩니다.

<a id="part-5"></a>
## Part 5. Masking 질의 — qₜ = maskβ(ŝₜ)

검색이 필요하면 임시 문장에서 β 미만 토큰을 제외합니다.

$$
q_t=\operatorname{mask}_{\beta}(\hat{s}_t)
$$

```python
confident_scores = [
    score for score in scores
    if score.logprob >= self.mask_logprob_threshold
]
```

θ는 “검색할까?”, β는 “무엇을 제거할까?”에 대응합니다. 첫 검색 이후에는 사용자 질문을 덧붙이지 않고 남은 예측 문장만 검색어로 사용합니다. `[MASK]`나 밑줄을 실제 검색어에 삽입하지 않습니다.

한국어처럼 토큰 경계가 문자 경계와 다를 수 있는 경우를 위해 API의 바이트를 연결합니다.

```python
raw = b"".join(bytes(score.token_bytes or ()) for score in confident_scores)
confident = raw.decode("utf-8", errors="ignore").strip()
```

`errors="ignore"`는 제거 과정에서 남은 불완전한 문자를 버리는 처리입니다. 원래 글자를 복원하거나 완전한 단어를 보장하지 않습니다. 토큰을 제외하면 검색어 문법이 어색해질 수도 있습니다.

<a id="part-6"></a>
## Part 6. 검색과 재생성 — sₜ = LM([Dqₜ, x, y&lt;t])

$$
D_{q_t}=\operatorname{ret}(q_t)
$$

```python
query = self._build_search_query(scores)
documents = self.retriever.search(query, self.search_results)
```

현재 [WikipediaRetriever.search()](retriever.py)는 질의를 그대로 Wikipedia API에 전달하고 문서 도입부를 반환합니다. 별도 검색어 폴백이나 관련성 검증은 없습니다.

문서를 얻으면 같은 위치의 문장을 다시 생성합니다.

$$
s_t=LM([D_{q_t},x,y_{<t}])
$$

```python
if documents:
    sentence, _ = self._predict_next_sentence(
        question, answer, self._format_evidence(documents)
    )
```

임시 문장은 누적 답변에 넣지 않았으므로, 임시 문장 뒤에 이어 쓰는 것이 아닙니다. 기존 답변 바로 다음 위치를 새로 작성합니다. 재생성된 토큰 확률은 다시 검사하지 않습니다.

현재 코드의 예외: 검색 결과가 비어 있으면 재생성하지 않고 초안을 채택합니다. 문서가 존재해도 관련성이 낮으면 잘못된 답변이 나올 수 있습니다.

<a id="part-7"></a>
## Part 7. 답변 누적과 context 수명

논문의 기본 선택식은 다음과 같습니다.

$$
y_t=
\begin{cases}
\hat{s}_t & \text{if all }p_i\ge\theta \\
LM([D_{q_t},x,y_{<t}]) & \text{otherwise}
\end{cases}
$$

채택한 문장을 누적합니다.

```python
answer = f"{answer} {sentence}".strip()
```

다음 임시 생성은 다시 `_predict_next_sentence(question, answer)`로 호출합니다. 검색 문서가 Python 변수에 남아 있더라도 다음 요청에 포함되지 않으므로 모델의 입력에서는 제외됩니다. 확정 문장에 담긴 정보는 `answer`를 통해 이어집니다.

```text
[질문 + 누적 답변] → 임시 문장 → 확률 검사
    ├─ 검색 불필요 → 초안 채택
    └─ 검색 필요 → masking → 검색 → 근거로 재생성 → 채택
                                            ↓
                                    확정 답변에 추가
                                            ↓
                          이전 검색 문서 없이 다음 임시 생성
```

현재 종료 조건은 최대 단계 수, 빈 응답, 동일 문장 반복, 특정 종료 문구입니다. API의 종료 사유를 이용해 전체 답변 완료를 판정하는 구현은 아닙니다.

<a id="logs"></a>
## 로그 읽기

`--verbose`를 켜면 다음 항목을 관찰할 수 있습니다.

| 로그 | 의미 |
|---|---|
| initial query | 최초 사용자 질문 검색 |
| generated sentence | 최초 생성 결과 |
| temporary sentence | 확정 전 다음 문장 |
| masked search query | β 기준으로 토큰을 제외한 실제 질의 |
| documents found | 반환 문서 수, 관련성 점수가 아님 |
| regenerated sentence | 검색 결과가 있을 때 재생성한 문장 |
| no retrieval | 현재 초안에서 검색 조건이 발동하지 않음 |

검색어와 재생성 결과를 비교하면, 저신뢰 토큰 제거가 검색과 생성에 어떤 영향을 주었는지 확인할 수 있습니다.

## 블로그에서 연결하기

블로그의 「코드로 구현해 보기」에는 다음처럼 짧게 연결할 수 있습니다.

> 전체 코드와 실행 방법은 GitHub에 정리했다. README에서는 최초 검색, 임시 문장 생성, 확률 기반 검색 판단, masking, 재생성, context 관리 순서로 논문의 수식과 실제 함수를 연결한다. 현재 구현과 논문 실험 설정의 차이도 함께 표시했다.

- [전체 코드 해설](https://github.com/dosilt/Active-Retrieval-Augmented-Generation-FLARE-dosilt/tree/docs/flare-code-walkthrough#part-1)
- [검색 판단 θ](https://github.com/dosilt/Active-Retrieval-Augmented-Generation-FLARE-dosilt/tree/docs/flare-code-walkthrough#part-4)
- [Masking β](https://github.com/dosilt/Active-Retrieval-Augmented-Generation-FLARE-dosilt/tree/docs/flare-code-walkthrough#part-5)
- [재생성과 context 관리](https://github.com/dosilt/Active-Retrieval-Augmented-Generation-FLARE-dosilt/tree/docs/flare-code-walkthrough#part-6)

원 논문의 §3.2, Appendix A, Table 9와 함께 읽으면 알고리즘·실험 설정·현재 구현을 구분하기 쉽습니다.
