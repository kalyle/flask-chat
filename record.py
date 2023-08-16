import types


class Meta(type):
    def __new__(cls, clsname, bases, dct):
        methods = {}
        for name, val in dct.items():
            if not name.startswith('__'):
                methods[name.upper()] = val
            else:
                methods[name] = val
            print(type(val), val, name)
            if isinstance(val, types.FunctionType):
                setattr(val, "default", "default")
                val(cls)

        return type.__new__(cls, clsname, bases, methods)


class Base(object, metaclass=Meta):
    def one(self, *args, **kwargs):
        print("one", *args, **kwargs)

    def two(self, *args, **kwargs):
        print("two", *args, **kwargs)


Base()

# Base.one()
