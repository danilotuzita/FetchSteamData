import re
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def to_string(self, repr):
        return re.sub(
            r"^ *|\n", "",
            repr, flags=re.MULTILINE
        )
