from importlib import import_module


def import_object_from_string(path):
    """x.y.z.A ==> from x.y.z import A
    """
    module_name, cls_name = path.rsplit('.', 1)
    module = import_module(module_name)
    cls = getattr(module, cls_name)
    return cls


def load_service(service):
    """通过字符串reflect service class, 通常只在可能出现循环导入情况下使用
    Args:
        service: str, e.g bidong.service.project
    """
    try:
        cls = import_object_from_string(service)
    except:
        raise Exception("{} service class not exists!")
    else:
        return cls()
