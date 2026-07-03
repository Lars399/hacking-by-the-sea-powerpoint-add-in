import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dataclasses import asdict

# Zorg dat Python in de huidige map zoekt naar de scripts
current_dir = Path(__file__).parent.resolve()
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

# IMPORT AANPASSING: We importeren direct 'PDFAccessibilityChecker'
from checker import AccessibilityChecker as PptxAccessibilityChecker
from pdf_checker import PDFAccessibilityChecker  # <-- Dit is de juiste naam!

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# INITIALISATIE AANPASSING: Gebruik de juiste klassenaam
pptx_checker = PptxAccessibilityChecker()
pdf_checker = PDFAccessibilityChecker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Geen bestand geselecteerd'}), 400
    
    file = request.files['file']
    file_type = request.form.get('type')  # 'pptx' of 'pdf'
    
    if file.filename == '':
        return jsonify({'error': 'Geen bestand gekozen'}), 400

    # Sla het bestand tijdelijk op in de uploads map
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    path_obj = Path(filepath)

    try:
        if file_type == 'pptx':
            # Roep de PowerPoint-checker aan
            raw_findings = pptx_checker.check_pptx(path_obj)
            findings = [asdict(f) for f in raw_findings]
            
        elif file_type == 'pdf':
            # Roep de PDF-checker aan. 
            # Note: als jouw PDF-klasse een andere methodenaam gebruikt (bijv. check_pdf ipv check_pptx), pas dit hieronder dan aan!
            raw_findings = pdf_checker.check_pdf(path_obj) 
            findings = [asdict(f) for f in raw_findings]
            
        else:
            return jsonify({'error': 'Onbekend bestandstype'}), 400
            
        return jsonify({'findings': findings})

    except Exception as e:
        return jsonify({'error': f"Er ging iets mis tijdens de controle: {str(e)}"}), 500
        
    finally:
        # Netjes het tijdelijke bestand opruimen
        if path_obj.exists():
            os.remove(path_obj)

if __name__ == '__main__':
    app.run(debug=True)