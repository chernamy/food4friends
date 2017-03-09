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

    @classmethod
    def FromDbData(cls, data):
        return cls(*data)

    @classmethod
    def FromDict(cls, d):
        data_values = []
        data_names = cls._COL_NAMES
        for name in data_names:
            data_values.append(d[name])

        return cls(*data_values)

    @classmethod
    def BuildQuery(cls, args):
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
        delete_str = "DELETE FROM %s" %(self._TABLE)
        args = []
        for name in self._COL_NAMES:
            args.append((name, self.__dict__[name]))
        return delete_str + BuildQueryArgs(args)

    def ToUpdateCommand(self, change):
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


class ItemData(Data):

    _TABLE = "ITEM"
    _COL_NAMES = ["userid", "photo", "servings", "end", "price", "address",
                    "description"]

    def __init__(self, *data_values):
        super(ItemData, self).__init__(data_values)


CURR_TIME_SECS = calendar.timegm(time.gmtime())
# This is a test item that will expire in 10 minutes
TEST_ITEM1 = ItemData(TEST_USER1.userid, "1.png", 10, CURR_TIME_SECS + 600,
                        12.25, "42.28, -83.73","tasty")

# This is a test item that expired 10 minutes ago
TEST_ITEM2 = ItemData(TEST_USER2.userid, "2.png", 20, CURR_TIME_SECS - 600,
                        25.00, "42.30, -83.73", "yummy")


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
    _COL_NAMES = ["communityid", "userid"]

    def __init__(self, *data_values):
        super(MembershipData, self).__init__(data_values)


TEST_MEMBERSHIP1 = MembershipData(1, TEST_USER1.userid)
TEST_MEMBERSHIP2 = MembershipData(1, TEST_USER2.userid)
TEST_MEMBERSHIP3 = MembershipData(1, TEST_USER3.userid)
TEST_MEMBERSHIP4 = MembershipData(1, TEST_USER4.userid)
TEST_MEMBERSHIP5 = MembershipData(1, TEST_USER5.userid)

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

def SetUpTestItemData():
    ExecuteCommand(TEST_ITEM1.ToInsertCommand())
    ExecuteCommand(TEST_ITEM2.ToInsertCommand())

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

def SetUpTestDatabase():
    global conn
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root",
                            db="test")

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
                    "communityid int NOT NULL, "\
                    "userid varchar(20) NOT NULL);")
    SetUpTestMembershipData()

def SetUpProdDatabase():
    global conn
    conn = MySQLdb.connect(host="localhost", user=config.db_user,
                            passwd=config.db_passwd, db="prod")
    
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

def AddData(data):
    """Adds the given data to the database.

    Args:
        data: (Data) Data to be added to the database.
    """
    ExecuteCommand(data.ToInsertCommand())

def DeleteData(data):
    """Deletes the given data from the database.

    Args:
        data: (Data) Data to be deleted from the database.
    """
    ExecuteCommand(data.ToDeleteCommand())

def QueryUsers(args=[]):
    """Returns user data in the database with the specified properties.
    Args:
        args: A list of (property, value) or (property, value, op) tuples.

    Returns:
        (list of UserData) All users with the properties specified in args.
    """
    return Query(UserData, args)

def UpdateUserRole(user_data, new_role):
    """Updates the given user's role in the database.

    Args:
        user_data: (UserData) The user to update.
        new_role: (string) "buyer", "seller" or "none" - the new role of the
            user
    """
    ExecuteCommand(user_data.GetUpdateRoleCommand(new_role))
    user_data.role = new_role

def QueryItems(args=[]):
    """Returns item data in the database with the specified properties.

    Args:
        args: A list of (property, value) or (property, value, op) tuples.
        
    Returns:
        (list of ItemData) All items with the properties specifid in args.
    """
    return Query(ItemData, args)

def UpdateItem(change, item):
    """Updates item data in the database with the specified change.

    Args:
        change: (string) A change to make
        item: (ItemData) The item to change
    """
    command = item.ToUpdateCommand(change)
    x = conn.cursor()
    x.execute(command)

def AddItem(item):
    """Adds the given item to the database.

    Args:
        item: (ItemData) The item to insert.
    """
    AddData(item)

def DeleteItem(item):
    """Deletes the given item from the database.

    Args:
        item: (ItemData) The item to delete.
    """
    DeleteData(item)

def QueryTransactions(args=[]):
    """Returns transaction data in the database with the specified properties.
    """
    return Query(TransactionData, args)

def AddTransaction(transaction_data):
    """Adds the given transaction to the database.

    Args:
        transaction_data: (TransactionData) A transaction that needs to be
            completed.
    """
    AddData(transaction_data)

def CompleteTransaction(transaction_data):
    """Deletes the given buying record from the database.

    Args:
        transaction_data: (TransactionData) The buying data to delete.
    """
    DeleteData(transaction_data)

def QueryCommunities(args=[]):
    return Query(CommunityData, args)

def AddCommunity(community_data):
    """Adds the given community to the database.

    Args:
        community_data: (CommunityData) The community to be added to the
            database.
    """
    AddData(community_data)

def QueryMembership(args=[]):
    return Query(MembershipData, args)

def AddMembership(membership_data):
    """Adds the given membership data to the database.

    Args:
        membership_data: (MembershipData) The membership data to be added to
            the database.
    """
    AddData(membership_data)
