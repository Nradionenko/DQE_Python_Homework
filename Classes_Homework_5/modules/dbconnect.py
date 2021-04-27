import sqlite3 as sql

from exec_utils.configloader import Config
from modules.file import Files

cnf = Config()
f = Files()

label1, label2, label3 = cnf.get_values("LABELS", "news_label"), \
                         cnf.get_values("LABELS", "ad_label"), \
                         cnf.get_values("LABELS", "recipe_label")


class DBconnection:
    def __init__(self, db_name):
        with sql.connect(f.get_path(db_name)) as self.con:
            self.curs = self.con.cursor()

    def go(self, statement, predicates=''):
        """Execute sql statement"""
        self.curs.execute(statement, predicates)
        self.con.commit()

    def create_table(self, table_name):
        if table_name == label1:  # News
            self.go(cnf.get_values("SQL", "create_table_news"))
        elif table_name == label2:  # Private ad
            self.go(cnf.get_values("SQL", "create_table_ad"))
        elif table_name == label3:  # Recipe
            self.go(cnf.get_values("SQL", "create_table_recipe"))


# db = DBconnection(cnf.get_values("PATHS", "db_name"))
# db.go("drop table news")
# db.go("drop table ad")
# db.go("drop table recipe")
# db.curs.close()

