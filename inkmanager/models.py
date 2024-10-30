import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import func, text, types
from sqlalchemy.orm import Mapped, mapped_column, registry


table_registry = registry()


class NeedleModel(str, Enum):
    round_liner = 'RL'
    round_shader = 'RS'
    magnum = 'MG'
    magnum_rounded = 'MGR'


class NeedleSize(str, Enum):
    n08_01 = '0801'
    n08_03 = '0803'
    n08_05 = '0805'
    n08_07 = '0807'
    n08_09 = '0809'
    n08_11 = '0811'
    n08_13 = '0813'
    n08_14 = '0814'
    n08_15 = '0815'
    n08_17 = '0817'
    n08_19 = '0819'
    n08_21 = '0821'
    n08_23 = '0823'
    n08_25 = '0825'
    n08_27 = '0827'
    n10_01 = '1001'
    n10_03 = '1003'
    n10_05 = '1005'
    n10_07 = '1007'
    n10_09 = '1009'
    n10_11 = '1011'
    n10_13 = '1013'
    n10_14 = '1014'
    n10_15 = '1015'
    n10_17 = '1017'
    n10_19 = '1019'
    n10_21 = '1021'
    n10_23 = '1023'
    n10_25 = '1025'
    n10_27 = '1027'
    n12_01 = '1201'
    n12_03 = '1203'
    n12_05 = '1205'
    n12_07 = '1207'
    n12_09 = '1209'
    n12_11 = '1211'
    n12_13 = '1213'
    n12_14 = '1214'
    n12_15 = '1215'
    n12_17 = '1217'
    n12_19 = '1219'
    n12_21 = '1221'
    n12_23 = '1223'
    n12_25 = '1225'
    n12_27 = '1227'


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        init=False,
        server_default=text('gen_random_uuid()'),
    )
    name: Mapped[str] = mapped_column(unique=True)
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Ink:
    __tablename__ = 'inks'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        init=False,
        server_default=text('gen_random_uuid()'),
    )
    name: Mapped[str]
    brand: Mapped[str]
    color: Mapped[str]
    weight: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Neddle:
    __tablename__ = 'neddles'

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        init=False,
        server_default=text('gen_random_uuid()'),
    )
    name: Mapped[str]
    brand: Mapped[str]
    model: Mapped[NeedleModel]
    size: Mapped[NeedleSize]
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
