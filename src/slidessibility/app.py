import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dataclasses import asdict

# Zorg dat Python in de huidige map zoekt naar checker.py
current_dir = Path(__file__).parent.resolve()
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

# Importeer nu ZONDER de punt
from checker import AccessibilityChecker

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialispython app.pyeer jouw checker
checker = AccessibilityChecker()

def check_pdf(filepath):
    # TODO: Jouw echte PDF-logica (als je die al hebt)
    # Deze functie retourneert nu nog een simpele tekst/lijst
    return [{"severity": "minor", "rule_id": "PDF_DUMMY", "wcag_criterion": "N.v.t.", "message": f"PDF-check uitgevoerd voor {os.path.basename(filepath)}.", "slide_number": 0, "location": "Document", "fix_hint": "Geen actie vereist."}]

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

    # Sla het bestand tijdelijk op
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    path_obj = Path(filepath)

    try:
        if file_type == 'pptx':
            # Roep jouw exacte script aan
            raw_findings = checker.check_pptx(path_obj)
            # Zet de Finding dataclasses om naar dictionaries zodat Flask ze als JSON kan versturen
            findings = [asdict(f) for f in raw_findings]
        elif file_type == 'pdf':
            findings = check_pdf(filepath)
        else:
            return jsonify({'error': 'Onbekend bestandstype'}), 400
            
        return jsonify({'findings': findings})

    except Exception as e:
        return jsonify({'error': f"Er ging iets mis tijdens de controle: {str(e)}"}), 500
        
    finally:
        # Altijd netjes het geüploade bestand opruimen
        if path_obj.exists():
            os.remove(path_obj)

if __name__ == '__main__':
    app.run(debug=True)