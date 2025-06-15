from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
# ADMINS = env.list("ADMINS")  # adminlar ro'yxati

# ADMINS = ['1058730773', ] #'1078225150'

IP = env.str("ip")  # Xosting ip manzili
# CHANNEL = ["-1001399918173", "-1001820602074", "@Kohinur_Academy_Group", "@Kohinur_Academy_Nuriston_Group"]
# CHANNEL = ['@practice_for_project', '@practise_groupp']

DEVELOPER_ID = '1058730773'

REFERRAL_LINK = "https://t.me/Kohinur_Academy_Konkursbot?start=ref_"
# REFERRAL_LINK = "https://t.me/egwikiuzbot?start=ref_"

EXCEL_FILE = './data/all_in_one.xlsx'

# try:
#     ADMINS = db_admin1.get_adminstrators_as_list()
#     CHANNEL = db_admin1.get_channels_as_a_list()
# except Exception:
#     ADMINS = ['1058730773', '1078225150']
#     CHANNEL = ["@Kohinur_Academy_Group"]


# ADMINS = ['1058730773']
# CHANNEL = ['-1001799885048']
