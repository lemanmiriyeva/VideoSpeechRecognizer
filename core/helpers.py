# import os

# def handle_uploaded_file(video,token):
#     path = os.getcwd()
#     os.chdir(f"{path}/media")
#     with open(f'{token}.mp4', 'wb+') as destination:
#         for chunk in video.chunks():
#             destination.write(chunk)