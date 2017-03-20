import calendar
import config
import decimal
import fb_test
import MySQLdb
import MySQLdb.cursors
import time


def BuildQueryArgs(args):
    """Builds the argument list for a MySQL query.
    Args:
        args: list of (property, value) or (property, value, op) tuples.
            If the tuple is (property, value), it represents the condition
            "<property>='<value>'". If the tuple is (property, value, op),
            it represents the condition "'<property><op>'<value>'". The
            conditions are always ANDed together.
    Returns:
        (string) The appropriate argument list for the MySQL query.
            For example, if the input is [], no argument list is returned.
            If the input is [(userid, "mjchao")],
            " where  userid = 'mjchao'" is returned. If the input is
            [(firstname, "Mickey"), (lastname, "Chao"),
            " where firstname = 'Mickey' and lastname = 'Chao'" is returned.
    """
    properties = []
    for prop in args:
        # (property, value) case
        if len(prop) == 2:
            prop_name, prop_val = prop[0], prop[1]
            properties.append(" %s = '%s' " %(prop_name, prop_val))

        # (property, value, op) case:
        elif len(prop) == 3:
            prop_name, prop_val, op = prop[0], prop[1], prop[2]
            properties.append(" %s %s '%s'" %(prop_name, op, prop_val))

    if len(properties) > 0:
        return " where " + "and".join(properties) + ";"
    else:
        return ""


class Data(object):
    """Represents data stored in a MySQL table. Every data type that
    inherits from Data should define a static string _TABLE that is the
    name of the table in the database and _COL_NAMES that is the
    name of each column in the table.
    """

    # Name of the table for this data
    _TABLE = None

    # Name of each element in this data.
    _COL_NAMES = None

    def __init__(self, data_values=None):
        """Creates a generic data object.

        Args:
            data_values: (list) A list of the values of this data object in
                the same order specified by _COL_NAMES.
        """
        data_names = type(self)._COL_NAMES
        if data_values is not None and data_names is not None:
            if len(data_names) != len(data_values):
                raise ValueError("Incorrect number of data values provided.")

            data_dict = {}
            for i in range(len(data_names)):
                # MySQL queries will return floats as Decimals instead
                # we need to convert decimals to floats so that they can
                # be sent through JSON.
                if type(data_values[i]) != decimal.Decimal:
                    data_dict[data_names[i]] = data_values[i]
                else:
                    data_dict[data_names[i]] = float(data_values[i])

            # Allow references to data values as if they were properties of
            # this object for convenience. Now you can directly access
            # <object name>.<data name> and <data_value> is returned. For
            # example, test_user_data.userid will now return the userid.
            self.__dict__ = data_dict

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(frozenset(self.__dict__))

    @classmethod
    def FromDbData(cls, data):
        """Creates this object from a list of data. This can be useful for
        converting MySQL query results into object form.

        Args:
            data: (list) The data values in the same order as specified by
                the _COL_NAMES field.

        Returns:
            (cls) The data object.
        """
        return cls(*data)

    @classmethod
    def FromDict(cls, d):
        """Creates this object from a dictionary of its data values. This can
        be useful for converting JSON back into object form.

        Args:
            d: (dict) A dictionary of data values.

        Returns:
            (cls) The data object.
        """
        data_values = []
        data_names = cls._COL_NAMES
        for name in data_names:
            data_values.append(d[name])

        return cls(*data_values)

    @classmethod
    def BuildQuery(cls, args):
        """Creates the MySQL command to query for data with the specific
        arguments in the database. See BuildQueryArgs() for details on
        what to pass in for the args parameter.

        Args:
            args: list of (property, value) or (property, value, op) tuples.
                If the tuple is (property, value), it represents the condition
                "<property>='<value>'". If the tuple is (property, value, op),
                it represents the condition "'<property><op>'<value>'". The
                conditions are always ANDed together.

        Returns:
            (string) The MySQL query.
        """
        if cls._TABLE is None:
            raise UnboundLocalError("Subclass " + str(cls) +
                                    " has not defined a _TABLE value")
        return "SELECT * FROM %s %s" %(cls._TABLE, BuildQueryArgs(args))

    def ToInsertCommand(self):
        """Creates the MySQL command to insert this data into the database.
        For example, "INSERT INTO USER VALUES('1', 'seller', '-')"

        Returns:
            (string) The MySQL command used to insert this data into the
                database.
        """
        data_values_as_str = []
        for name in self._COL_NAMES:
            value = self.__dict__[name]
            if type(value) == str or type(value) == unicode:
                data_values_as_str.append("'%s'" %(value))
            else:
                data_values_as_str.append(str(value))

        insert_str = "INSERT INTO %s " %(self._TABLE)
        values_str = "VALUES(" + ", ".join(data_values_as_str) + ")"
        return insert_str + values_str

    def ToDeleteCommand(self):
        """Creates the MySQL command to delete this data from the database.
        
        Returns:
            (string) The MySQL command used to delete this data from the
                database.
        """
        delete_str = "DELETE FROM %s" %(self._TABLE)
        args = []
        for name in self._COL_NAMES:
            args.append((name, self.__dict__[name]))
        return delete_str + BuildQueryArgs(args)

    def ToUpdateCommand(self, change):
        """Creates the MySQL command to update this data entry with the
        specified change.

        Args:
            change: (string) the change to make, e.g. "userid=2", to change
                the userid property to 2.

        Returns:
            (string) The MySQL command used to update this data entry.
        """
        update_str = "UPDATE %s SET %s " %(self._TABLE, change)
        args = []
        for name in self._COL_NAMES:
            args.append((name, self.__dict__[name]))
        return update_str + BuildQueryArgs(args)


