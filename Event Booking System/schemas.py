from marshmallow import Schema, fields


class PlainRoleSchema(Schema):
    id= fields.Int(dump_only=True)
    role=fields.Str(required=True)

class PlainAccountSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class PlainPerformerSchema(Schema):
    id = fields.Int(dump_only=True)
    acc_id = fields.Int(required=True)
    price = fields.Int(required=True)
    is_booked = fields.Bool(required=True)

class PlainEventSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    genre = fields.Str(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    venue_id = fields.Int(required=True)
    performer_id = fields.Int(required=True)
    organiser_id = fields.Int( load_only=True)
    ticket_price =fields.Int(required=True)
    total_tickets = fields.Int(required=True)
    sold_tickets = fields.Int(required=True)

class PlainVenueSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str()
    price = fields.Int(required=True)
    no_of_tickets = fields.Int(required=True)
    organiser_id=fields.Int()

class PlainBookingSchema(Schema):
    id= fields.Int(dump_only=True)
    user_id= fields.Int()
    no_of_tickets= fields.Int(required=True)
    event_id=fields.Int(required=True)

class PlainTicketSchema(Schema):
    id= fields.Int(dump_only=True)
    event_id=fields.Int(required=True)
    seat_id= fields.Str()
    is_booked=fields.Bool(required=True)
    
class RoleSchema(PlainRoleSchema):
    accounts = fields.List(fields.Nested(PlainAccountSchema()))

class AccountSchema(PlainAccountSchema):
    role = fields.Int(required=True)
    roles = fields.Nested(PlainRoleSchema())
    performers= fields.List(fields.Nested(PlainPerformerSchema()))
    events= fields.List(fields.Nested(PlainEventSchema()), dump_only=True)
    venues=fields.List(fields.Nested(PlainVenueSchema()), dump_only=True)
    bookings=fields.List(fields.Nested(PlainBookingSchema()))

class PerformerSchema(PlainPerformerSchema):
    accounts= fields.Nested(PlainAccountSchema())
    event = fields.Nested(PlainEventSchema())

class EventSchema(PlainEventSchema):
    organiser = fields.Nested(PlainAccountSchema())
    performer = fields.Nested(PlainPerformerSchema())
    tickets=fields.List(fields.Nested(PlainTicketSchema()))
    bookings = fields.List(fields.Nested(PlainBookingSchema()))
  
class VenueSchema(PlainVenueSchema):
    organiser=fields.Nested(PlainAccountSchema())

class BookingSchema(PlainBookingSchema):
    user = fields.Nested(PlainAccountSchema())
    tickets= fields.List(fields.Nested(PlainTicketSchema()))
    event=fields.Nested(PlainEventSchema())

class TicketSchema(PlainTicketSchema):
    bookings=fields.List(fields.Nested(PlainBookingSchema()))
    events=fields.Nested(PlainEventSchema())
    booking_id= fields.Int()





