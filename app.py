import os, re, uuid, wave, subprocess, shutil
import numpy as np
import torch
import gradio as gr
from dotenv import load_dotenv
from TTS.api import TTS

load_dotenv()

ffmpeg_path = os.getenv("FFMPEG_PATH") or shutil.which("ffmpeg")
if not ffmpeg_path:
    print("Warning: ffmpeg not found in path")

torch.backends.cudnn.benchmark = True
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Automatically accept the Coqui CPML non-commercial license terms via environment variables
os.environ["COQUI_TOS_AGREED"] = "1"

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def clean_ref(input_wav):
    out_name = f"clean_ref_{uuid.uuid4().hex[:8]}.wav"
    subprocess.run([
        ffmpeg_path, "-y", "-i", input_wav,
        "-af", "highpass=f=80,lowpass=f=12000,silenceremove=start_periods=1:start_duration=0.25:start_threshold=-40dB:stop_periods=-1:stop_duration=0.3:stop_threshold=-40dB",
        "-ac", "1", "-ar", "22050", out_name
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_name

def get_chunks(text, max_len=200):
    text = re.sub(r"\s+", " ", text).strip()
    sents = re.split(r'(?<=[.!?])\s+', text)
    res = []
    curr = ""
    for s in sents:
        if len(curr) + len(s) > max_len:
            if curr: res.append(curr.strip())
            curr = s
        else:
            curr += " " + s
    if curr: res.append(curr.strip())
    return res

def fade_out(aud, ms, rate, fl=0.85):
    s = int(rate * ms / 1000)
    if s <= 0 or s > len(aud): return aud
    f = np.linspace(1.0, fl, s)
    aud = aud.astype(np.float32)
    aud[-s:] *= f
    return aud.astype(np.int16)

def fade_in(aud, ms, rate, fl=0.85):
    s = int(rate * ms / 1000)
    if s <= 0 or s > len(aud): return aud
    f = np.linspace(fl, 1.0, s)
    aud = aud.astype(np.float32)
    aud[:s] *= f
    return aud.astype(np.int16)

def merge_audio(files, out_file):
    final_audio = None
    rate = ch = sw = None
    
    for f in files:
        with wave.open(f, "rb") as wf:
            rate = wf.getframerate()
            ch = wf.getnchannels()
            sw = wf.getsampwidth()
            aud = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).copy()
        
        if final_audio is None:
            final_audio = aud
            continue
        
        final_audio = fade_out(final_audio, 5, rate, 1.2)
        aud = fade_in(aud, 5, rate, 1.2)
        final_audio = np.concatenate([final_audio, aud])

    with wave.open(out_file, "wb") as wf:
        wf.setnchannels(ch)
        wf.setsampwidth(sw)
        wf.setframerate(rate)
        wf.writeframes(final_audio.tobytes())

def run_tts(txt, ref_audio, lang):
    if not txt.strip(): 
        return None, "Error: Text is empty"
    if not ref_audio: 
        return None, "Error: Reference audio missing"

    chunks = get_chunks(txt)
    cleaned = clean_ref(ref_audio)
    
    tmps = []
    with torch.no_grad():
        for c in chunks:
            tmp_out = f"chk_{uuid.uuid4().hex[:6]}.wav"
            tts.tts_to_file(text=c, speaker_wav=cleaned, language=lang, file_path=tmp_out)
            tmps.append(tmp_out)
    
    out_f = "final_output.wav"
    merge_audio(tmps, out_f)

    for x in tmps + [cleaned]:
        if os.path.exists(x): os.remove(x)

    return out_f, f"Done! Generated {len(chunks)} chunks smoothly."

with gr.Blocks() as app:
    gr.Markdown("### XTTS v2 Continuous Narration")
    
    txt_in = gr.Textbox(label="Text input", lines=6)
    ref_in = gr.Audio(label="Reference Audio (WAV)", type="filepath")
    lang_sel = gr.Dropdown(["en", "ar", "fr"], value="en", label="Language")
    
    gen_btn = gr.Button("Generate Audio")
    audio_out = gr.Audio(label="Result", type="filepath")
    status_msg = gr.Textbox(label="Status")
    
    gen_btn.click(
        fn=run_tts, 
        inputs=[txt_in, ref_in, lang_sel], 
        outputs=[audio_out, status_msg]
    )

if __name__ == "__main__":
    app.launch(share=True, debug=True)