class UserData(Data):

    _TABLE = "USER"
    _COL_NAMES = ["userid", "role", "location"]
    
    def __init__(self, *data_values):
        super(UserData, self).__init__(data_values)

    def GetUpdateRoleCommand(self, new_role):
        """Creates the command to update this user's role.

        Args:
            new_role: (string) "buyer", "seller", or "none" - the new role
                for this user.

        Returns:
            (string) The MySQL command to update the user's role.
        """
        if new_role != "buyer" and new_role != "seller" and new_role != "none":
            raise ValueError("Invalid new role")
        return self.ToUpdateCommand("role='%s'" %(new_role))


TEST_USER1 = UserData(fb_test.FBTest.TEST_USER_IDS[0], "seller", "-")
TEST_USER2 = UserData(fb_test.FBTest.TEST_USER_IDS[1], "seller", "-")
TEST_USER3 = UserData(fb_test.FBTest.TEST_USER_IDS[2], "none", "-")
TEST_USER4 = UserData(fb_test.FBTest.TEST_USER_IDS[3], "none", "-")
TEST_USER5 = UserData(fb_test.FBTest.TEST_USER_IDS[4], "buyer", "-")
TEST_USER6 = UserData(fb_test.FBTest.TEST_USER_IDS[5], "none", "-")
TEST_USER7 = UserData(fb_test.FBTest.TEST_USER_IDS[6], "seller", "-")
TEST_USER8 = UserData(fb_test.FBTest.TEST_USER_IDS[7], "seller", "-")
TEST_USER9 = UserData(fb_test.FBTest.TEST_USER_IDS[8], "none", "-")


class ItemData(Data):

    _TABLE = "ITEM"
    _COL_NAMES = ["userid", "photo", "servings", "end", "price", "address",
                    "description"]

    def __init__(self, *data_values):
        super(ItemData, self).__init__(data_values)


CURR_TIME_SECS = calendar.timegm(time.gmtime())
# This is a test item that will expire in 10 minutes
TEST_ITEM1 = ItemData(TEST_USER1.userid, "images/%s.jpg" %(TEST_USER1.userid),
                        10, CURR_TIME_SECS + 600, 12.25, "42.28, -83.73",
                        "tasty")

# This is a test item that expired 10 minutes ago
TEST_ITEM2 = ItemData(TEST_USER2.userid, "images%s.jpg" %(TEST_USER2.userid),
                        20, CURR_TIME_SECS - 600, 25.00, "42.30, -83.73",
                        "yummy")

TEST_ITEM3 = ItemData(TEST_USER7.userid, "images/%s.jpg" %(TEST_USER7.userid),
                        20, CURR_TIME_SECS + 1200, 25.00, "42.30, -83.73",
                        "yummy7")

TEST_ITEM4 = ItemData(TEST_USER8.userid, "images/%s.jpg" %(TEST_USER8.userid),
                        20, CURR_TIME_SECS + 1200, 25.00, "42.30, -83.73",
                        "yummy8")


class TransactionData(Data):

    _TABLE = "TRANSACTION"
    _COL_NAMES = ["sellerid", "buyerid", "servings"]
    
    def __init__(self, *data_values):
        super(TransactionData, self).__init__(data_values)

    
TEST_TRANSACTION1 = TransactionData(TEST_USER1.userid, TEST_USER5.userid, 10)


class CommunityData(Data):

    _TABLE = "COMMUNITY"
    _COL_NAMES = ["communityid", "communityname"]

    def __init__(self, *data_values):
        # Note: communityid is autoincremented by the database. Setting it in
        # the constructor will have no affect on how this data interacts
        # with the database.
        super(CommunityData, self).__init__(data_values)

    def ToInsertCommand(self):
        """Creates the command to insert this community into the database.

        Returns:
            (string) The MySQL command to insert this community into the
                database.
        """
        # Have to override parent insert command because
        # we can't insert the communityid value since the database
        # autoincrements it
        return "INSERT INTO COMMUNITY (communityname) VALUES('%s')" %(
                self.communityname)


