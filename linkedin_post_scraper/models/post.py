from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class PostLead:
    author: str
    profile_url: str
    headline: str
    post_url: str
    text: str

class PostCollection:
    def __init__(self):
        self.leads: List[PostLead] = []

    def add_lead(self, lead: PostLead):
        self.leads.append(lead)

    def to_list_of_dicts(self) -> List[Dict]:
        return [asdict(l) for l in self.leads]