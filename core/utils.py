from core.models import Address, Supervisor


def has_related_object(user):
    has_address = False
    try:
        has_address = (user.address is not None)
    except Address.DoesNotExist:
        pass
    return has_address
def has_related_supervisor(user):
    has_supervisor = False
    try:
        has_supervisor = (user.supervisor is not None)
    except Supervisor.DoesNotExist:
        pass
    return has_supervisor