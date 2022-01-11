# Simple site for small business (Optic Store)

# You can:
1. Find the Product you want and Order it 
2. Make an appointment with the doctor
3. Send a message, make a suggestion, ask for information...
4. Register as a Customer and gain 5% discount as a new User

# Through implementation of Django Signals:
1. On every appointment submitted, one mail is send to the secretary for confirmation and specification of details.
2. When appointment is set and confirmed, one mail is sent to the doctor with the details and exact time of the appointment
3. By registering as User, mail is sent to you with unique uuid code for corresponding discount on first order.

# With Django Rest_framework:
1. Get APIs for Products, Orders, Appointments and Used Coupons 
2. Post APIs for creating new Product
