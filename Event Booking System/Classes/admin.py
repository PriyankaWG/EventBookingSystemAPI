from organiser import Organiser
import user
import performer
import event


class Admin:

    def __init__(self):
        self.accounts = []
        # self.user_list = []
        # self.organiser_list = []
        # self.performer_list = []
        self.events_list = []
        
        self.performer_list.append(performer.Performer("Taylor Swift","TS","TS13",13000))
        self.performer_list.append(performer.Performer("Akash Gupta","AG","AG10",5000))

        self.organiser_list.append(Organiser("Priyanka","pri","PB20"))

        self.user_list.append(user.User("User1","us1","US1"))


    def update_user_tickets(self,event):
        for item in self.user_list:
            for i in item.my_bookings:
                if i.name==event:
                    item.my_bookings.remove(i)

    def show_performers(self):
        for index, item in enumerate(self.performer_list):
            if(item.isBooked==True):
                msg="Booked"
            else:
                msg="Not Booked"
            print(f"{index+1}) Performer:{item.name}\n   Price:{item.price}\n   {msg}")
        return



    def get_performer(self,option):
        return self.performer_list[option-1]



    def get_performer_by_name(self,name):
        for item in self.performer_list:
            if(item.name)==name:
                return item


   
    def update_performer(self,performer,org_name,ev_name,bool):
        performer.organiser=org_name
        performer.event=ev_name
        performer.isBooked=bool
        return



    def book_performer(self):
        if len(self.performer_list)==0:
            print("No performers to book.")
            return 
        self.show_performers()
        option=input("Select performer you want to book:\n")
        performer=self.get_performer(int(option))
        if (performer.isBooked==False):
            return performer
        else:
            print("The performer is already booked. Choose someone else.")
            self.book_performer()   



    def add_event(self,name,genre,date,time,venue,performer,ticket_price,nbr_tickets):
        new_event=event.Event(name,genre,date,time,venue,performer,ticket_price,nbr_tickets)
        self.events_list.append(new_event)
        return



    def show_events(self):
        if(len(self.events_list)==0):
            print("No events available. Please try again later.\n\n")
            return
        for index, item in enumerate(self.events_list):
            tickets_left=item.total_tickets-item.sold_tickets
            print(f"{index+1}) EVENT:{item.name}\n   Venue:{item.venue}\n   Performer:{item.performer}\n   Date:{item.date}\n   Time:{item.time}\n   Tickets Left:{tickets_left}\n\n")
        return


    def show_event_by_performer(self):
        i=0
        for item in self.performer_list:
            if(item.isBooked==True):
                event=self.get_event_by_name(item.event)
                tickets_left=event.total_tickets-event.sold_tickets
                print(f"{i+1}) PERFORMER:{item.name}\n   Event:{event.name}\n   Venue:{event.venue}\n   Date:{event.date}\n   Time:{event.time}\n   Tickets Left:{tickets_left}\n\n")
                i+=1

    def show_event_by_genre(self, genre):
        i=0
        for item in self.events_list:
            if(item.genre==genre):
                tickets_left=item.total_tickets-item.sold_tickets
                print(f"{i+1}) EVENT:{item.name}\n   Venue:{item.venue}\n   Performer:{item.performer}\n   Date:{item.date}\n   Time:{item.time}\n   Tickets Left:{tickets_left}\n\n")
                i+=1
        if i==0:
            print("No events found for this genre. Try again later.")
            return False
        else:
            return True

    
    def get_event_by_genre(self,genre,option):
        i=0
        for item in self.events_list:
            if item.genre==genre:
                i+=1
                if i==option:
                    return item
                

    def get_event(self,option):
        return self.events_list[option-1]  



    def get_event_by_name(self,name):
        for item in self.events_list:
            if(item.name)==name:
                return item

    def get_event_by_performer(self,option):
        i=0
        for item in self.performer_list:
            if item.isBooked==True:
                i+=1
                if i==option:
                    event=self.get_event_by_name(item.event)
                    return event




    def remove_event(self,event):
        self.events_list.remove(event)
        return



    def create_user(self,name,id,password):
        new_user=user.User(name, id, password)
        self.user_list.append(new_user)
        return 



    def create_organiser(self,name,id,password):
        new_organiser=Organiser(name,id,password)
        self.organiser_list.append(new_organiser)
        return



    def create_performer(self, name, id, password):
        price=input("Enter price per show: \n")
        new_performer=performer.Performer(name,id,password,price)
        self.performer_list.append(new_performer)
        return    
        

    # def authenticate_user(self,id,password):
    #     for item in self.user_list:
    #         if (item.id==id and item.password==password):
    #             return item
    
    # def authenticate_organiser(self): 
    #     for item in self.organiser_list:
    #         if (item.id==id and item.password==password):
    #             return item
    
    # def authenticate_performer(self): 
    #     for item in self.performer_list:
    #         if (item.id==id and item.password==password):
    #             return item
        