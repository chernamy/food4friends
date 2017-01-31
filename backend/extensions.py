import MySQLdb
import MySQLdb.cursors
import config

class UserData(object):
    
    def __init__(self, username, password, firstname, lastname, role,
                location):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.location = location

    @staticmethod
    def FromDbData(data):
        """Creates a UserData object from a MySQL data tuple.
        """
        return UserData(*data)

    def ToInsertCommand(self):
        """Creates the command to insert this user into the database.
        """
        return "INSERT INTO USER VALUES('%s', '%s', '%s', '%s', '%s', '%s')" %(
                    self.username, self.password, self.firstname,
                    self.lastname, self.role, self.location)

    @staticmethod
    def BuildQuery(args):
        return "SELECT * FROM USER" + BuildQueryArgs(args)

TEST_USER1 = UserData("username", "password", "First1", "Last1", "none", "-")
TEST_USER2 = UserData("username2", "password2", "First2", "Last2", "buyer", "-")

class ItemData(object):

    def __init__(self, userid, photo, servings, duration, price, address,
                                                                description):
        self.userid = userid
        self.photo = photo
        self.servings = servings
        self.duration = duration
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
                                        self.servings, self.duration,
                                        self.price, self.address,
                                        self.description)

    @staticmethod
    def BuildQuery(args):
        return "SELECT * FROM ITEM" + BuildQueryArgs(args)

    @staticmethod
    def BuildUpdate(update, args):
        return "UPDATE ITEM SET " + update + BuildQueryArgs(args)

TEST_ITEM1 = ItemData("user1", "1.png", 10, 3, 12.25, "42.28, -83.73","tasty")
TEST_ITEM2 = ItemData("user2", "2.png", 20, 5, 25.00, "42.30, -83.73", "yummy")

conn = None

def ExecuteCommand(command):
    x = conn.cursor()
    x.execute(command)
    conn.commit()

def SetUpTestUserData():
    ExecuteCommand(TEST_USER1.ToInsertCommand())
    ExecuteCommand(TEST_USER2.ToInsertCommand())

def SetUpTestItemData():
    ExecuteCommand(TEST_ITEM1.ToInsertCommand())
    ExecuteCommand(TEST_ITEM2.ToInsertCommand())

def SetUpTestDatabase():
    global conn
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root",
                            db="test")

    ExecuteCommand("DROP TABLE IF EXISTS USER;")
    ExecuteCommand("CREATE TABLE USER("\
                "username VARCHAR(20) NOT NULL, "\
                "password VARCHAR(20) NOT NULL, "\
                "firstname VARCHAR(25) NOT NULL, "\
                "lastname VARCHAR(25) NOT NULL, "\
                "role ENUM('none', 'buyer', 'seller') NOT NULL, "\
                "location VARCHAR(255), "\
                "PRIMARY KEY(username));")
    SetUpTestUserData()

    ExecuteCommand("DROP TABLE IF EXISTS ITEM;")
    ExecuteCommand("CREATE TABLE ITEM("\
                "userid VARCHAR(40) NOT NULL, "\
                "photo VARCHAR(40) NOT NULL, "\
                "servings INT NOT NULL, "\
                "duration INT NOT NULL, "\
                "price DECIMAL(5, 2) NOT NULL, "\
                "address VARCHAR(255) NOT NULL, "\
                "description TEXT, "\
                "PRIMARY KEY(userid));")
    SetUpTestItemData()

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
            If the input is [(username, "mjchao")],
            " where  username = 'mjchao'" is returned. If the input is
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

