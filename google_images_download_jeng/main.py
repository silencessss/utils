from google_images_download_jeng  import google_images_download 


Search_keyword = 'acne'
Number_download = 100
Output_path = 'F:/Google_search_image/'

Downloader = google_images_download.googleimagesdownload()

Downloader.download(
    {
        'keywords':Search_keyword,
        'limit':Number_download,
        'format':'jpg',
        'output_directory':Output_path
    }
)
print('--------------done------------------')
