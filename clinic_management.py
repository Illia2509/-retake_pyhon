import json
from datetime import datetime


# Декаратор для проверки календаря
def check_schedule(func):
    def wrapper(self, patient_id, date_time):
        if date_time in self.schedule:
            print(f"Помилка: Лікар зайнятий на {date_time}")
            return False
        return func(self, patient_id, date_time)
    return wrapper


# Класс для доктора
class Doctor:
    def __init__(self, doctor_id, name, specialty, schedule=None):
        self.doctor_id = doctor_id
        self.name = name
        self.specialty = specialty
        self.schedule = schedule if schedule else {}

    @check_schedule
    def add_appointment(self, patient_id, date_time):
        self.schedule[date_time] = patient_id
        print(f"Запис додано: {self.name}, {date_time} для пацієнта {patient_id}")
        return True

    def to_dict(self):
        return {
            "doctor_id": self.doctor_id,
            "name": self.name,
            "specialty": self.specialty,
            "schedule": self.schedule
        }


# Класс для пациента
class Patient:
    def __init__(self, patient_id, name, age):
        self.patient_id = patient_id
        self.name = name
        self.age = age

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age
        }


# Клас для управление клиникой
class Clinic:
    def __init__(self, doctors_file='doctors.json', patients_file='patients.json'):
        self.doctors_file = doctors_file
        self.patients_file = patients_file
        self.doctors = self.load_data(doctors_file, Doctor)
        self.patients = self.load_data(patients_file, Patient)

    def load_data(self, file_name, obj_class):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [obj_class(**item) for item in data]
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.doctors_file, 'w', encoding='utf-8') as f:
            json.dump([d.to_dict() for d in self.doctors], f, indent=4, ensure_ascii=False)
        with open(self.patients_file, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.patients], f, indent=4, ensure_ascii=False)

    def add_doctor(self, doctor_id, name, specialty):
        doctor = Doctor(doctor_id, name, specialty)
        self.doctors.append(doctor)
        self.save_data()

    def add_patient(self, patient_id, name, age):
        patient = Patient(patient_id, name, age)
        self.patients.append(patient)
        self.save_data()

    def make_appointment(self, doctor_id, patient_id, date_time):
        doctor = next((d for d in self.doctors if d.doctor_id == doctor_id), None)
        if not doctor:
            print("Лікар не знайдений")
            return False

        if not next((p for p in self.patients if p.patient_id == patient_id), None):
            print("Пацієнт не знайдений")
            return False

        if doctor.add_appointment(patient_id, date_time):
            self.save_data()
            return True
        return False


# Пример работы
if __name__ == "__main__":
    clinic = Clinic()

    # Додавання лікарів і пацієнтів
    clinic.add_doctor(1, "Іван Іванов", "Кардіолог")
    clinic.add_patient(1, "Петро Петренко", 45)

    # Створення запису
    clinic.make_appointment(1, 1, "2024-12-21 11:00")




