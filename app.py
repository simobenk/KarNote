from flask import Flask, render_template, request, url_for, send_from_directory, redirect, jsonify, send_file
import os
from dotenv import load_dotenv

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
import extraire
import prop
import renamme
from PyPDF2 import PdfReader, PdfWriter
import propprof
import renammeprof
from reportlab.lib.pagesizes import letter
import google.generativeai as genai

app = Flask(__name__)

load_dotenv()

####
##LOGIN
####

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

####
##LOGIN
users = {
    'mohamed.benkirane@gmail.com': {'password': 'password', 'type': 'student'},
    'professeur@gmail.com': {'password': 'password', 'type': 'professor'}
}
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        user_type = users[username]['type']
        if user_type == 'student':
            # Redirection vers l'interface étudiant
            return redirect(url_for('indexetu'))
        elif user_type == 'professor':
            # Redirection vers l'interface professeur
            return redirect(url_for('indexprof'))
    # Si l'authentification échoue ou le type d'utilisateur n'est pas reconnu, afficher un message d'erreur
    return render_template('index.html', error='Invalid username or password.')
#### end

####
##PROF
####

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PROCESSED_FOLDER'] = 'static/prof/mes_fichiers/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)


@app.route('/indexprof')
def indexprof():
    return render_template('indexprof.html')

@app.route('/get_files')
def get_files():
    folder_path = app.config['UPLOAD_FOLDER']
    files = os.listdir(folder_path)
    return jsonify(files)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    js_variable = data['js_variable']
    print(f"Received text: {js_variable}")  # Affiche le texte reçu dans la console

    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    
    styles = getSampleStyleSheet()
    style = styles['Normal']
    
    story = [Paragraph(js_variable, style)]
    
    doc.build(story)
    
    return jsonify({"status": "success", "message": "PDF generated", "path": pdf_path})

@app.route('/coursprof')
def coursprof():
    if not os.path.exists(outputt):
        return render_template('coursprof.html', speech="Aucun fichier n'a été uploadé")
    speech = extraire.extract_text_from_pdf(outputt)
    return render_template('coursprof.html', speech=speech)

@app.route('/synthese')
def synthese():
    return render_template('synthese.html')

@app.route('/mon_profilprof')
def mon_profilprof():
    return render_template('mon_profilprof.html')

def process_pdf(input_path, output_path):
    with open(input_path, 'rb') as infile:
        reader = PdfReader(infile)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        with open(output_path, 'wb') as outfile:
            writer.write(outfile)
outputt = os.path.join(os.getcwd(), 'uploads', 'output.pdf')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and file.filename.endswith('.pdf'):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            propprof.process(filepath, outputt)
            # Utiliser des chemins relatifs
            mes_fichiers_path = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
            renammeprof.rename_pdf_files(mes_fichiers_path, "temp.pdf", "Synthese du cours  " + filename)
            renammeprof.delete_file(mes_fichiers_path, "temp.aux")
            renammeprof.delete_file(mes_fichiers_path, "temp.log")
            renammeprof.delete_file(mes_fichiers_path, "temp.tex")
            return redirect(url_for('view_processed_file1', filename="Synthese du cours  " + filename))
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/prof/view_pdf_linkprof/<filename>', methods=['GET'])
def view_processed_file1(filename):
    file_url = url_for('static', filename='mes_fichiers/' + filename)
    return render_template('view_pdf_linkprof.html', file_url=file_url)



def approve_summary(filename):
    filepath = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    
    # Assuming extraire.deplacer_pdf is a function that moves the file
    target_path = os.path.join(app.config['APPROVED_FOLDER'], filename)
    extraire.deplacer_pdf(filepath, target_path)
    
    # Optionally, you can print the filepath for debugging purposes
    print(filepath)
    
    return jsonify({'message': 'File approved successfully'})

# Define another route for serving static files if needed
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
    




@app.route('/prof/download/<filename>', methods=['GET'])
def download_processed_file(filename):
    filepath = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "Processed file not found"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)
###############################
@app.route('/seul')
def seul():
    speech=extraire.extract_text_from_pdf(outputt)
    return render_template('seul.html',speech=speech)
@app.route('/upload2', methods=['GET', 'POST'])
def upload_file2():
    if outputt !=0:
            propprof.resumee(outputt)
            # Utiliser des chemins relatifs
            mes_fichiers_path = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
            renammeprof.rename_pdf_files1(mes_fichiers_path, "temp.pdf", "RESUME DU SPEECH.pdf")
            renammeprof.delete_file(mes_fichiers_path, "temp.aux")
            renammeprof.delete_file(mes_fichiers_path, "temp.log")
            renammeprof.delete_file(mes_fichiers_path, "temp.tex")
            return redirect(url_for('view_processed_file1', filename="RESUME DU SPEECH.pdf"))
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

#######
@app.route('/seul1')
def seul1():
    speech=extraire.extract_text_from_pdf(outputt)
    return render_template('seul1.html',speech=speech)
