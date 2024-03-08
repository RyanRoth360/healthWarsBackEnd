# sqlite db communication
import sqlite3
import math


class database:

    DB_NAME = "health_wars.db"

    def __init__(self):
        self.db_conn = sqlite3.connect(self.DB_NAME)
        self.activity_weights = {
            "hiking": (1.0, 0.6, 0.4),
            "cycling": (0.8, 0.6, 0.6),
            "running": (1.0, 0.6, 0.6),
            "swimming": (0.6, 0.6, 0.6),
            "climbing": (0.6, 0.6, 0.4),
            "meditating": (0.1, 1.0, 0.8),
            "strength": (0.5, 0.6, 0.6),
            "reading": (0.1, 1.0, 1.0),
            "studying": (0.1, 1.0, 0.2),
            "arts": (0.1, 1.0, 0.2),
        }

    def select(self, table_name, columns=[], where={}, in_operator=False):
        # by default, query all columns
        if not columns:
            columns = [k for k in self.schema]

        # build query string
        columns_query_string = ", ".join(columns)
        query = "SELECT %s FROM %s" % (columns_query_string, table_name)
        # build where query string
        """Modified this for when user is searching for speakers"""
        if where:
            where_query_string = []
            for k, v in where.items():
                if k == "speakers":
                    where_query_string.append(
                        "(%s LIKE '%%; %s; %%' OR %s LIKE '%s; %%' OR %s LIKE '%%; %s' OR %s = '%s')"
                        % (k, v, k, v, k, v, k, v)
                    )

                else:
                    where_query_string.append("%s = '%s'" % (k, v))
            query += " WHERE " + " AND ".join(where_query_string)

        # print(query)
        result = []
        # SELECT id, name FROM users [ WHERE id=42 AND name=John ]
        #
        # Note that columns are formatted into the string without using sqlite safe substitution mechanism
        # The reason is that sqlite does not provide substitution mechanism for columns parameters
        # In the context of this project, this is fine (no risk of user malicious input)
        for row in self.db_conn.execute(query):
            result_row = {}
            # convert from (val1, val2, val3) to { col1: val1, col2: val2, col3: val3 }
            for i in range(0, len(columns)):
                result_row[columns[i]] = row[i]
            result.append(result_row)

        return result

    def execute_query(self, query):
        return self.db_conn.execute(query)

    def insert(self, table_name, item):
        # Build columns & values queries
        columns_query = ", ".join(item.keys())
        values_query = ", ".join(["'%s'" % v for v in item.values()])

        # Prepare the SQL query with table name, columns, and values
        sql_query = "INSERT INTO %s (%s) VALUES (%s)" % (
            table_name,
            columns_query,
            values_query,
        )

        # Execute the SQL query
        cursor = self.db_conn.cursor()
        cursor.execute(sql_query)

        # Commit the transaction
        self.db_conn.commit()

        # Get the last inserted row ID
        last_row_id = cursor.lastrowid

        # Close the cursor
        cursor.close()

        return last_row_id

    # def update(self, values, where):
    #     # build set & where queries
    #     set_query = ", ".join(["%s = '%s'" % (k, v)
    #                           for k, v in values.items()])
    #     where_query = " AND ".join(["%s = '%s'" % (k, v)
    #                                for k, v in where.items()])

    #     cursor = self.db_conn.cursor()
    #     cursor.execute("UPDATE %s SET %s WHERE %s" %
    #                    (self.name, set_query, where_query))
    #     cursor.close()
    #     self.db_conn.commit()
    #     return cursor.rowcount

    def close(self):
        self.db_conn.close()

    # SPECIFIC INSERTS
    def insert_user(self, username, password, name_first, name_last):
        """Inserts user and returns the user_id primary key"""
        user_dict = {}
        user_dict['user_name'] = username
        user_dict['password'] = password
        user_dict['name_first'] = name_first
        user_dict['name_last'] = name_last
        self.insert('users', user_dict)
        return self.select('users', ['user_id'], {
            'user_name': username})[0]['user_id']

    def insert_friendship(self, user_id1, user_id2):
        friend_dict = {}
        friend_dict["user_id1"] = user_id1
        friend_dict["user_id2"] = user_id2
        self.insert("friendship", friend_dict)

    def insert_friendship_usernames(self, username1, username2):
        '''Add error handling is a username doesn't exist'''
        user_id1 = self.get_userid(username1)
        user_id2 = self.get_userid(username2)
        self.insert_friendship(user_id1, user_id2)

    def insert_interests(self, username, interests):
        '''Takes list of interest'''
        user_id = self.select('users', ['user_id'], {
            'user_name': username})[0]['user_id']
        interests_dict = {i: 1 for i in interests}
        interests_dict["user_id"] = user_id
        self.insert("interests", interests_dict)

    def insert_reccomendation(self, title, category):
        rec_dict = {}
        rec_dict["title"] = title
        rec_dict["category"] = category
        rec_dict["steps_rel"] = self.activity_weights[category][0]
        rec_dict["screen_time_rel"] = self.activity_weights[category][1]
        rec_dict["sleep_rel"] = self.activity_weights[category][2]
        self.insert("reccomendations", rec_dict)

    def insert_health_data(self, user_id, steps, screen_time, sleep):
        health_dict = {}
        step_score = round(min(1, steps / 10000), 2)
        scree_time_score = round(min(1, 1 - screen_time / 10), 2)
        sleep_score = round(min(1, sleep / 8), 2)
        health_dict['user_id'] = user_id
        health_dict['steps'] = steps
        health_dict['screen_time'] = screen_time
        health_dict['sleep'] = sleep
        health_dict['overall_score'] = round((
            step_score + scree_time_score + sleep_score) / 3, 2)
        health_dict['step_score'] = step_score
        health_dict['screen_time_score'] = scree_time_score
        health_dict['sleep_score'] = sleep_score
        self.insert('health_data', health_dict)
