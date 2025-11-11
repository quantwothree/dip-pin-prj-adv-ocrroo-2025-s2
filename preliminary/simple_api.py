"""Provides a simple API for your basic OCR client

Drive the API to complete "interprocess communication"

Requirements
"""

from fastapi import FastAPI, HTTPException
from fastapi import Response
from pydantic import BaseModel
from pathlib import Path
from library_basics import CodingVideo


app = FastAPI()


# We'll create a lightweight "database" for our videos
# You can add uploads later (not required for assessment)
# For now, we will just hardcode are samples
# VIDEOS: dict[str, Path] = {
#     "demo": Path("../resources/oop.mp4")
# }

VIDEOS: dict[str, Path] = {
    "demo": Path(__file__).resolve().parent.parent / "resources" / "oop.mp4"
}

class VideoMetaData(BaseModel):

#BaseModel is used to define data models with type hints
#Could think of it like Models in Laravel

    fps: float
    frame_count: int
    duration_seconds: float
    _links: dict | None = None

#Pydantic will automatically validate those attributes againts their expexted data types
#And raises ValidationError if it's not the right data type

@app.get("/video")
def list_videos():
    """List all available videos with HATEOAS-style links."""
    return {
        "count": len(VIDEOS),
        "videos": [
            {
                "id": vid,
                "path": str(path), # Not standard for debug only
                "_links": {
                    "self": f"/video/{vid}",
                    "frame_example": f"/video/{vid}/frame/1.0"
                }
            }
            for vid, path in VIDEOS.items()
        ]
    }
#The reason why the for loop is at the bottom is because this is just a cleaner way to write it
#It does exactly this:
# video_list = []
# for vid, path in VIDEOS.items():
#     video_list.append({
#         "id": vid,
#         "path": str(path),
#         "_links": {
#             "self": f"/video/{vid}",
#             "frame_example": f"/video/{vid}/frame/1.0"
#         }
#     })


def _open_vid_or_404(vid: str) -> CodingVideo:
    path = VIDEOS.get(vid)
    if not path or not path.is_file():
        raise HTTPException(status_code=404, detail="Video not found")
    try:
        return CodingVideo(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Could not open video {e}")

def _meta(video: CodingVideo) -> VideoMetaData:
    return VideoMetaData(
            fps=video.fps,
            frame_count=video.frame_count,
            duration_seconds=video.duration
    )


@app.get("/video/{vid}", response_model=VideoMetaData)
def video(vid: str):
    video = _open_vid_or_404(vid)
    try:
            meta = _meta(video)
            meta._links = {
                "self": f"/video/{vid}",
                "frames": f"/video/{vid}/frame/{{seconds}}"
            }
            return meta
    finally:
        video.capture.release()


@app.get("/video/{vid}/frame/{t}", response_class=Response)
def video_frame(vid: str, t: float):
    try:
        video = _open_vid_or_404(vid) #This is now a CodingVideo object
        return Response(content=video.get_image_as_bytes(t), media_type="image/png")
    finally:
      video.capture.release()

# TODO: add enpoint to get ocr e.g. /video/{vid}/frame/{t}/ocr
@app.get("/video/{vid}/frame/{t}/ocr")
def video_frame_ocr(vid: str, t: float):
    try:
        video = _open_vid_or_404(vid)
        text = video.get_text_from_time(t)
        return {"text": text}
    finally:
        video.capture.release()