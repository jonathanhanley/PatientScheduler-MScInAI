from Patient import Patient
import joblib
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


class DummyPredictor:
    def __init__(self):
        # Adds a cache to save us reclassifying the attendance multiple times.
        self.cache = {}

    def attends(self,  patient: Patient):
        return True


class Predictor(DummyPredictor):
    def __init__(self):
        super().__init__()
        self.model = joblib.load("models/knn.joblib")

    def attends(self,  patient: Patient):
        try:
            result = self.model.predict(patient.meta_data)
            self.cache[patient] = result
            return result
        except ValueError:
            return True


class PredictorWithCache(Predictor):
    def __init__(self):
        super().__init__()
        # Adds a cache to save us reclassifying the attendance multiple times.
        self.cache = {}

    def attends(self, patient: Patient):
        if patient in self.cache:
            return self.cache.get(patient)

        return super().attends(patient)


def get_predictor():
    try:
        return PredictorWithCache()
    except NotImplementedError:
        return DummyPredictor()
