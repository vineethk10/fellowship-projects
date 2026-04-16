DEFAULT_SEARCH_FIELD = "from"
class DataStore:
    store_count = 0 

    def __init__(self, store_name):
        DataStore.store_count+= 1
        self.store_name = store_name
        self.records = []

    def add(self, record_dict):
        try:
            if  not isinstance(record_dict, dict):
                raise ValueError("Records must be of type dictionaries")
            self.records.append(record_dict)
            print(f'[{self.store_name}] Added : {record_dict}')
        except ValueError as error:
            print(f'[{self.store_name}] Add failed: {error}')

    def search(self, query_value, field=DEFAULT_SEARCH_FIELD):
        matching_records = [record for record in self.records
                            if query_value.lower() in str(record.get(field, "").lower())]
        return matching_records
    
    def delete(self, query_value, field=DEFAULT_SEARCH_FIELD):
        original_count = len(self.records)
        self.records = [record for record in self.records
                            if query_value.lower() not in str(record.get(field, "").lower())]
        delete_count = original_count - len(self.records)
        print(f'[{self.store_name}] Deleted {delete_count} record(s) matching {query_value}')

    def list_all(self):
        if not self.records:
            print(f'[{self.store_name}] has no records')
            return
        print(f'\n[{self.store_name} All recods {len(self.records)}] total: ')
        for index,record in enumerate(self.records, start=1):
            print(f' {index}.     {record}')

class ConversionStore(DataStore):
    def __init__(self, session_name):
        super().__init__(store_name = f'conversions_{session_name}')
        self.session_name = session_name
        self.conversion_count = 0
    
    def log_conversion(self, input_value, input_unit, output_value, output_unit):
        self.conversion_count += 1
        conversion_record = {
           'from': f'{input_value}, {input_unit}',
            'to' : f'{output_value}, {output_unit}'
        }
        self.add(conversion_record)
    
    def summary(self):
        print(f'\n[Conversion Log] session: {self.session_name}, total conversions: {self.conversion_count}')

if __name__ == '__main__':
    print('*'*50)
    print('OOP DEMO')
    print('*'*50)
    print(f'Stores created so far {DataStore.store_count}')

    store = DataStore("Unit conversions")
    print(f'Stores created so far {DataStore.store_count}')

    store.add({'from': '5.0 kg', 'to': '11.0 lb'})
    store.add({'from': '10.0 km', 'to': '6.0 miles'})
    store.add({'from': '100.0 C', 'to': '22.0 F'})

    store.list_all()

    print('\n Lets search for kg')
    results = store.search('kg')
    for r in results:
        print(f' Found: {r}')

    print('\n Delete record for km')
    store.delete('km')
    store.list_all()

    log = ConversionStore("Session 05")
    log.log_conversion(5.0, 'kg', 11.0, 'lb')
    log.log_conversion(10.0, 'km', 6.0, 'miles')
    log.log_conversion(100.0, 'C', 22.0, 'F')
    log.summary()