

class Event:

    def __init__(self,name,genre,date,time,venue,performer,ticket_price,total_tickets):
        self.name=name
        self.genre=genre
        self.date=date
        self.time=time
        self.venue=venue
        self.performer=performer
        self.ticket_price=ticket_price
        self.total_tickets=total_tickets
        self.sold_tickets=0
    