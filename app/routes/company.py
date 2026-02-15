from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.model import Company, db

company_bp = Blueprint('company', __name__)

@company_bp.route('/company', methods=['GET', 'POST'])
def company_settings():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session.get('user_role') != 'admin':
        flash('Unauthorized access.')
        return redirect(url_for('dashboard.dashboard'))

    company = Company.query.first()

    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        gst = request.form.get('gst')
        pan = request.form.get('pan')
        tan = request.form.get('tan')
        pf = request.form.get('pf')
        esi = request.form.get('esi')
        pt_circle = request.form.get('pt_circle')

        if not company:
            company = Company(name=name, address=address, gst_number=gst, pan_number=pan, tan_number=tan, pf_code=pf, esi_code=esi, pt_circle=pt_circle)
            db.session.add(company)
        else:
            company.name = name
            company.address = address
            company.gst_number = gst
            company.pan_number = pan
            company.tan_number = tan
            company.pf_code = pf
            company.esi_code = esi
            company.pt_circle = pt_circle
        
        db.session.commit()
        flash('Company details updated successfully!')
        return redirect(url_for('company.company_settings'))

    return render_template('company.html', company=company)