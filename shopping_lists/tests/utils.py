def login(client, user):
    password = 'password'
    user.set_password(password)
    user.save()
    client.login(username=user.username, password=password)
    return user
