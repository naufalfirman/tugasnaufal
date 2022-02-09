import datetime
waktu = datetime.datetime.now()

#__init__
import sqlite3
with sqlite3.connect("5210411166_DB_Responsi_ALPRO_Kel5.db") as db :
    cursor = db.cursor()

#Inputan Kendaraan
def inputData():
    # Plat Nomor
    
    print("\n\t##########","INPUT KENDARAAN","##########")
    Plat_Nomor = (input("\nMasukan Plat Nomor Kendaraan : ")).upper()

    #Jenis Kendaraan
    print("\n\t","*"*10,"KODE KENDARAAN","*"*10)
    print("Sepeda Motor     ==> 1")
    print("Mobil            ==> 2")

    Jenis_Knd = input("Masukan Jenis Kendaraan : ").upper()
    Jenis = " "
    if Jenis_Knd == '1':
        Jenis = 'MOTOR'
    elif Jenis_Knd == '2':
        Jenis = 'MOBIL'

    model_knd = str(input("Masukan Model Kendaraan : ")).upper()
    warna = str(input("Masukan Warna Kendaraan : ")).upper()


    cursor.execute('INSERT INTO `DATA_PARKIR` (`NOMOR_PLAT`, `JENIS`, `MODEL`, `WARNA`, `WAKTU_MASUK`) VALUES ("%s", "%s", "%s", "%s", datetime("now","localtime"));' % (Plat_Nomor, Jenis, model_knd, warna))
    db.commit()

    print("\nWAKTU PARKIR BERJALAN DARI SEKARANG!!!",waktu)


#Inputan Waktu_Keluar
def Outputan(input_plat):
    print("Format Inputan : YY-MM-DD H:M:S")
    tanggal = str(input("Masukkan Hari keluar : "))
    jam = int(input("Masukkan Jam keluar : "))
    menit = int(input("Masukkan Menit keluar : "))

    waktu_keluar = waktu.strftime(f"%Y-%m-{tanggal} {jam}:{menit}:%S")
    
    cursor.execute(f'''UPDATE DATA_PARKIR SET WAKTU_KELUAR  = datetime('{waktu_keluar}') WHERE NOMOR_PLAT = '{input_plat}' ''')
    db.commit()
    

