# brew install postgresql
# pip install psycopg2-binary
import psycopg2
import csv
from datetime import datetime
import eilcommon

conn = psycopg2.connect(
    dbname=eilcommon.pg_database, 
    user=eilcommon.pg_user, 
    password=eilcommon.pg_password, 
    host=eilcommon.pg_host, 
    port=eilcommon.pg_port
)
cur = conn.cursor()

first = True
csvStart = False

with open("./datasets/files/2022-08_GSEC_Listing_of_UUPG_100K_removals.csv", newline='') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    next(reader)
    for row in reader:
        # rows.append(row)
        # if csvStart == False and row[0]:
        #     csvStart = True
        #     continue
        if not all(i is '' for i in row):
            print(f"PEID {row[0]}\n Affinity Bloc {row[1]}\n People Cluster {row[2]}\n Country {row[3]}\n People Group {row[4]}\n Global Status of Evangelical Christianity {row[5]}\n Language {row[6]}\n Religion {row[7]}\n Population {row[8]}\n Addition Date {row[9]}\n Addition Reasons {row[10]}\n\n\n")
            # break

            cur.execute("insert into gsec_listing_of_uupg_100k_removals (peid,affinity_bloc,people_cluster,country,people_group,global_status_of_evangelical_christianity,language,religion,population,addition_date,addition_reasons) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        ((row[0] or None), row[1], row[2], row[3], row[4], (row[5] or None), row[6], row[7], (row[8].replace(",", "") or None), (None if row[9] == '' else datetime.strptime(row[9], '%m/%d/%y')), row[10]))
            conn.commit()

cur.close()
conn.close()
