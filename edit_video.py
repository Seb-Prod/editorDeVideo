import base64
from dataclasses import dataclass
from mutagen.mp4 import MP4
import images


@dataclass
class Metadata:
    name: str
    artist: str
    album_artist: str
    album: str
    genre: str
    year: str
    track_number: tuple
    show_name: str
    channel: str
    episode_id: str
    tv_season: int
    tv_episode: int
    description: str
    long_description: str
    tv_description: str
    encoded_by: str
    media_kind: int
    image: str
    apple_itunes: str


def get_metadata(file: str) -> Metadata:
    video = MP4(file)
    return Metadata(
        name=get_tag(video, '©nam'),
        artist=get_tag(video, '\xa9ART'),
        album_artist=get_tag(video, 'aART'),
        album=get_tag(video, '\xa9alb'),
        genre=get_tag(video, '\xa9gen'),
        year=get_year(video),
        track_number=tuple(get_tag(video, 'trkn')),
        show_name=get_tag(video, 'tvsh'),
        channel=get_tag(video, 'tvnn'),
        episode_id=get_tag(video, 'tven'),
        tv_season=get_tag(video, 'tvsn'),
        tv_episode=get_tag(video, 'tves'),
        description=get_tag(video, 'desc'),
        long_description=get_tag(video, 'ldes'),
        tv_description=get_tag(video, 'sdes'),
        encoded_by=get_tag(video, '\xa9too'),
        media_kind=get_tag(video, 'stik'),
        image=get_image(video),
        apple_itunes=get_tag(video, '----:com.apple.iTunes:iTunMOVI')
    )

def get_tag(video: MP4, key: str) -> str:
    try:
        array = video[key]
        return array[0]
    except KeyError:
        return ""


def get_year(video: MP4) -> str:
    try:
        array = video['\xa9day']
        max_length = 10
        cut = array[0][:max_length] if len(
            array[0]) > max_length else array[10]
        parts = cut.split("-")
        return parts[2] + "-" + parts[1] + '-' + parts[0]
    except KeyError:
        return "15-04-1977"


def get_image(video: MP4):
    try:
        if "covr" in video:
            cover_data = video["covr"][0]  # Récupérer la première image
            base64_cover = base64.b64encode(cover_data).decode("utf-8")
            return base64_cover
        else:
            return images.image_missing
    except KeyError:
        return images.image_missing
