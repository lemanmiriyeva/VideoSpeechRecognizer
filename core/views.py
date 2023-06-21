import os
from django.shortcuts import render
import speech_recognition as sr 
import moviepy.editor as mp
from pathlib import Path
import pafy
import textwrap
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from unidecode import unidecode

def home(request):
    if request.method == 'POST':
        token = str(request.COOKIES.get('csrftoken')).lower()
        if os.path.exists(f"media/{token}.wav"):
            i = 2
            while os.path.exists(f"media/{token}({i}).wav"):
                i += 1
            token = f'{token}({i})'
            
        if os.path.exists(f"media/{token}.txt"):
            i = 2
            while os.path.exists(f"media/{token}({i}).txt"):
                i += 1
            token = f'{token}({i})'
            
        try:
            uploadfrom = request.POST.get('uploadfrom')
            if uploadfrom == 'device':
                uploaded_video = request.FILES.get('video')
                if not uploaded_video:
                    return render(request,'home.html',context={'download':False,'error':True,'message':'Please upload a video file.'})
                if  Path(uploaded_video.name).suffix == '.mp4' or  Path(uploaded_video.name).suffix == '.mov' or  Path(uploaded_video.name).suffix == '.m4a':
                    if uploaded_video.size // 1024 // 1024 > 100:
                        return render(request,'home.html',context={'download':False,'error':True,'message':'Please select less than 100MB'})    

                    video = mp.VideoFileClip(uploaded_video.temporary_file_path())
                    video.audio.write_audiofile(os.path.join(settings.MEDIA_ROOT, f'{token}.wav'))             
                    audio = sr.AudioFile(os.path.join(settings.MEDIA_ROOT, f'{token}.wav'))                
                    r = sr.Recognizer()
                    with audio as source:
                        r.adjust_for_ambient_noise(source)  
                        audio_file = r.record(source)
                    text = r.recognize_google(audio_file,language=request.POST.get('lang'))
                    with open(os.path.join(settings.MEDIA_ROOT, f'{token}.txt'),mode ='w',encoding="utf-8") as file: 
                        wrapped = textwrap.fill(text, 100)
                        file.write(wrapped)
                    return render(request,'home.html', context={'download':True,'token':token, 'error':False, 'filename':(uploaded_video.name.split('.'))[0]})
            
                else:
                    return render(request,'home.html',context={'download':False,'error':True,'message':'Please upload only mp4, mov, m4a.'})
            elif uploadfrom == 'youtube':
                ytlink = request.POST.get('video')
                if not ytlink:
                    return render(request,'home.html',context={'download':False,'error':True,'message':'Please paste the video url.'})
                else:
                    video = pafy.new(ytlink)
                    
                if int(video.length) > int(1200) :
                    return render(request,'home.html',context={'download':False,'error':True,'message':'Please select less than 5 minute'})
                else:    
                    bestaudio = video.getbestaudio(preftype='m4a')
                    bestaudio.download(quiet=False, filepath=(f'{settings.MEDIA_ROOT}/{token}.m4a'))
                    raw_audio = mp.AudioFileClip(os.path.join(settings.MEDIA_ROOT, f'{token}.m4a'))
                    raw_audio.write_audiofile(os.path.join(settings.MEDIA_ROOT, f'{token}.wav'))
                    os.remove(os.path.join(settings.MEDIA_ROOT, f'{token}.m4a'))
                    audio = sr.AudioFile(os.path.join(settings.MEDIA_ROOT, f'{token}.wav'))
                    r = sr.Recognizer()
                    with audio as source:
                        r.adjust_for_ambient_noise(source)  
                        audio_file = r.record(source)
                    text = r.recognize_google(audio_file,language=request.POST.get('lang'))
                    
                    with open(os.path.join(settings.MEDIA_ROOT, f'{token}.txt'),mode ='w',encoding="utf-8") as file: 
                        wrapped = textwrap.fill(text, 100)
                        file.write(wrapped)
                        
                    return render(request,'home.html', context={'download':True,'token':token, 'error':False,'filename': video.title})
        except:
            print('execept')
            return render(request,'home.html',context={'download':False,'error':True,'message':'Somthing goes wrong. Try again.'})
        
    return render(request,'home.html',context={'download':False,'error':False})
    
        
        
        




def DownloadMedia(request):
    file_name = request.GET.get('filename')
    transliterated_file_name = unidecode(file_name)
    if os.path.exists(f'media/{request.GET.get("filepath")}'):
        file_path = os.path.join(settings.MEDIA_ROOT, request.GET.get('filepath'))
        with open(file_path, 'rb') as f:
            file_content = f.read()
        response = HttpResponse(file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(transliterated_file_name)
        os.remove(file_path)
        return response
    else:
        return HttpResponse('This file downloaded')



def clean_media(request):
    folder = os.listdir(settings.MEDIA_ROOT)
    for file in folder:
        file_path = os.path.join(settings.MEDIA_ROOT, file)
        creation_time = os.path.getctime(file_path)
        creation_datetime = datetime.fromtimestamp(creation_time)
        now = datetime.now()
        delta = relativedelta(now,creation_datetime)
        if delta.seconds >= 1:
            print('Cleaning media files...')
            os.remove(file_path)
    return HttpResponse('Trash media file cleaned!')