import configparser
import os

from sqlalchemy.engine import URL, make_url


class ConfigError(Exception):
    pass


class Config(object):
    SYSTEM_CONFIG = "/etc/flume"
    conf_database_args = [
        "uri",
        "drivername",
        "user",
        "password",
        "host",
        "port",
        "database",
    ]
    conf_media_args = ["dir"]

    def __init__(self, args=None):
        user_configuration = "{}/{}".format(os.getenv("HOME"), ".flume")
        self.config = configparser.ConfigParser()
        # try with the passed in configuration, if any
        if args and args.config:
            self.config.read(args.config)
        # try with the system wide configuration
        elif os.path.isfile(Config.SYSTEM_CONFIG):
            self.config.read(Config.SYSTEM_CONFIG)
        # try with the local user configuration
        elif os.path.isfile(user_configuration):
            self.config.read(user_configuration)

        # override now with passed in arguments
        if not "Database" in self.config:
            self.config["Database"] = {}
        if not "Media" in self.config:
            self.config["Media"] = {}

        if args:
            for c in self.conf_media_args:
                cv = getattr(args, c, None)
                if cv:
                    self.config["Media"][c] = cv
            for c in self.conf_database_args:
                cv = getattr(args, c, None)
                if cv:
                    self.config["Database"][c] = cv

        # Generate the other parameters based on the uri
        if "uri" in self.config["Database"]:
            url = make_url(self.config["Database"]["uri"])
            for c in self.conf_database_args:
                if c == "uri":
                    continue
                cv = getattr(url, c, None)
                if cv:
                    self.config["Database"][c] = cv
                elif c in self.config["Database"]:
                    del self.config["Database"][c]

        # Generate the uri based on the other parameters
        url = URL.create(
            self.config["Database"]["driver"],
            username=self.config["Database"].get("user", None),
            password=self.config["Database"].get("password", None),
            host=self.config["Database"].get("host", None),
            port=self.config["Database"].get("port", None),
            database=self.config["Database"].get("database", None),
        )
        self.config["Database"]["uri"] = str(url)

        if not "uri" in self.config["Database"]:
            raise ConfigError("Missing database uri")
        if not "dir" in self.config["Media"]:
            raise ConfigError("Missing media directory")

    def get_media_files_directory(self):
        return self.config["Media"]["dir"]

    def get_database_uri(self):
        return self.config["Database"]["uri"]

    def get_database_driver(self):
        return self.config["Database"]["driver"]

    def get_database_user(self):
        return self.config["Database"]["user"]

    def get_database_password(self):
        return self.config["Database"]["password"]

    def get_database_host(self):
        return self.config["Database"]["host"]

    def get_database_port(self):
        return self.config["Database"]["port"]

    def get_database_database(self):
        return self.config["Database"]["database"]
