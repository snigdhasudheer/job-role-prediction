import streamlit as st
import pickle
import numpy as np
import pandas as pd

def load_model():
    with open('resume_classifier.pkl', 'rb') as f:
        data = pickle.load(f)
    return data

data=load_model()

clf = data['model']
le = data['label_encoder']
word_vectorizer = data['vectorizer']
common_skills = [
    "python", "java", "c++", "sql", "machine learning", "deep learning",
    "data analysis", "django", "flask", "html", "css", "javascript",
    "react", "nodejs", "nlp", "tensorflow", "keras", "pandas", "numpy",
    "data visualization", "aws", "git", "linux"
]

def show_predict_page():
    st.title("Know the job roles your resume best fit for!!")
    uploaded_file = st.file_uploader("Choose a resume file", type=["docx", "txt"])

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        # Optionally read the text content depending on file type
        file_type = uploaded_file.name.split('.')[-1].lower()

        if file_type == "txt":
            resume_text = uploaded_file.read().decode("utf-8")
        elif file_type == "docx":
            import docx
            doc = docx.Document(uploaded_file)
            resume_text = "\n".join([para.text for para in doc.paragraphs])
        else:
            st.warning("Unsupported file type.")
            return
        matched_skills = [skill for skill in common_skills if skill in resume_text.lower()]
        score = 0

        # Skill points
        score += len(matched_skills) * 5

        # Resume length check
        resume_length = len(resume_text)
        if resume_length > 1000:
            score += 10

        # Clamp score to 100 max and 0 min
        score = max(0, min(score, 100))

        st.text_area("Extracted Resume Text", resume_text, height=300)
        if st.button("Predict Job Role"):
            vector = word_vectorizer.transform([resume_text])

            # Get predicted probabilities
            proba = clf.predict_proba(vector)[0]

            # Get indices of top 3 predictions
            top_n = 3
            top_n_indices = np.argsort(proba)[::-1][:top_n]  # sort in descending order

            st.subheader("Top Role Matches:")
            for idx in top_n_indices:
                role = le.inverse_transform([idx])[0]
                confidence = proba[idx] * 100
                st.write(f"- **{role}** — {confidence:.2f}% confidence")

            st.subheader("📊 Resume Quality Score:")
            st.progress(score)
            st.write(f"Your resume quality score is: **{score}/100**")

            if score >= 80:
                st.success("🔥 Great resume! You're job-ready!")
            elif score >= 50:
                st.info("🙂 Decent resume. Add more details/skills.")
            else:
                st.warning("⚠️ Needs improvement. Try adding more relevant skills.")