import winsound

wav_dir = "./wav/"
wav_level1 = "normal.wav"
wav_level2 = "risky.wav"
wav_level3 = "dangerous.wav"

print(wav_level1)
winsound.PlaySound(wav_dir+wav_level1, winsound.SND_FILENAME)
print(wav_level2)
winsound.PlaySound(wav_dir+wav_level2, winsound.SND_FILENAME)
print(wav_level3)
winsound.PlaySound(wav_dir+wav_level3, winsound.SND_FILENAME)