import sys
from src.logic.data_etl import DataHandler
from src.logic.details_etl import DetailsHandler

def main(*args, **kwargs):
    data_handler = DataHandler()
    details_handler = DetailsHandler()
    
    if args[0] == 'load_data':
        response = data_handler.load_dataset()
        return response
    
    if args[0] == 'load_order_details_defect':
        response = details_handler.load_order_details_by_defect(kwargs['order'])
        return response
    
    if args[0] == 'load_order_details_origin':
        response = details_handler.load_order_details_by_origin(kwargs['order'])
        return response

if __name__ == '__main__':
    main(sys.argv[1])