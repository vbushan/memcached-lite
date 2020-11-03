import re
import threading


def set(key, value, size, lock):
    """
    1) Validate the input.
    2) Update value if the key is already in the file, else add the key.

    """

    try:
        print(f'Setting Key {key}. User Input-({key},{value},{size}) ')

        assert(len(value) ==
               size), 'Number of bytes must be equal to the length of value'

        assert(re.match("[A-Za-z0-9]+", key)), "Invalid key error"

        print('Input data is valid')

        with lock:
            with open('db.txt', 'r+') as db:

                found = False

                content = ""

                for line in db:

                    row = line.split(" ")
                    # print(row)
                    if row[0] == key:

                        found = True
                        content += f"{key} {size} {value}\n"

                    else:
                        content += line

                #print('Content', content)

                if not found:
                    content += f"{key} {size} {value}\n"

                db.truncate(0)
                db.seek(0)
                db.write(content)

        print('Value stored')

        return 'Stored\r\n'

    except AssertionError as error:

        print('Error Occured in setting the key. Error description - \n', error)
        return 'Not Stored\r\n'


def get(key):
    """
    1) Validate the input.
    2) Return the 

    """

    try:
        print(f'Getting value of Key- {key}')
        assert(re.match("[a-zA-Z]*", key)), "Invalid key error"

        print('Key is valid')

        value = ""
        bytes = 0
        with open('db.txt', 'r') as db:

            for line in db:

                #t_key, t_bytes, t_value = tuple(line.split(" "))

                row = line.split(" ")
                t_key = row[0]
                t_bytes = row[1]
                t_value = ' '.join(row[2:])

                if t_key == key:

                    bytes = t_bytes
                    value = t_value

                    break

        resp = f"VALUE {key} {bytes}\r\n{value}\r\n"

        # if value:
        print('Read Value', resp)
        return resp

        # Else return a user-friendly message

    except:
        print("Error Occured in getting the value")
        return "Not found"
