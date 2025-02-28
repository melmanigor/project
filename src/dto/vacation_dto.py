from dataclasses import dataclass


@dataclass
class VacationDTO:
    id: int
    id_country: int
    vacation_description: str
    start_date: str
    end_date: str
    file_image: str
    price: str
