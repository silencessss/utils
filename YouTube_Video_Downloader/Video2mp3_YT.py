from pytube import YouTube
link = '<Which link you want to download?>'
yt = YouTube(link)
print('download...')

yt.streams.filter().get_audio_only().download(filename='oxxostudio.mp3') # 儲存為 mp3

print('ok!')