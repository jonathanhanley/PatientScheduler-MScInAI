from OLASScheduler import OLASScheduler


class UniformScheduler(OLASScheduler):
    def __init__(self, patients, appointment_duration):
        super().__init__(patients, appointment_duration, 0)
