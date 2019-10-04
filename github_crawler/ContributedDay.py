from datetime import datetime


class ContributedDay:
    def __init__(self, date, contributes):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.contributes = int(contributes)

    def __repr__(self):
        if self.contributes == 1:
            return f'You contribute {self.contributes} time on {self.date.date()}'
        return f'You contribute {self.contributes} times on {self.date.date()}'
