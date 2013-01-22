class modelObject(object):
    def __init__(self):
        pass
    def set(self, p_Property, p_Value):
        setattr(self, p_Property, p_Value)
    def get(self, p_Property):
        return getattr(self, p_Property)