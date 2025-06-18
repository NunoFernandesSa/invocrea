# 🧾 Invocrea – Invoices & Quotates Management App

A simple Nextjs & Django-based application to create quotes and invoices.

---

## 💼 Features

### 1. 👥 Client Management
- Add, edit, and delete clients
- View a complete list of clients

### 2. 📄 Quote Creation
- Automatic quote numbering
- Add line items (description, quantity, unit price, tax)
- Export quotes as PDF
- Convert quotes into invoices

### 3. 🧾 Invoice Creation
- Automatic invoice numbering
- Invoice status: draft, sent, paid
- Payment tracking
- Export invoices as PDF

### 4. 📊 Dashboard & History
- View all quotes and invoices
- Statistics: total invoiced, pending quotes, revenue tracking

### 5. ⚙️ Company Settings
- Configure company name, address
- Add legal notices or payment terms

---

## 🚀 Technologies Used

- Python 3
- Django 4+
- SQLite
- NEXTJS (with Tailwind)
- ReportLab / WeasyPrint (for PDF export)

---

## 🔧 Installation (Local)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/invoiceapp.git
cd invoiceapp

# 2. Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Run the server
python manage.py runserver
```

📝 License
This project is open-source and available under the MIT License.

🙌 Contribution
Pull requests and contributions are welcome. Please open an issue to discuss any major changes beforehand.

📧 Contact
For questions or suggestions: n.fernandes.contact@gmail.com
