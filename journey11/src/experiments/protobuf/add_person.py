#! /usr/bin/env python

# Modified from https://raw.githubusercontent.com/protocolbuffers/protobuf/master/examples/add_person.py

import journey11.src.experiments.protobuf.addressbook_pb2 as addressbook_pb2
import sys

raw_input = input  # Python 3


# This function fills in a Person message based on user input.
def PromptForAddress(person):
    person.id = 3142
    person.name = "Necromancer"
    person.email = "necro@gmail.com"

    phone_number = person.phones.add()
    phone_number.number = "123456789"
    type = "home"
    if type == "mobile":
        phone_number.type = addressbook_pb2.Person.MOBILE
    elif type == "home":
        phone_number.type = addressbook_pb2.Person.HOME
    elif type == "work":
        phone_number.type = addressbook_pb2.Person.WORK
    else:
        print("Unknown phone type; leaving as default value.")

    pn2 = person.PhoneNumber()
    pn2.type =addressbook_pb2.Person.WORK
    pn2.number = "0876373784"
    person.phone2.CopyFrom(pn2)

    print(str(phone_number))
    return

def main():
    # Read the existing address book.
    try:
        with open(sys.argv[1], "rb") as f:
            address_book.ParseFromString(f.read())
    except IOError:
        print(sys.argv[1] + ": File not found.  Creating a new file.")

    # Add an address.

    # Write the new address book back to disk.
    with open(sys.argv[1], "wb") as f:
        f.write(address_book.SerializeToString())


if __name__ == "__main__":
    address_book = addressbook_pb2.AddressBook()
    PromptForAddress(address_book.people.add())
