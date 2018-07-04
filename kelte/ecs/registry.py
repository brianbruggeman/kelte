# Registry requirements
#    Queryable entries by name if name is present
#
import functools


class Registrar(type):
    meta_bases = []

    def __new__(metacls, name, bases, namespace):
        metabases = [b for b in bases if b in metacls.meta_bases]
        named_cls_type = namespace.get("type")
        if any(metabases):
            for base in metabases:
                new_cls = type.__new__(metacls, name, bases, namespace)
                base.registry.setdefault(named_cls_type, new_cls)
        else:
            namespace.setdefault("registry", {})
            if "__new__" in namespace:
                namespace["__new__"] = metacls.dunder_new_wrapper(namespace["__new__"])
            else:
                namespace["__new__"] = metacls._new_subclass_
            new_cls = type.__new__(metacls, name, bases, namespace)
            new_cls.registry[named_cls_type] = new_cls
            metacls.meta_bases.append(new_cls)
        return new_cls

    @staticmethod
    def _new_subclass_(cls, *args, **kwds):
        named_cls_type = kwds.get("type")
        new_cls = cls.registry.get(named_cls_type) or cls
        try:
            new_cls_instance = object.__new__(new_cls, *args, **kwds)
        except TypeError as e:
            new_cls_instance = object.__new__(new_cls)
        return new_cls_instance

    @staticmethod
    def dunder_new_wrapper(f):
        @functools.wraps(f)
        def wrapper(cls, *args, **kwds):
            named_cls_type = kwds.get("type")
            cls = cls.registry.get(named_cls_type) or cls
            try:
                new_cls = super().__new__(cls, *args, **kwds)
            except TypeError:
                new_cls = super().__new__(cls)
            return new_cls

        return wrapper
