
class Performer():

    def __init__(self, name, id, password, price):
        self.name=name
        self.id=id
        self.password=password
        self.price=price
        self.organiser=''
        self.event=''
        self.isBooked=False

    def check_event(self):
        if self.event == '':
            print("No event booked")
        else:
            return self.event

    def check_organiser(self):
        if self.organiser == '':
            print("No organiser has booked you")
        else:
            return self.organiser

