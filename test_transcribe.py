from app.video_processing import transcribe_english_video
import os

if __name__ == "__main__":
    # Ruta corregida al video de prueba
    test_video = os.path.join("uploads", "test_video.mp4")
    abs_path = os.path.abspath(test_video)  # Obtener ruta absoluta
    
    print(f"Starting transcription test for: {abs_path}")
    
    # Verificar si el archivo existe
    if not os.path.exists(abs_path):
        print(f"\nERROR: File not found at {abs_path}")
        print("Please place a test video in the 'uploads' folder named 'test_video.mp4'")
    else:
        transcript = transcribe_english_video(abs_path)
        
        print("\nTranscription Result:")
        if transcript and not transcript.startswith("Error"):
            print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
        else:
            print(transcript)