from models import User

def StringChecker(string, name, charMinAmount, charMaxAmount, needsUnique, uniqueList):
    if " " in string: return "No Spaces Allowed"

    length = len(string)
    if length < charMinAmount:
        return f"{name} is too short."
    elif length > charMaxAmount:
        return f"{name} is too long."
    
    if needsUnique:
        if not uniqueList == None and string in uniqueList:
            return f"{name} needs to be unique."
        
    return None # Anu errori ar aris.

def UsedUsernames():
    users = User.query.all()
    usernames = []

    for user in users:
        usernames.append(user.username)
    return usernames

def UsedEmails():
    users = User.query.all()
    emails = []

    for user in users:
        emails.append(user.email)

    return emails