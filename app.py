#Import the necessary library
import yt_dlp
from faster_whisper import WhisperModel
import streamlit as st
import os

def transcribe_youtube(url):
    # Download the video audio as an MP3 file
    options = {
        'format': 'bestaudio',  # Specify audio format only
        'outtmpl': 'audio.mp3',
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

#    st.write("音声再生: " + url)
#    st.audio("audio.mp3", format="mp3")

    model_size = "large-v2"
    #model_size = "small"

    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    #model = WhisperModel(model_size, device="cpu")
    segments, _ = model.transcribe("audio.mp3")
    segments = list(segments)  # The transcription will actually run here.

    # Extract and connect the text from all segments
    connected_text = " ".join(segment.text for segment in segments)

    # Print the connected text
    #print(connected_text)
    #st.write("文字起こしを表示")
    st.write(connected_text)

    # Delete the audio file after downloading
    os.remove("audio.mp3")  # Remove the file

st.title("文字起こしアプリ")
st.header("概要")
st.write("URLを入力してください。文字起こしします。")
url = st.text_input(label = 'YoutubeのURLを入力:  ', value= "https://www.youtube.com/shorts/ACuXn0EQfS0")

if st.button("文字起こし"):
    comment = st.empty()
    comment.write("文字起こしを開始します")
    with st.spinner('Wait for it...'):
      transcribe_youtube(url)
    comment.write("文字起こしが完了しました!!")
