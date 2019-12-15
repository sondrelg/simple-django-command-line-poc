from decouple import config

# Auth -------------------------------------------------

LOGIN_URL = 'django_auth_adfs:login'
LOGIN_REDIRECT_URL = '/'

AUTH_ADFS = {
    'LOGIN_EXEMPT_URLS': [],
    'TENANT_ID': '',  # TODO: insert tenant ID
    'CLIENT_ID': '',  # TODO: insert client ID
    'CLIENT_SECRET': config('ADFS_CLIENT_SECRET'),
    # TODO: Make sure you have your secret labelled ADFS_CLIENT_SECRET, or change the name here
    'RELYING_PARTY_ID': 'api://...',
    'AUDIENCE': 'api://...',
    'CLAIM_MAPPING': {'first_name': 'given_name', 'last_name': 'family_name', },
    'GROUPS_CLAIM': 'roles',
    'MIRROR_GROUPS': True,
    'USERNAME_CLAIM': 'upn',
}

AUTHENTICATION_BACKENDS = (
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    'django_auth_adfs.backend.AdfsAccessTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
)
