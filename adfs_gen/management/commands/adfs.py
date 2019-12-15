import os

from django.core.management.base import BaseCommand

"""
To write our settings to the settings file we need to know two things.
1. Where is the content we want to copy in?
2. Where is the location of the settings file?
"""

root_folder = os.path.abspath(os.path.dirname(__name__))
template_path = root_folder + '/adfs_gen/templates/adfs/__init__.py'
root_name = root_folder.split("\\")[-1]
settings_path = root_folder + f'/{root_name}/settings.py'


class Command(BaseCommand):
    help = 'Generate ADFS settings for your project.'

    def handle(self, *args, **options):
        decouple_imported = False
        try:
            # Read settings and check whether imports have been made
            with open(settings_path, 'rb') as f:
                content = f.readlines()
                for line in content:
                    if b'from decouple import config' in line:
                        decouple_imported = True

            # Check for .env variable
            if os.path.isfile(root_folder + '/.env'):
                with open(root_folder + '/.env', 'rb') as env:
                    env_content = env.read()
                    if b'ADFS_CLIENT_SECRET=' not in env_content:
                        with open(root_folder + '/.env', 'wb') as env_write:
                            env_write.write(env_content + b'ADFS_CLIENT_SECRET=\n')
                            print('-- Added `ADFS_CLIENT_SECRET`-variable to your .env file.')
            else:
                with open(root_folder + '/.env', 'wb') as env_write:
                    print()
                    env_write.write(b'ADFS_CLIENT_SECRET=\n')
                    print('-- Added .env file to your project, with the variable `ADFS_CLIENT_SECRET`.')

            # Check for import
            print(decouple_imported)
            if not decouple_imported:
                with open(settings_path, 'wb') as settings_file:
                    for line in content:
                        if line[:6] == b"import":
                            line = line + b'from decouple import config\n'
                        settings_file.write(line)
                print('-- Added `decouple` import to the top of your settings file.')

            # Check for ADFS setup
            if b'AUTH_ADFS = {\r\n' in content:
                print('-- ADFS settings have already been added. Exiting script.')
                exit()

            if "AUTH_ADFS" not in content:
                with open(template_path, 'rb') as f:
                    template = f.read()

                with open(settings_path, 'ab') as settings_file:
                    settings_file.write(template)

                print('-- Added ADFS settings to the bottom of your settings file.')

        except IOError:
            print("File not accessible")
