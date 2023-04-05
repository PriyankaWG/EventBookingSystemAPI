import event
import venue


class Organiser():

    def __init__(self, name, id, password):
        self.name=name
        self.id=id
        self.password=password
        self.venue_list = []
        self.events_list = []

    

    def add_event(self,name,genre,date,time,venue,performer,ticket_price,nbr_tickets):
        new_event=event.Event(name,genre,date,time,venue,performer,ticket_price,nbr_tickets)
        self.events_list.append(new_event)

    def get_event(self,option):
        return self.events_list[option-1] 
    
    def show_events(self):
        for index, item in enumerate(self.events_list):
            tickets_left=item.total_tickets-item.sold_tickets
            print(f"{index+1}) EVENT:{item.name}\n   Venue:{item.venue}\n   Performer:{item.performer}\n   Date:{item.date}\n   Time:{item.time}\n   Tickets Left:{tickets_left}\n\n")
        
    def delete_event(self,event):
        self.events_list.remove(event)

    def show_venue(self):
        for index,item in enumerate(self.venue_list):
            print(f'{index+1}:{item.address}\n') 
        

    def add_venue(self):
        print("ADD A VENUE")
        address= input("Enter the Address of the venue:")
        price= input("Enter the Price of the venue:")
        nbr_tickets=input("Enter the number of tickets for the venue:")

        new_venue=venue.Venue(address,int(price),int(nbr_tickets))
        self.venue_list.append(new_venue)

    def select_venue(self):
        if len(self.venue_list)==0:
            print("Empty List! First add a venue.")
            self.add_venue()

        print( "Pick a venue:\n" )
        
        self.show_venue()
        
        selected_opt = input('Your choice: ')
        return self.venue_list[int(selected_opt)-1]

    
    def delete_venue(self):
        if len(self.venue_list)==0:
            print("No venue found.")
            return
    
        print( "Pick the venue you want to delete:\n" )
        
        self.show_venue()
        
        option=input('Your choice: \n')

        self.venue_list.pop(int(option)-1)


    def check_profit(self,performer_list):
        cost=0
        self.show_events()
        option =input("Enter the event: ")
        event=self.get_event(int(option))

        venue_name=event.venue

        for item in self.venue_list:
            if item.address == venue_name:
                venue = item

        cost+=venue.price

        performer_name=event.performer

        for item in performer_list:
            if item.name == performer_name:
                performer = item

        cost+=performer.price

        revenue=0
        revenue += event.sold_tickets * event.ticket_price

        profit = revenue-cost
        print(f'Profit for {event.name} is {profit}')
