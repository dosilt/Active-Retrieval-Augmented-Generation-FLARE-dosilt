"""Command-line entry point for the FLARE example."""

from __future__ import annotations

import argparse
import os

from openai import OpenAI
from dotenv import load_dotenv

from flare import FlareGenerator
from retriever import WikipediaRetriever


load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="FLARE-style Wikipedia RAG")
    parser.add_argument("question", nargs="?", help="Question to answer")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    parser.add_argument("--threshold", type=float, default=0.40,
                        help="theta: retrieval trigger probability")
    parser.add_argument("--mask-threshold", type=float, default=0.40,
                        help="beta: query masking probability")
    parser.add_argument("--max-sentences", type=int, default=6)
    parser.add_argument("--language", default="ko", help="Wikipedia language code")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    question = args.question or input("질문: ").strip()
    if not question:
        raise SystemExit("질문을 입력해 주세요.")
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY 환경변수를 먼저 설정해 주세요.")

    generator = FlareGenerator(
        client=OpenAI(),
        retriever=WikipediaRetriever(language=args.language),
        model=args.model,
        probability_threshold=args.threshold,
        mask_probability_threshold=args.mask_threshold,
        max_sentences=args.max_sentences,
    )
    print(generator.generate(question, verbose=args.verbose))


if __name__ == "__main__":
    main()
