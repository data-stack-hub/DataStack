def get_ds_class(my_module, datastack, _type="new"):
    for a, b in {
        k: v for k, v in my_module.__dict__.items() if not k.startswith("__")
    }.items():
        if _type == "new":
            from types import ModuleType

            if isinstance(b, ModuleType) and b.__name__ == "datastack.ds_c":
                for k1, v1 in b.__dict__.items():
                    if k1 == "main":
                        class_object_name = "main"
                        main_class = getattr(b, class_object_name)
        else:
            if type(b) == datastack and b.main:
                class_object_name = a
                main_class = getattr(my_module, class_object_name)
    return class_object_name, main_class
