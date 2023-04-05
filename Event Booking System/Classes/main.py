import admin


class Application:

    def __init__(self,):
        self.admin=admin.Admin()

    
    def book_tickets(self,user,event,nbr_tickets):

        if(event.sold_tickets>=event.total_tickets):
            print("Event fully booked!")
            self.user_ui(user)
        
        elif(nbr_tickets > event.total_tickets-event.sold_tickets ):
            print(f'Only {event.total_tickets-event.sold_tickets} tickets left\n')
            self.user_ui(user)
    
        else:
            user.add_bookings(event,nbr_tickets)
            for i in self.admin.organiser_list:
                for item in i.events_list:
                    if item.name==event.name:
                        item.sold_tickets+=nbr_tickets

        return



    def book_tickets_ui(self,user):
        if (len(self.admin.events_list)==0):
            print("No Events present. Please Try later!")
            return
        
        else:
            print("View events by:\n\n   1)Name\n   2)Performer\n   3)Genre\n   4)Back\n\n")

            option=input("Your choice: \n\n")

            if (option=="1"):
                self.admin.show_events()

                selected_opt=input("Select event of your choice:\n")
                event=self.admin.get_event(int(selected_opt))

                tickets=input("Enter the number of tickets you want: ")
                self.book_tickets(user,event,int(tickets))
                return
            
            elif (option=="2"):
                self.admin.show_event_by_performer()

                selected_opt=input("Select event of your choice:\n")
                event=self.admin.get_event_by_performer(int(selected_opt))

                tickets=input("Enter the number of tickets you want: ")
                self.book_tickets(user,event,int(tickets))
                return
            
            elif (option=="3"):
                Genre=["Comedy","Musical","Theatre"]
                print("Available Genres:\n")
                
                for index,item in enumerate(Genre):
                    print(f"{index+1}) {item}\n")

                option =input("Select the genre of your choice:\n")
                bool=self.admin.show_event_by_genre(Genre[int(option)-1])
                if bool==False:
                    self.book_tickets_ui(user)

                selected_opt=input("Select event of your choice:\n")

                event=self.admin.get_event_by_genre(Genre[int(option)-1],int(selected_opt))

                tickets=input("Enter the number of tickets you want: ")
                self.book_tickets(user,event,int(tickets))
                self.user_ui(user)


    
    def unbook_tickets(self,user):
        if(len(user.my_bookings)==0):
            print("No bookings to be deleted")
            return

        user.show_bookings()
        selected_opt=input("Choose the ticket you want to unbook: \n")

        ticket=user.get_ticket(selected_opt)
        event_name=ticket.name
        event=self.admin.get_event_by_name(event_name)
        user.delete_bookings(ticket,event)
        return
      



    def user_ui(self,user):
        print("\n\nWelcome User!\n")
        option=input("Choose an action: \n1) Book Tickets to an event\n2) Cancel Tickets\n3) My bookings\n4) Back\n")

        if(option=="1"):
            self.book_tickets_ui(user)
            self.user_ui(user)

        elif(option=="2"):
            nbr_tickets=input("Enter the number of tickets to be cancelled:\n")
            for i in range(int(nbr_tickets)):
                self.unbook_tickets(user)
            self.user_ui(user)
            
        elif (option=="3") :
            user.show_bookings()
            self.user_ui(user)

        elif (option=="4"):
            return

        else:
            print("Invalid input.")
            self.user_ui(user)



    
    def add_event(self,organiser):
        print("ADD AN EVENT\n")
        ev_name= input("Enter the name of the event:\n")

        #Choosing genre
        Genre=["Comedy","Musical","Theatre"]
        for index,item in enumerate(Genre):
            print(f"\n{index+1}) {item}")

        option= input("\nEnter the genre of the event:\n")

        genre=Genre[int(option)-1]

        #Choosing date and time
        date= input("Enter the date of the event:\n")
        time= input("Enter the time of the event:\n")

        #Choosing venue and performer    
        venue=organiser.select_venue()
        performer=self.admin.book_performer()
        self.admin.update_performer(performer,organiser.name,ev_name,True)

        #Selecting price of ticket
        min_ticket_price=(performer.price+venue.price)/venue.nbr_tickets

        ticket_price='0'
        while(int(ticket_price)<min_ticket_price):
            ticket_price=input(f'Breakeven Price for this event: {min_ticket_price}\nEnter the price of each ticket: \n')

        #Adding event
        self.admin.add_event(ev_name,genre,date,time,venue.address,performer.name,int(ticket_price),venue.nbr_tickets)
        organiser.add_event(ev_name,genre,date,time,venue.address,performer.name,int(ticket_price),venue.nbr_tickets)
        return




    def delete_event(self,organiser):
        print("Pick the event you want to delete:\n")
        
        organiser.show_events()
        option=input()

        event=organiser.get_event(int(option))
        name=event.name
        performer_name=event.performer
        performer=self.admin.get_performer_by_name(performer_name)
        self.admin.update_performer(performer,'','',False)
        organiser.delete_event(event)

        event=self.admin.get_event_by_name(name)
        self.admin.remove_event(event)

        self.admin.update_user_tickets(name)
        return




    def organiser_ui(self,organiser):
        print("\n\nWelcome Organiser!\n")

        option=input("Choose an action.\n\n1)Add an event\n2)Delete an event\n3)Add a venue\n4)Check profit\n5)My Events\n6)My Venues\n7)Back\n")

        if (option == "1"):
            self.add_event(organiser)
            self.organiser_ui(organiser)

        elif (option =="2"):
            self.delete_event(organiser)
            self.organiser_ui(organiser)

        elif (option == "3"):
            organiser.add_venue()
            self.organiser_ui(organiser)

        # elif (option == "4"):
        #     organiser.delete_venue()
        #     self.organiser_ui(organiser)

        elif (option =="4"):
            organiser.check_profit(self.admin.performer_list)
            self.organiser_ui(organiser)

        elif (option =="5"):
            organiser.show_events()
            self.organiser_ui(organiser)
        
        elif (option == "6"):
            organiser.show_venue()
            self.organiser_ui(organiser)

        elif (option == "7"):
            return

        else:
            print("Invalid input")
            self.organiser_ui(organiser)




    def performer_ui(self,performer):

        print("Welcome Performer!\n")
        option=input("Choose an action.\n1) Check event \n 2) Check Organiser\n3) Back")

        if (option == "1"):
            performer.check_event()
            self.performer_ui(performer)

        elif (option =="2"):
            performer.check_organiser()
            self.performer_ui(performer)

        elif (option =="3"):
            return
        
        else:
            print("Invalid User")
            self.performer_ui()

        


    def login(self):
        id=input("Enter your id: \n")
        password=input("Enter your password:\n")

        for item in self.admin.user_list:
            if (item.id==id and item.password==password):
                user=item
                self.user_ui(user)
                return
        

        for item in self.admin.organiser_list:
            if (item.id==id and item.password==password):
                organiser=item
                self.organiser_ui(organiser)
                return

        for item in self.admin.performer_list:
            if (item.id==id and item.password==password):
                performer=item
                self.performer_ui(performer)
                return
    
            print("No such account found")
            return




    def signup(self):

        option=["User","Organiser","Performer","Back"]
        print("Choose the type of account:")

        for index, item in enumerate(option):
            print(f'{index+1}) {item}\n')

        type = input()
            
        name=input("Enter your name: \n")
        id=input("Enter your id: \n")
        password=input("Enter your password:\n")

        if type=="1":
            self.admin.create_user(name,id,password)
            return

        elif type=="2":
            self.admin.create_organiser(name,id,password)
            return

        elif type=="3":
            self.admin.create_performer(name,id,password)
            return

        elif type=="4":
            return
        
        else:
            print("Invalid Input")
            self.signup()





if __name__=="__main__":
    
    app=Application()

    print("       WELCOME TO EVENT BOOKING SYSTEM      \n\n")

    user_input=0
    while(user_input!="3"):
        print("CURRENT EVENTS\n")
        app.admin.show_events()
        user_input=input("1)Existing Account \n2)New Account \n3)Exit\n\n")

        if(user_input=="1"):
            app.login()
        elif(user_input=="2"):
            app.signup()
        elif(user_input !="1" and user_input !="2" and user_input !="3"):
            print("Invalid input")

        