from src.dal.data_base import Vacation_db_connect
from src.dal.show_table import Show_table
from src.dal.get_row_by_id import Get_row_by_id
from src.dal.delete_row_by_id import DELETE_row_by_id
from src.dal.db_config import host,dbname,user,password
from src.dal.update_row_by_id import Update_table

db=Vacation_db_connect(host=host, dbname=dbname, user=user, password=password)
db.connect()
# show=Show_table(db)
# show.get_table("vacation")
# show_id=Get_row_by_id(db)
# show_id.get_row_by_id("vacation",2)
# delete=DELETE_row_by_id(db)
# delete.delete_row_by_id("vacation",16)
update=Update_table(db)
update.update_row_by_id("vacation","price",5000,16)