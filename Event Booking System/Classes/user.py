import ticket

class User():

    def __init__(self, name, id, password):
        self.name=name
        self.id=id
        self.password=password
        self.my_bookings = []


    def add_bookings(self,event,tickets):

        i=0
        while i in range(tickets) and event.sold_tickets<event.total_tickets:
            new_ticket=ticket.Ticket(event.name,event.date,event.time,event.ticket_price,event.sold_tickets)
            self.my_bookings.append(new_ticket)
            event.sold_tickets+=1
            i+=1

    def delete_bookings(self,ticket,event):
            event.sold_tickets-=1
            self.my_bookings.remove(ticket)

    def show_bookings(self):
        for index, item in enumerate(self.my_bookings):
            print(f'{index+1}) Event:{item.name}\n   Seat id:{item.seat_id}')

    def get_ticket(self,index):
        return self.my_bookings[int(index)-1]


