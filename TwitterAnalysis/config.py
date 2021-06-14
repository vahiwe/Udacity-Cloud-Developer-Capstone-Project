from decouple import config

KEY = config('DJANGO_KEY', 'fodpvv*w-x8f1o0vxs#kszzd78tr7babmn4_t')
DEBUG_VALUE = config("DEBUG_VALUE", default=True, cast=bool)