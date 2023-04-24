import pickle
from constants import READING_ERROR_NAME, WRITING_ERROR_NAME


def write_into_binary(path:str, data: list | dict | tuple):
    try:
        with open(path, 'wb') as b_file:
            pickle.dump(data, b_file)
            return True
    except Exception as ex:
        print(f'{WRITING_ERROR_NAME}: {ex}')


def read_from_binary(path:str):
    try:
        with open(path, 'rb') as b_file:
            data = pickle.load(b_file)
        return data
    except Exception as ex:
        print(f'{READING_ERROR_NAME}: {ex}')



def main():
    pass   


if __name__ == '__main__': 
    main()
