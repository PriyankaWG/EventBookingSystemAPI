

class Ticket:

    def __init__(self,name,date,time,price,seat_id):
        self.name=name
        self.date=date
        self.time=time
        self.price=price
        self.seat_id=seat_id

    def __str__(self):
        return f"{self.name} on {self.date} {self.time} \n price:{self.price} \n seat id: {self.seat_id}"
