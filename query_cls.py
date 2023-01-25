import sqlite3
import os

class Query():
    """
    The class performs various queries to the database depending
    on the parameters passed.
    """
    def __init__(self) -> None:
        # conn = sqlite3.connect(self._add_path("budzet.db"))
        # cur = conn.cursor()
        pass

    def _remove_special_char(self, Value):
        """
        Handles special characters to avoid conflicts with SQL syntax.
        Special characters: ' , " , backslash
        """
        pass
    
    def _add_path(self, file_name):
       """
       Finds the absolute path to the file.
       """
       a = os.path.abspath(os.getcwd())
       c = r" \ "
       c = c.strip()
       a = a + c + file_name
       return a

    def add_path(file_name):
       """
       Finds the absolute path to the file.
       """
       a = os.path.abspath(os.getcwd())
       c = r" \ "
       c = c.strip()
       a = a + c + file_name
       return a

print ()
print (Query.add_path("PARENT Proba"))
print ()