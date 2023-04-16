ORM_OBJ_COL_NAMES = {'item': ('item_name', 'Category', 'amount'),
                     'rental':('rental_name', 'Client', 'rental_date', 'details', 'rental_status'),
                     'category': ('category_name',),
                     'client': ('client_name', 'phone_number', 'email')
                     }

DEBUG = True
HEADERS_CLIENTS = ['Name', 'Phone', 'Email', '_filter']
HEADERS_CATS = ['Category', '_filter']
HEADERS_RENTALS = ['Event/Rent', 'Client', 'Date', 'Descr', 'Status', '_filter']
HEADERS_ITEMS = ['Item', 'Category', 'Amount', '_filter']
