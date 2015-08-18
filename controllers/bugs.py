import datetime
from app.handler import JsonController


class LevelController(JsonController):

    PATH = '/bug/level'

    def get(self):
        response = {
            "Error": "FBCA04",
            "Suggest": "159818",
            "Emergency": "FC2929",
            "Danger": "EB6420",
            "Warning": "0052CC",
            "Invalid": "5319E7"
        }
        self.write_json(response)


class ListController(JsonController):

    PATH = '/bug/list'

    def get(self):
        dbh = self.db().cursor()
        query = 'SELECT `id`, `level`, `title`, `created_at`, `updated_at` FROM `bug` WHERE `status` = "open"'
        bugs = []
        dbh.execute(query)
        for (bug_id, level, title, created_at, updated_at) in dbh:
            bugs.append({
                'id': bug_id,
                'level': level,
                'title': title,
                'created_at': created_at.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
                'updated_at': updated_at.strftime('%Y-%m-%dT%H:%M:%S+08:00')
            })
        dbh.close()
        self.write_json(bugs)


class DisplayController(JsonController):

    PATH = r'/bug/([\d]+)'

    def get(self, bug_id):
        dbh = self.db().cursor(buffered=True)
        query = ('SELECT `id`, `level`, `title`, `status`, `detail`, `created_at`, `updated_at`'
                'FROM `bug` WHERE `id` = {0} LIMIT 1').format(bug_id)
        dbh.execute(query)

        response = None

        for (bug_id, level, title, status, detail, created_at, updated_at) in dbh:
            response = {
                'id': bug_id,
                'level': level,
                'title': title,
                'status': status,
                'detail': detail,
                'created_at': created_at.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
                'updated_at': updated_at.strftime('%Y-%m-%dT%H:%M:%S+08:00')
            }
            break

        dbh.close()
        self.write_json(response)


class UpdateController(JsonController):

    PATH = r'/bug/updates/([\d]+)'

    def get(self, last_update):
        dbh = self.db().cursor(buffered=True)
        query = ('SELECT `id`, `level`, `title`, `created_at`, `updated_at` FROM `bug` '
            'WHERE `created_at` >= FROM_UNIXTIME({0})').format(last_update)
        dbh.execute(query)

        bugs = []
        for (bug_id, level, title, created_at, updated_at) in dbh:
            bugs.append({
                'id': bug_id,
                'level': level,
                'title': title,
                'created_at': created_at.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
                'updated_at': updated_at.strftime('%Y-%m-%dT%H:%M:%S+08:00')
            })
        dbh.close()
        self.write_json(bugs)
