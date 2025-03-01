from src.dto.vacation_dto import VacationDTO
from src.user_repository import User_repository

from datetime import date

class VacationFacade:
    def __init__(self,vacation_repo:User_repository):
        self.vacation_repo=vacation_repo
    
    def get_all_vacation(self,sort_by:str="start_date")->list[VacationDTO]:
        vacations=self.vacation_repo.get_all_vacations()
        if sort_by == "newest":
            vacations.sort(key=lambda v: v.start_date, reverse=True)
        else:
            vacations.sort(key=lambda v: v.start_date)
       
        return vacations
    
    def ad_vacation(self, country_id:int,vacation_description:str,start_date:date,end_date:date,file_img:str,price:float):
        today=date.today()
        if price<0 or price>10000:
            raise ValueError("The price should be between 0 and 10000")
        if start_date<today:
            raise ValueError("It impossible to enter vacation on the past")
        vacation_dto=VacationDTO(None,country_id,vacation_description,start_date,end_date,file_img,price)
        self.vacation_repo.add_vacation(vacation_dto)

    def delete_vacation(self,id:int):
        self.vacation_repo.del_vacation_by_id(id)