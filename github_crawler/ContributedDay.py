from datetime import datetime


class ContributedDay:
    def __init__(self, date, contribute):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.contribute = contribute

    def __repr__(self):
        if self.contribute == 1:
            return f'You contribute {self.contribute} time on {self.date}'
        return f'You contribute {self.contribute} times on {self.date}'
