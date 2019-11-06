import glob
import re

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.management.base import BaseCommand

from fala.settings.base import root


class Command(BaseCommand):
    help = "Rewrites static file paths within our compiled css file, to be aware of our storage backend"
    css_dir = root("assets", "css")

    def handle(self, *args, **kwargs):
        for file_path in glob.glob("{dir}/*.css".format(dir=self.css_dir)):
            self.stdout.write("Rewriting paths in {file_path}".format(file_path=file_path))
            with open(file_path, "r") as css_file:
                contents = css_file.read()
                pattern = r"url\((\"?(?:{static_url}|\.\./)(.*?)\"?)\)".format(static_url=settings.STATIC_URL)
                matches = re.findall(pattern, contents)
                for url, path in matches:
                    new_url = static(path)
                    self.stdout.write("  Rewriting {old_url} to {new_url}".format(old_url=url, new_url=new_url))
                    contents = contents.replace(url, new_url)
            with open(file_path, "w") as css_file:
                css_file.write(contents)
                self.stdout.write("  Done")
