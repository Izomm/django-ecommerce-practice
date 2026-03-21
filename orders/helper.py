import random

data = {
    'first_name': ['James', 'Amina', 'Carlos', 'Yuki', 'Fatima'],
    'last_name': ['Smith', 'Okafor', 'Rivera', 'Tanaka', 'Al-Hassan'],
    'email': ['james@email.com', 'amina@email.com', 'carlos@email.com', 'yuki@email.com', 'fatima@email.com'],
    'address': ['12 Baker St', '45 Elm Ave', '8 Mango Close', '77 Sakura Lane', '3 Desert Rd'],
    'postal_code': ['10001', '20002', '30003', '40004', '50005'],
    'city': ['New York', 'Lagos', 'Mexico City', 'Tokyo', 'Riyadh'],
}

def randomData(data = data):
    random_data = {field: random.choice(values) for field, values in data.items()}
    
    #if  you want to strictly pick for 1 person
    i = random.randint(0, 4)
    random_entry = {field: values[i] for field, values in data.items()}

    return random_data