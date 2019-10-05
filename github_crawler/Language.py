from multiprocessing import Lock


class Language:
    lock = Lock()
    language_dict = {}
    total_use = 0.0

    def __init__(self, language, use):
        with self.lock:
            if language not in self.language_dict.keys():
                self.name = language
                self.use = use
            else:
                self.language_dict[language] += use
        self.total_use += use

    def __repr__(self):
        if self.total_use == 0:
            raise ZeroDivisionError
        return f'{self.name}: {self.use/self.total_use}'
