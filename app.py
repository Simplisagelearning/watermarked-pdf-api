from flask import Flask, request, send_file
from datetime import datetime
import uuid
import fitz  # PyMuPDF
import os

app = Flask(__name__)

@app.route('/watermark', methods=['POST'])
def watermark():
    data = request.get_json()
    customer = data.get("customer")
    email = data.get("email")

    if not customer or not email:
        return {"error": "Missing 'customer' or 'email' field"}, 400

    order_number = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:5]}"
    input_pdf = "original_pdf.pdf"
    output_pdf = f"watermarked_{order_number}.pdf"

    # Try opening the PDF
    try:
        doc = fitz.open(input_pdf)
    except Exception as e:
        print("PDF open error:", e)
        return {"error": f"Failed to open PDF: {str(e)}"}, 500

    # Apply watermark to each page
    for page in doc:
        page.insert_text((50, 50), f"Order: {order_number}\n{email}", fontsize=12, opacity=0.5)

    doc.save(output_pdf)

    return send_file(output_pdf, as_attachment=True)

# Run with Render-compatible port
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

