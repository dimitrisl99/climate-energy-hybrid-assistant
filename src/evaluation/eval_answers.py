from src.app.hybrid_assistant import run_assistant
from src.evaluation.answer_test_set import ANSWER_TEST_SET


def contains_keyword(text: str, keyword: str) -> bool:
    return keyword.lower() in text.lower()


def evaluate_answer(answer: str, expected_keywords: list[str], forbidden_keywords: list[str]) -> dict:
    found_expected = [
        keyword for keyword in expected_keywords
        if contains_keyword(answer, keyword)
    ]

    found_forbidden = [
        keyword for keyword in forbidden_keywords
        if contains_keyword(answer, keyword)
    ]

    expected_score = len(found_expected) / len(expected_keywords) if expected_keywords else 1.0
    hallucination_flag = len(found_forbidden) > 0

    return {
        "expected_score": expected_score,
        "found_expected": found_expected,
        "missing_expected": [
            keyword for keyword in expected_keywords
            if keyword not in found_expected
        ],
        "found_forbidden": found_forbidden,
        "hallucination_flag": hallucination_flag,
    }


def evaluate_answers():
    total = len(ANSWER_TEST_SET)
    total_score = 0
    hallucination_count = 0

    print("\n================ ANSWER EVALUATION ================")

    for item in ANSWER_TEST_SET:
        question = item["question"]
        expected_keywords = item["expected_keywords"]
        forbidden_keywords = item["forbidden_keywords"]

        result = run_assistant(question)
        answer = result["answer"]

        evaluation = evaluate_answer(
            answer=answer,
            expected_keywords=expected_keywords,
            forbidden_keywords=forbidden_keywords,
        )

        total_score += evaluation["expected_score"]

        if evaluation["hallucination_flag"]:
            hallucination_count += 1

        print("\n---------------------------------------------------")
        print(f"Question: {question}")
        print(f"Route: {result['type']}")
        print(f"Expected keyword score: {evaluation['expected_score']:.2f}")
        print(f"Found expected: {evaluation['found_expected']}")
        print(f"Missing expected: {evaluation['missing_expected']}")
        print(f"Forbidden found: {evaluation['found_forbidden']}")
        print("\nAnswer preview:")
        print(answer[:700])

    average_score = total_score / total
    hallucination_rate = hallucination_count / total

    print("\n================ SUMMARY ================")
    print(f"Total questions: {total}")
    print(f"Average expected keyword score: {average_score:.2f}")
    print(f"Hallucination flag rate: {hallucination_rate:.2f}")


if __name__ == "__main__":
    evaluate_answers()