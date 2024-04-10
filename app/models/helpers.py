def set_attrs_from_dict(entity, updated_attrs):
    for attr in updated_attrs:
        has_attr = hasattr(entity, attr)
        if has_attr:
            setattr(entity, attr, updated_attrs[attr])
