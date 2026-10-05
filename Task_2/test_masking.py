from Task_2.masking import mask_text

tests = [
    "My email is shourya@gmail.com",
    "You can call me on 9988776655 or +91 9876543210",
    "Payment has been done by card number 4111 1111 1111 1111",
    "Issue is of Order ORD-4521 , amount is Rs 499",
    "Email shourya@.com, phone 9876543210, card 4111-1111-1111-1111",
]

for t in tests:
    print("IN : " , t)
    print("OUT : " , mask_text(t) , "\n")