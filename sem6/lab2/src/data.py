from controller.UserController import UserController

menu_list = {
    'Main menu': {
        'Registration': UserController.registration,
        'Sign in': UserController.sign_in,
        'Exit': UserController.stop,
    },
    'Utilizer menu': {
        'Sign out': UserController.sign_out,
        'Send a message': UserController.send_message,
        'Inbox messages': UserController.inbox_message,
        'My messages statistics': UserController.get_message_statistics,
    },
    'Admin menu': {
        'Sign out': UserController.sign_out,
        'Online users': UserController.get_online_users,
        'Top senders': UserController.get_top_senders,
        'Top spamers': UserController.get_top_spamers,
    }
}

roles = {
    'utilizer': 'Utilizer menu',
    'admin': 'Admin menu'
}
