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


class TemperatureLog(DataStore):
    """Inherits from DataStore. Logs temperature conversions in a clean format."""
    
    def __init__(self, location_name):
        super().__init__(store_name=f"temperatures_{location_name}")
        self.location_name = location_name
        self.temp_count = 0
    
    def log_temp(self, celsius):
        """Compute Fahrenheit and log the temperature conversion."""
        self.temp_count += 1
        fahrenheit = (celsius * 9/5) + 32
        record = {"celsius": celsius, "fahrenheit": fahrenheit}
        self.add(record)
    
    def list_all(self):
        """Override to display temperatures in custom format."""
        if not self.records:
            print(f"[TemperatureLog] '{self.location_name}': No temps logged yet.")
            return
        print(f"\n[TemperatureLog] '{self.location_name}' — {len(self.records)} reading(s):")
        for i, r in enumerate(self.records, 1):
            print(f"  {i}.  {r['celsius']}°C  →  {r['fahrenheit']:.1f}°F")
    
    def summary(self):
        """Print how many temperatures have been logged."""
        print(f"\n[TemperatureLog] Location '{self.location_name}': {self.temp_count} reading(s) total.")

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

    print('{Search for km in conversion log}')

    for r in log.search('km'):
        print(f' Found in log: {r}')

    # Part C: Test TemperatureLog
    print('\n' + '='*50)
    print('PART C: Testing TemperatureLog')
    print('='*50)
    temp_log = TemperatureLog("New York")
    print(f"Stores created: {DataStore.store_count}")  # Should be 3
    
    # Log some temperatures
    temp_log.log_temp(0)      # Freezing point
    temp_log.log_temp(100)    # Boiling point
    temp_log.log_temp(37)     # Body temperature
    
    # Call overridden list_all()
    temp_log.list_all()
    
    # Call summary() method
    temp_log.summary()

    # Part D: Prove the Class Variable
    print('\n' + '='*50)
    print('PART D: Class Variable Proof')
    print('='*50)
    print(f"DataStore.store_count (via class): {DataStore.store_count}")
    print(f"store.store_count (via DataStore object): {store.store_count}")
    print(f"log.store_count (via ConversionStore object): {log.store_count}")
    print(f"temp_log.store_count (via TemperatureLog object): {temp_log.store_count}")
    
    print("\nExplanation:")
    print("All four print statements show the same number (3) because store_count is a")
    print("CLASS VARIABLE that lives on the DataStore class itself, not on individual")
    print("objects. All objects—DataStore, ConversionStore, and TemperatureLog—share")
    print("the same counter. When any object is created, it increments the shared counter.")