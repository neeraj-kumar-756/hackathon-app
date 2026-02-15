from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import HRFlowable

def generate_form16(filename="Form16_FY_2025_26.pdf", data=None, company=None):

    if data is None:
        data = {}
    if company is None:
        company = {}
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("FORM 16 - TAX DEDUCTION CERTIFICATE (Part A)", styles["Heading1"]))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph("Certificate under Section 203 of Income Tax Act", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(HRFlowable(width="100%"))
    elements.append(Spacer(1, 0.2 * inch))

    # Employer Details
    employer_data = [
        ["Employer Details", ""],
        ["Name:", company.get('name', "XYZ Pvt Ltd")],
        ["PAN:", company.get('pan', "AAAPZ1234C")],
        ["TAN:", company.get('tan', "DELC12345D")]
    ]

    employer_table = Table(employer_data, colWidths=[120, 300])
    employer_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))

    elements.append(employer_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Employee Details
    employee_data = [
        ["Employee Details", ""],
        ["Name:", data.get('name', "Raj Kumar")],
        ["PAN:", data.get('pan', "ABCPK1234K")],
        ["UAN:", data.get('uan', "100123456789")],
        ["Salary Period:", data.get('period', "FY 2025-26 (April 2025 - March 2026)")]
    ]

    employee_table = Table(employee_data, colWidths=[120, 300])
    employee_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))

    elements.append(employee_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Tax Summary Section
    tax_data = [
        ["PART A - Tax Deduction Summary", ""],
        ["Amount Paid/Credited:", data.get('amount_paid', "Rs. 2,16,000")],
        ["Total TDS Deducted:", data.get('tax_deducted', "Rs. 10,800")],
        ["TDS Deposited with Govt:", data.get('tax_deposited', "Rs. 10,800")],
        ["Standard Deduction:", "Rs. 50,000"],
        ["Taxable Salary:", data.get('taxable_salary', "Rs. 1,55,200")]
    ]

    tax_table = Table(tax_data, colWidths=[200, 220])
    tax_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ]))

    elements.append(tax_table)

    doc.build(elements)

    print("✅ Form 16 PDF Generated Successfully!")