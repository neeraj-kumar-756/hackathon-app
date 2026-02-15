from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import HRFlowable

def generate_pf_esi_summary(filename="PF_ESI_Monthly_Summary_Feb_2026.pdf", employees=None, company=None):
    if company is None:
        company = {}

    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("PF & ESI MONTHLY CONTRIBUTION SUMMARY - Feb 2026", styles["Heading1"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(HRFlowable(width="100%"))
    elements.append(Spacer(1, 0.2 * inch))

    # Organization Info
    org_data = [
        ["Organization:", company.get('name', "XYZ Pvt Ltd")],
        ["PF Account:", company.get('pf_code', "DL/ABC/12345")],
        ["ESI Code:", company.get('esi_code', "270000000000000001")]
    ]

    org_table = Table(org_data, colWidths=[120, 300])
    org_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    elements.append(org_table)
    elements.append(Spacer(1, 0.3 * inch))

    # PF Contribution Section
    elements.append(Paragraph("PROVIDENT FUND (PF) CONTRIBUTION:", styles["Heading3"]))
    elements.append(Spacer(1, 0.2 * inch))

    pf_headers = ["Employee", "Employee PF (Rs.)", "Employer PF (Rs.)", "Total PF (Rs.)"]
    pf_data = [pf_headers]

    if employees:
        for emp in employees:
            pf_data.append([
                emp.get('name', ''),
                emp.get('emp_pf', '0'),
                emp.get('employer_pf', '0'),
                emp.get('total_pf', '0')
            ])
    else:
        pf_data.append(["Raj Kumar", "900", "900", "1,800"])

    pf_table = Table(pf_data)
    pf_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (1,1), (-1,-1), 'CENTER')
    ]))

    elements.append(pf_table)
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Total PF Due: (Calculated based on above)", styles["Normal"]))
    elements.append(Paragraph("ECR Filed: Yes | Payment Status: Pending (Due: 15th)", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # ESI Section
    elements.append(Paragraph("ESIC CONTRIBUTION (Salary < Rs. 21,000):", styles["Heading3"]))
    elements.append(Spacer(1, 0.2 * inch))

    esi_headers = ["Employee", "Employee ESI (Rs.)", "Employer ESI (Rs.)", "Total ESI (Rs.)"]
    esi_data = [esi_headers]

    if employees:
        for emp in employees:
            esi_data.append([
                emp.get('name', ''),
                emp.get('emp_esi', '0'),
                emp.get('employer_esi', '0'),
                emp.get('total_esi', '0')
            ])
    else:
        esi_data.append(["Raj Kumar", "135", "270", "405"])

    esi_table = Table(esi_data)
    esi_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (1,1), (-1,-1), 'CENTER')
    ]))

    elements.append(esi_table)
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Total ESI Due: (Calculated based on above)", styles["Normal"]))
    elements.append(Paragraph("Payment Status: Pending (Due: 21st)", styles["Normal"]))

    doc.build(elements)

    print("✅ PF & ESI Summary PDF Generated Successfully!")