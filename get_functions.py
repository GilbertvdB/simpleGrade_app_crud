# get database functions
import sqlite3

db = sqlite3.connect("school.db")
cursor = db.cursor()


# database queries
def get_t_info(select='*', where='All', table=None, target=None):
    """ A dynamic sqlite query function that gets data from the database
    according to the chosen parameters. Gets the header columns and appends
    it to the data returns a list of tuples with data for each row.

    :param select: represents SELECT. Default is '*'.
    :param where: represents WHERE. Default is 'ALL'
    :param table: represents TABLE. Default is None
    :param target: represents ? in WHERE 'x' = ?. Default is None
    :return: a list of tuples with the data + header from the table.
    """
    if where == 'All':
        col_names = cursor.execute(f"SELECT {select} FROM {table}")
        rows = cursor.fetchall()
        header = tuple([x[0] for x in col_names.description])  # return column names
        rows.insert(0, header)
        return rows
    else:
        col_names = cursor.execute(f"SELECT {select} FROM {table} WHERE {where} = '{target}' ")
        rows = cursor.fetchall()
        header = tuple([x[0] for x in col_names.description])
        rows.insert(0, header)
        return rows


def get_reg_id_fullname(name):
    """ Gets the registry id number from a view using fullname and returns it."""
    cursor.execute(f"SELECT RegID from fullnames_view WHERE FullName = '{name}' ")
    row = cursor.fetchone()
    reg_id = row[0]
    return reg_id


def get_fullname_from_regid(id):
    """ Gets the fullname from a view using regId and returns it."""
    cursor.execute(f"SELECT FullName from fullnames_view WHERE RegId = '{id}' ")
    row = cursor.fetchone()
    fullname = row[0]
    return fullname


def get_subjects():
    """ Returns a list of the subjects from the database."""
    cursor.execute("SELECT * FROM Subjects")
    all_subjects = cursor.fetchall()
    return all_subjects


def get_classes():
    """ Gets all info from the Classes table and returns the data."""
    cursor.execute("SELECT * FROM Classes")
    data = cursor.fetchall()
    return data


if __name__ == '__main__':
    pass

    cursor.close()
    db.cursor()
