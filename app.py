import os, re, uuid, shutil
import torch, gradio as gr
from audio_utils import clean_ref, merge_audio
from TTS.api import TTS

os.environ["COQUI_TOS_AGREED"] = "1"
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def run_tts(txt, ref_audio, lang):
    chunks = re.split(r'(?<=[.!?])\s+', txt.strip())
    ffmpeg_path = shutil.which("ffmpeg")
    cleaned = clean_ref(ref_audio, ffmpeg_path)
    
    tmps = []
    for c in chunks:
        tmp = f"chk_{uuid.uuid4().hex[:6]}.wav"
        tts.tts_to_file(text=c, speaker_wav=cleaned, language=lang, file_path=tmp)
        tmps.append(tmp)
    
    out_f = "final_output.wav"
    merge_audio(tmps, out_f)
    for x in tmps + [cleaned]: 
        if os.path.exists(x): os.remove(x)
    return out_f, "Generation complete!"

with gr.Blocks() as app:
    gr.Markdown("# 🎙️ XTTS v2 Continuous Narration Pipeline")
    with gr.Row():
        txt = gr.Textbox(label="Text", lines=5)
        ref = gr.Audio(label="Reference", type="filepath")
    btn = gr.Button("Generate")
    out = gr.Audio(label="Output")
    btn.click(run_tts, [txt, ref, gr.Dropdown(["en","ar"], value="en")], [out, gr.Textbox()])

if __name__ == "__main__":
    app.launch()
