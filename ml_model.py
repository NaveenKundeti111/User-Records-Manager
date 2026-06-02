import numpy as np
from sklearn.tree import DecisionTreeClassifier

STYLE_PALETTES = {
    "Ocean": {
        "accent": "#38bdf8",
        "background": "Deep blue with bright turquoise gradient",
        "style": "cool and calm",
        "textColor": "#0f172a"
    },
    "Sunset": {
        "accent": "#fb7185",
        "background": "Warm coral and soft gold tones",
        "style": "vibrant and uplifting",
        "textColor": "#f8fafc"
    },
    "Forest": {
        "accent": "#4ade80",
        "background": "Earthy greens with natural warmth",
        "style": "fresh and grounded",
        "textColor": "#0f172a"
    },
    "Neon": {
        "accent": "#c084fc",
        "background": "Bright purple neon glow",
        "style": "bold and futuristic",
        "textColor": "#ffffff"
    }
}


def build_model():
    X = np.array([
        [4, 22],
        [5, 27],
        [6, 33],
        [3, 20],
        [7, 35],
        [4, 18],
        [5, 28],
        [6, 40],
        [8, 45],
        [4, 25],
        [6, 30],
        [5, 20],
        [7, 38],
        [6, 26],
        [3, 19]
    ])
    y = np.array([
        "Ocean",
        "Sunset",
        "Forest",
        "Ocean",
        "Forest",
        "Ocean",
        "Sunset",
        "Forest",
        "Neon",
        "Sunset",
        "Forest",
        "Ocean",
        "Neon",
        "Sunset",
        "Ocean"
    ])

    model = DecisionTreeClassifier(max_depth=4, random_state=42)
    model.fit(X, y)
    return model


MODEL = build_model()


def recommend_style(name: str, age: int):
    normalized_age = max(1, min(age, 100))
    feature = np.array([[len(name), normalized_age]])
    theme = MODEL.predict(feature)[0]
    palette = STYLE_PALETTES[theme].copy()
    palette["theme"] = theme
    palette["age"] = age
    return palette
