class InventoryResponseCache:

    isDirty = False
    store = {}

    @staticmethod
    def getCache(key, default=None):
        if not InventoryResponseCache.isDirty:
            return InventoryResponseCache.store.get(key, default)

    @staticmethod
    def setCache(key, data):
        InventoryResponseCache.isDirty = False
        InventoryResponseCache.store[key] = data

    @staticmethod
    def setIsDirty(flag=True):
        InventoryResponseCache.isDirty = flag
