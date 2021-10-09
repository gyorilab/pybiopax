from .biopax import BioPaxObject


def find_objects(start_obj: BioPaxObject, path_str: str):
    parts = path_str.split('/')
    last = True if len(parts) == 1 else False
    for part in parts:
        if ':' in part:
            attribute, class_constraint = part.split(':', maxsplit=1)
        else:
            attribute, class_constraint = part, None
        val = getattr(start_obj, attribute, None)
        if val is None:
            return []
        elif isinstance(val, BioPaxObject):
            if not last:
                return find_objects(val, '/'.join(parts[1:]))
            else:
                return [val]
        elif isinstance(val, list):
            results = []
            for v in val:
                if not last:
                    results.append(find_objects(v, '/'.join(parts[1:])))
                else:
                    results.append(v)
            return results
