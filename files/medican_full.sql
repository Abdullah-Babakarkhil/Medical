
DROP DATABASE IF EXISTS mediican;
CREATE DATABASE mediican CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE mediican;

-- Users
INSERT INTO users (user_id, full_name, username, password, role, is_active) VALUES (4, 'حسین رضا زاده', 'user4', SHA2('password123', 256), 'staff', FALSE);
INSERT INTO users (user_id, full_name, username, password, role, is_active) VALUES (5, 'جناب آقای دکتر مبین نوری', 'user5', SHA2('password123', 256), 'admin', TRUE);
INSERT INTO users (user_id, full_name, username, password, role, is_active) VALUES (6, 'نازنين علی شاهی', 'user6', SHA2('password123', 256), 'admin', TRUE);
INSERT INTO users (user_id, full_name, username, password, role, is_active) VALUES (7, 'عباس ضابطی', 'user7', SHA2('password123', 256), 'staff', TRUE);
INSERT INTO users (user_id, full_name, username, password, role, is_active) VALUES (8, 'اسرا کرمانی', 'user8', SHA2('password123', 256), 'admin', FALSE);
INSERT INTO users (user_id, full_name, username, password, role, is_active) VALUES (9, 'عسل علیجانی', 'user9', SHA2('password123', 256), 'staff', TRUE);
INSERT INTO users (user_id, full_name, username, password, role, is_active) VALUES (10, 'كیانا اشتری', 'user10', SHA2('password123', 256), 'admin', TRUE);
INSERT INTO users (user_id, full_name, username, password, role, is_active) VALUES (11, 'كیان عقیلی', 'user11', SHA2('password123', 256), 'admin', TRUE);
INSERT INTO users (user_id, full_name, username, password, role, is_active) VALUES (12, 'حلما ملکیان', 'user12', SHA2('password123', 256), 'admin', TRUE);
INSERT INTO users (user_id, full_name, username, password, role, is_active) VALUES (13, 'جناب آقای دکتر علیرضا پویان', 'user13', SHA2('password123', 256), 'admin', TRUE);

-- Patients
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (4, 'ايليا', 'شبیری', '1999-05-18', 'male', '+98 912 654 2351');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (5, 'نازنین', 'صیادی', '1950-11-16', 'male', '011 5940 7816');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (6, 'فاطمه زهرا', 'میردامادی', '1964-03-30', 'male', '+98 58 9593 1034');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (7, 'فاطمه زهرا', 'رسته', '2003-04-05', 'female', '+98 999 647 5255');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (8, 'مائده', 'یزدی', '1962-06-18', 'male', '0192 8327 6483');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (9, 'اميررضا', 'ظفری', '2001-08-26', 'female', '0920 305 6413');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (10, 'ایلیا', 'عبدالمالکی', '1965-09-16', 'male', '026 7672 4238');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (11, 'امیرمهدی', 'شاکری', '1995-02-17', 'male', '+98 76 6965 3287');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (12, 'نازنین', 'کمالی', '1947-07-03', 'male', '+98 932 269 1669');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (13, 'محمدرضا', 'سغیری', '1961-05-27', 'male', '+98 13 0184 5146');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (14, 'الینا', 'ترکاشوند', '1944-07-07', 'female', '024 8281 4893');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (15, 'حدیث', 'صارمی', '1996-03-08', 'male', '+98 903 880 9570');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (16, 'رقیه', 'شمشیری', '2004-02-03', 'female', '028 3039 1171');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (17, 'پارسا', 'پارسا', '1996-05-29', 'female', '+98 901 278 2489');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (18, 'دانیال', 'نوروزی', '2007-07-05', 'male', '056 3465 7871');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (19, 'سوگند', 'نوری', '1948-08-26', 'female', '044 0983 9301');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (20, 'علي', 'هومن', '1948-04-20', 'male', '025 1051 8347');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (21, 'نازنين', 'ضابطی', '1953-04-19', 'female', '077 9737 6311');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (22, 'متين', 'سعیدی', '1968-05-28', 'male', '+98 17 6701 0651');
INSERT INTO patients (patient_id, first_name, last_name, birth_date, gender, phone) VALUES (23, 'سوگند', 'خسروجردی', '1957-03-28', 'female', '+98 56 7262 4731');

