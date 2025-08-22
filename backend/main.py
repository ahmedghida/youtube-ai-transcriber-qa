import os
from fastapi import FastAPI,HTTPException
from fastapi.responses import FileResponse
from services import QAProcessingAgent,YouTubeContentExtractor,Speech_to_text
from models import RequestSchema,ResponseSchema

app=FastAPI()
yt_extractor=YouTubeContentExtractor()



@app.post("/subtitle", response_model=ResponseSchema)
def get_subtitle(request: RequestSchema):
    watch_url = yt_extractor.get_watchurl(request.url)
    video_id = yt_extractor.extract_videoid(watch_url)

    # Add a default or optional language argument
    result = yt_extractor.fetch_subtitle(video_id, languages=["ar"])  # change as needed

    if result:
        text = " ".join(i.text for i in result.snippets)
        return ResponseSchema(text=text)
    else:
        return ResponseSchema(text=None, QA=None)

    


@app.post("/download-audio")
def download_audio(request: RequestSchema):
    watch_url = yt_extractor.get_watchurl(str(request.url))  # ensure string
    result = yt_extractor.download_audio(
        watch_url
    )
    
    if "error" in result:
        # you could raise an HTTPException instead
        return {"error": result["error"]}
    
    return FileResponse(
        path=result["file"],
        filename="my_audio.mp3",
        media_type="audio/mpeg"
    )

    

@app.post("/full-app", response_model=ResponseSchema)
def Full_app(request: RequestSchema):
    """
    Full pipeline for processing a YouTube video:
    1. Try to fetch subtitles if available.
    2. If no subtitles or STT is requested, download audio (with retries) and run STT.
    3. Optionally generate Q&A from the extracted text.
    """

    watch_url = yt_extractor.get_watchurl(request.url)
    video_id = yt_extractor.extract_videoid(watch_url)

    # --- Try fetching subtitles ---
    subtitle_result = yt_extractor.fetch_subtitle(video_id)
    if subtitle_result:
        text = " ".join(i.text for i in subtitle_result.snippets)

        if request.qa_option:
            agent = QAProcessingAgent(llm_apikey=request.llm_api_key, llm_name=request.llm_name)
            qa_results = agent.QA_generator(text)
            qa_results.text = text
            return qa_results
        else:
            return ResponseSchema(text=text)

    # --- If subtitles not available or STT requested ---
    if request.stt_option:
        max_retries = 3
        audio_result = None
        for attempt in range(1, max_retries + 1):
            audio_result = yt_extractor.download_audio(watch_url)
            if "error" not in audio_result:
                break
            if attempt < max_retries:
                continue  # retry
            else:
                # failed after 3 attempts
                raise HTTPException(status_code=400, detail=f"Audio download failed after {max_retries} attempts: {audio_result['error']}")

        try:
            # STT returns plain string now
            transcript_text = Speech_to_text(
                audio_file_path=audio_result['file'],
                stt_name=request.stt_name,
                stt_api_key=request.stt_api_key
            )

            if request.qa_option:
                agent = QAProcessingAgent(llm_apikey=request.llm_api_key, llm_name=request.llm_name)
                qa_results = agent.QA_generator(transcript_text)
                qa_results.text = transcript_text
                return qa_results
            else:
                return ResponseSchema(text=transcript_text)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"STT failed: {str(e)}")

        finally:
            if os.path.exists(audio_result['file']):
                os.remove(audio_result['file'])

    # --- If neither subtitles nor STT is available ---
    raise HTTPException(status_code=400, detail="No subtitle available and STT option is False")

    

            
        


