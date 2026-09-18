import streamlit as st
from PIL import Image
from transformers import pipeline

st.set_page_config(
    page_title="DermaSheba | ডার্মাসেবা",
    page_icon="🩺",
    layout="centered"
)

@st.cache_resource
def load_model():
    return pipeline(
        "image-classification",
        model="Anwarkh1/Skin_Cancer-Image_Classification"
    )

classifier = load_model()

URGENCY_MAP = {
    "Melanoma": {
        "urgency": "🔴 HIGH",
        "bangla": "মেলানোমা",
        "action": "⚠️ See a dermatologist URGENTLY within 3-5 days."
    },
    "Basal Cell Carcinoma": {
        "urgency": "🔴 HIGH",
        "bangla": "ব্যাসাল সেল কার্সিনোমা",
        "action": "⚠️ See a dermatologist as soon as possible this week."
    },
    "Actinic Keratosis": {
        "urgency": "🟡 MEDIUM",
        "bangla": "অ্যাক্টিনিক কেরাটোসিস",
        "action": "📅 Book an appointment with a local doctor within 2 weeks."
    },
    "Benign Keratosis": {
        "urgency": "🟢 LOW",
        "bangla": "বিনাইন কেরাটোসিস",
        "action": "🏠 Monitor at home. See a doctor if it grows or changes."
    },
    "Dermatofibroma": {
        "urgency": "🟢 LOW",
        "bangla": "ডার্মাটোফাইব্রোমা",
        "action": "🏠 Usually harmless. No urgent action needed."
    },
    "Melanocytic Nevi": {
        "urgency": "🟢 LOW",
        "bangla": "মেলানোসাইটিক নেভি (সাধারণ তিল)",
        "action": "🏠 Common mole. Monitor for changes in size or color."
    },
    "Vascular Lesion": {
        "urgency": "🟡 MEDIUM",
        "bangla": "ভাস্কুলার লেশন",
        "action": "📅 See a local doctor for evaluation."
    },
}

BANGLA_EXPLANATIONS = {
    "Melanoma": "মেলানোমা একটি গুরুতর ধরনের ত্বকের সমস্যা যা ত্বকের রঙ্গক কোষ থেকে তৈরি হয়। এটি সাধারণত গাঢ় রঙের অনিয়মিত আকারের দাগ হিসেবে দেখা যায়। দ্রুত চিকিৎসা না করলে এটি ছড়িয়ে পড়তে পারে। মনে রাখবেন, এটি শুধুমাত্র একটি প্রাথমিক ধারণা। সঠিক রোগ নির্ণয়ের জন্য একজন ডাক্তারের সাথে পরামর্শ করুন।",
    "Basal Cell Carcinoma": "ব্যাসাল সেল কার্সিনোমা ত্বকের একটি সাধারণ সমস্যা যা ত্বকের উপরের স্তরে দেখা দেয়। এটি সাধারণত মুখ বা ঘাড়ে ছোট উঁচু দাগ হিসেবে দেখা যায়। সঠিক সময়ে চিকিৎসা নিলে এটি সম্পূর্ণ ভালো হয়। মনে রাখবেন, এটি শুধুমাত্র একটি প্রাথমিক ধারণা। সঠিক রোগ নির্ণয়ের জন্য একজন ডাক্তারের সাথে পরামর্শ করুন।",
    "Actinic Keratosis": "অ্যাক্টিনিক কেরাটোসিস সূর্যের আলোর কারণে ত্বকে তৈরি হওয়া একটি রুক্ষ, আঁশযুক্ত দাগ। এটি সাধারণত লাল বা বাদামি রঙের হয় এবং মুখ, হাত বা মাথায় দেখা যায়। সময়মতো চিকিৎসা নিলে সহজেই ভালো হয়। মনে রাখবেন, এটি শুধুমাত্র একটি প্রাথমিক ধারণা। সঠিক রোগ নির্ণয়ের জন্য একজন ডাক্তারের সাথে পরামর্শ করুন।",
    "Benign Keratosis": "বিনাইন কেরাটোসিস ত্বকের একটি সাধারণ, ক্ষতিহীন বৃদ্ধি যা বয়সের সাথে দেখা যায়। এটি সাধারণত বাদামি বা কালো রঙের এবং মসৃণ বা আঁশযুক্ত হয়। এটি ক্যান্সার নয় এবং সাধারণত কোনো চিকিৎসার প্রয়োজন হয় না। মনে রাখবেন, এটি শুধুমাত্র একটি প্রাথমিক ধারণা। সঠিক রোগ নির্ণয়ের জন্য একজন ডাক্তারের সাথে পরামর্শ করুন।",
    "Dermatofibroma": "ডার্মাটোফাইব্রোমা ত্বকের নিচে একটি শক্ত, ছোট গোটা যা সাধারণত পায়ে দেখা যায়। এটি সম্পূর্ণ নিরীহ এবং সাধারণত কোনো সমস্যা করে না। বেশিরভাগ ক্ষেত্রে কোনো চিকিৎসার প্রয়োজন হয় না। মনে রাখবেন, এটি শুধুমাত্র একটি প্রাথমিক ধারণা। সঠিক রোগ নির্ণয়ের জন্য একজন ডাক্তারের সাথে পরামর্শ করুন।",
    "Melanocytic Nevi": "মেলানোসাইটিক নেভি হলো সাধারণ তিল যা ত্বকে দেখা যায়। এগুলো সাধারণত গোলাকার, মসৃণ এবং বাদামি রঙের হয়। বেশিরভাগ তিল সম্পূর্ণ নিরীহ তবে আকার বা রঙ পরিবর্তন হলে ডাক্তার দেখানো উচিত। মনে রাখবেন, এটি শুধুমাত্র একটি প্রাথমিক ধারণা। সঠিক রোগ নির্ণয়ের জন্য একজন ডাক্তারের সাথে পরামর্শ করুন।",
    "Vascular Lesion": "ভাস্কুলার লেশন হলো ত্বকের রক্তনালী সংক্রান্ত একটি সমস্যা যা লাল বা বেগুনি দাগ হিসেবে দেখা যায়। এটি সাধারণত জন্মগত বা আঘাতের কারণে হয়। বেশিরভাগ ক্ষেত্রে এটি নিরীহ তবে ডাক্তারের পরামর্শ নেওয়া ভালো। মনে রাখবেন, এটি শুধুমাত্র একটি প্রাথমিক ধারণা। সঠিক রোগ নির্ণয়ের জন্য একজন ডাক্তারের সাথে পরামর্শ করুন।",
}

