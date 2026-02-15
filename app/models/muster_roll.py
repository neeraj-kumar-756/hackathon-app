from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import HRFlowable

def generate_muster_roll(filename="Monthly_Muster_Roll_Feb_2026.pdf", employees=None):

    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # Title
    title_style = styles["Heading1"]
    elements.append(Paragraph("MUSTER ROLL - REGISTER OF WAGES", title_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(HRFlowable(width="100%"))
    elements.append(Spacer(1, 0.2 * inch))

    # Company Info Table
    company_data = [
        ["Organization:", "XYZ Pvt Ltd", "Month:", "February 2026"],
        ["Address:", "Delhi NCR", "PF Account:", "DL/ABC/12345"],
        ["ESI Code:", "270000000000000001", "PT Circle:", "Delhi"]
    ]

    company_table = Table(company_data, colWidths=[90, 150, 90, 120])
    company_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
    ]))

    elements.append(company_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Main Payroll Table
    headers = ["Sl", "Employee Name", "Days Present", "Gross (Rs.)", "Deduction (Rs.)", "Net Pay (Rs.)", "PF (Rs.)", "ESI (Rs.)"]
    payroll_data = [headers]

    if employees:
        for emp in employees:
            payroll_data.append([
                emp.get('sl', ''),
                emp.get('name', ''),
                emp.get('present', '0'),
                emp.get('gross', '0'),
                emp.get('deduction', '0'),
                emp.get('net', '0'),
                emp.get('pf', '0'),
                emp.get('esi', '0')
            ])
    else:
        payroll_data.append(["1", "Raj Kumar", "26", "18000", "500", "17080", "1800", "135"])

    payroll_table = Table(payroll_data, repeatRows=1)
    payroll_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (2,1), (-1,-1), 'CENTER')
    ]))

    elements.append(payroll_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Totals Section
    # Simple static total for now, or calculate if needed
    total_count = len(employees) if employees else 0
    
    totals_data = [
        ["TOTAL", f"{total_count} Employees", "-", "-", "-", "-"]
    ]

    totals_table = Table(totals_data, colWidths=[70, 90, 110, 110, 80, 80])
    totals_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))

    elements.append(totals_table)

    doc.build(elements)

    print("✅ Muster Roll PDF Generated Successfully!")