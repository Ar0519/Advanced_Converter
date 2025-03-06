# Advanced_Converter

The Advanced Document Converter is a fullstack web application that allows users to convert between different document formats.

It supports:
# Images to PDF
Convert multiple images into a single PDF.

# PDF to Word
Convert DF files to editable Word documents.

# Word to PDF 
Convert Word documents to PDF files.

The application is built using Flask (Python) for the backend and HTML/CSS/JavaScript for the frontend.

# Features

Drag-and-Drop File Upload

Multiple Image to PDF

PDF to Word Conversion

Word to PDF Conversion

Download Converted Files

# Responsive Design
Works seamlessly on both desktop and mobile devices.

# Technologies Used

Frontend:

HTML, CSS, JavaScript

Backend:

Flask (Python)

Libraries:

Pillow (Image processing)

reportlab (PDF generation)

pdf2docx (PDF to Word conversion)

docx2pdf (Word to PDF conversion)

# Screenshots
![WhatsApp Image 2025-03-06 at 08 43 53_258cb918](https://github.com/user-attachments/assets/333ad406-6f1f-4da2-a4a8-ddb7e763e478)

![Screenshot 2025-03-06 090150](https://github.com/user-attachments/assets/d26659e6-1f7b-4a37-b2ea-066d171ae80c)

# How to Use

1. Prerequisites
   
Make sure you have the following installed:

Python 3.x

pip (Python package manager)

2. Installation
Clone the Repository:

bash
Copy
git clone https://github.com/your-username/advanced-document-converter.git
cd advanced-document-converter
Install Dependencies:

bash
Copy
pip install -r requirements.txt
Run the Application:

bash
Copy
python app.py
Access the Application:
Open your browser and go to:

Copy
http://127.0.0.1:5000/
Usage
Upload Files:

Drag and drop files into the upload area or click to select files.

# Supported file types:

Images: .png, .jpg, .jpeg, .gif, .bmp, .tiff

PDF: .pdf

Word: .docx, .doc

Select Conversion Type:

Choose the desired conversion type from the dropdown menu:

Images to PDF

PDF to Word

Word to PDF

# Convert and Download:

Click the Convert button.

Once the conversion is complete, a download link will appear.

Click the link to download the converted file.

# Folder Structure
Copy
advanced-document-converter/
├── app.py                  # Flask backend
├── templates/
│   └── index.html          # Frontend HTML
├── static/
│   ├── styles.css          # Frontend CSS
│   └── script.js           # Frontend JavaScript
├── uploads/                # Folder for uploaded and converted files
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

# Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

Fork the repository.

Create a new branch for your feature or bugfix.

Commit your changes.

Push your branch and submit a pull request.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments
Flask: For providing a lightweight and flexible backend framework.

Pillow: For image processing capabilities.

pdf2docx and docx2pdf: For document conversion functionality.

# Contact
For questions or feedback, feel free to reach out:

Aruneshwaran T

Email: aruneshpvt@gmail.com


Enjoy using the Advanced Document Converter! 🚀