def get_info(label):
    for key in URGENCY_MAP:
        if key.lower() in label.lower():
            return key, URGENCY_MAP[key]
    return label, {
        "urgency": "🟡 MEDIUM",
        "bangla": label,
        "action": "📅 Please consult a local doctor for proper evaluation."
    }

def get_bangla_explanation(condition_name):
    for key in BANGLA_EXPLANATIONS:
        if key.lower() in condition_name.lower():
            return BANGLA_EXPLANATIONS[key]
    return "এই ত্বকের সমস্যাটি সম্পর্কে একজন বিশেষজ্ঞ ডাক্তারের পরামর্শ নিন। মনে রাখবেন, এটি শুধুমাত্র একটি প্রাথমিক ধারণা। সঠিক রোগ নির্ণয়ের জন্য একজন ডাক্তারের সাথে পরামর্শ করুন।"

st.title("🩺 DermaSheba | ডার্মাসেবা")
st.subheader("AI-powered Skin Condition Awareness Tool")

st.warning("""
⚠️ **Disclaimer:** This tool is for awareness only.
It is NOT a medical diagnosis. Always consult a qualified doctor.
""")

st.divider()

uploaded_file = st.file_uploader(
    "📸 Upload a clear photo of the skin area",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Analyzing... please wait"):
        results = classifier(img)
        top = results[0]
        label = top["label"]
        confidence = top["score"] * 100
        condition_name, info = get_info(label)

    st.divider()
    st.subheader("📊 Result")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Detected Condition", condition_name)
        st.metric("In Bangla", info["bangla"])
    with col2:
        st.metric("Confidence", f"{confidence:.1f}%")
        st.metric("Urgency Level", info["urgency"])

    st.markdown("### 👉 What to do next:")
    st.markdown(f"**{info['action']}**")

    st.divider()

    explanation = get_bangla_explanation(condition_name)
    st.subheader("📝 বাংলায় ব্যাখ্যা")
    st.info(explanation)

    st.divider()
    st.error("""
🚨 **If you are concerned, please visit:**
- Your nearest **Upazila Health Complex**
- **Dhaka Medical College Hospital** — Dermatology Dept
- **BIRDEM Hospital** or any certified dermatologist
    """)