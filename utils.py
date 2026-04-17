def user_is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='admin').exists())

def user_is_manager(user):
    return user.is_authenticated and user.groups.filter(name='manager').exists()

def user_is_client(user):
    return user.is_authenticated and user.groups.filter(name='client').exists()

def user_is_guest(user):
    return not user.is_authenticated
