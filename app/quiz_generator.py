from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

def generate_english_quiz(transcript: str) -> str:
    """
    Genera un quiz en inglés basado en una transcripción usando GPT-3.5-turbo
    
    Args:
        transcript (str): Transcripción del video
    
    Returns:
        str: Quiz formateado o mensaje de error
    """
    try:
        # Obtener API key de OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY no encontrada en .env")
            return "Error: OpenAI API key no configurada"
        
        # Crear cliente OpenAI
        client = OpenAI(api_key=api_key)
        
        # Validar transcripción
        if not transcript or len(transcript) < 100:
            logger.warning("Transcripción demasiado corta para generar quiz")
            return "Error: Transcripción demasiado corta para generar preguntas"
        
        # Crear prompt en inglés
        prompt = f"""
        Generate 5 multiple-choice questions in ENGLISH based exclusively on the following video transcript.
        For each question, provide 4 options (A, B, C, D) and indicate the correct answer.

        Format each question as:
        
        Q1: [question text]
        A) [option A]
        B) [option B]
        C) [option C]
        D) [option D]
        Answer: [correct letter]
        
IMPORTANT: The questions MUST be directly based on specific details from the transcript.

        Transcript:
        {transcript}
        """
        
        logger.info("Solicitando generación de quiz a OpenAI...")
        
        # Llamar a la API de OpenAI (versión actualizada)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en educación que crea cuestionarios basados en contenido en video."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        # Extraer y formatear el contenido
        quiz_content = response.choices[0].message.content.strip()
        logger.info("Quiz generado exitosamente")
        
        return quiz_content
        
    except Exception as e:
        logger.exception("Error generando quiz")
        return f"Error: Fallo al generar preguntas - {str(e)}"