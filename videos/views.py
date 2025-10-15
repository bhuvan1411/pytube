from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Video, VideoProgress
from .forms import VideoForm
from channels.models import Channel
from django.http import JsonResponse
from django.utils.timezone import now
import json
# Create your views here.

def video_list(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)
    videos = Video.objects.filter(channel=channel).order_by('order')
    
    progress_dict = {}
    for video in videos:
        try:
            prog = VideoProgress.objects.get(user=request.user, video=video)
            progress_dict[video.id] = prog
        except VideoProgress.DoesNotExist:
            progress_dict[video.id] = None

    return render(request, 'videos/list.html', {
        'channel': channel,
        'videos': videos,
        'progress_dict': progress_dict
    })

@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    # Previous / next video
    previous_video = video.channel.videos.filter(order__lt=video.order).order_by('-order').first()
    next_video = video.channel.videos.filter(order__gt=video.order).order_by('order').first()

    progress = None
    if request.user.is_authenticated:
        from .models import VideoProgress
        try:
            progress = VideoProgress.objects.get(user=request.user, video=video)
        except VideoProgress.DoesNotExist:
            progress = None

    context = {
        'video': video,
        'previous_video': previous_video,
        'next_video': next_video,
        'progress': progress,  # None if not logged in
    }
    return render(request, 'videos/detail.html', context)



@login_required
def save_progress(request, video_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        progress, created = VideoProgress.objects.get_or_create(
            user=request.user,
            video_id=video_id
        )
        progress.current_time = data.get('current_time', 0)
        progress.watched_percentage = data.get('watched_percentage', 0)
        progress.last_watched = now()
        progress.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def convert_to_embed(youtube_url):
    if "watch?v=" in youtube_url:
        video_id = youtube_url.split("v=")[-1].split("&")[0]
        return f"https://www.youtube.com/embed/{video_id}"
    elif "youtu.be/" in youtube_url:
        video_id = youtube_url.split("/")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    return youtube_url


@login_required
def video_create(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.channel = channel
            video.youtube_url = convert_to_embed(video.youtube_url)
            video.save()
            return redirect('videos:video_list', channel_id=channel.id)
    else:
        form = VideoForm()
    return render(request, 'videos/form.html', {'form': form, 'channel': channel})


@login_required
def video_edit(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            video = form.save(commit=False)
            # Convert YouTube URL to embed
            video.youtube_url = convert_to_embed(video.youtube_url)
            video.save()
            return redirect('videos:video_detail', video_id=video.id)
    else:
        form = VideoForm(instance=video)
    return render(request, 'videos/form.html', {'form': form, 'video': video})


@login_required
def video_delete(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        video.delete()
        return redirect('videos:video_list', channel_id=video.channel.id)
    return render(request, 'videos/confirm_delete.html', {'video': video})
