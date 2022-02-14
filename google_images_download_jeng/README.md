# google search images and download
## Introduction
原本由github/hardikvasa開發的google-images-download沒辦法使用了。所以改為下列作者(tsjeng45)的code。

### by tsjeng45 or this repository
- by tsjeng45 [#link](https://github.com/tsjeng45/google_images_download_jeng)
1. Install. `$pip install google-images-download-jeng`
2. Import. `from google_images_download_jeng  import google_images_download`
3. Useage.
```
Search_keyword = '<your keyword>'
Number_download = 100
Output_path = '<your path>'
Downloader = google_images_download.googleimagesdownload()
Downloader.download(
    {
        'keywords':Search_keyword,
        'limit':Number_download,
        'format':'jpg',
        'output_directory':Output_path
    }
)
```

- by this repository
1. Install. Download this repositroy.
2. Import. `import google_images_download`
3. Useage.
```
Search_keyword = '<your keyword>'
Number_download = 100
Output_path = '<your path>'
Downloader = google_images_download.googleimagesdownload()
Downloader.download(
    {
        'keywords':Search_keyword,
        'limit':Number_download,
        'format':'jpg',
        'output_directory':Output_path
    }
)
```

## Reference
- [PyPI] https://pypi.org/project/google-images-download-jeng/
- [github/tsjeng45/google_images_download_jeng] https://github.com/tsjeng45/google_images_download_jeng
- [github/hardikvasa/google-images-download] https://github.com/hardikvasa/google-images-download
