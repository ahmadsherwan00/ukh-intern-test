from fpdf import FPDF
from flask import send_file
from io import BytesIO

def generate_form_pdf(entry, form_number=1, filename='form_entry.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Internship Form {form_number} Submission", ln=True, align='C')
    pdf.ln(5)

    pdf.set_font("Arial", '', 12)

    # Group fields based on section hints (A, B, C...) if present
    last_section = ""
    for key, value in entry.__dict__.items():
        if key.startswith('_') or value in [None, ""]:
            continue

        # Try to extract section label if applicable
        if key.lower().startswith('section_') or key.lower().startswith('part_'):
            section = key.split('_')[1].upper()
            if section != last_section:
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"Section {section}", ln=True)
                pdf.set_font("Arial", '', 12)
                last_section = section

        label = key.replace('_', ' ').title()
        value = str(value)

        # Render field nicely
        if len(value) > 90 or '\n' in value:
            pdf.set_font("Arial", 'B', 12)
            pdf.multi_cell(0, 8, f"{label}:", ln=False)
            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 10, value)
        else:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(60, 10, f"{label}:", ln=False)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, value, ln=True)

    pdf.output(filename)


def generate_all_entries_pdf(entries, form_number, filename="all_entries.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for idx, entry in enumerate(entries, start=1):
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"Form {form_number} - Entry #{idx}", ln=True, align='C')
        pdf.ln(3)
        pdf.set_font("Arial", size=12)

        for key, value in entry.__dict__.items():
            if key.startswith('_') or value in [None, ""]:
                continue

            label = key.replace('_', ' ').title()
            value = str(value)

            if len(value) > 90 or '\n' in value:
                pdf.set_font("Arial", 'B', 12)
                pdf.multi_cell(0, 8, f"{label}:", ln=False)
                pdf.set_font("Arial", '', 12)
                pdf.multi_cell(0, 10, value)
            else:
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(60, 10, f"{label}:", ln=False)
                pdf.set_font("Arial", '', 12)
                pdf.cell(0, 10, value, ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return send_file(
        BytesIO(pdf_bytes),
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )


def download_pdf(filename='form_entry.pdf'):
    return send_file(filename, as_attachment=True)