TEST_COMMUNITY1 = CommunityData(1, "TestCommunity1")
TEST_COMMUNITY2 = CommunityData(2, "TestCommunity2")


class MembershipData(Data):

    _TABLE = "MEMBERSHIP"
    _COL_NAMES = ["userid", "communityid", "status"]

    def __init__(self, *data_values):
        super(MembershipData, self).__init__(data_values)


TEST_MEMBERSHIP1 = MembershipData(TEST_USER1.userid, 1, "joined")
TEST_MEMBERSHIP2 = MembershipData(TEST_USER2.userid, 1, "joined")
TEST_MEMBERSHIP3 = MembershipData(TEST_USER3.userid, 1, "joined")
TEST_MEMBERSHIP4 = MembershipData(TEST_USER4.userid, 1, "joined")
TEST_MEMBERSHIP5 = MembershipData(TEST_USER5.userid, 1, "joined")
TEST_MEMBERSHIP6 = MembershipData(TEST_USER7.userid, 1, "joined")
TEST_MEMBERSHIP7 = MembershipData(TEST_USER8.userid, 1, "joined")


class RatingData(Data):

    _TABLE = "RATING"
    _COL_NAMES = ["ratingid", "sellerid", "buyerid", "rating", "description"]

    def __init__(self, *data_values):
        super(RatingData, self).__init__(data_values)

    def ToInsertCommand(self):
        """Creates the command to insert this community into the database.

        Returns:
            (string) The MySQL command to insert this community into the
                database.
        """
        # Have to override parent insert command because
        # we can't insert the communityid value since the database
        # autoincrements it
        return "INSERT INTO RATING (sellerid, buyerid, rating, description) " \
                "VALUES('%s', '%s', '%s', '%s')" %(self.sellerid,
                self.buyerid, self.rating, self.description)


TEST_RATING1 = RatingData(1, TEST_USER1.userid, TEST_USER2.userid, "5", "good")
TEST_RATING2 = RatingData(2, TEST_USER1.userid, TEST_USER3.userid, "1", "bad")
TEST_RATING3 = RatingData(3, TEST_USER1.userid, TEST_USER3.userid, "2", "bad")
TEST_RATING4 = RatingData(4, TEST_USER1.userid, TEST_USER4.userid, "pending",
                            "")

conn = None


def ExecuteCommand(command):
    x = conn.cursor()
    x.execute(command)
    conn.commit()


def SetUpTestUserData():
    ExecuteCommand(TEST_USER1.ToInsertCommand())
    ExecuteCommand(TEST_USER2.ToInsertCommand())
    ExecuteCommand(TEST_USER3.ToInsertCommand())
    ExecuteCommand(TEST_USER4.ToInsertCommand())
    ExecuteCommand(TEST_USER5.ToInsertCommand())
    ExecuteCommand(TEST_USER6.ToInsertCommand())
    ExecuteCommand(TEST_USER7.ToInsertCommand())
    ExecuteCommand(TEST_USER8.ToInsertCommand())
    ExecuteCommand(TEST_USER9.ToInsertCommand())


def SetUpTestItemData():
    ExecuteCommand(TEST_ITEM1.ToInsertCommand())
    ExecuteCommand(TEST_ITEM2.ToInsertCommand())
    ExecuteCommand(TEST_ITEM3.ToInsertCommand())
    ExecuteCommand(TEST_ITEM4.ToInsertCommand())


def SetUpTestTransactionData():
    ExecuteCommand(TEST_TRANSACTION1.ToInsertCommand())


def SetUpTestCommunityData():
    ExecuteCommand(TEST_COMMUNITY1.ToInsertCommand())
    ExecuteCommand(TEST_COMMUNITY2.ToInsertCommand())


def SetUpTestMembershipData():
    ExecuteCommand(TEST_MEMBERSHIP1.ToInsertCommand())
    ExecuteCommand(TEST_MEMBERSHIP2.ToInsertCommand())
    ExecuteCommand(TEST_MEMBERSHIP3.ToInsertCommand())
    ExecuteCommand(TEST_MEMBERSHIP4.ToInsertCommand())
    ExecuteCommand(TEST_MEMBERSHIP5.ToInsertCommand())
    ExecuteCommand(TEST_MEMBERSHIP6.ToInsertCommand())
    ExecuteCommand(TEST_MEMBERSHIP7.ToInsertCommand())


