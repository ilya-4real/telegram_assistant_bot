from aiogram.utils.markdown import text

def common_message():
    msg = text(
        'Hello!',
        'I am your personal assistant.',
        'Now I can show you weather, currency rates and manage your tasks',
    sep='\n'
    )
    return msg

def getme_message(user_model):
    msg = text("your saved on server data is:",
               f'user id : {user_model.id}',
               f'username : {user_model.username}',
               f'email : {user_model.email} ',
               f'verified: {user_model.is_verified}',
               f'date of registration : {user_model.registered_at}',
               sep='\n'
               )
    return msg