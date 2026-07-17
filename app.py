import os
import yt_dlp
import gradio as gr
import spaces

# This decorator satisfies Hugging Face's ZeroGPU requirement so our script can run
@spaces.GPU
def download_video_interface(url):
    output_path = './downloads'
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'ignoreerrors': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            final_file_path = os.path.splitext(filename)[0] + ".mp4"
            
        if os.path.exists(final_file_path):
            return final_file_path, "✨ Success! Your 4K file is ready. Click below to save it."
        else:
            return None, "❌ Error: The file could not be compiled properly."
            
    except Exception as e:
        return None, f"❌ An error occurred: {str(e)}"

with gr.Blocks(title="4K YouTube Downloader") as demo:
    gr.Markdown("# 🎥 Permanent 4K 60fps YouTube Downloader")
    gr.Markdown("Paste your link below to fetch the absolute highest quality stream.")
    
    with gr.Row():
        url_input = gr.Textbox(label="YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
    
    btn = gr.Button("Process 4K File", variant="primary")
    
    status_output = gr.Textbox(label="Status")
    file_output = gr.File(label="Download Your MP4 File Here")
    
    btn.click(fn=download_video_interface, inputs=url_input, outputs=[file_output, status_output])

demo.launch()