#Pengecekan dan perhitungan biaya
def HitungParkir(input_plat):

    cursor.execute(f"SELECT COUNT(*) FROM DATA_PARKIR WHERE NOMOR_PLAT = '{input_plat}'")
    db.commit()
    for i in cursor.fetchall() :

        if i[0] == 1 :
            x = f'''SELECT JENIS like '%MOBIL%' FROM DATA_PARKIR  WHERE NOMOR_PLAT = '{input_plat}' '''
            cursor.execute(x)
            db.commit()

            for g in cursor.fetchall():
                Outputan(input_plat)

                #Mobil
                if g[0] == 1 :
                    
                    cursor.execute(f'''SELECT CAST ((substr(WAKTU_KELUAR,9, 2)) as int) FROM DATA_PARKIR WHERE NOMOR_PLAT = '{input_plat}' ''')
                    db.commit()
                    for s in cursor.fetchall():
                        s

                    cursor.execute(f'''SELECT CAST ((substr(WAKTU_MASUK,9, 2)) as int) FROM DATA_PARKIR WHERE NOMOR_PLAT = '{input_plat}' ''')
                    db.commit()
                    for q in cursor.fetchall():
                        q
      
                    if s[0] == q[0] :
                        cursor.execute(f'''SELECT * FROM DATA_PARKIR WHERE NOMOR_PLAT = '{input_plat}' ''')
                        data_waktu = cursor.fetchall()[0]
                        y = data_waktu[6]
                        t = data_waktu[5]

                        durasi_sewa = waktu.strptime(y, f"%Y-%m-%d %H:%M:%S") - waktu.strptime(t, f"%Y-%m-%d %H:%M:%S")
                        durasi = durasi_sewa.total_seconds()
                        bagi = durasi / 60
                            
                        if bagi <= 60 :
                            biaya = 3000

                        elif bagi > 60 :
                            biaya = 6000

                    else :
                        biaya = 100000

                # #Motor
                else :
                    cursor.execute(f'''SELECT CAST ((substr(WAKTU_KELUAR,9, 2)) as int) FROM DATA_PARKIR WHERE NOMOR_PLAT = '{input_plat}' ''')
                    db.commit()
                    for s in cursor.fetchall():
                        s
                
                    cursor.execute(f'''SELECT CAST ((substr(WAKTU_MASUK,9, 2)) as int) FROM DATA_PARKIR WHERE NOMOR_PLAT = '{input_plat}' ''')
                    db.commit()
                    for q in cursor.fetchall():
                        q
        
                    if s[0] == q[0] :
                        cursor.execute(f'''SELECT * FROM DATA_PARKIR WHERE NOMOR_PLAT = '{input_plat}' ''')
                        data_waktu = cursor.fetchall()[0]
                        y = data_waktu[6]
                        t = data_waktu[5]

                        durasi_sewa = waktu.strptime(y, f"%Y-%m-%d %H:%M:%S") - waktu.strptime(t, f"%Y-%m-%d %H:%M:%S")
                        durasi = durasi_sewa.total_seconds()
                        bagi = durasi / 60
                            
                        if bagi <= 60 :
                            
                            biaya = 2000

                        elif bagi > 60:
                            
                            biaya = 3000

                    else :
                        biaya = 50000

                print("Nominal Yang Harus Dibayarkan : ",biaya)
                usermasuk = int(input("Masukan Nominal Pembayaran : "))

                while usermasuk < biaya :
                    print("Nominal pembayaran harus lebih besar atau sama dengan", biaya)
                    usermasuk = int(input("Masukkan nominal yang dibayarkan : "))
                cursor.execute(f'''UPDATE DATA_PARKIR SET BIAYA_PARKIR  = {biaya}, NOMINAL_BAYAR  = {usermasuk} WHERE NOMOR_PLAT = '{input_plat}' ''')
                db.commit()
                print('''\nDATA PARKIR KENDARAAN BERHASIL DIUPDATE !!!
SILAHKAN PILIH MENU NOMOR 3 UNTUK CETAKK STRUK''')

        elif i[0] == 0:
            print("Plat Nomot ",input_plat,"Tidak Ditemukan")
        

while True:

    print("\n","*"*10,"APLIKASI SISTEM PARIR","*"*10)
    print("1.   Input data kendaraan masuk ")
    print("2.   Hitung biaya parkir")
    print("3.   Cetak bukti bayar parkir")
    print("4.   Keluar Aplikasi \n")
    print("*"*45, "\n")

    pilihan = int(input("Masukan Pilihan Anda : "))

    if pilihan == 1:

        inputData()

    elif pilihan == 2:
        print("\n","*"*10,"HITUNG TOTAL BIAYA PARKIR","*"*10)
        z = str(input("Masukan Plat Nomor : ")).upper()
        print("\n")
        HitungParkir(z)


    elif pilihan == 3:
        plat_nomor = str(input("Masukkan plt nomor : ")).upper()
        print("\n")
        cursor.execute(f"SELECT COUNT(*) FROM DATA_PARKIR WHERE NOMOR_PLAT = '{plat_nomor}'")
        for i in cursor.fetchall():
            i
        
        if i[0] < 1: 
            print("NOMOR PLAT ",plat_nomor,"TIDAK DITEMUKAN" )
        else : 
            cursor.execute(f"SELECT * FROM DATA_PARKIR WHERE NOMOR_PLAT = '{plat_nomor}'")
            data = cursor.fetchall()[0]
            print("******** STRUK PEMBAYARAN *********")
            print(f'''
            
Plat Nomor	: {plat_nomor}
Jenis	: {data[2]}
Model	: {data[3]}
Warna	: {data[4]}
Waktu Masuk	: {data[5]}		
Waktu Keluar	: {data[6]}		
*****************************************
Biaya yang harus dibayarkan:
Rp. {data[7]}

Nominal yang dibayarkan:
Rp. {data[8]}

Kembalian : Rp. { int(data[8]) - int(data[7]) }
*****************************************
            ''')

            # hapus datanya setelah di cetak
            cursor.execute(f'DELETE FROM DATA_PARKIR WHERE NOMOR_PLAT = "{plat_nomor}"')
            db.commit()


    elif pilihan == 4:
        print("\nKELUAR DARI APLIKASI")
        db.close()
        break