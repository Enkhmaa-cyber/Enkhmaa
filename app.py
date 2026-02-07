from flask import Flask, render_template, request, flash
import re
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "replace-with-secure-key"

EMAIL_REGEX = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
PHONE_REGEX = re.compile(r'^\+?\d{7,15}$')

EXCEL_FILE = 'Register.xlsx'


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        surname = request.form.get('surname', '').strip()
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()

        errors = []
        if not surname:
            errors.append('Овог оруулна уу.')
        if not name:
            errors.append('Нэр оруулна уу.')
        if not PHONE_REGEX.match(phone):
            errors.append('Утасны дугаар буруу. Жишээ: +97699112233 эсвэл 99112233')
        if not EMAIL_REGEX.match(email):
            errors.append('Имэйл буруу форматтай. Жишээ: example@domain.com')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('register.html', surname=surname, name=name, phone=phone, email=email)

        # Save to Excel (append if file exists)
        row = {'Surname': surname, 'Name': name, 'Phone': phone, 'Email': email}
        df = pd.DataFrame([row])
        if os.path.exists(EXCEL_FILE):
            try:
                existing = pd.read_excel(EXCEL_FILE, engine='openpyxl')
                df = pd.concat([existing, df], ignore_index=True)
            except Exception:
                pass

        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
        return render_template('success.html', surname=surname, name=name)

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
