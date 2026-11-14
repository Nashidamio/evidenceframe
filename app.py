import csv
from io import StringIO

import streamlit as st

# Keep reviews while this browser session is active.
if "reviews" not in st.session_state:
    st.session_state.reviews = []

st.title("EvidenceFrame")
st.write("Check whether a video supports a proposed answer.")

video = st.file_uploader("Upload an MP4 video", type=["mp4"])
question = st.text_input("Question")
answer = st.text_input("Proposed answer")
start = st.number_input("Evidence starts at (seconds)", min_value=0.0)
end = st.number_input("Evidence ends at (seconds)", min_value=0.0)
decision = st.selectbox("Decision", ["Approve", "Reject", "Needs review"])

if video is not None:
    st.video(video)

if st.button("Record review"):
    if video is None or not question.strip() or not answer.strip():
        st.error("Video, question, and answer are required.")
    elif end <= start:
        st.error("End time must be later than start time.")
    else:
        review = {
            "video": video.name,
            "question": question.strip(),
            "answer": answer.strip(),
            "evidence_start": start,
            "evidence_end": end,
            "decision": decision,
        }
        st.session_state.reviews.append(review)
        st.success("Review recorded!")

if st.session_state.reviews:
    st.subheader("Recorded reviews")
    st.dataframe(st.session_state.reviews)

    output = StringIO()
    columns = [
        "video", "question", "answer",
        "evidence_start", "evidence_end", "decision"
    ]
    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()
    writer.writerows(st.session_state.reviews)

    st.download_button(
        "Download reviews as CSV",
        data=output.getvalue().encode("utf-8-sig"),
        file_name="evidenceframe_reviews.csv",
        mime="text/csv",
    )