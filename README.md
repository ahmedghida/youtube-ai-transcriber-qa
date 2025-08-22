# YouTube Video Transcription & Q/A Tool

A **full-stack AI-powered application** to extract, transcribe, and analyze YouTube video content.
This tool intelligently handles subtitles or audio transcription and can generate **challenging, compound question-answer pairs** using large language models.

---

## Features

* **YouTube Video Processing**

  * Extract video metadata, subtitles, and audio.
  * Download audio as MP3.

* **Automatic Transcription**

  * Converts video/audio into text using STT models (OpenAI/Whisper).
  * Supports multiple languages including Arabic and English.

* **Advanced Q\&A Generation**

  * Extracts **multi-part, information-rich Q\&A pairs** from video content.
  * Ensures detailed answers using structured LLM prompts.

* **Token & Cost Tracking**

  * Displays **input/output tokens and estimated LLM costs** for each request.

* **Containerized Deployment**

  * Backend: FastAPI
  * Frontend: Streamlit
  * Reverse proxy: Nginx
  * Fully orchestrated with Docker Compose

---

## Project Structure

```
.
├── backend
│   ├── Dockerfile
│   ├── main.py
│   ├── models
│   ├── services
│   └── requirements.txt
├── frontend
│   ├── Dockerfile
│   ├── app.py
│   ├── Config
│   ├── services
│   └── requirements.txt
├── docker-compose.yml
├── nginx.conf
└── README.md
```

---

## Installation

### Prerequisites

* Docker & Docker Compose installed
* Internet connection (for YouTube API and OpenAI API access)
* OpenAI API key (for STT & LLM models)

### Run Locally

1. Clone the repository:

```bash
git clone https://github.com/your-username/youtube-transcription-qa.git
cd youtube-transcription-qa
```

2. Set API keys in `frontend/Config/config.py` or through environment variables.

3. Build and run containers:

```bash
docker-compose up --build
```

4. Open your browser:

```
http://localhost
```

Nginx routes to the Streamlit frontend.

---

## Usage

1. **Input a YouTube video URL**.

2. **Select options**:

   * Download Audio
   * Generate Transcription/Subtitles
   * Generate Q\&A

3. **View Results**:

   * Tab 1: Readable Markdown output
   * Tab 2: Raw JSON output
   * Download audio if selected

4. **Advanced Metrics**:

   * Tokens used
   * Input/output cost per model
   * Total cost

---

## API Endpoints

* `POST /subtitle` → Extract subtitles from video.
* `POST /download-audio` → Download audio as MP3.
* `POST /full-app` → Full pipeline: subtitles → STT → Q\&A

---

## Docker Compose Tips

### Stop Containers (Without Removing Them)

```bash
docker-compose stop
```

* Stops all running containers but **does not remove** them.
* Useful if you want to temporarily halt the app and resume later.

### Restart Stopped Containers

```bash
docker-compose start
```

* Restarts containers that were previously stopped using `docker-compose stop`.
* Useful for resuming your app **without rebuilding**.

### Full Rebuild & Run

```bash
docker-compose up --build
```

* Rebuilds images if there are changes and starts all containers from scratch.

### Custom Container Names

```bash
docker-compose -p my_custom_project_name up --build
```

* Containers will be prefixed with `my_custom_project_name` instead of the default directory name.
* Example: `my_custom_project_name_frontend`, `my_custom_project_name_backend`, `my_custom_project_name_nginx`.
* Useful for running **multiple instances** on the same machine.

---

## Technologies Used

* Python 3.12
* FastAPI, Uvicorn
* Streamlit
* Docker & Docker Compose
* Nginx reverse proxy
* OpenAI LLMs & Whisper
* pytube, yt-dlp, youtube-transcript-api

---

## Highlights

* Full **containerized AI solution** ready for production.
* Modular and **scalable architecture**.
* Intelligent fallback: **subtitles → audio → STT**.
* Advanced **LLM-driven question-answering**.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


