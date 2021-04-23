from openpyxl import Workbook
import src.day_nudge_count
import src.stb_id_count
import src.extraction_stb_id
from datetime import datetime


def make_xl():

    # try:
    save_day = datetime.today().strftime("%Y-%m-%d")

    write_wb = Workbook()
    nudge_count = src.day_nudge_count.nudge_count()
    stb_count = src.stb_id_count.stb_id_count()
    ext_count = src.extraction_stb_id.extraction_stb_count()
    write_ws = write_wb.active

    nudge_row_count = 1
    for n_count in nudge_count:
        nudge_count_key = str(list(n_count.keys())).replace("[", '').replace(']', '').replace("'", "")
        nudge_count_value = str(list(n_count.values())).replace("[", '').replace(']', '').replace("'", "")

        a = 'A'+str(nudge_row_count)
        write_ws[a] = nudge_count_key

        b = 'B' + str(nudge_row_count)
        write_ws[b] = nudge_count_value

        nudge_row_count += 1

    stb_row_count = 1
    for s_count in stb_count:
        stb_count_key = str(list(s_count.keys())).replace("[", '').replace(']', '').replace("'", "")
        stb_count_value = str(list(s_count.values())).replace("[", '').replace(']', '').replace("'", "")

        d = 'D' + str(stb_row_count)
        write_ws[d] = stb_count_key

        e = 'E' + str(stb_row_count)
        write_ws[e] = stb_count_value

        stb_row_count += 1

    ext_row_count = 1
    for e_count in ext_count:
        ext_count_key = str(list(e_count.keys())).replace("[", '').replace(']', '').replace("'", "")
        ext_count_value = str(list(e_count.values())).replace("[", '').replace(']', '').replace("'", "")

        g = 'G' + str(ext_row_count)
        write_ws[g] = ext_count_key


        h = 'H' + str(ext_row_count)
        write_ws[h] = ext_count_value

        ext_row_count += 1

    i = 'I1'
    write_ws[i] = "D9=active 셋탑건수 = zapping 추출대상건수"
    i2 = 'I2'
    write_ws[i2] = "dcmark추출대상 IAM통해서 구해야함"

    write_wb.save('C:/Users/정민채/OneDrive/바탕 화면/Files/넛지통계('+save_day+').xlsx')
    # except Exception as err:
    #     print("MAKE XLSX ERROR", err)