def SetUpTestRatingData():
    ExecuteCommand(TEST_RATING1.ToInsertCommand())
    ExecuteCommand(TEST_RATING2.ToInsertCommand())
    ExecuteCommand(TEST_RATING3.ToInsertCommand())
    ExecuteCommand(TEST_RATING4.ToInsertCommand())


def SetUpTestDatabase():
    global conn
    conn = MySQLdb.connect(host="localhost", user=config.env["db_user"],
                            passwd=config.env["db_passwd"], db="test")

    ExecuteCommand("DROP TABLE IF EXISTS USER;")
    ExecuteCommand("CREATE TABLE USER("\
                "userid VARCHAR(20) NOT NULL, "\
                "role ENUM('none', 'buyer', 'seller') NOT NULL, "\
                "location VARCHAR(255), "\
                "PRIMARY KEY(userid));")
    SetUpTestUserData()

    ExecuteCommand("DROP TABLE IF EXISTS ITEM;")
    ExecuteCommand("CREATE TABLE ITEM("\
                "userid VARCHAR(40) NOT NULL, "\
                "photo VARCHAR(40) NOT NULL, "\
                "servings INT NOT NULL, "\
                "end INT NOT NULL,"\
                "price DECIMAL(5, 2) NOT NULL, "\
                "address VARCHAR(255) NOT NULL, "\
                "description TEXT, "\
                "PRIMARY KEY(userid));")
    SetUpTestItemData()

    ExecuteCommand("DROP TABLE IF EXISTS TRANSACTION;")
    ExecuteCommand("CREATE TABLE TRANSACTION("\
                    "sellerid VARCHAR(40) NOT NULL, "\
                    "buyerid VARCHAR(40) NOT NULL, "\
                    "servings INT NOT NULL);")
    SetUpTestTransactionData()

    ExecuteCommand("DROP TABLE IF EXISTS COMMUNITY;")
    ExecuteCommand("CREATE TABLE COMMUNITY("\
                    "communityid int NOT NULL AUTO_INCREMENT, "\
                    "communityname varchar(255) NOT NULL, "\
                    "PRIMARY KEY(communityid));")
    SetUpTestCommunityData()

    ExecuteCommand("DROP TABLE IF EXISTS MEMBERSHIP;")
    ExecuteCommand("CREATE TABLE MEMBERSHIP("\
                    "userid varchar(20) NOT NULL, "\
                    "communityid int NOT NULL, "\
                    "status ENUM('pending', 'joined') NOT NULL);")
    SetUpTestMembershipData()

    ExecuteCommand("DROP TABLE IF EXISTS RATING;")
    ExecuteCommand("CREATE TABLE RATING("\
                    "ratingid int NOT NULL AUTO_INCREMENT, "\
                    "sellerid varchar(20) NOT NULL, "\
                    "buyerid varchar(20) NOT NULL, "\
                    "rating ENUM('1', '2', '3', '4', '5', 'pending') NOT NULL,"\
                    "description varchar(255), " \
                    "PRIMARY KEY(ratingid));")
    SetUpTestRatingData()


def SetUpProdDatabase():
    global conn
    conn = MySQLdb.connect(host="localhost", user=config.env["db_user"],
                            passwd=config.env["db_passwd"], db="prod")


def Init():
    """Reinitializes the database. If this is prod, the connection will just
    be reset. If this is test, the test data will be reset.
    """
    if config.env["state"] == "test":
        SetUpTestDatabase()
    else:
        SetUpProdDatabase()


def Query(data_class, args=[]):
    """Returns data in the database with the specified properties.

    Args:
        args: A list of (property, value) or (property, value, op) tuples.

    Returns:
        (list of data_class objects) All data with the properties specified
            in args.
    """
    query = data_class.BuildQuery(args)
    x = conn.cursor()
    x.execute(query)
    return [data_class.FromDbData(result) for result in x.fetchall()]

def Insert(data):
    """Adds the given data to the database.

    Args:
        data: (Data) Data to be added to the database.
    """
    ExecuteCommand(data.ToInsertCommand())


def Delete(data):
    """Deletes the given data from the database.

    Args:
        data: (Data) Data to be deleted from the database.
    """
    ExecuteCommand(data.ToDeleteCommand())


def Update(data, change):
    """Updates the given data in the database. Note: the data object is not
    changed. You will have to updated the attributes of the data object as well.

    Args:
        data: (Data) Data to be updated in the database.
        change: (string) The change to make (will be included in the MySQL
            command)
    """
    ExecuteCommand(data.ToUpdateCommand(change))


def GetLastAutoIncID():
    """Gets the last ID that was generated by an autoincrement.

    Returns:
        (int) The last ID generated by an autoincrement.
    """
    x = conn.cursor()
    x.execute("SELECT LAST_INSERT_ID();")
    return int(x.fetchone()[0])

