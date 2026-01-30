
print("You have reached the answering machine for Daniel Dubon.")
print('Enter name:', end= ' ')
name = input()
print('Enter contact information:', end= ' ')
contact = input()
print('Enter reason for contact:', end= ' ')
reason = input()

# Write information to a file (bonus)
file = open("messages.txt", "a")

file.write("New Message\n")
file.write("Name: " + name + "\n")
file.write("Contact Information: " + contact + "\n")
file.write("Reason for Contact: " + reason + "\n")
file.write("-" * 30 + "\n")

file.close()

print("\nYour message has been recorded. Thank you!")