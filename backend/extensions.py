import calendar
import config
import MySQLdb
import MySQLdb.cursors
import time

class UserData(object):
    
    def __init__(self, userid, role, location):
        self.userid = userid
        self.role = role
        self.location = location

    @staticmethod
    def FromDbData(data):
        """Creates a UserData object from a MySQL data tuple.
        """
        return UserData(*data)

    def ToInsertCommand(self):
        """Creates the command to insert this user into the database.

        Returns:
            (string) The MySQL command to insert this user into the database.
        """
        return "INSERT INTO USER VALUES('%s', '%s', '%s')" %(self.userid,
            self.role, self.location)

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
        return "UPDATE USER SET role='%s' where userid='%s'" %(new_role,
                                                                self.userid)

    @staticmethod
    def BuildQuery(args):
        return "SELECT * FROM USER" + BuildQueryArgs(args)

TEST_USER1 = UserData("user1", "seller", "-")
TEST_USER2 = UserData("user2", "seller", "-")
TEST_USER3 = UserData("user3", "none", "-")
TEST_USER4 = UserData("user4", "none", "-")
TEST_USER5 = UserData("user5", "buyer", "-")

class ItemData(object):

    def __init__(self, userid, photo, servings, end, price, address,
                                                                description):
        self.userid = userid
        self.photo = photo
        self.servings = servings
        self.end = end
        self.price = float(price)
        self.address = address
        self.description = description

    @staticmethod
    def FromDbData(data):
        return ItemData(*data)

    def ToInsertCommand(self):
        """Creates the command to insert this item into the database.
        """
        return "INSERT INTO ITEM VALUES('%s', '%s', '%s', '%s',"\
                    "'%s', '%s', '%s')" %(self.userid, self.photo,
                                        self.servings, self.end,
                                        self.price, self.address,
                                        self.description)

    def ToDeleteCommand(self):
        """Creates the command to delete this item from the database.
        """
        return "DELETE FROM ITEM WHERE userid='%s'" %(self.userid) 

    @staticmethod
    def BuildQuery(args):
        return "SELECT * FROM ITEM" + BuildQueryArgs(args)

    @staticmethod
    def BuildUpdate(update, args):
        return "UPDATE ITEM SET " + update + BuildQueryArgs(args)


CURR_TIME_SECS = calendar.timegm(time.gmtime())
# This is a test item that will expire in 10 minutes
TEST_ITEM1 = ItemData("user1", "1.png", 10, CURR_TIME_SECS + 600, 12.25,
                        "42.28, -83.73","tasty")

# This is a test item that expired 10 minutes ago
TEST_ITEM2 = ItemData("user2", "2.png", 20, CURR_TIME_SECS - 600, 25.00,
                        "42.30, -83.73", "yummy")

class TransactionData(object):
    
    def __init__(self, sellerid, buyerid, servings):
        self.sellerid = sellerid
        self.buyerid = buyerid
        self.servings = servings

    @staticmethod
    def FromDbData(data):
        return TransactionData(*data)

    def ToInsertCommand(self):
        """Creates the command to insert this item into the database.

        Returns:
            (string) The MySQL command to insert this item in the database.
        """
        return "INSERT INTO TRANSACTION VALUES('%s', '%s', '%s')" %(
                                    self.sellerid, self.buyerid, self.servings)
    
    def ToDeleteCommand(self):
        """Creates the command to delete this item from the database.

        Returns:
            (string) The MySQL command to delete this item from the database.
        """
        return "DELETE FROM TRANSACTION WHERE buyerid='%s' and sellerid='%s'" %(
            self.buyerid, self.sellerid)
    
    @staticmethod
    def BuildQuery(args):
        return "SELECT * FROM TRANSACTION" + BuildQueryArgs(args)

TEST_TRANSACTION1 = TransactionData("user1", "user5", 10)

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

def SetUpProdDatabase():
    global conn
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root",
                            db="prod")
    
def Init():
    """Reinitializes the database. If this is prod, the connection will just
    be reset. If this is test, the test data will be reset.
    """
    if config.env["state"] == "test":
        SetUpTestDatabase()
    else:
        SetUpProdDatabase()

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

def QueryUsers(args=[]):
    """Returns user data in the database with the specified properties.
    Args:
        args: A list of (property, value) or (property, value, op) tuples.

    Returns:
        (list of UserData) All users with the properties specified in args.
    """
    query = UserData.BuildQuery(args)
    x = conn.cursor()
    x.execute(query)
    return [UserData.FromDbData(result) for result in x.fetchall()]

def UpdateUserRole(user_data, new_role):
    """Updates the given user's role in the database.

    Args:
        user_data: (UserData) The user to update.
        new_role: (string) "buyer", "seller" or "none" - the new role of the
            user
    """
    user_data.role = new_role
    ExecuteCommand(user_data.GetUpdateRoleCommand(new_role))

def QueryItems(args=[]):
    """Returns item data in the database with the specified properties.

    Args:
        args: A list of (property, value) or (property, value, op) tuples.
        
    Returns:
        (list of ItemData) All items with the properties specifid in args.
    """
    query = ItemData.BuildQuery(args)
    x = conn.cursor()
    x.execute(query)
    return [ItemData.FromDbData(result) for result in x.fetchall()]

def UpdateItems(change, args=[]):
    """Updates item data in the database with the specified change.

    Args:
        change: (string) A change to make
        args: A list of (property, value) or (property, value, op) tuples.
    """
    command = ItemData.BuildUpdate(change, args)
    x = conn.cursor()
    x.execute(command)

def AddItem(item):
    """Adds the given item to the database.

    Args:
        item: (ItemData) The item to insert.
    """
    ExecuteCommand(item.ToInsertCommand())

def DeleteItem(item):
    """Deletes the given item from the database.

    Args:
        item: (ItemData) The item to delete.
    """
    ExecuteCommand(item.ToDeleteCommand())

def QueryTransactions(args=[]):
    """Returns transaction data in the database with the specified properties.
    """
    query = TransactionData.BuildQuery(args)
    x = conn.cursor()
    x.execute(query)
    return [TransactionData.FromDbData(result) for result in x.fetchall()]

def AddTransaction(transaction_data):
    """Adds the given transaction to the database.

    Args:
        transaction_data: (TransactionData) A transaction that needs to be
            completed.
    """
    ExecuteCommand(transaction_data.ToInsertCommand())

def CompleteTransaction(transaction_data):
    """Deletes the given buying record from the database.

    Args:
        transaction_data: (TransactionData) The buying data to delete.
    """
    ExecuteCommand(transaction_data.ToDeleteCommand())
