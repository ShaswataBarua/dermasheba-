# 🩺 DermaSheba | ডার্মাসেবা

**AI-powered Skin Condition Awareness Tool** — upload a photo of a skin concern and get an instant assessment with urgency guidance, explained in both English and Bangla.

Built for Bangladesh: rural patients often can't reach a dermatologist quickly, and language barriers make generic health tools hard to use. DermaSheba bridges that gap with a simple photo upload and plain-language Bangla explanations.

## ✨ Features

- 📸 **Photo upload** — accepts JPG/PNG, runs entirely in the browser
- 🔍 **Instant AI analysis** — image classification using a fine-tuned Vision Transformer (`Anwarkh1/Skin_Cancer-Image_Classification`)
- 🚦 **Urgency levels** — HIGH / MEDIUM / LOW with clear "what to do next" guidance
- 📝 **Bangla explanations** — every result explained in simple Bengali so non-English speakers understand their situation
- ⚠️ **Built-in disclaimer** — always reminds users this is awareness, not diagnosis

## 🧠 Detects 7 skin conditions

| Condition | Urgency |
|---|---|
| Melanoma | 🔴 High |
| Basal Cell Carcinoma | 🔴 High |
| Actinic Keratosis | 🟡 Medium |
| Vascular Lesion | 🟡 Medium |
| Benign Keratosis | 🟢 Low |
| Dermatofibroma | 🟢 Low |
| Melanocytic Nevi (common mole) | 🟢 Low |

## 🛠️ Tech Stack

- **Python + Streamlit** — frontend & app logic
- **Transformers (Hugging Face)** — `image-classification` pipeline
- **PyTorch + Pillow** — image handling & inference
- Deployed as a [Hugging Face Space](https://huggingface.co/spaces/TheRealShaswata/dermasheba)

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
