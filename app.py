#Import the necessary library
import yt_dlp
from faster_whisper import WhisperModel
import streamlit as st

def transcribe_youtube(url):
    #st.write(url)
    video_url = url

    # Download the video audio as an MP3 file
    options = {
        'format': 'bestaudio',  # Specify audio format only
        'outtmpl': 'audio.mp3',
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    st.write("音声の再生")
    st.write(video_url)
    st.audio("audio.mp3", format="mp3")

    # Fetch YouTube video information
    video_info = yt_dlp.YoutubeDL().extract_info(video_url, download=False)
    video_title = video_info.get('title', 'Unknown Title')
    video_description = video_info.get('description', 'No Description Available')
    video_views = video_info.get('view_count', '0')
    video_likes = video_info.get('like_count', '0')
    video_dislikes = video_info.get('dislike_count', '0')

    # Construct the video sin(segment.text for segment in segments)
    video_summary = f"Title: {video_title}  \nDescription: {video_description}  \nViews: {video_views}  \nLikes: {video_likes}  \nDislikes: {video_dislikes}"

    # Print the video summary
    st.write("Youtube情報を表示します")
    #st.write(video_summary)
    #print(video_summary)

    #model_size = "large-v2"
    model_size = "small"


    # Run on GPU with FP16
    #model = WhisperModel(model_size, device="cuda", compute_type="float16")
    model = WhisperModel(model_size, device="cpu")
    segments, _ = model.transcribe("audio.mp3",initial_prompt=video_summary)
    segments = list(segments)  # The transcription will actually run here.

    # Extract and connect the text from all segments
    connected_text = " ".join(segment.text for segment in segments)

    # Print the connected text
    #print(connected_text)
    st.write("文字起こしを表示します")
    st.write(connected_text)

st.title("文字起こしアプリ")
st.header("概要")
st.write("URLを入力してください。文字起こしします。")
#url = st.text_input('YoutubeのURLを入力',"https://www.youtube.com/shorts/ACuXn0EQfS0")
url = st.text_input(label = 'YoutubeのURLを入力', value= "https://www.youtube.com/shorts/ACuXn0EQfS0")

if st.button("文字起こし"):
    comment = st.empty()
    comment.write("文字起こしを開始します")
    comment.write("文字起こしを開始します")
    #comment.write(url)
    transcribe_youtube(url)
    comment.write("文字起こしが完了しました!!")
