import csv
from io import StringIO

import streamlit as st

# Reviews remain available while this browser session is active.
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

# An issue label makes a negative or uncertain decision actionable.
issue_type = "None"
if decision != "Approve":
    issue_type = st.selectbox(
        "Issue type",
        [
            "Select an issue",
            "Wrong answer",
            "Unsupported by video",
            "Ambiguous question",
            "Insufficient temporal evidence",
            "Other",
        ],
    )

reason = st.text_area("Why did you make this decision?")

if st.button("Record review"):
    if video is None or not question.strip() or not answer.strip() or not reason.strip():
        st.error("Video, question, answer, and decision reason are required.")
    elif end <= start:
        st.error("End time must be later than start time.")
    elif decision != "Approve" and issue_type == "Select an issue":
        st.error("Select an issue type for a rejected or uncertain item.")
    else:
        review = {
            "video": video.name,
            "question": question.strip(),
            "answer": answer.strip(),
            "evidence_start": start,
            "evidence_end": end,
            "decision": decision,
            "issue_type": issue_type,
            "reason": reason.strip(),
        }
        st.session_state.reviews.append(review)
        st.success("Review recorded!")

if st.session_state.reviews:
    st.subheader("Recorded reviews")
    st.dataframe(st.session_state.reviews)

    output = StringIO()
    columns = [
        "video",
        "question",
        "answer",
        "evidence_start",
        "evidence_end",
        "decision",
        "issue_type",
        "reason",
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
