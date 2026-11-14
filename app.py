import streamlit as st

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
    if video is None or not question or not answer:
        st.error("Video, question, and answer are required.")
    elif end <= start:
        st.error("End time must be later than start time.")
    else:
        st.success("Valid review!")
        st.write({
            "question": question,
            "answer": answer,
            "evidence_start": start,
            "evidence_end": end,
            "decision": decision,
        })