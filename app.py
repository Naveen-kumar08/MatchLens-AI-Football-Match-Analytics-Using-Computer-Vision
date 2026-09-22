import os
import tempfile
from pathlib import Path
import streamlit as st
from matchlens.pipeline import MatchLensPipeline

st.set_page_config(page_title="MatchLens AI", layout="wide")
st.title("⚽ MatchLens AI")
st.caption("YOLOv8 + ByteTrack + Team Clustering + Homography + Tactical View")

video = st.file_uploader("Upload a football video", type=["mp4", "mov", "avi", "mkv"])

if video:
    if st.button("Run analysis"):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / video.name
            source.write_bytes(video.getbuffer())

            output = Path("outputs") / "matchlens_streamlit.mp4"
            output.parent.mkdir(exist_ok=True)

            with st.spinner("Running detection, tracking and pitch mapping..."):
                MatchLensPipeline("config.yaml").run(str(source), str(output))

            st.success("Analysis complete.")
            st.video(str(output))

            csv_path = output.with_name("tracks.csv")
            if csv_path.exists():
                st.download_button(
                    "Download track CSV",
                    csv_path.read_bytes(),
                    file_name="tracks.csv",
                    mime="text/csv",
                )
