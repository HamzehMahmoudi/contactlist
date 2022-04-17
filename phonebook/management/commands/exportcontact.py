import json
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from phonebook.models import PhoneBook


class Command(BaseCommand):
    help = "export user phone book "

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("-U", "--user", nargs="+", type=str)

    def handle(self, *args, **options):
        username = options["user"][0] if options["user"] else ""
        if not username:
            username = input("enter username :")
        User = get_user_model()

        try:
            user = User.objects.get(username=username)
            qs = PhoneBook.objects.filter(user=user)
            dictionary = {}
            for contact in qs:
                dictionary.update(
                    {
                        contact.pk: {
                            "phone number": contact.phone_number,
                            "firstname": contact.first_name,
                            "lastname": contact.last_name,
                        }
                    }
                )

            with open("phonebook.json", "w") as output:
                json.dump(dictionary, output)
                print("done! you can find your data in phonebook.json")
        except User.DoesNotExist:
            print("user dose not exist ")