@app.route('/upload3', methods=['GET', 'POST'])
def upload_file3():
    if outputt !=0:
            propprof.enrichir(outputt)
            # Utiliser des chemins relatifs
            mes_fichiers_path = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
            renammeprof.rename_pdf_files1(mes_fichiers_path, "temp.pdf", "RESUME ENRECHI DU SPEECH.pdf")
            renammeprof.delete_file(mes_fichiers_path, "temp.aux")
            renammeprof.delete_file(mes_fichiers_path, "temp.log")
            renammeprof.delete_file(mes_fichiers_path, "temp.tex")
            return redirect(url_for('view_processed_file1', filename="RESUME ENRECHI DU SPEECH.pdf"))
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''    

########

@app.route('/st')
def st():
    speech=extraire.extract_text_from_pdf(outputt)
    return render_template('st.html',speech=speech)
    
@app.route('/upload4', methods=['GET', 'POST'])
def upload_file4():
    if outputt !=0:
            propprof.st(outputt)
            # Utiliser des chemins relatifs
            mes_fichiers_path = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
            renammeprof.rename_pdf_files1(mes_fichiers_path, "temp.pdf", "SPEECH TRAITE.pdf")
            renammeprof.delete_file(mes_fichiers_path, "temp.aux")
            renammeprof.delete_file(mes_fichiers_path, "temp.log")
            renammeprof.delete_file(mes_fichiers_path, "temp.tex")
            return redirect(url_for('view_processed_file1', filename="SPEECH TRAITE.pdf"))
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''    





####
##PROF
####END




####
##ETUDIANT
####

PDF_FOLDER = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
PDF_FOLDER1 = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
PDF_FOLDER8 = os.path.join(os.getcwd(), 'static', 'mes_fichiers')

@app.route('/indexetu')
def indexetu():
    return render_template('indexetu.html')

@app.route('/cours')
def cours():
    pdf_files = [f for f in os.listdir(PDF_FOLDER8) if f.endswith('.pdf')]
    pdf_files_with_urls = {}
    for pdf in pdf_files:
        # Replace with actual logic to generate URLs for each PDF
        pdf_files_with_urls[pdf] = f"static/cours/"+pdf
    return render_template('cours.html', pdf_files=pdf_files_with_urls)

@app.route('/mes_documents/<path:filename>')
def download_pdf1(filename):
    # Téléchargement du fichier PDF depuis le dossier PDF_FOLDER
    return send_from_directory(PDF_FOLDER, filename, as_attachment=True)

@app.route('/inserer_notes')
def inserer_notes():
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')]
    return render_template('inserer_notes.html', pdf_files=pdf_files)

@app.route('/mes_stats')
def mes_stats():
    return render_template('mes_stats.html')

@app.route('/mon_profil')
def mon_profil():
    return render_template('mon_profil.html')

@app.route('/probleme')
def     probleme():
    pdf_folder = os.path.join(app.static_folder, 'cours')
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    return render_template('Problème.html', pdf_files=pdf_files)

@app.route('/handle_probleme', methods=['POST'])
def handle_probleme():
    data = request.get_json()
    filename = request.json.get('filename')
    pdf_folder = os.path.join(app.static_folder, 'cours')
    full_path = os.path.join(pdf_folder, filename)
    data = request.get_json()
    color_name = data.get('colorName')
    print(color_name)
    if full_path!="":
        result = prop.xensfinal2(full_path,color_name)
        # Utiliser des chemins relatifs
        mes_fichiers_path = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
        renamme.rename_pdf_files(mes_fichiers_path, "temp.pdf", "PROBLEME DU COURS "+filename)
        renamme.delete_file(mes_fichiers_path, "temp.aux")
        renamme.delete_file(mes_fichiers_path, "temp.log")
        renamme.delete_file(mes_fichiers_path, "temp.tex")
        return jsonify({'redirect_url': url_for('view_processed_file',filename= "PROBLEME DU COURS "+filename)})
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/downloadP/<filename>')
def downloadP(filename):
    pdf_folder = os.path.join(app.static_folder, 'cours')
    return send_from_directory("static/mes_fichiers", "PROBLEME DU COURS "+filename, as_attachment=True)

@app.route('/quiz')
def quiz():
    pdf_folder = os.path.join(app.static_folder, 'cours')
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    return render_template('quiz.html', pdf_files=pdf_files)

@app.route('/handle_quizfinal', methods=['POST'])
def handle_quizfinal():
    data = request.get_json()
    filename = data.get('filename')
    color_name = data.get('colorName')
    pdf_folder = os.path.join(app.static_folder, 'cours')
    full_path = os.path.join(pdf_folder, filename)
    
    print(color_name)
    if full_path:
        result = prop.quizfinal(full_path, color_name)
        new_filename = "QUIZ DU COURS " + filename
        # Utiliser des chemins relatifs
        mes_fichiers_path = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
        renamme.rename_pdf_files(mes_fichiers_path, "temp.pdf", new_filename)
        renamme.delete_file(mes_fichiers_path, "temp.aux")
        renamme.delete_file(mes_fichiers_path, "temp.log")
        renamme.delete_file(mes_fichiers_path, "temp.tex")
        
        return jsonify({'redirect_url': url_for('view_processed_file', filename=new_filename)})
    
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/download/<filename>')
def download(filename):
    pdf_folder = os.path.join(app.static_folder, 'cours')
    return send_from_directory("static/mes_fichiers", "QUIZ DU COURS "+filename, as_attachment=True)

