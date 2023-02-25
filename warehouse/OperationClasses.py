class DataCache:
    def __init__(self):
        self._cache_list = []
        self._active_cell = None
        self._active_model = None

    def set_cache_list(self, data:list):
        self._cache_list = data

    def get_cache_list(self):
        return self._cache_list

    def set_active_sell(self, value):
        self._active_cell = value

    def get_active_sell(self):
        return self._active_cell

    def set_active_model(self, model):
        self._active_model = model

    def get_active_model(self):
        return self._active_model


class DataHandler(DataCache):
    def __init__(self):
        super().__init__()
        self._active_model = None

    def set_active_model(self, model):
        self._active_model = model

    def get_active_model(self):
        return self._active_model


if __name__ == '__main__':
    pass
