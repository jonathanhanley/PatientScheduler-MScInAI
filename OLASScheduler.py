from Patient import Patient


class OLASScheduler:
    def __init__(self, patients, appointment_duration, overlap_percentage):
        self.__patients = patients
        self.__appointment_duration = appointment_duration
        self.__overlap_percentage = overlap_percentage

    def get_schedule(self):
        schedule = []
        previous_patient = None
        for patient in self.__patients:
            if previous_patient is None:
                schedule.append(patient)
            else:
                self.__get_next_start_time(previous_patient, patient)
                schedule.append(patient)
            previous_patient = patient
        return schedule

    def __get_next_start_time(self, previous_patient: Patient, current_patient: Patient):
        start_time = previous_patient.start_time + (self.__appointment_duration * (1 - self.__overlap_percentage))
        current_patient.start_time = start_time