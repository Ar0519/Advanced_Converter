import os
import uuid
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import pdf2docx
import docx2pdf

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'},
    'pdf': {'pdf'},
    'word': {'docx', 'doc'}
}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename, file_type):
    """Check if file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[file_type]

def convert_images_to_pdf(image_paths, output_path):
    """
    Convert list of image paths to a single PDF.
    
    Args:
        image_paths (list): List of image file paths
        output_path (str): Path to save the output PDF
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    for image_path in image_paths:
        try:
            img = Image.open(image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_width, img_height = img.size
            aspect = img_height / img_width
            
            page_width = width - 2*inch
            scaled_width = page_width
            scaled_height = scaled_width * aspect
            
            if scaled_height > height - 2*inch:
                scaled_height = height - 2*inch
                scaled_width = scaled_height / aspect
            
            x_centered = (width - scaled_width) / 2
            y_centered = (height - scaled_height) / 2
            
            c.drawImage(
                image_path, 
                x_centered, 
                y_centered, 
                width=scaled_width, 
                height=scaled_height
            )
            c.showPage()
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
    
    c.save()

def convert_pdf_to_docx(pdf_path, docx_path):
    """
    Convert PDF to DOCX using pdf2docx library.
    
    Args:
        pdf_path (str): Path to input PDF file
        docx_path (str): Path to save output DOCX file
    """
    try:
        print(f"Converting PDF: {pdf_path} to DOCX: {docx_path}")
        converter = pdf2docx.Converter(pdf_path)
        converter.convert(docx_path)
        converter.close()
        return True
    except Exception as e:
        print(f"Error converting PDF to DOCX: {e}")
        return False

def convert_docx_to_pdf(docx_path, pdf_path):
    """
    Convert DOCX to PDF using docx2pdf library.
    
    Args:
        docx_path (str): Path to input DOCX file
        pdf_path (str): Path to save output PDF file
    """
    try:
        print(f"Converting DOCX: {docx_path} to PDF: {pdf_path}")
        docx2pdf.convert(docx_path, pdf_path)
        return True
    except Exception as e:
        print(f"Error converting DOCX to PDF: {e}")
        return False

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads and conversions."""
    conversion_type = request.form.get('conversion_type', '')
    
    if conversion_type not in ['images_to_pdf', 'pdf_to_docx', 'docx_to_pdf']:
        return jsonify({'error': 'Invalid conversion type'}), 400
    
    try:
        unique_id = str(uuid.uuid4())
        
        if conversion_type == 'images_to_pdf':
            if 'images' not in request.files:
                return jsonify({'error': 'No files uploaded'}), 400
            
            files = request.files.getlist('images')
            
            valid_images = []
            for file in files:
                if file and allowed_file(file.filename, 'image'):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
                    file.save(filepath)
                    valid_images.append(filepath)
            
            if not valid_images:
                return jsonify({'error': 'No valid images uploaded'}), 400
            
            output_pdf = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_converted.pdf")
            convert_images_to_pdf(valid_images, output_pdf)
            
            for img_path in valid_images:
                os.remove(img_path)
            
            return jsonify({
                'message': 'Conversion successful', 
                'filename': os.path.basename(output_pdf)
            })
        
        elif conversion_type == 'pdf_to_docx':
            if 'pdf' not in request.files:
                return jsonify({'error': 'No PDF uploaded'}), 400
            
            pdf_file = request.files['pdf']
            
            if not allowed_file(pdf_file.filename, 'pdf'):
                return jsonify({'error': 'Invalid PDF file'}), 400
            
            pdf_filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{pdf_filename}")
            pdf_file.save(pdf_path)
            
            docx_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_converted.docx")
            success = convert_pdf_to_docx(pdf_path, docx_path)
            
            os.remove(pdf_path)
            
            if not success:
                return jsonify({'error': 'Conversion failed'}), 500
            
            return jsonify({
                'message': 'Conversion successful', 
                'filename': os.path.basename(docx_path)
            })
        
        elif conversion_type == 'docx_to_pdf':
            if 'docx' not in request.files:
                return jsonify({'error': 'No DOCX uploaded'}), 400
            
            docx_file = request.files['docx']
            
            if not allowed_file(docx_file.filename, 'word'):
                return jsonify({'error': 'Invalid DOCX file'}), 400
            
            docx_filename = secure_filename(docx_file.filename)
            docx_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{docx_filename}")
            docx_file.save(docx_path)
            
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_converted.pdf")
            success = convert_docx_to_pdf(docx_path, pdf_path)
            
            os.remove(docx_path)
            
            if not success:
                return jsonify({'error': 'Conversion failed'}), 500
            
            return jsonify({
                'message': 'Conversion successful', 
                'filename': os.path.basename(pdf_path)
            })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Serve file for download."""
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename), 
            as_attachment=True
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)