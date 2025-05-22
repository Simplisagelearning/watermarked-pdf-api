from flask import Flask, request, send_file
import fitz  # PyMuPDF
import os
from datetime import datetime
import uuid

app = Flask(__name__)

@app.route('/watermark', methods=['POST'])
def watermark():
    data = request.get_json()
    customer = data.get("customer")
    email = data.get("email")

    order_number = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:5]}"
    input_pdf = "original_pdf.pdf"
    output_pdf = f"temp/watermarked_{order_number}.pdf"

    doc = fitz.open(input_pdf)
    for page in doc:
        page.insert_text((50, 50), f"Order: {order_number}\n{email}", fontsize=12, opacity=0.5)
    doc.save(output_pdf)

    return send_file(output_pdf, as_attachment=True)

if __name__ == '__main__':
   import os
port = int(os.environ.get("PORT", 10000))
app.run(host='0.0.0.0', port=port)