-- Diseases
INSERT INTO diseases (disease_id, name, category, severity) VALUES (4, 'numquamی', 'تنفسی', 3);
INSERT INTO diseases (disease_id, name, category, severity) VALUES (5, 'quoی', 'مزمن', 4);
INSERT INTO diseases (disease_id, name, category, severity) VALUES (6, 'consequunturی', 'ویروسی', 2);
INSERT INTO diseases (disease_id, name, category, severity) VALUES (7, 'architectoی', 'مزمن', 3);
INSERT INTO diseases (disease_id, name, category, severity) VALUES (8, 'totamی', 'گوارشی', 2);
INSERT INTO diseases (disease_id, name, category, severity) VALUES (9, 'quisی', 'تنفسی', 2);
INSERT INTO diseases (disease_id, name, category, severity) VALUES (10, 'accusantiumی', 'تنفسی', 3);
INSERT INTO diseases (disease_id, name, category, severity) VALUES (11, 'consecteturی', 'ویروسی', 1);
INSERT INTO diseases (disease_id, name, category, severity) VALUES (12, 'exی', 'تنفسی', 5);
INSERT INTO diseases (disease_id, name, category, severity) VALUES (13, 'doloremqueی', 'تنفسی', 4);

-- Symptoms
INSERT INTO symptoms (symptom_id, name, description) VALUES (4, 'تب', 'Laborum distinctio id animi fugiat voluptates.');
INSERT INTO symptoms (symptom_id, name, description) VALUES (5, 'سرفه', 'Unde quos eligendi possimus quas.');
INSERT INTO symptoms (symptom_id, name, description) VALUES (6, 'خستگی', 'Optio laborum deleniti dolor animi quasi aperiam.');
INSERT INTO symptoms (symptom_id, name, description) VALUES (7, 'درد شکم', 'Animi nesciunt magnam sequi culpa vero.');
INSERT INTO symptoms (symptom_id, name, description) VALUES (8, 'تهوع', 'Sed architecto architecto similique.');
INSERT INTO symptoms (symptom_id, name, description) VALUES (9, 'سرگیجه', 'Blanditiis tempora doloribus nisi nulla in.');
INSERT INTO symptoms (symptom_id, name, description) VALUES (10, 'تنگی نفس', 'Natus et ea pariatur et eaque consectetur officia.');
INSERT INTO symptoms (symptom_id, name, description) VALUES (11, 'بی‌خوابی', 'Et quibusdam asperiores itaque voluptatum voluptatum asperiores.');
INSERT INTO symptoms (symptom_id, name, description) VALUES (12, 'خارش', 'Magni consequatur expedita architecto doloribus.');
INSERT INTO symptoms (symptom_id, name, description) VALUES (13, 'افسردگی', 'Culpa rerum provident nostrum voluptates.');

-- Disease Symptoms
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (4, 11);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (4, 4);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (5, 10);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (5, 13);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (6, 4);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (6, 13);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (7, 6);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (7, 6);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (8, 12);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (8, 10);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (9, 7);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (9, 11);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (10, 6);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (10, 6);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (11, 5);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (11, 11);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (12, 10);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (12, 13);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (13, 13);
INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (13, 8);

-- Drugs
INSERT INTO drugs (drug_id, name) VALUES (4, 'استامینوفن');
INSERT INTO drugs (drug_id, name) VALUES (5, 'آزیترومایسین');
INSERT INTO drugs (drug_id, name) VALUES (6, 'آموکسی‌سیلین');
INSERT INTO drugs (drug_id, name) VALUES (7, 'انسولین');
INSERT INTO drugs (drug_id, name) VALUES (8, 'قرص معده');
INSERT INTO drugs (drug_id, name) VALUES (9, 'ضد حساسیت');
INSERT INTO drugs (drug_id, name) VALUES (10, 'ویتامین D');

