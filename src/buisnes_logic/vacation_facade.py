from src.dto.vacation_dto import VacationDTO
from src.user_repository import User_repository

from datetime import date

class VacationFacade:
    def __init__(self,vacation_repo:User_repository):
        self.vacation_repo=vacation_repo
    
    def get_all_vacation(self,sort_by:str="start_date")->list[VacationDTO]:
        """
        Retrieves all vacations from the repository and sorts them based on the specified criteria.

        Args:
            sort_by (str): The sorting criterion. 
                       - "newest" sorts vacations by start_date in descending order (newest first).
                       - Any other value sorts vacations by start_date in ascending order (oldest first).

        Returns:
        list[VacationDTO]: A list of VacationDTO objects sorted by the specified criterion.
        
        """
        vacations=self.vacation_repo.get_all_vacations()
        if sort_by == "newest":
            vacations.sort(key=lambda v: v.start_date, reverse=True)
        else:
            vacations.sort(key=lambda v: v.start_date)
       
        return vacations
    
    def ad_vacation(self, country_id:int,vacation_description:str,start_date:date,end_date:date,file_img:str,price:float):
        
        """
        Adds a new vacation to the repository after validating input parameters.

        Args:
           country_id (int): The ID of the country where the vacation is located.
           vacation_description (str): A description of the vacation.
           start_date (date): The starting date of the vacation.
           end_date (date): The ending date of the vacation.
           file_img (str): The file name path  the vacation image.
           price (float): The price of the vacation, which must be between 0 and 10,000.

    Raises:
        ValueError: If the price is not within the range of 0 to 10,000.
        ValueError: If the start_date is in the past.

    Returns:
        None
        """
        
        today=date.today()
        if price<0 or price>10000:
            raise ValueError("The price should be between 0 and 10000")
        if start_date<today:
            raise ValueError("It impossible to enter vacation on the past")
        vacation_dto=VacationDTO(None,country_id,vacation_description,start_date,end_date,file_img,price)
        self.vacation_repo.add_vacation(vacation_dto)

    def delete_vacation(self,id:int):
        """
         Deletes a vacation from the repository by its ID.

         Args:
            id (int): The unique identifier of the vacation to be deleted.

         Returns:
            None
        """
        self.vacation_repo.del_vacation_by_id(id)