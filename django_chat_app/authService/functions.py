def set_user_data(request):
    newUsername = request.POST['username']
    newFirst_name = request.POST['first_name']
    newLast_name = request.POST['last_name']
    newEmail = request.POST['email']
    newPassword = request.POST['password']
    confirm_password = request.POST['confirm_password']

    user_data = {
        'username': newUsername,
        'first_name': newFirst_name,
        'last_name': newLast_name,
        'email': newEmail,
        'password': newPassword,
        'confirm_password': confirm_password
    }

    return user_data
