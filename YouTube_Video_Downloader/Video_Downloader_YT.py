from pytube import YouTube
link = 'https://www.youtube.com/watch?v=WDyoYrNz7VY'
yt = YouTube(link)
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
print('download finished..', link)