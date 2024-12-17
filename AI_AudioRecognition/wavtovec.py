import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Load model and processor
model = Wav2Vec2ForCTC.from_pretrained("m3hrdadfi/wav2vec2-large-xlsr-persian")
processor = Wav2Vec2Processor.from_pretrained("m3hrdadfi/wav2vec2-large-xlsr-persian")

# Load and preprocess audio file
audio_input, sample_rate = torchaudio.load("user_voice.wav")
resampler = torchaudio.transforms.Resample(sample_rate, 16000)
audio_input = resampler(audio_input).squeeze().numpy()

# Process the input audio and perform inference
inputs = processor(audio_input, sampling_rate=16000, return_tensors="pt", padding=True)
with torch.no_grad():
    logits = model(inputs.input_values).logits
predicted_ids = torch.argmax(logits, dim=-1)

# Decode the output to text
transcription = processor.decode(predicted_ids[0])
print("Transcription:", transcription)