@app.route('/mes_documents')
def mes_documents():
    pdf_files = [f for f in os.listdir(PDF_FOLDER8) if f.endswith('.pdf')]
    fp=["/static/mes_fichiers/"+f for f in pdf_files]
    return render_template('mes_documents.html', pdf_files=pdf_files,fp=fp, zip=zip)

@app.route('/mes_documents/<path:filename>')
def download_pdf(filename):
    # Téléchargement du fichier PDF depuis le dossier PDF_FOLDER
    return send_from_directory(PDF_FOLDER, filename, as_attachment=True)


#################@app.route('/list_pdf_files')
PDF_FOLDER = os.path.join(os.getcwd(), 'static', 'syntheses')
app.config['UPLOAD_FOLDER2'] = os.path.join(os.getcwd(), 'static', 'mes_transcription')
@app.route('/enrechir', methods=['GET', 'POST'])
def enrechir():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        selected_file_path = os.path.join("static", "syntheses", request.form.get('selectedFilePath'))
        if file.filename == '':
            return 'No selected file'
        if file and file.filename.endswith('.jpg'):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER2'], filename)
            print(filepath)
            score = prop.enrechir_final(filepath, selected_file_path)
            # Utiliser des chemins relatifs
            mes_fichiers_path = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
            renamme.rename_pdf_files(mes_fichiers_path, "temp.pdf", "Resumé de la note perso.pdf")
            renamme.delete_file(mes_fichiers_path, "temp.aux")
            renamme.delete_file(mes_fichiers_path, "temp.log")
            renamme.delete_file(mes_fichiers_path, "temp.tex")
            return redirect(url_for('vieww', filename="Resumé de la note perso.pdf", score=score))
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/view/<filename>', methods=['GET'])
def view_processed_file(filename):
    file_url = url_for('static', filename='mes_fichiers/' + filename)
    score = request.args.get('score', None)
    return render_template('view_pdf_link.html', file_url=file_url,score=score)

@app.route('/vieww/<filename>', methods=['GET'])
def vieww(filename):
    file_url = url_for('static', filename='mes_fichiers/' + filename)
    score = request.args.get('score', None)
    return render_template('view.html', file_url=file_url,score=score)


###########
app.config['UPLOAD_FOLDER4'] = 'static/cours'
@app.route('/inserer_cours')
def inserer_cours():
    return render_template('inserer_cours.html')
@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        
        if file.filename == ''  :
            return 'No selected file'
        if file and file.filename.endswith('.pdf'):
            filename = file.filename
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER4'], filename)
            print(filepath)
            prop.resume4(filepath)       
            # Utiliser des chemins relatifs
            mes_fichiers_path = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
            renamme.rename_pdf_files(mes_fichiers_path, "temp.pdf", "Resumé de votre document"+filename)
            renamme.delete_file(mes_fichiers_path, "temp.aux")
            renamme.delete_file(mes_fichiers_path, "temp.log")
            renamme.delete_file(mes_fichiers_path, "temp.tex")
            return redirect(url_for('view_processed_file', filename="Resumé de votre document"+filename))
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



###############
###########
app.config['UPLOAD_FOLDER5'] = 'static/mes_cours'
@app.route('/inserer_td')
def inserer_td():
    return render_template('inserer_td.html')
@app.route('/td', methods=['GET', 'POST'])
def td():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        
        if file.filename == ''  :
            return 'No selected file'
        if file and file.filename.endswith('.pdf'):
            filename = file.filename
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER5'], filename)
            print(filepath)
            prop.td(filepath)       
            # Utiliser des chemins relatifs
            mes_fichiers_path = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
            renamme.rename_pdf_files(mes_fichiers_path, "temp.pdf", "Exercices comme le TD"+filename)
            renamme.delete_file(mes_fichiers_path, "temp.aux")
            renamme.delete_file(mes_fichiers_path, "temp.log")
            renamme.delete_file(mes_fichiers_path, "temp.tex")
            return redirect(url_for('view_processed_file', filename="Exercices comme le TD"+filename))
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

####
##ETUDIANT
#### END

@app.route('/api/get-openai-key')
@login_required  # Assurez-vous que l'utilisateur est authentifié
def get_openai_key():
    return jsonify({
        'apiKey': os.getenv('OPENAI_API_KEY')
    })

@app.route('/api/get-gemini-response', methods=['POST'])
@login_required
def get_gemini_response():
    message = request.json.get('message')
    
    # Configuration de Gemini avec la clé API depuis les variables d'environnement
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(message)
        return jsonify({
            'reply': response.text
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
