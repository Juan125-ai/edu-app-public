from app.quiz_generator import generate_english_quiz
from app.video_processing import transcribe_english_video
import os

if __name__ == "__main__":
    # Usar la transcripción REAL del video procesado
    video_path = "uploads/test_video.mp4"  # Asegúrate de tener un video real aquí
    
    # Obtener transcripción real
    print("Obteniendo transcripción del video...")
    transcript = transcribe_english_video(video_path)
    
    if "Error" in transcript:
        print(f"\nError en transcripción: {transcript}")
    else:
        print("\nTranscripción obtenida:")
        print(transcript[:200] + "..." if len(transcript) > 200 else transcript)
        
        # Generar quiz basado en la transcripción REAL
        print("\nGenerando preguntas basadas en la transcripción...")
        quiz = generate_english_quiz(transcript)
        
        print("\nGenerated Quiz:")
        print(quiz)