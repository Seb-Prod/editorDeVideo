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
        name=get_name(video),
        artist=get_artist(video),
        album_artist=get_album_artist(video),
        album=get_album(video),
        genre=get_genre(video),
        year=get_year(video),
        track_number=get_track_number(video),
        show_name=get_show_name(video),
        channel=get_channel(video),
        episode_id=get_episode_id(video),
        tv_season=get_tv_season(video),
        tv_episode=get_tv_episode(video),
        description=get_description(video),
        long_description=get_long_description(video),
        tv_description=get_tv_description(video),
        encoded_by=get_encoded_by(video),
        media_kind=get_media_kind(video),
        image=get_image(video),
        apple_itunes=get_apple_itunes(video)
    )


def get_name(video: MP4) -> str:
    try:
        array = video['©nam']
        return array[0]
    except KeyError:
        return ""


def get_artist(video: MP4) -> str:
    try:
        array = video['\xa9ART']
        return array[0]
    except KeyError:
        return ""


def get_album_artist(video: MP4) -> str:
    try:
        array = video['aART']
        return array[0]
    except KeyError:
        return ""


def get_album(video: MP4) -> str:
    try:
        array = video['\xa9alb']
        return array[0]
    except KeyError:
        return ""


def get_genre(video: MP4) -> str:
    try:
        array = video['\xa9gen']
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


def get_track_number(video: MP4) -> tuple:
    try:
        array = video['trkn']
        return array[0]
    except KeyError:
        return []


def get_show_name(video: MP4) -> str:
    try:
        array = video['tvsh']
        return array[0]
    except KeyError:
        return ""


def get_channel(video: MP4) -> str:
    try:
        array = video['tvnn']
        return array[0]
    except KeyError:
        return ""


def get_episode_id(video: MP4) -> str:
    try:
        array = video['tven']
        return array[0]
    except KeyError:
        return ""


def get_tv_season(video: MP4) -> int:
    try:
        array = video['tvsn']
        return array[0]
    except KeyError:
        return 0


def get_tv_episode(video: MP4) -> int:
    try:
        array = video['tves']
        return array[0]
    except KeyError:
        return 0


def get_description(video: MP4) -> str:
    try:
        array = video['desc']
        return array[0]
    except KeyError:
        return ""


def get_long_description(video: MP4) -> str:
    try:
        array = video['ldes']
        return array[0]
    except KeyError:
        return ""


def get_tv_description(video: MP4) -> str:
    try:
        array = video['sdes']
        return array[0]
    except KeyError:
        return ""


def get_encoded_by(video: MP4) -> str:
    array = video['\xa9too']
    return array[0]


def get_media_kind(video: MP4) -> int:
    try:
        array = video['stik']
        return array[0]
    except KeyError:
        return 0


def get_apple_itunes(video: MP4) -> str:
    try:
        array = video['----:com.apple.iTunes:iTunMOVI']
        return array[0]
    except KeyError:
        return ""


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




    