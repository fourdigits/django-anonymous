import os

from setuptools import Command, find_packages, setup

from django_anonymous import __version__


def readme():
    with open("README.md") as f:
        return f.read()


class PublishCommand(Command):
    description = "Publish to PyPI"
    user_options = []

    def run(self):
        os.system("python setup.py sdist bdist_wheel")
        os.system("twine upload dist/*")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class CreateTagCommand(Command):
    description = "Create release tag"
    user_options = []

    def run(self):
        os.system(f"git tag -a {__version__} -m 'v{__version__}'")
        os.system("git push --tags")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


setup(
    name="django-anonymous",
    version=__version__,
    packages=find_packages(include=["django_anonymous", "django_anonymous.*"]),
    python_requires=">=3.6",
    install_requires=["Faker"],
    cmdclass={"publish": PublishCommand, "tag": CreateTagCommand},
    # metadata for upload to PyPI
    description="Simple Djanngo module to anonymize production data for safe usage on none production environments",  # noqa E501
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords=["Django", "anonymous", "anonymize"],
    author="Maikel Martens",
    author_email="maikel@martens.me",
    url="https://github.com/krukas/django-anonymous",
    download_url=f"https://github.com/krukas/django-anonymous/releases/tag/{__version__}",  # noqa E501
    license="GPL3",
    platforms=["any"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
