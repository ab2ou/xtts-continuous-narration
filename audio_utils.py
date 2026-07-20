import uuid, wave, subprocess
import numpy as np

def clean_ref(input_wav, ffmpeg_path):
    out_name = f"clean_ref_{uuid.uuid4().hex[:8]}.wav"
    subprocess.run([
        ffmpeg_path, "-y", "-i", input_wav,
        "-af", "highpass=f=80,lowpass=f=12000,silenceremove=start_periods=1:start_duration=0.25:start_threshold=-40dB:stop_periods=-1:stop_duration=0.3:stop_threshold=-40dB",
        "-ac", "1", "-ar", "22050", out_name
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_name

def fade_audio(aud, ms, rate, mode='out', fl=0.85):
    s = int(rate * ms / 1000)
    if s <= 0 or s > len(aud): return aud
    f = np.linspace(1.0 if mode=='out' else fl, fl if mode=='out' else 1.0, s)
    aud = aud.astype(np.float32)
    if mode == 'out': aud[-s:] *= f
    else: aud[:s] *= f
    return aud.astype(np.int16)

def merge_audio(files, out_file):
    final_audio = None
    rate = ch = sw = None
    for f in files:
        with wave.open(f, "rb") as wf:
            rate, ch, sw = wf.getframerate(), wf.getnchannels(), wf.getsampwidth()
            aud = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).copy()
        if final_audio is None: final_audio = aud
        else:
            final_audio = fade_audio(final_audio, 5, rate, 'out')
            aud = fade_audio(aud, 5, rate, 'in')
            final_audio = np.concatenate([final_audio, aud])
    with wave.open(out_file, "wb") as wf:
        wf.setnchannels(ch); wf.setsampwidth(sw); wf.setframerate(rate)
        wf.writeframes(final_audio.tobytes())
