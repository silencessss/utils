from pytube import YouTube
link = '<Which link you want to download?>'
yt = YouTube(link)
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
print('download finished..', link)
