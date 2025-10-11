from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Video
from .forms import VideoForm
from channels.models import Channel
# Create your views here.

def video_list(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)
    videos = Video.objects.filter(channel=channel).order_by('order')
    return render(request, 'videos/list.html', {'channel': channel, 'videos': videos})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    # Get previous video
    previous_video = video.channel.videos.filter(order__lt=video.order).order_by('-order').first()
    # Get next video
    next_video = video.channel.videos.filter(order__gt=video.order).order_by('order').first()

    context = {
        'video': video,
        'previous_video': previous_video,
        'next_video': next_video
    }
    return render(request, 'videos/detail.html', context)


def convert_to_embed(youtube_url):
    """
    Converts standard YouTube URL to embed URL.
    Examples:
    https://www.youtube.com/watch?v=VIDEO_ID -> https://www.youtube.com/embed/VIDEO_ID
    """
    if "watch?v=" in youtube_url:
        video_id = youtube_url.split("v=")[-1].split("&")[0]  # remove extra params
        return f"https://www.youtube.com/embed/{video_id}"
    return youtube_url  # already embed or other URL


@login_required
def video_create(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.channel = channel
            # Convert YouTube URL to embed
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
