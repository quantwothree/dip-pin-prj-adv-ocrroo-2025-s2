# Overview
This section contains preliminary familiarisation steps with the core libraries of the project. It is also designed to complement (and satisfy) the performance requirements of the preliminary assessment.

## Required performance demonstration

You must demonstrate your ability at:

- Determining an organisation’s technology, development tools, and UI platform
- Enabling interprocess communication in Python while using third-party libraries and referencing third-party documentation


## Instructions

1. Complete the knowledge section (Word document) available via Blackboard
2. Fork this repository
3. Clone the repository to your local computer
4. Install `uv` and check that it is running with `uv --version`
5. Obtain a video that can be used to test the functionality and place in the `resources/` folder - your instructor will provide you with one
6. Follow the steps in the remainder of the guide insuring your commit to git whenever prompted
7. Submit a `zip` of this repository along with the `.git` folder. **Do not include your `venv/`**. Ensure your submission includes the assessment Word document with all of the questions in it attempted.


## Steps
Complete the steps below and fill in the `> block` sections
> If you see a section like this, fill it in!


### Installing and running OpenCV

1. Examine the `pyproject.toml` what dependencies does it currently identify?
> None
>
2. Create a `.venv` in this folder using `uv venv`
3. Activate the `venv` as instructed by `uv`
4. In order to complete the project, we need to install OpenCV. Fill in the following:
  - What role does OpenCV have in this project?
  > OpenCV allows us to directly interact with any given video by using cv2.VideoCapture
  - What is the `uv pip` command to install OpenCV?
  > `uv pip install opencv-python`
  - What is the URL of this library's git repo?
  > [https://github.com/opencv/opencv-python]
5. Add OpenCV to your project using the `uv add` command:
  > `uv add opencv-python

6. Have the dependencies in the `pyproject.toml` changed? If so, how?
  >Yes, now we have opencv-python>=4.12.0.88 in the dependencies 
  >
7. Why did we use `uv add` over `uv pip`?
  > Because uv add also update the dependencies list automatically 
  >
8. The `numpy` library is required for OpenCV. Should you add an explicit requirement for it? Why/Why not?
  > Yes. Because eventually we will need numpy for opencv to work, therefore adding it to the requirement ensures that
  > if someone else or if we want to bring the project to a different computer, we only need to run 'uv sync' to automatically
  > install everything we need for the project to work
  >
9. Commit the changes so far to git. Use the message `chore: add OpenCV dependency`
10. Go to `preliminary/library_basics.py` and complete the required functionality.
11. Commit your changes with `feat: save video frames`


### Installing and running Tesseract

[Tesseract OCR](https://github.com/tesseract-ocr/tesseract) provides optical character recognition (OCR) functionality needed for the project.

Tesseract consists of both an OCR Engine and a command line program. It is predominantly written in C++.

1. Examine the [Readme](https://github.com/tesseract-ocr/tesseract?tab=readme-ov-file) and find a list of Python wrappers.

2. What is the URL that lists Python wrappers for Tesseract?
  > https://tesseract-ocr.github.io/tessdoc/AddOns

3. Select a Python wrapper. What wrapper did you choose and why? Ensure you address each element below in your answer
> name of the python library: tesserocr 
> how long ago was a commit made to the library: 3 weeks, on Oct 10th 2025
> does it have external dependencies: according to its readme file, it requires libtesseract (>=3.04) and libleptonica (>=1.71)
> how does it suite the project requirements: tesserocr is suitable for this project because it does not require a tesseract executable like 
> pytesseract, we don't need to do OCR on PDFs like tesseract-ocr-wrapper does. And we don't need to work with large datasets either,
> so image2text is overkill. 

4. Use UV to add the dependency to your project and your `pyproject.toml`

5. If your library has additional requirements (e.g. installing tesseract binaries), note it in your README.md

6. Commit the new dependency `chore: add tesseract dependency`

7. Add a new method in `library_basics.py` that returns the text of a given frame/time/image (you decide!)

8. Commit the changes as `feat: OCR an image


### Install and run FastAPI

FastAPI will allow us to enable communication with our OCR service from other processes on the current machine or across a network.

1. Add the requirement for FastAPI using UV. FastAPI has optional requirements so the command is a little different:
`uv add fastapi --extra standard`
2. Commit the new dependency `chore: add FastAPI dependency`
3. Run in development mode using:
`uv run fastapi dev preliminary/simple_api.py`
4. Run the following curl command (may require git bash on Windows):
`curl 127.0.0.1:8000/video`
5. Confirm that a list of videos and URLs is returned by copying the output below:
> {"count":1,"videos":[{"id":"demo","path":"../resources/oop.mp4","_links":{"self":"/video/demo","frame_example":"/video/demo/frame/1.0"}}]}
6. What are the names of the two processes that just communicated?
> It's client-server communication, using HTTP over TCP/IP 
6. Modify the simple_api.py so that it works correctly with your implementation and complete any TODO markers
7. Demonstrate the use of at least two other end points below:
> First endpoint: /video/{vid}/frame/{t}
> 
> This endpoint serves the frame at a requested time point as an image 
> When we have a GET request at 127.0.0.1:8000/video/demo/frame/4, video_frame() gets called which calls _open_vid_or_404() with the provided 'vid'.
> The 'vid' is found inside VIDEOS by _open_vid_or_404(), and it returns a CodingVideo object. 
> Then video_frame() calls get_image_as_bytes() on that CodingVideo object with the specified time 't' to return the video frame as raw bytes 
> This results in an image of the video frame being generated 
> 
> Second endpoint: /video/{vid}/frame/{t}/ocr
> 
> This endpoint serves a GET request, for example, at 127.0.0.1:8000/video/demo/frame/4/ocr
> It does the exact same thing as the endpoint above but rather than returning a Response with raw bytes data as an image, this endpoint uses 
> get_text_from_time() to return a dictionary containing the text in the frame at the given time 't' 
> 
> 
>
>
