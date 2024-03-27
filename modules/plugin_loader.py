import pluginlib


@pluginlib.Parent("parser")
class Parser(object):

    @pluginlib.abstractmethod
    def parse(self, **kwargs):
        pass


@pluginlib.Parent("slackevent")
class SlackEvent(object):

    @pluginlib.abstractmethod
    def react(self):
        pass


@pluginlib.Parent("files")
class FileHandling(object):

    @pluginlib.abstractmethod
    def download(self, **kwargs):
        pass

    @pluginlib.abstractmethod
    def upload(self, **kwargs):
        pass


@pluginlib.Parent("Database")
class Database(object):

    @pluginlib.abstractmethod
    def __new__(cls, config):
        pass

    @pluginlib.abstractmethod
    def get_conn(self):
        pass

    @pluginlib.abstractmethod
    def release_conn(self, conn):
        pass

    @pluginlib.abstractmethod
    def execute_query(self, query, params=None):
        pass


@pluginlib.Parent("eventlogger")
class EventLogger(object):

    @pluginlib.abstractmethod
    def __init__(self, body, app, db):
        pass

    @pluginlib.abstractmethod
    def parse_event(self):
        pass

    @pluginlib.abstractmethod
    def parse_user(self):
        pass

    @pluginlib.abstractmethod
    def parse_files(self):
        pass

    @pluginlib.abstractmethod
    def log_event(self):
        pass

    @pluginlib.abstractmethod
    def to_dict(self):
        pass

    @pluginlib.abstractmethod
    def process_file(self, file):
        pass

    @pluginlib.abstractmethod
    def parse_command(self):
        pass
