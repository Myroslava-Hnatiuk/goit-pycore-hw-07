def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact is not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
    
@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."
  
@input_error
def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args, contacts): 
    name = args[0]
    return contacts[name]
    
@input_error
def show_all(contacts): 
    result = []
    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")
    return "\n".join(result)
