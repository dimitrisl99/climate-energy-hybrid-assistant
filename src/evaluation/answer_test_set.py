ANSWER_TEST_SET = [
    {
        "question": "What are the EU climate neutrality targets?",
        "expected_keywords": [
            "climate neutrality",
            "2050",
            "2030",
            "55%",
        ],
        "forbidden_keywords": [
            "carbon neutral by 2035",
            "net zero by 2040",
        ],
    },
    {
        "question": "What are the main climate risks in Europe?",
        "expected_keywords": [
            "ecosystems",
            "food",
            "health",
            "infrastructure",
            "economy",
            "Southern Europe",
        ],
        "forbidden_keywords": [
            "earthquake",
            "volcanic",
        ],
    },
    {
        "question": "How does climate change affect agriculture?",
        "expected_keywords": [
            "food security",
            "agricultural productivity",
            "crop yield",
        ],
        "forbidden_keywords": [
            "increases crop yields everywhere",
        ],
    },
    {
        "question": "Compare Greece and Germany emissions and explain what this means.",
        "expected_keywords": [
            "Germany",
            "Greece",
            "2024",
            "CO2",
            "per capita",
            "not supported",
        ],
        "forbidden_keywords": [
            "because Germany uses more coal",
            "because Greece has no industry",
        ],
    },
]