from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.follow import FollowRSSPath

x_user_list = [
    "karpathy",
    "AndrewYNg",
    "ShunyuYao",
    "ilyasut",
    # "ylecun",
    # "feifeili",
    # "timnitGebru",
    # "mmitchell_ai",
    # "mathbabedotorg",
    # "lawrennd",
    # "bethsingler",
    # "odsch",
    # "iamtrask",
    # "JeffDean",
    # "geoffreyhinton",
    # "ybengioy",
    # "Kdnuggets",
    # "KirkDBorne",
    # "jonathan_schulz",
    # "woj_zaremba",
    # "katecrawford",
    # "jovialjoy",
    # "danielarus",
    # "tom_mitchell",
    # "PieterAbbeel",
    # "zoubin",
    # "f_dde",
    # "OriolVinyalsML",
    # "david_silver",
    # "jackclarkSF",
    # "sama",
    # "kaifulee",
    # "demishassabis",
    # "gdb",
]


user_id = "DQPoHXKpxwuMEHHgU86Ltbsssp3cdOMz"


async def initial_test(session: AsyncSession):
    users = []
    for x_user in x_user_list:
        users.append(FollowRSSPath(user_id=user_id, rss_path=f"/twitter/user/{x_user}"))
    session.add_all(users)
    await session.commit()
