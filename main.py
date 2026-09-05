from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import hashlib
from datetime import datetime

class MedicalSystem:
    def __init__(self, window):
        image=PhotoImage(file="A:\\Lessons\\Projects\\medican\\files\\icons8_man_health_worker_32.png")
        self.window = window
        self.window.title("سیستم مدیریت بیماری ها")
        self.window.geometry("1300x850")
        self.window.iconphoto(True,image)
       
        self.db = self.connect_database()
        if not self.db:
            messagebox.showerror("خطا", "امکان اتصال به پایگاه داده وجود ندارد")
            self.window.destroy()
            return
       
        self.current_user = None
        self.setup_ui()
        self.load_initial_data()

    def connect_database(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='advanced_medical_system',
                auth_plugin='mysql_native_password',
                port =3306
            )
            return conn
        except Error as e:
            messagebox.showerror("خطا", f"خطای اتصال به پایگاه داده: {str(e)}")
            return None

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.window)
       
        self.setup_login_tab()
        self.setup_dashboard_tab()
        self.setup_diseases_tab()
        self.setup_patients_tab()
        self.setup_appointments_tab()
        self.setup_prescriptions_tab()
        self.setup_users_tab()
       
        self.notebook.pack(expand=True, fill='both')
       
        for i in range(1, len(self.notebook.tabs())):
            self.notebook.tab(i, state='hidden')

    def toggle_theme(self):
        style = ttk.Style()
        current = style.theme_use()
        style.theme_use("clam" if current == "default" else "default")

    # ------------------------ تب لاگین ------------------------
    def setup_login_tab(self):
        self.login_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.login_tab, text='ورود به سیستم')
       
        login_frame = ttk.LabelFrame(self.login_tab, text='ورود کاربر', padding=20)
        login_frame.pack(pady=50, padx=50, fill='both', expand=True)

        
        ttk.Label(login_frame, text='نام کاربر:',font=("Times New Roman",24)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.username_entry = ttk.Entry(login_frame,width=22,font=("Times New Roman",24))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
       
        ttk.Label(login_frame, text='رمز عبور:',font=("Times New Roman",24)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.password_entry = ttk.Entry(login_frame, show='*',width=22,font=("Times New Roman",24))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
       
        btn_frame = ttk.Frame(login_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
       
        ttk.Button(btn_frame, text='ورود', command=self.authenticate_user).pack(side='right', padx=5)
        ttk.Button(btn_frame, text='خروج', command=self.window.quit).pack(side='left', padx=5)

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
       
        if not username or not password:
            messagebox.showwarning("هشدار", "لطفا نام کاربری و رمز عبور را وارد کنید")
            return
       
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            print(hashed_password)
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM users
                WHERE username = %s AND password = %s AND is_active = TRUE
            """, (username, hashed_password))
            user = cursor.fetchone()
           
            if user:
                self.current_user = user
                self.notebook.hide(0)
                for i in range(1, len(self.notebook.tabs())):
                    self.notebook.tab(i, state='normal')
                self.update_dashboard()
            else:
                messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است")
               
        except Error as e:
            messagebox.showerror("خطا", f"خطای پایگاه داده: {str(e)}")

    def setup_users_tab(self):
        self.users_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.users_tab, text='مدیریت کاربران')

        frame = ttk.LabelFrame(self.users_tab, text="لیست کاربران", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        columns = ("id", "fullname", "username", "role", "status")
        self.users_tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, anchor='center')
        self.users_tree.pack(fill='both', expand=True)

        ttk.Button(self.users_tab, text="Refresh Users", command=self.load_users).pack(pady=5)
        ttk.Button(self.users_tab, text="فعال/غیرفعال", command=self.toggle_user_active).pack(pady=5)

    def load_users(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT user_id, full_name, username, is_active FROM users")
            rows = cursor.fetchall()
            self.users_tree.delete(*self.users_tree.get_children())
            for row in rows:
                self.users_tree.insert('', 'end', values=(
                    row[0], row[1], row[2], "فعال" if row[3] else "غیرفعال"
                ))
        except Error as e:
            messagebox.showerror("خطا", f"خطا در Refresh کاربران: {str(e)}")

    def toggle_user_active(self):
        selected = self.users_tree.focus()
        if not selected:
            messagebox.showwarning("هشدار", "لطفاً یک کاربر را انتخاب کنید")
            return
        user_id = self.users_tree.item(selected)['values'][0]
        status = self.users_tree.item(selected)['values'][3]
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE users SET is_active = %s WHERE user_id = %s", (
                False if status == "فعال" else True, user_id))
            self.db.commit()
            self.load_users()
            self.log_action(f"تغییر وضعیت کاربر ID:{user_id}")
        except Error as e:
            messagebox.showerror("خطا", f"خطا در تغییر وضعیت کاربر: {str(e)}")

    # ------------------------ تب داشبورد ------------------------
    def setup_dashboard_tab(self):
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text='داشبورد')
       
        stats_frame = ttk.LabelFrame(self.dashboard_tab, text="آمار کلی", padding=10)
        stats_frame.pack(fill='x', padx=10, pady=10)
       
        ttk.Label(stats_frame, text="تعداد بیماران:").grid(row=0, column=0, padx=5, pady=5)
        self.patient_count = ttk.Label(stats_frame, text="0", font=('Tahoma', 12, 'bold'))
        self.patient_count.grid(row=0, column=1, padx=5, pady=5)
       
        ttk.Label(stats_frame, text="تعداد نوبت‌های امروز:").grid(row=0, column=2, padx=5, pady=5)
        self.today_appointments = ttk.Label(stats_frame, text="0", font=('Tahoma', 12, 'bold'))
        self.today_appointments.grid(row=0, column=3, padx=5, pady=5)
       
        ttk.Label(stats_frame, text="تعداد بیماری‌ها:").grid(row=0, column=4, padx=5, pady=5)
        self.disease_count = ttk.Label(stats_frame, text="0", font=('Tahoma', 12, 'bold'))
        self.disease_count.grid(row=0, column=5, padx=5, pady=5)
       
        
        charts_frame = ttk.Frame(self.dashboard_tab)
        charts_frame.pack(fill='both', expand=True, padx=10, pady=10)
       
        
        disease_chart_frame = ttk.LabelFrame(charts_frame, text="توزیع بیماری‌ها")
        disease_chart_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.disease_chart = self.create_chart(disease_chart_frame)
       
        
        appt_chart_frame = ttk.LabelFrame(charts_frame, text="وضعیت نوبت‌ ها")
        appt_chart_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        self.appt_chart = self.create_chart(appt_chart_frame)
        
        ttk.Button(self.dashboard_tab, text="تغییر رنگ (شب/روشن)", command=self.toggle_theme).pack(pady=10)

    def create_chart(self, parent):
        fig, ax = plt.subplots(figsize=(5, 3))
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        return fig, ax, canvas

    def update_dashboard(self):
        try:
            cursor = self.db.cursor()
        
            cursor.execute("SELECT COUNT(*) FROM patients")
            self.patient_count.config(text=cursor.fetchone()[0])
           
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE DATE(appointment_date) = %s", (today,))
            self.today_appointments.config(text=cursor.fetchone()[0])
           
           
            cursor.execute("SELECT COUNT(*) FROM diseases")
            self.disease_count.config(text=cursor.fetchone()[0])
           
           
            cursor.execute("SELECT category, COUNT(*) FROM diseases GROUP BY category")
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=['Category', 'Count'])
            self.disease_chart[1].clear()
            df.plot(kind='bar', x='Category', y='Count', ax=self.disease_chart[1], legend=False)
            self.disease_chart[1].set_title('Explaining diseases based on classification')
            self.disease_chart[2].draw()
           
            
            cursor.execute("SELECT status, COUNT(*) FROM appointments GROUP BY status")
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=['Status', 'Count'])
            self.appt_chart[1].clear()
            df.plot(kind='pie', y='Count', labels=df['Status'], ax=self.appt_chart[1], legend=False, autopct='%1.1f%%')
            self.appt_chart[1].set_title('Status of turns')
            self.appt_chart[2].draw()
           
        except Error as e:
            messagebox.showerror("خطا", f"خطا در به‌روزرسانی داشبورد: {str(e)}")
    # ------------------------ تب بیماری‌ها ------------------------
    def setup_diseases_tab(self):
        self.diseases_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.diseases_tab, text='مدیریت بیماری‌ها')
       
        search_frame = ttk.LabelFrame(self.diseases_tab, text="جستجوی بیماری‌ها", padding=10)
        search_frame.pack(fill='x', padx=10, pady=5)
       
        ttk.Label(search_frame, text="نام بیماری:").grid(row=0, column=0, padx=5, pady=5)
        self.disease_search = ttk.Entry(search_frame)
        self.disease_search.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_frame, text="جستجو", command=self.search_diseases).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(search_frame, text="حذف کردن", command=self.Delete_diseases).grid(row=0, column=3, padx=5, pady=5)

        tree_frame = ttk.Frame(self.diseases_tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
       
        columns = ("id", "name", "category", "severity")
        self.diseases_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
       
        self.diseases_tree.heading("id", text="شناسه")
        self.diseases_tree.heading("name", text="نام بیماری")
        self.diseases_tree.heading("category", text="دسته‌بندی")
        self.diseases_tree.heading("severity", text="سطح خطر")
       
        self.diseases_tree.column("id", width=50, anchor='center')
        self.diseases_tree.column("name", width=200,anchor='center')
        self.diseases_tree.column("category", width=150,anchor='center')
        self.diseases_tree.column("severity", width=100, anchor='center')
       
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.diseases_tree.yview)
        self.diseases_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
       
        self.diseases_tree.pack(fill='both', expand=True)
       
        btn_frame = ttk.Frame(self.diseases_tab)
        btn_frame.pack(fill='x', padx=10, pady=10)
       
        ttk.Button(btn_frame, text="Refresh", command=self.load_diseases).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="بیماری جدید", command=self.show_add_disease_form).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="مشاهده جزئیات", command=self.show_disease_details).pack(side='left', padx=5)

    def load_diseases(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT disease_id, name, category, severity FROM diseases")
           
            self.diseases_tree.delete(*self.diseases_tree.get_children())
            for row in cursor:
                self.diseases_tree.insert('', 'end', values=row)
               
        except Error as e:
            messagebox.showerror("خطا", f"خطا در Refresh بیماری‌ها: {str(e)}")

    def Delete_diseases(self):
        selected_item = self.diseases_tree.focus()
        if not selected_item:
            messagebox.showwarning("هشدار", "لطفاً یک بیماری را انتخاب کنید")
            return
       
        disease_id = self.diseases_tree.item(selected_item)['values'][0]
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("DELETE FROM `disease_symptoms` WHERE disease_id = %s",(disease_id,))
        cursor.execute("DELETE FROM `diseases` WHERE disease_id = %s", (disease_id,))
        self.db.commit()
        messagebox.showinfo("موفقیت", "بیماری با موفقیت حذف شد")
        self.load_diseases()
                
    def search_diseases(self):
        search_term = self.disease_search.get()
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT disease_id, name, category, severity FROM diseases WHERE name LIKE %s",
                          (f"%{search_term}%",))
           
            self.diseases_tree.delete(*self.diseases_tree.get_children())
            for row in cursor:
                self.diseases_tree.insert('', 'end', values=row)
               
        except Error as e:
            messagebox.showerror("خطا", f"خطا در جستجوی بیماری‌ها: {str(e)}")

    def show_add_disease_form(self):
        add_window = Toplevel(self.window)
        add_window.title("افزودن بیماری جدید")
        add_window.geometry("600x500")

        form_frame = ttk.LabelFrame(add_window, text="اطلاعات بیماری", padding=10)
        form_frame.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Label(form_frame, text="نام بیماری:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="دسته‌بندی:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        category_entry = ttk.Entry(form_frame)
        category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="سطح خطر (1-5):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        severity_spin = ttk.Spinbox(form_frame, from_=1, to=5)
        severity_spin.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="علت بیماری:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        cause_entry = ttk.Entry(form_frame, width=50)
        cause_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="راه‌حل یا تداوی:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        treatment_entry = ttk.Entry(form_frame, width=50)
        treatment_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="تعداد علائم:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        rite = ttk.Spinbox(form_frame, from_=1, to=10)
        rite.grid(row=5, column=1, padx=5, pady=5)

        self.symptom_entries = []

        def Add_info():
            self.symptom_frames = []
            self.symptom_entries = []

            try:
                count = int(rite.get())
            except ValueError:
                messagebox.showwarning("خطا", "عدد معتبر وارد کنید")
                return

            for widget in form_frame.winfo_children():
                if getattr(widget, "tag", "") == "symptom":
                    widget.destroy()

            y = 5
            for i in range(count):
                y += 1
                frame = ttk.Frame(form_frame)
                frame.grid(row=y, column=0, columnspan=2, pady=5, padx=5, sticky='ew')
                frame.tag = "symptom"

                ttk.Label(frame, text=f"علامت {i+1}:").grid(row=0, column=0, padx=5)

                name_entry = ttk.Entry(frame, width=20)
                name_entry.grid(row=0, column=1, padx=5)

                desc_entry = ttk.Entry(frame, width=30)
                desc_entry.grid(row=0, column=2, padx=5)

                def remove_frame(f=frame):
                    f.destroy()
                    self.symptom_entries = [
                        pair for pair in self.symptom_entries if pair[0].winfo_exists()
                    ]

                del_btn = ttk.Button(frame, text="حذف", command=remove_frame)
                del_btn.grid(row=0, column=3, padx=5)

                self.symptom_entries.append((name_entry, desc_entry))
                self.symptom_frames.append(frame)

        ttk.Button(form_frame, text="اضافه کردن علائم", command=Add_info).grid(row=6, column=3, sticky='w', padx=5, pady=5)

        def save():
            name = name_entry.get()
            category = category_entry.get()
            severity = severity_spin.get()
            cause = cause_entry.get().strip()
            treatment = treatment_entry.get().strip()
            symptom_data = [(n.get().strip(), d.get().strip())
                            for n, d in self.symptom_entries if n.get().strip()]
            print(symptom_data)

            if not name or not category or not severity:
                messagebox.showwarning("هشدار", "همه فیلدهای اصلی را پر کنید")
                return

            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO diseases (name, category, severity, cause, treatment)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, category, severity, cause, treatment))
                
                disease_id = cursor.lastrowid
                for sym_name, sym_desc in symptom_data:
                    cursor.execute("SELECT symptom_id FROM symptoms WHERE name = %s", (sym_name,))
                    row = cursor.fetchone()
                    if row:
                        symptom_id = row[0]
                    else:
                        cursor.execute("""
                            INSERT INTO symptoms (name, description) VALUES (%s, %s)
                        """, (sym_name, sym_desc))
                        symptom_id = cursor.lastrowid

                    cursor.execute("""
                        INSERT INTO disease_symptoms (disease_id, symptom_id)
                        VALUES (%s, %s)
                    """, (disease_id, symptom_id))

                self.db.commit()
                messagebox.showinfo("موفقیت", "بیماری با موفقیت ذخیره شد")
                self.load_diseases()
                add_window.destroy()
            except Error as e:
                messagebox.showerror("خطا", f"خطا در ذخیره بیماری: {str(e)}")

        ttk.Button(form_frame, text="ذخیره", command=save).grid(row=7, column=3, pady=10, sticky='w')
    
    def show_disease_details(self):
        selected_item = self.diseases_tree.focus()
        if not selected_item:
            messagebox.showwarning("هشدار", "لطفاً یک بیماری را انتخاب کنید")
            return
       
        disease_id = self.diseases_tree.item(selected_item)['values'][0]
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM diseases WHERE disease_id = %s", (disease_id,))
            disease = cursor.fetchone()
           
            if not disease:
                messagebox.showerror("خطا", "بیماری مورد نظر یافت نشد")
                return
            cursor.execute("""
                SELECT s.name, s.description
                FROM disease_symptoms ds
                JOIN symptoms s ON ds.symptom_id = s.symptom_id
                WHERE ds.disease_id = %s
            """, (disease_id,))
            symptoms = cursor.fetchall()
            
            detail_window =Toplevel(self.window)
            detail_window.title(f"جزئیات بیماری: {disease['name']}")
            detail_window.geometry("600x650")
           
            info_frame = ttk.LabelFrame(detail_window, text="اطلاعات پایه")
            info_frame.pack(fill='x', padx=10, pady=5)
           
            ttk.Label(info_frame, text="نام:").pack(anchor='w')
            name_label = ttk.Label(info_frame, text=disease['name'])
            name_label.pack(anchor='w')

            ttk.Label(info_frame, text="دسته‌بندی:").pack(anchor='w')
            category_label = ttk.Label(info_frame, text=disease['category'])
            category_label.pack(anchor='w')

            ttk.Label(info_frame, text="سطح خطر:").pack(anchor='w')
            severity_label = ttk.Label(info_frame, text=str(disease['severity']))
            severity_label.pack(anchor='w')

            ttk.Label(info_frame, text="علت بیماری:").pack(anchor='w')
            cause_entry =Text(info_frame, height=3, width=60)
            cause_entry.insert('1.0', disease.get('cause', ''))
            cause_entry.pack(anchor='w', padx=5, pady=2)

            ttk.Label(info_frame, text="راه‌حل/تداوی:").pack(anchor='w')
            treatment_entry =Text(info_frame, height=3, width=60)
            treatment_entry.insert('1.0', disease.get('treatment', ''))
            treatment_entry.pack(anchor='w', padx=5, pady=2)
            
            
            symptoms_frame = ttk.LabelFrame(detail_window, text="ویرایش علائم")
            symptoms_frame.pack(fill='both', expand=True, padx=10, pady=5)

            editable_entries = []

            def draw_symptoms():
                for widget in symptoms_frame.winfo_children():
                    widget.destroy()
                editable_entries.clear()

                for idx, s in enumerate(symptoms):
                    row = ttk.Frame(symptoms_frame)
                    row.pack(fill='x', pady=3)

                    name_entry = ttk.Entry(row)
                    name_entry.insert(0, s['name'])
                    name_entry.pack(side='left', padx=5)

                    desc_entry = ttk.Entry(row, width=50)
                    desc_entry.insert(0, s['description'])
                    desc_entry.pack(side='left', padx=5)

                    def remove_symptom(row_frame=row, entry_pair=(name_entry, desc_entry)):
                        row_frame.destroy()
                        editable_entries.remove(entry_pair)

                    ttk.Button(row, text="حذف", command=remove_symptom).pack(side='left', padx=5)
                    editable_entries.append((name_entry, desc_entry))

            draw_symptoms()
            def add_symptom_field():
                row = ttk.Frame(symptoms_frame)
                row.pack(fill='x', pady=3)

                name_entry = ttk.Entry(row)
                name_entry.pack(side='left', padx=5)

                desc_entry = ttk.Entry(row, width=50)
                desc_entry.pack(side='left', padx=5)

                def remove_symptom(row_frame=row, entry_pair=(name_entry, desc_entry)):
                    row_frame.destroy()
                    editable_entries.remove(entry_pair)

                ttk.Button(row, text="حذف", command=remove_symptom).pack(side='left', padx=5)
                editable_entries.append((name_entry, desc_entry))

            ttk.Button(symptoms_frame, text="اضافه علامت", command=add_symptom_field).pack(pady=5)
            def save_edited_symptoms():
                try:
                    cursor = self.db.cursor()
                    cursor.execute("DELETE FROM disease_symptoms WHERE disease_id = %s", (disease_id,))

                    for name_entry, desc_entry in editable_entries:
                        name = name_entry.get().strip()
                        desc = desc_entry.get().strip()
                        if not name:
                            continue

                        cursor.execute("SELECT symptom_id FROM symptoms WHERE name = %s", (name,))
                        row = cursor.fetchone()
                        if row:
                            symptom_id = row[0]
                        else:
                            cursor.execute("INSERT INTO symptoms (name, description) VALUES (%s, %s)", (name, desc))
                            symptom_id = cursor.lastrowid

                        cursor.execute("""
                            INSERT INTO disease_symptoms (disease_id, symptom_id)
                            VALUES (%s, %s)
                        """, (disease_id, symptom_id))

                    self.db.commit()
                    messagebox.showinfo("موفقیت", "علائم با موفقیت به‌روزرسانی شدند")
                    detail_window.destroy()
                    self.load_diseases()

                except Error as e:
                    messagebox.showerror("خطا", f"خطا در ذخیره علائم: {str(e)}")

            ttk.Button(detail_window, text="ذخیره علائم", command=save_edited_symptoms).pack(pady=10)
                
            def save_cause_treatment():
                new_cause = cause_entry.get("1.0", "end-1c").strip()
                new_treatment = treatment_entry.get("1.0", "end-1c").strip()
                #UPDATE `diseases` SET `cause` = 'jkjjk' WHERE `diseases`.`disease_id` = 4;
                try:
                    cursor = self.db.cursor()
                    cursor.execute("""
                        UPDATE `diseases` SET `cause` = %s,
                        treatment =%s WHERE
                        `diseases`.`disease_id` = %s;
                    """, (new_cause, new_treatment, disease_id))
                    self.db.commit()
                    messagebox.showinfo("موفقیت", "علت و تداوی با موفقیت ذخیره شد")
                    detail_window.destroy()
                    self.load_diseases()
                except Error as e:
                    messagebox.showerror("خطا", f"خطا در ذخیره علت/تداوی: {str(e)}")

            ttk.Button(detail_window, text="ذخیره علت و تداوی", command=save_cause_treatment).pack(pady=5)
        except Error as e:
            messagebox.showerror("خطا", f"خطا در دریافت اطلاعات بیماری: {str(e)}")
            
    # ------------------------ تب بیماران ------------------------
    def setup_patients_tab(self):
        self.patients_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.patients_tab, text='مدیریت بیماران')
       
        
        search_frame = ttk.LabelFrame(self.patients_tab, text="جستجوی بیماران", padding=10)
        search_frame.pack(fill='x', padx=10, pady=5)
       
        ttk.Label(search_frame, text="نام/نام خانوادگی:").grid(row=0, column=0, padx=5, pady=5)
        self.patient_search = ttk.Entry(search_frame)
        self.patient_search.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_frame, text="جستجو", command=self.search_patients).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(search_frame, text="حذف کردن", command=self.Delete_patients).grid(row=0, column=3, padx=5, pady=5)

        
        tree_frame = ttk.Frame(self.patients_tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
       
        columns = ("id", "name", "birth_date", "gender", "phone")
        self.patients_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
       
        self.patients_tree.heading("id", text="شناسه")
        self.patients_tree.heading("name", text="نام کامل")
        self.patients_tree.heading("birth_date", text="تاریخ تولد")
        self.patients_tree.heading("gender", text="جنسیت")
        self.patients_tree.heading("phone", text="تلفن")
       
        self.patients_tree.column("id", width=50, anchor='center')
        self.patients_tree.column("name", width=200,anchor='center')
        self.patients_tree.column("birth_date", width=100,anchor='center')
        self.patients_tree.column("gender", width=80, anchor='center')
        self.patients_tree.column("phone", width=120,anchor='center')
       
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
       
        self.patients_tree.pack(fill='both', expand=True)
       
        
        btn_frame = ttk.Frame(self.patients_tab)
        btn_frame.pack(fill='x', padx=10, pady=10)
       
        ttk.Button(btn_frame, text="Refresh", command=self.load_patients).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="بیمار جدید", command=self.show_add_patient_form).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="مشاهده پرونده", command=self.show_patient_record).pack(side='left', padx=5)

    def load_patients(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT patient_id, CONCAT(first_name, ' ', last_name),
                       birth_date, gender, phone
                FROM patients
                ORDER BY last_name, first_name
            """)
           
            self.patients_tree.delete(*self.patients_tree.get_children())
            for row in cursor:
                self.patients_tree.insert('', 'end', values=row)
               
        except Error as e:
            messagebox.showerror("خطا", f"خطا در Refresh بیماران: {str(e)}")

    def Delete_patients(self):
        selected_item = self.patients_tree.focus()
        if not selected_item:
            messagebox.showwarning("هشدار", "لطفاً یک بیمار را انتخاب کنید")
            return

        patient_id = self.patients_tree.item(selected_item)['values'][0]
        try:
            cursor = self.db.cursor()

            cursor.execute("DELETE FROM prescription_items WHERE prescription_id IN (SELECT prescription_id FROM prescriptions WHERE patient_id = %s)", (patient_id,))
            cursor.execute("DELETE FROM prescriptions WHERE patient_id = %s", (patient_id,))
            cursor.execute("DELETE FROM appointments WHERE patient_id = %s", (patient_id,))
            cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))

            self.db.commit()
            messagebox.showinfo("موفقیت", "بیمار با موفقیت حذف شد")
            self.load_patients()
        except Error as e:
            messagebox.showerror("خطا", f"خطا در حذف بیمار: {str(e)}")
                
    def search_patients(self):
        search_term = self.patient_search.get()
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT patient_id, CONCAT(first_name, ' ', last_name),
                       birth_date, gender, phone
                FROM patients
                WHERE first_name LIKE %s OR last_name LIKE %s
                ORDER BY last_name, first_name
            """, (f"%{search_term}%", f"%{search_term}%"))
           
            self.patients_tree.delete(*self.patients_tree.get_children())
            for row in cursor:
                self.patients_tree.insert('', 'end', values=row)
               
        except Error as e:
            messagebox.showerror("خطا", f"خطا در جستجوی بیماران: {str(e)}")

    def show_add_patient_form(self):
        add_window =Toplevel(self.window)
        add_window.title("افزودن بیمار جدید")
        add_window.geometry("500x400")
       
        form_frame1 = ttk.LabelFrame(add_window, text="اطلاعات بیمار", padding=10)
        form_frame1.pack(fill='both', expand=True, padx=10, pady=10)
       
        ttk.Label(form_frame1, text="نام:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        first_name_entry = ttk.Entry(form_frame1)
        first_name_entry.grid(row=0, column=1, padx=5, pady=5)
       
        ttk.Label(form_frame1, text="نام خانوادگی:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        last_name_entry = ttk.Entry(form_frame1)
        last_name_entry.grid(row=1, column=1, padx=5, pady=5)
       
        ttk.Label(form_frame1, text="تاریخ تولد:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        birth_date_entry =ttk.Entry(form_frame1)
        birth_date_entry.grid(row=2, column=1, padx=5, pady=5)
        birth_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Label(form_frame1, text="جنسیت:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        gender_combo = ttk.Combobox(form_frame1, values=['male', 'female','other'], state='readonly')
        gender_combo.grid(row=3, column=1, padx=5, pady=5)
       
        ttk.Label(form_frame1, text="تلفن:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        phone_entry = ttk.Entry(form_frame1)
        phone_entry.grid(row=4, column=1, padx=5, pady=5)
        

        def save():
            try:
                
                birth_date = birth_date_entry.get()
                try:
                    datetime.strptime(birth_date, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    messagebox.showerror("خطا", "فرمت تاریخ تولد باید به صورت YYYY-MM-DD باشد")
                    return

                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO patients (first_name, last_name, birth_date, gender, phone)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    first_name_entry.get(),
                    last_name_entry.get(),
                    birth_date,
                    gender_combo.get(),
                    phone_entry.get()
                ))
                self.db.commit()
                messagebox.showinfo("موفقیت", "بیمار جدید با موفقیت اضافه شد")
                self.load_patients()
                add_window.destroy()
                self.log_action(f"افزودن بیمار جدید: {first_name_entry.get()} {last_name_entry.get()}")
            except Error as e:
                messagebox.showerror("خطا", f"خطا در ذخیره بیمار: {str(e)}")

        ttk.Button(form_frame1, text="بستن", command=add_window.destroy).grid(row=5, column=0, pady=10, padx=25)     
        ttk.Button(form_frame1, text="ذخیره", command=save).grid(row=5, column=1,pady=10,padx=25)
     
    def show_patient_record(self):
        selected_item = self.patients_tree.focus()
        if not selected_item:
            messagebox.showwarning("هشدار", "لطفاً یک بیمار را انتخاب کنید")
            return
       
        patient_id = self.patients_tree.item(selected_item)['values'][0]
       
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            patient = cursor.fetchone()
           
            if not patient:
                messagebox.showerror("خطا", "بیمار مورد نظر یافت نشد")
                return
           
            
            record_window =Toplevel(self.window)
            record_window.title(f"پرونده بیمار: {patient['first_name']} {patient['last_name']}")
            record_window.geometry("800x600")
           
            
            info_frame = ttk.LabelFrame(record_window, text="اطلاعات شخصی")
            info_frame.pack(fill='x', padx=10, pady=5)
           
            ttk.Label(info_frame, text=f"نام کامل: {patient['first_name']} {patient['last_name']}").pack(anchor='w')
            ttk.Label(info_frame, text=f"تاریخ تولد: {patient['birth_date']}").pack(anchor='w')
            ttk.Label(info_frame, text=f"جنسیت: {patient['gender']}").pack(anchor='w')
            ttk.Label(info_frame, text=f"تلفن: {patient['phone']}").pack(anchor='w')
           
            
            appointments_frame = ttk.LabelFrame(record_window, text="نوبت‌های بیمار")
            appointments_frame.pack(fill='both', expand=True, padx=10, pady=5)
           
            cursor.execute("""
                SELECT a.appointment_date, a.status,
                       u.full_name AS doctor_name
                FROM appointments a
                JOIN users u ON a.doctor_id = u.user_id
                WHERE a.patient_id = %s
                ORDER BY a.appointment_date DESC
            """, (patient_id,))
            appointments = cursor.fetchall()
           
            if appointments:
                columns = ("date", "doctor", "status")
                tree = ttk.Treeview(appointments_frame, columns=columns, show='headings')
               
                tree.heading("date", text="تاریخ و زمان")
                tree.heading("doctor", text="پزشک")
                tree.heading("status", text="وضعیت")
               
                tree.column("date", width=150)
                tree.column("doctor", width=150)
                tree.column("status", width=100)
               
                scrollbar = ttk.Scrollbar(appointments_frame, orient='vertical', command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                scrollbar.pack(side='right', fill='y')
               
                tree.pack(fill='both', expand=True)
               
                for appt in appointments:
                    tree.insert('', 'end', values=(
                        appt['appointment_date'].strftime("%Y-%m-%d %H:%M"),
                        appt['doctor_name'],
                        appt['status']
                    ))
            else:
                ttk.Label(appointments_frame, text="هیچ نوبتی ثبت نشده است").pack()
           
        except Error as e:
            messagebox.showerror("خطا", f"خطا در دریافت اطلاعات بیمار: {str(e)}")
    # ------------------------ تب نوبت‌دهی ------------------------
    def setup_appointments_tab(self):
        self.appointments_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.appointments_tab, text='نوبت‌دهی')
       
        
        filter_frame = ttk.LabelFrame(self.appointments_tab, text="فیلتر نوبت‌ها", padding=10)
        filter_frame.pack(fill='x', padx=10, pady=5)
       
        ttk.Label(filter_frame, text="تاریخ از:").grid(row=0, column=0, padx=5, pady=5)
        self.appt_date_from = ttk.Entry(filter_frame)
        self.appt_date_from.grid(row=0, column=1, padx=5, pady=5)
        self.appt_date_from.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(filter_frame, text="تا:").grid(row=0, column=2, padx=5, pady=5)
        self.appt_date_to = ttk.Entry(filter_frame)
        self.appt_date_to.grid(row=0, column=3, padx=5, pady=5)
        self.appt_date_to.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Button(filter_frame, text="اعمال فیلتر", command=self.filter_appointments).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(filter_frame, text="حذف کردن", command=self.Delete_appointments).grid(row=0, column=5, padx=5, pady=5)

        
        tree_frame = ttk.Frame(self.appointments_tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
       
        columns = ("id", "patient", "doctor", "date", "time", "status")
        self.appointments_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
       
        self.appointments_tree.heading("id", text="شناسه")
        self.appointments_tree.heading("patient", text="بیمار")
        self.appointments_tree.heading("doctor", text="پزشک")
        self.appointments_tree.heading("date", text="تاریخ")
        self.appointments_tree.heading("time", text="زمان")
        self.appointments_tree.heading("status", text="وضعیت")
       
        self.appointments_tree.column("id", width=50, anchor='center')
        self.appointments_tree.column("patient", width=150)
        self.appointments_tree.column("doctor", width=150)
        self.appointments_tree.column("date", width=100)
        self.appointments_tree.column("time", width=80)
        self.appointments_tree.column("status", width=100)
       
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
       
        self.appointments_tree.pack(fill='both', expand=True)
       
        
        btn_frame = ttk.Frame(self.appointments_tab)
        btn_frame.pack(fill='x', padx=10, pady=10)
       
        ttk.Button(btn_frame, text="Refresh", command=self.load_appointments).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="نوبت جدید", command=self.show_add_appointment_form).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="تغییر وضعیت", command=self.update_appointment_status).pack(side='left', padx=5)

    def load_appointments(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    a.appointment_id,
                    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
                    u.full_name AS doctor_name,
                    DATE_FORMAT(a.appointment_date, '%Y-%m-%d') AS date,
                    DATE_FORMAT(a.appointment_date, '%H:%i') AS time,
                    a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN users u ON a.doctor_id = u.user_id
                ORDER BY a.appointment_date DESC
                LIMIT 100
            """)
           
            self.appointments_tree.delete(*self.appointments_tree.get_children())
            for row in cursor:
                self.appointments_tree.insert('', 'end', values=(
                    row['appointment_id'],
                    row['patient_name'],
                    row['doctor_name'],
                    row['date'],
                    row['time'],
                    row['status']
                ))
               
        except Error as e:
            messagebox.showerror("خطا", f"خطا در Refresh نوبت‌ها: {str(e)}")

    def Delete_appointments(self):
        selected_item = self.appointments_tree.focus()
        if not selected_item:
            messagebox.showwarning("هشدار", "لطفاً یک نوبت را انتخاب کنید")
            return

        appointment_id = self.appointments_tree.item(selected_item)['values'][0]
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM appointments WHERE appointment_id = %s", (appointment_id,))
            self.db.commit()
            messagebox.showinfo("موفقیت", "نوبت با موفقیت حذف شد")
            self.load_appointments()
        except Error as e:
            messagebox.showerror("خطا", f"خطا در حذف نوبت: {str(e)}")
                
    def filter_appointments(self):
        date_from = self.appt_date_from.get()
        date_to = self.appt_date_to.get()

        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT
                    a.appointment_id,
                    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
                    u.full_name AS doctor_name,
                    DATE_FORMAT(a.appointment_date, '%Y-%m-%d') AS date,
                    DATE_FORMAT(a.appointment_date, '%H:%i') AS time,
                    a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN users u ON a.doctor_id = u.user_id
            """
            params = []
            where_clauses = []

            if date_from:
                where_clauses.append("DATE(a.appointment_date) >= %s")
                params.append(date_from)
            if date_to:
                where_clauses.append("DATE(a.appointment_date) <= %s")
                params.append(date_to)

            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

            query += " ORDER BY a.appointment_date DESC LIMIT 100"

            cursor.execute(query, params)

            self.appointments_tree.delete(*self.appointments_tree.get_children())
            for row in cursor:
                self.appointments_tree.insert('', 'end', values=(
                    row['appointment_id'],
                    row['patient_name'],
                    row['doctor_name'],
                    row['date'],
                    row['time'],
                    row['status']
                ))
        except Error as e:
            messagebox.showerror("خطا", f"خطا در فیلتر نوبت‌ها: {str(e)}")
            
    def show_add_appointment_form(self):
        add_window = Toplevel(self.window)
        add_window.title("افزودن نوبت جدید")
        add_window.geometry("500x400")
       
        form_frame = ttk.LabelFrame(add_window, text="اطلاعات نوبت", padding=10)
        form_frame.pack(fill='both', expand=True, padx=10, pady=10)
       
        patients = []
        doctors = []
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT patient_id, CONCAT(first_name, ' ', last_name) FROM patients")
            patients = cursor.fetchall()
           
            cursor.execute("SELECT user_id,full_name FROM users WHERE is_active = TRUE")
            doctors = cursor.fetchall()
        except Error as e:
            messagebox.showerror("خطا", f"خطا در دریافت اطلاعات: {str(e)}")
            add_window.destroy()
            return
       
        ttk.Label(form_frame, text="بیمار:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        patient_combo = ttk.Combobox(form_frame, values=[f"{name} (ID:{pid})" for pid, name in patients])
        patient_combo.grid(row=0, column=1, padx=5, pady=5)
       
        ttk.Label(form_frame, text="پزشک:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        doctor_combo = ttk.Combobox(form_frame, values=[f"{name} (ID:{did})" for did, name in doctors])
        doctor_combo.grid(row=1, column=1, padx=5, pady=5)
       
        ttk.Label(form_frame, text="تاریخ و زمان:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        datetime_entry = ttk.Entry(form_frame)
        datetime_entry.grid(row=2, column=1, padx=5, pady=5)
        datetime_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
       
        ttk.Label(form_frame, text="توضیحات:").grid(row=3, column=0, padx=5, pady=5, sticky='ne')
        notes_entry =Text(form_frame, height=5, width=30)
        notes_entry.grid(row=3, column=1, padx=5, pady=5)
       
        def save():
            try:
                
                patient_id = int(patient_combo.get().split("(ID:")[1].rstrip(")"))
                doctor_id = int(doctor_combo.get().split("(ID:")[1].rstrip(")"))
                
                birth_date = datetime_entry.get()
                try:
                    datetime.strptime(birth_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("خطا", "فرمت تاریخ تولد باید به صورت YYYY-MM-DD باشد")
                    return
               
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    patient_id,
                    doctor_id,
                    birth_date,
                    notes_entry.get("1.0", "end-1c"),
                    "ثبت شده"
                ))
                self.db.commit()
                messagebox.showinfo("موفقیت", "نوبت جدید با موفقیت ثبت شد")
                self.load_appointments()
                add_window.destroy()
            except (Error, ValueError, IndexError) as e:
                messagebox.showerror("خطا", f"خطا در ثبت نوبت: {str(e)}")
       
        ttk.Button(form_frame, text="ذخیره", command=save).grid(row=4, column=1, pady=10)

    def update_appointment_status(self):
        selected_item = self.appointments_tree.focus()
        if not selected_item:
            messagebox.showwarning("هشدار", "لطفاً یک نوبت را انتخاب کنید")
            return
       
        appointment_id = self.appointments_tree.item(selected_item)['values'][0]
        current_status = self.appointments_tree.item(selected_item)['values'][5]
       
        status_window =Toplevel(self.window)
        status_window.title("تغییر وضعیت نوبت")
        status_window.geometry("300x200")
       
        form_frame = ttk.LabelFrame(status_window, text="وضعیت جدید", padding=10)
        form_frame.pack(fill='both', expand=True, padx=10, pady=10)
       
        status_var =StringVar(value=current_status)
        ttk.Radiobutton(form_frame, text="ثبت شده", variable=status_var, value="scheduled").pack(anchor='w')
        ttk.Radiobutton(form_frame, text="تأیید شده", variable=status_var, value="no show").pack(anchor='w')
        ttk.Radiobutton(form_frame, text="انجام شده", variable=status_var, value="completed").pack(anchor='w')
        ttk.Radiobutton(form_frame, text="لغو شده", variable=status_var, value="canceled").pack(anchor='w')
       
        def save():
            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    UPDATE appointments
                    SET status = %s
                    WHERE appointment_id = %s
                """, (status_var.get(), appointment_id))
                self.db.commit()
                messagebox.showinfo("موفقیت", "وضعیت نوبت با موفقیت به‌روزرسانی شد")
                self.load_appointments()
                print(status_var.get())
                status_window.destroy()
            except Error as e:
                messagebox.showerror("خطا", f"خطا در به‌روزرسانی وضعیت: {str(e)}")
       
        ttk.Button(form_frame, text="ذخیره", command=save).pack(pady=10)

    # ------------------------ تب نسخه‌نویسی ------------------------
    def setup_prescriptions_tab(self):
        self.prescriptions_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.prescriptions_tab, text='نسخه‌نویسی')
        
        info_frame = ttk.LabelFrame(self.prescriptions_tab, text="اطلاعات نسخه", padding=10)
        info_frame.pack(fill='x', padx=10, pady=5)
       
        ttk.Label(info_frame, text="بیمار:").grid(row=0, column=0, padx=5, pady=5)
        self.patient_combo = ttk.Combobox(info_frame, state='readonly')
        self.patient_combo.grid(row=0, column=1, padx=5, pady=5)
       
        ttk.Label(info_frame, text="تاریخ:").grid(row=0, column=2, padx=5, pady=5)
        self.prescription_date = ttk.Entry(info_frame)
        self.prescription_date.grid(row=0, column=3, padx=5, pady=5)
        self.prescription_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        ttk.Button(info_frame, text="حذف کردن", command=self.Delete_prescription).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(info_frame, text="اضافه کردن دارو", command=self.show_add_drug_form).grid(row=0,column=5, padx=5)

        
        drugs_frame = ttk.LabelFrame(self.prescriptions_tab, text="داروهای تجویزی", padding=10)
        drugs_frame.pack(fill='both', expand=True, padx=10, pady=5)
       
        columns = ("drug_id","drug", "dosage", "frequency", "duration")
        self.prescription_tree = ttk.Treeview(drugs_frame, columns=columns, show='headings')
       
        self.prescription_tree.heading("drug_id", text="شناسه دارو")
        self.prescription_tree.heading("drug", text="نام دارو")
        self.prescription_tree.heading("dosage", text="مقدار مصرف")
        self.prescription_tree.heading("frequency", text="تعداد دفعات")
        self.prescription_tree.heading("duration", text="مدت مصرف")
        
        
       
        scrollbar = ttk.Scrollbar(drugs_frame, orient='vertical', command=self.prescription_tree.yview)
        self.prescription_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
       
        self.prescription_tree.pack(fill='both', expand=True)
       
        
        btn_frame = ttk.Frame(self.prescriptions_tab)
        btn_frame.pack(fill='x', padx=10, pady=10)
       
        #ttk.Button(btn_frame, text="ذخیره نسخه", command=self.save_prescription).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.load_prescription_data).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="چاپ نسخه", command=self.print_prescription).pack(side='left', padx=5)
        
        history_frame = ttk.LabelFrame(self.prescriptions_tab, text="لیست نسخه‌های قبلی", padding=10)
        history_frame.pack(fill='both', expand=True, padx=10, pady=5)

        columns = ("id", "patient", "doctor", "date")
        self.prescription_list_tree = ttk.Treeview(history_frame, columns=columns, show='headings')
        self.prescription_list_tree.heading("id", text="شناسه نسخه")
        self.prescription_list_tree.heading("patient", text="بیمار")
        self.prescription_list_tree.heading("doctor", text="پزشک")
        self.prescription_list_tree.heading("date", text="تاریخ صدور")
        self.prescription_list_tree.pack(fill='both', expand=True)
        ttk.Button(history_frame, text="حذف نسخه انتخاب‌شده", command=self.Delete_prescription).pack(pady=5)
        ttk.Button(history_frame, text="Refresh نسخه‌ها", command=self.load_prescription_data).pack(pady=5)

    def load_prescription_data(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT patient_id, CONCAT(first_name, ' ', last_name) FROM patients")
            patients = cursor.fetchall()
            self.patient_combo['values'] = [f"{name} (ID:{pid})" for pid, name in patients]
           
            for item in self.prescription_tree.get_children():
                self.prescription_tree.delete(item)
               
        except Error as e:
            messagebox.showerror("خطا", f"خطا در Refresh داده‌های نسخه: {str(e)}")
        
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT p.prescription_id, CONCAT(pa.first_name, ' ', pa.last_name) AS patient_name,
                    u.full_name AS doctor_name, p.issue_date
                FROM prescriptions p
                JOIN patients pa ON p.patient_id = pa.patient_id
                JOIN users u ON p.doctor_id = u.user_id
                ORDER BY p.issue_date DESC
            """)
            rows = cursor.fetchall()
            self.prescription_list_tree.delete(*self.prescription_list_tree.get_children())
            for row in rows:
                self.prescription_list_tree.insert('', 'end', values=row)
        except Error as e:
            messagebox.showerror("خطا", f"خطا در Refresh نسخه‌ها: {str(e)}")

    def show_add_drug_form(self):
        if not self.patient_combo.get():
            messagebox.showwarning("هشدار", "لطفاً ابتدا یک بیمار انتخاب کنید")
            return
       
        add_window =Toplevel(self.window)
        add_window.title("افزودن داروی جدید")
        add_window.geometry("400x300")
       
        form_frame = ttk.LabelFrame(add_window, text="اطلاعات دارو", padding=10)
        form_frame.pack(fill='both', expand=True, padx=10, pady=10)
       
        drugs = []
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT drug_id, name FROM drugs")
            drugs = cursor.fetchall()
        except Error as e:
            messagebox.showerror("خطا", f"خطا در دریافت لیست داروها: {str(e)}")
            add_window.destroy()
            return

        
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        #drug_combo = ttk.Combobox(form_frame, values=[f"{name} (ID:{did})" for did, name in drugs])
        drug_id =ttk.Entry(form_frame)
        drug_id.grid(row=0, column=1, padx=5, pady=5)
       
        
        ttk.Label(form_frame, text="دارو:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        #drug_combo = ttk.Combobox(form_frame, values=[f"{name} (ID:{did})" for did, name in drugs])
        drug_combo =ttk.Entry(form_frame)
        drug_combo.grid(row=1, column=1, padx=5, pady=5)
       
        ttk.Label(form_frame, text="مقدار مصرف:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        dosage_entry = ttk.Entry(form_frame)
        dosage_entry.grid(row=2, column=1, padx=5, pady=5)
       
        ttk.Label(form_frame, text="تعداد دفعات:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        frequency_entry = ttk.Entry(form_frame)
        frequency_entry.grid(row=3, column=1, padx=5, pady=5)
       
        ttk.Label(form_frame, text="مدت مصرف:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        duration_entry = ttk.Entry(form_frame)
        duration_entry.grid(row=4, column=1, padx=5, pady=5)
        
        def add():
            try:
                full_text = drug_combo.get()
                print(full_text)
                #drug_id = int(full_text.split(" (ID:")[1].rstrip(")"))
                drug_name = full_text.split(" (ID:")[0]
                self.prescription_tree.insert('', 'end', values=(
                    drug_id.get(),
                    drug_name,
                    dosage_entry.get(),
                    frequency_entry.get(),
                    duration_entry.get()
                ))
                add_window.destroy()
            except (ValueError, IndexError, AttributeError):
                messagebox.showerror("خطا", "لطفاً یک دارو را انتخاب کنید")
       
        ttk.Button(form_frame, text="افزودن", command=add).grid(row=7, column=1, pady=10)

    def save_prescription(self):
        if not self.patient_combo.get():
            messagebox.showwarning("هشدار", "لطفاً ابتدا یک بیمار انتخاب کنید")
            return
       
        if not self.prescription_tree.get_children():
            messagebox.showwarning("هشدار", "هیچ دارویی به نسخه اضافه نشده است")
            return
       
        try:    
            patient_id = int(self.patient_combo.get().split("(ID:")[1].rstrip(")"))
            birth_date = self.prescription_date.get()
            print(patient_id)
                
            try:
                datetime.strptime(birth_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("خطا", "فرمت تاریخ تولد باید به صورت YYYY-MM-DD باشد")
                return

            cursor = self.db.cursor()
           
            cursor.execute("""
                INSERT INTO prescriptions (patient_id, doctor_id, issue_date)
                VALUES (%s, %s, %s)
            """, (
                patient_id,
                self.current_user['user_id'],
                birth_date
            ))
            prescription_id = cursor.lastrowid
           
            for item in self.prescription_tree.get_children():
                values = self.prescription_tree.item(item)['values']
                drug_id = values[0]
                print(drug_id)
               
                cursor.execute("""
                    INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    prescription_id,
                    values[0],
                    #drug_id,
                    values[2],
                    values[3],
                    values[4]
                ))
           
            self.db.commit()
            self.log_action(f"ثبت نسخه برای بیمار ID:{patient_id}")
            messagebox.showinfo("موفقیت", "نسخه با موفقیت ثبت شد")
            self.load_prescription_data()
           
        except Error as e:
            messagebox.showerror("خطا", f"خطا در ثبت نسخه: {str(e)}")
                                 
    def Delete_prescription(self):
        selected_item = self.prescription_list_tree.focus()
        if not selected_item:
            messagebox.showwarning("هشدار", "لطفاً یک نسخه را انتخاب کنید")
            return
        prescription_id = self.prescription_list_tree.item(selected_item)['values'][0]
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM prescription_items WHERE prescription_id = %s", (prescription_id,))
            cursor.execute("DELETE FROM prescriptions WHERE prescription_id = %s", (prescription_id,))
            self.db.commit()
            messagebox.showinfo("موفقیت", "نسخه با موفقیت حذف شد")
            self.load_prescription_data()
        except Error as e:
            messagebox.showerror("خطا", f"خطا در حذف نسخه: {str(e)}")
                
    def print_prescription(self):
        if not self.patient_combo.get():
            messagebox.showwarning("هشدار", "لطفاً ابتدا یک بیمار انتخاب کنید")
            return

        if not self.prescription_tree.get_children():
            messagebox.showwarning("هشدار", "هیچ دارویی به نسخه اضافه نشده است")
            return

        try:
            patient_name = self.patient_combo.get().split(" (ID:")[1]
            issue_date = self.prescription_date.get()
            filename = f"نسخه_{patient_name.replace(' ', '_')}_{issue_date}.pdf"
            print(filename)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"نسخه برای بیمار: {patient_name}\n")
                f.write(f"تاریخ صدور: {issue_date}\n")
                f.write(f"{'-'*40}\n")
                f.write(f"{'نام دارو':<15}{'مقدار':<10}{'دفعات':<10}{'مدت':<10}\n")
                f.write(f"{'-'*40}\n")

                for item in self.prescription_tree.get_children():
                    values = self.prescription_tree.item(item)['values']
                    drug = values[1]
                    dosage = values[2]
                    frequency = values[3]
                    duration = values[4]
                    f.write(f"{dosage:<7}{frequency:<7}{duration:<7}{drug:<7}\n")

            messagebox.showinfo("چاپ", f"نسخه در فایل {filename} ذخیره شد")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در چاپ نسخه: {str(e)}")

    # ------------------------------------------------
    def load_initial_data(self):
        if hasattr(self, 'diseases_tree'):
            self.load_diseases()
        if hasattr(self, 'patients_tree'):
            self.load_patients()
        if hasattr(self, 'appointments_tree'):
            self.load_appointments()
        if hasattr(self, 'patient_combo'):
            self.load_prescription_data()

    def run(self):
        self.window.mainloop()

    def log_action(self, action):
        with open("log.pdf", "a", encoding="utf-8") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user = self.current_user['username'] if self.current_user else 'سیستم'
            f.write(f"[{now}] ({user}) - {action}\n")

if __name__ == "__main__":
    window =Tk()
    app = MedicalSystem(window)
    app.run()