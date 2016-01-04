class Config():
    # Flask settings
    SECRET_KEY                  = 'THIS IS AN INSECURE SECRET'
    SQLALCHEMY_DATABASE_URI     = 'sqlite:///db.sqlite'
    CSRF_ENABLED                = True

    # WTF Forms
    WTF_CSRF_ENABLED            = True

    # User plugin
    USER_ENABLE_EMAIL           = False
    USER_UNAUTHORIZED_ENDPOINT  = 'unauthorized'

    # App configs
    UPLOAD_FOLDER               = 'uploads'