-- Appointments
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (3, 13, 9, '2025-04-24 17:47:56', 'no show', 'Ab repellendus error optio vel consequatur blanditiis.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (4, 23, 4, '2025-04-11 11:10:59', 'no show', 'Culpa eligendi distinctio exercitationem porro sequi magnam.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (5, 15, 4, '2025-04-14 23:07:08', 'scheduled', 'At incidunt eius.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (6, 8, 11, '2025-04-08 22:53:44', 'no show', 'Quo odio ea qui mollitia incidunt.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (7, 4, 13, '2025-04-09 02:27:47', 'no show', 'Asperiores sunt temporibus molestias.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (8, 23, 10, '2025-04-17 19:54:51', 'scheduled', 'Mollitia inventore aliquam facilis ut voluptas aliquam facere.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (9, 10, 12, '2025-04-25 10:09:46', 'no show', 'Pariatur explicabo nam soluta voluptate.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (10, 15, 13, '2025-04-27 01:25:57', 'scheduled', 'Unde dolores cum reiciendis.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (11, 23, 4, '2025-04-13 03:58:14', 'canceled', 'Ad qui ex ut rem sint.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (12, 5, 4, '2025-04-28 13:07:33', 'canceled', 'Eaque ratione autem sit similique.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (13, 11, 5, '2025-04-14 06:24:26', 'completed', 'Repellendus itaque esse recusandae dolorem.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (14, 16, 9, '2025-04-09 10:36:56', 'completed', 'Id eius architecto quo expedita.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (15, 8, 4, '2025-04-21 05:34:50', 'scheduled', 'Perspiciatis sapiente ex adipisci soluta ea.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (16, 22, 7, '2025-04-22 23:02:53', 'scheduled', 'Alias nisi exercitationem ratione ipsa.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (17, 12, 8, '2025-04-21 06:45:20', 'completed', 'Harum nemo ducimus provident.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (18, 4, 8, '2025-04-08 21:48:55', 'completed', 'Unde modi quaerat quia perferendis facilis architecto.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (19, 8, 10, '2025-04-24 23:46:36', 'completed', 'Numquam optio commodi tempore magni pariatur.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (20, 4, 13, '2025-04-16 18:50:44', 'no show', 'Possimus mollitia deleniti pariatur fugit quibusdam.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (21, 7, 9, '2025-04-13 02:12:30', 'scheduled', 'Necessitatibus illo rerum esse distinctio ratione non eum.');
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status, notes) VALUES (22, 8, 11, '2025-04-19 14:11:21', 'completed', 'Perferendis maiores recusandae vero quasi omnis.');

-- Prescriptions & Items
INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, issue_date) VALUES (3, 18, 5, '2025-04-01');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (3, 6, '111mg', '3 بار در روز', '4 روز');
INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, issue_date) VALUES (4, 23, 13, '2025-04-13');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (4, 10, '271mg', '2 بار در روز', '9 روز');
INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, issue_date) VALUES (5, 17, 12, '2025-04-04');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (5, 8, '320mg', '1 بار در روز', '4 روز');
INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, issue_date) VALUES (6, 13, 8, '2025-03-23');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (6, 7, '416mg', '2 بار در روز', '5 روز');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (6, 8, '499mg', '3 بار در روز', '9 روز');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (6, 10, '185mg', '2 بار در روز', '6 روز');
INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, issue_date) VALUES (7, 20, 13, '2025-03-30');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (7, 4, '325mg', '3 بار در روز', '5 روز');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (7, 4, '361mg', '2 بار در روز', '10 روز');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (7, 9, '247mg', '2 بار در روز', '5 روز');
INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, issue_date) VALUES (8, 23, 8, '2025-04-03');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (8, 4, '303mg', '2 بار در روز', '8 روز');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (8, 10, '294mg', '1 بار در روز', '5 روز');
INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, issue_date) VALUES (9, 4, 5, '2025-03-29');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (9, 4, '451mg', '1 بار در روز', '10 روز');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (9, 10, '428mg', '2 بار در روز', '4 روز');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (9, 4, '174mg', '1 بار در روز', '6 روز');
INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, issue_date) VALUES (10, 21, 10, '2025-03-28');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (10, 9, '280mg', '3 بار در روز', '9 روز');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (10, 9, '479mg', '2 بار در روز', '7 روز');
INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, issue_date) VALUES (11, 14, 7, '2025-03-26');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (11, 4, '130mg', '3 بار در روز', '8 روز');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (11, 9, '239mg', '1 بار در روز', '10 روز');
INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, issue_date) VALUES (12, 11, 4, '2025-03-20');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (12, 5, '493mg', '3 بار در روز', '6 روز');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (12, 7, '149mg', '2 بار در روز', '7 روز');
INSERT INTO prescription_items (prescription_id, drug_id, dosage, frequency, duration) VALUES (12, 4, '355mg', '3 بار در روز', '3 روز');
