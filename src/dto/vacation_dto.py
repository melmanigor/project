from dataclasses import dataclass


@dataclass
class VacationDTO:
    id: int
    country_id: int
    description: str
    start_date: str
    end_date: str
    file_img: str
    price: str
