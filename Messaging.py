import json
import pprint
from datetime import datetime

Guests = json.load(open('Guests.json'))
Companies = json.load((open('Companies.json')))
Templates = json.load((open('Templates.json')))


def is_yes(word):
    return word.lower() in ['y', 'ye', 'yes', 'yea', 'ya']


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def time_of_day(time):
    hours = time.hour
    if hours < 4:
        return 'Night'
    elif hours < 12:
        return 'Morning'
    elif hours < 5:
        return 'Afternoon'
    elif hours < 8:
        return 'Evening'
    else:
        return 'Night'


# Checks for invalid or empty keys, replaces invalid/empty keys with variable name surrounded
# by angle brackets, and prints a warning message if replaced
def convert_key(dictionary, key):
    try:
        dictionary
    except:
        print("The object for {0} is undefined. You may have to replace it manually".format(key))
        return "<0>".format(key)
    else:
        try:
            dictionary[key]
        except:
            print("A key for {0} is undefined. You may have to replace it manually.".format(key))
            return "<0>".format(key)
        else:
            if dictionary[key] == "":
                print ("missing {0} variable. You may have to replace it manually.".format(key))
                return "{0}".format(key)
            else:
                return dictionary[key]


# Finds and replaces variables from guest or company within template and
# returns the respective message
def find_replace(template, guest, company):
    guest_to_message = {
        '<firstName>': guest['firstName'],
        '<lastName>': guest['lastName'],
        '<roomNumber>': guest['reservation']['roomNumber'],
        '<startTimestamp>': convert_time(guest['reservation']['startTimestamp']),
        '<endTimestamp>': convert_time(guest['reservation']['endTimestamp']),
    }

    company_to_message = {
        '<company>': company['company'],
        '<city>': company['city'],
        '<timezone>': company['timezone'],
    }

    var_to_message = {
        '<timeOfDay>': time_of_day(datetime.now()),
        '<greeting>': 'Good' + str(time_of_day(datetime.now()))
    }
    new_message = template['message']
    for key in guest_to_message.keys():
        new_message = new_message.replace(str(key), str(convert_key(guest_to_message, key)))

    for key in company_to_message.keys():
        new_message = new_message.replace(str(key), str(convert_key(company_to_message, key)))

    for key in var_to_message.keys():
        new_message = new_message.replace(str(key), str(convert_key(var_to_message, key)))

    return new_message


# Converts integer time to year/month/day hour:minute format
def convert_time(time):
    t = datetime.fromtimestamp(time / 1e3)
    return '' + str(t.year) + '/' + str(t.month) + '/' + str(t.day) + \
           ' ' + str(t.hour) + ':' + str(t.minute)


# Print every template in Templates.json in order
def print_all_templates():
    for template in Templates:
        pprint.pprint(template)
        print('\n')


# Print every guest in Guests.json in order
def print_all_guests():
    for guest in Guests:
        pprint.pprint(guest)
        print('\n')


# Print every company in Companies.json in order
def print_all_companies():
    for company in Companies:
        pprint.pprint(company)
        print('\n')


# Create a new template from terminal input
def new_template():
    title = input('Enter template title: ')
    print('\nYour message may contain placeholders for <variables>.  For example: \n')
    print(str(Templates[0]['message']) + '\n')
    message = input('Enter template message: ')
    template = {'id': len(Templates)+1,
                'title': title,
                'message': message
                }
    Templates.append(template)
    with open('Templates.json', 'w') as fp:
        json.dump(Templates, fp)
    print('Template Saved')


# Message a guest with a new template and potentially save the new template
def new_message_guest():
    print('Your message may contain placeholders for <variables>.  For example:')
    print(Templates[0]['message'])
    message = input('Enter template message: ')
    title = 'Title'
    if is_yes(input('Save template? ')):
        title = input('Input Title: ')
        template = {'id': len(Templates)+1,
                    'title': title,
                    'message': message
                    }
        Templates.append(template)
        with open('Templates.json', 'w') as fp:
            json.dump(Templates, fp)
        print('Template Saved')
    else:
        template = {'id': len(Templates)+1,
                    'title': title,
                    'message': message
                    }

    guest_id = input('Enter guestID: ')
    while not is_int(guest_id) or int(guest_id) < 1 or int(guest_id) > len(Guests):
        print("Guest ID must be an integer between 1 and {0}".format(len(Guests)))
        guest_id = input('Enter guestID: ')

    company_id = (input('Enter companyID: '))
    while not is_int(company_id) or int(company_id) < 1 or int(company_id) > len(Companies):
        print("Company ID must be an integer between 1 and {0}".format(len(Companies)))
        company_id = (input('Enter companyID: '))

    message = find_replace(template,
                           Guests[int(guest_id)-1],
                           Companies[int(company_id)-1])
    print(message)  # replace with send(message)


# Message a guest using a template that already exists in the system
def existing_message_guest():
    template_id = input('Enter template ID: ')
    while not is_int(template_id) or int(template_id) < 1 or int(template_id) > len(Templates):
        print("Template ID must be an integer between 1 and {0}".format(len(Templates)))
        template_id = input('Enter templateID: ')

    guest_id = input('Enter guest ID: ')
    while not is_int(guest_id) or int(guest_id) < 1 or int(guest_id) > len(Guests):
        print("Guest ID must be an integer between 1 and {0}".format(len(Guests)))
        guest_id = input('Enter guest ID: ')

    company_id = (input('Enter company ID: '))
    while not is_int(company_id) or int(company_id) < 1 or int(company_id) > len(Companies):
        print("Company ID must be an integer between 1 and {0}".format(len(Companies)))
        company_id = (input('Enter company ID: '))

    message = find_replace(Templates[int(template_id)-1],  # Note that this only works if templates remain in order
                           Guests[int(guest_id)-1],
                           Companies[int(company_id)-1])

    print(message)  # replace with send(message)


# Displays the menu for messaging a guest
def message_guest():
    menu_options = ['0', '1']
    selection = input('How  would you like to message your guest?\n'
                      '0: Use existing template\n'
                      '1: Use new template\n')
    while selection not in menu_options:
        print('Invalid selection.  Select from the following')
        selection = input('How  would you like to message your guest?\n'
                          '0: Use existing template\n'
                          '1: Use new template\n')

    if selection == '0':
        existing_message_guest()
    elif selection == '1':
        new_message_guest()
    else:
        print ("You broke guest messaging. How'd you do that?")
        message_guest()


# Displays the main menu
def main_menu():
    print ("Main menu")
    menu_options = ['0', '1', '2', '3', '4', '5']
    selection = input('What would you like to do?\n'
                      '0. Message Guests\n'
                      '1. New Template\n'
                      '2. View all templates\n'
                      '3. View all guests\n'
                      '4. View all companies\n'
                      '5. Exit program\n')
    while selection not in menu_options:
        print("invalid selection")
        selection = input('What would you like to do?\n'
                          '0. Message Guests\n'
                          '1. New Template\n'
                          '2. View all templates\n'
                          '3. View all guests\n'
                          '4. View all companies\n'
                          '5. Exit program\n')
    if selection == '0':
        message_guest()
    elif selection == '1':
        new_template()
    elif selection == '2':
        print_all_templates()
    elif selection == '3':
        print_all_guests()
    elif selection == '4':
        print_all_companies()
    elif selection == '5':
        return False
    else:
        print ("You broke the main menu.  How'd you do that?")
    return True


if __name__ == '__main__':
    while main_menu():
        print('\n')
