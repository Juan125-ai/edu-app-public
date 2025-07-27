import sys 
import whisper
import os
import logging

# Agregar ruta de FFmpeg al PATH
ffmpeg_path = os.path.join(sys.prefix, "Library", "bin")  # Ruta típica en Conda
os.environ["PATH"] += os.pathsep + ffmpeg_path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transcribe_english_video(video_path: str) -> str:
    """
    Transcribe English video content using Whisper
    Returns the transcription text in English
    
    Args:
        video_path (str): Path to the video file
    
    Returns:
        str: Transcription text or error message
    """
    try:
        # Validate input file
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return "Error: Video file not found"
            
        logger.info(f"Starting transcription for: {video_path}")
        
        # Load the model (base is sufficient for English)
        logger.info("Loading Whisper base model...")
        model = whisper.load_model("base")
        
        # Transcribe with English-specific parameters
        logger.info("Transcribing video...")
        result = model.transcribe(
            video_path,
            language='en',        # Force English language
            task='transcribe',    # Transcription only (no translation)
            verbose=False,        # Disable progress messages
            fp16=False            # Disable FP16 for CPU compatibility
        )
        
        transcript = result["text"].strip()
        logger.info(f"Transcription completed successfully. Length: {len(transcript)} characters")
        
        return transcript
    
    except Exception as e:
        error_msg = f"Transcription error: {str(e)}"
        logger.exception(error_msg)
        return error_msg