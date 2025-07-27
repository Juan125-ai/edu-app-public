import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app.video_processing import transcribe_english_video
from app.quiz_generator import generate_english_quiz

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB limit

# Crear directorios necesarios
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['video']
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        # Generar nombre único para el archivo
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(video_path)
        
        try:
            # Paso 1: Transcribir el video
            transcript = transcribe_english_video(video_path)
            
            # Paso 2: Generar cuestionario
            quiz = generate_english_quiz(transcript)
            
            # Guardar quiz
            quiz_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_filename}.quiz.txt")
            with open(quiz_path, 'w', encoding='utf-8') as f:
                f.write(quiz)
            
            return redirect(url_for('show_quiz', video_id=unique_filename))
        
        except Exception as e:
            # Manejar errores en el procesamiento
            return f"Error processing video: {str(e)}", 500

@app.route('/quiz/<video_id>')
def show_quiz(video_id):
    quiz_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{video_id}.quiz.txt")
    
    if not os.path.exists(quiz_path):
        return "Quiz not found", 404
    
    with open(quiz_path, 'r', encoding='utf-8') as f:
        quiz_content = f.read()
    
    return render_template('quiz.html', quiz=quiz_content)

if __name__ == '__main__':
    app.run(debug=True)