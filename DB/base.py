import mysql.connector
from config import host, user, password, db_name
from fpdf import FPDF


def data_con():
    return mysql.connector.connect(
        host=host,
        port=3360,
        user=user,
        password=password,
        database=db_name
    )


def file_create(text, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.multi_cell(200, 20, txt=text)
    pdf.output("static/dok/" + title + ".pdf")


def residents():
    connection = data_con()
    cursor = connection.cursor()
    quary = '''SELECT residents.id,residents.surname,residents.name,residents.fatherland,residents.phone,residents.groupp,residents.floor,residents.date_birth,residents.elder,contracts.contract,rooms.floor,rooms.block,rooms.room 
    FROM residents
    INNER JOIN `contracts` ON residents.id=contracts.id_rez 
    INNER JOIN `room_cont` ON room_cont.id_con=contracts.id 
    INNER JOIN `rooms` ON rooms.id=room_cont.id_room '''
    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result
print(residents())

def residents_search(search):
    connection = data_con()
    search = search.lower()
    cursor = connection.cursor()
    quary = '''SELECT residents.id,residents.surname,residents.name,residents.fatherland,residents.phone,residents.groupp,residents.floor,residents.date_birth,residents.elder,contracts.contract,rooms.floor,rooms.block,rooms.room 
        FROM residents
        INNER JOIN `contracts` ON residents.id=contracts.id_rez 
        INNER JOIN `room_cont` ON room_cont.id_con=contracts.id 
        INNER JOIN `rooms` ON rooms.id=room_cont.id_room '''
    cursor.execute(quary)
    result = cursor.fetchall()
    print(result)
    res = [i for i in result if
           (search in i[1].lower()) or (search in i[2].lower()) or (search in i[3].lower()) or (
                   search in i[4].lower()) or (search in i[5].lower()) or (
                   search.lower() in (i[2] + " " + i[3] + " " + i[4]).lower())]
    connection.commit()
    cursor.close()
    connection.close()
    return res
def residents_search_min(search):
    connection = data_con()
    search = search.lower()
    cursor = connection.cursor()
    quary = '''SELECT * FROM residents'''
    cursor.execute(quary)
    result = cursor.fetchall()
    print(result)
    res = [i for i in result if
           (search in i[1].lower()) or (search in i[2].lower()) or (search in i[3].lower()) or (
                   search in i[4].lower()) or (search in i[5].lower()) or (
                   search.lower() in (i[2] + " " + i[3] + " " + i[4]).lower())]
    connection.commit()
    cursor.close()
    connection.close()
    return res

def residents_upset(s):
    connection = data_con()
    cursor = connection.cursor()
    for i in s:
        quary = f'''UPDATE residents SET surname=%s,name=%s,fatherland=%s,phone=%s,elder=%s WHERE id={i} '''
        if len(s[i]) == 5:
            cursor.execute(quary, s[i])
        else:
            cursor.execute(quary, s[i] + [0])
    connection.commit()
    cursor.close()
    connection.close()


def residents_input(f):
    connection = data_con()
    cursor = connection.cursor()
    print(f)
    quary = f'''SELECT * FROM residents WHERE (surname="{f[0]}" AND `name`="{f[1]}" AND fatherland="{f[2]}" AND groupp="{f[4]}" AND floor="{f[5]}" AND date_birth="{f[6]}")'''
    cursor.execute(quary)
    result = cursor.fetchall()+[0]
    print(result)
    d = 0
    if len(result) == 1:
        quary = '''INSERT INTO residents (surname,name,fatherland,phone,groupp,floor,date_birth,elder) VALUE (%s,%s,%s,%s,%s,%s,%s,%s)'''
        cursor.execute(quary, f)
        d = 1
    connection.commit()
    cursor.close()
    connection.close()
    return d


def residents_selctor():
    connection = data_con()
    cursor = connection.cursor()
    quary = '''SELECT id,surname,name,fatherland FROM residents WHERE (SELECT COUNT(*) FROM contracts WHERE id_rez=residents.id)<=0'''
    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def residents_selctor():
    connection = data_con()
    cursor = connection.cursor()
    quary = '''SELECT id,contract FROM contracts'''
    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def rooms_selctor():
    connection = data_con()
    cursor = connection.cursor()
    quary = '''SELECT id,floor,block,room FROM rooms WHERE ((SELECT COUNT(*) FROM room_cont WHERE room_cont.id_room=rooms.id)<rooms.max_res)'''
    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result

def rooms_name(id):
    connection = data_con()
    cursor = connection.cursor()
    quary = f'''SELECT floor,block,room FROM rooms WHERE id={id}'''
    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result[0]

def equipments_selctor():
    connection = data_con()
    cursor = connection.cursor()
    quary = '''SELECT id,name FROM equipments'''
    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def contract_input(f):
    connection = data_con()
    cursor = connection.cursor()
    quary = '''INSERT INTO contracts (id_rez,contract,file,date,noactive) VALUE (%s,%s,%s,%s,%s)'''
    cursor.execute(quary, f)
    connection.commit()
    cursor.close()
    connection.close()


def contract_search(id):
    connection = data_con()
    cursor = connection.cursor()
    quary = f'''SELECT id FROM contracts WHERE id_rez={id}'''
    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def contract_room_input(f):
    connection = data_con()
    cursor = connection.cursor()
    quary = '''INSERT INTO room_cont (id_con,id_room,date,prov) VALUE (%s,%s,%s,%s)'''
    cursor.execute(quary, f)
    connection.commit()
    cursor.close()
    connection.close()


def contract_equipment_input(f):
    connection = data_con()
    cursor = connection.cursor()
    quary = '''INSERT INTO equipment_cont (id_con,id_equ,date,prov) VALUE (%s,%s,%s,%s)'''
    cursor.execute(quary, f)
    connection.commit()
    cursor.close()
    connection.close()


def contract_equipment_prov(id_con, id_eq):
    connection = data_con()
    cursor = connection.cursor()
    quary = f'''SELECT * FROM equipment_cont WHERE id_equ={id_eq} AND id_con={id_con}'''
    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def contracts():
    connection = data_con()
    cursor = connection.cursor()
    quary = f'''SELECT room_cont.id,contracts.contract,contracts.file,rooms.floor,rooms.block,rooms.room,contracts.date,room_cont.prov,room_cont.id_room 
    FROM room_cont 
    INNER JOIN `rooms` ON room_cont.id_room=rooms.id
    INNER JOIN `contracts` ON contracts.id=room_cont.id_con'''

    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def contracts_search(search):
    connection = data_con()
    search = search.lower()
    cursor = connection.cursor()
    quary = f'''SELECT room_cont.id,contracts.contract,contracts.file,rooms.floor,rooms.block,rooms.room,contracts.date,room_cont.prov,room_cont.id_room 
    FROM room_cont 
    INNER JOIN `rooms` ON room_cont.id_room=rooms.id
    INNER JOIN `contracts` ON contracts.id=room_cont.id_con'''
    cursor.execute(quary)
    result = cursor.fetchall()
    res = [i for i in result if
           (search in i[1].lower()) or (search in (str(i[3]) + str(i[4]) + i[5]).lower())]
    connection.commit()
    cursor.close()
    connection.close()
    return res


def room_upset(s):
    connection = data_con()
    cursor = connection.cursor()
    for i in s:
        quary = f'''UPDATE room_cont SET prov={s[i]} WHERE id={i} '''
        cursor.execute(quary)
    connection.commit()
    cursor.close()
    connection.close()


def equipment():
    connection = data_con()
    cursor = connection.cursor()
    quary = f'''SELECT equipment_cont.id,contracts.contract,contracts.file,equipments.name,contracts.date,equipment_cont.prov
    FROM equipment_cont
    INNER JOIN `contracts` ON contracts.id=equipment_cont.id_con
    INNER JOIN `equipments` ON equipment_cont.id_equ=equipments.id'''

    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def equipment_search(search):
    connection = data_con()
    search = search.lower()
    cursor = connection.cursor()
    quary = f'''SELECT equipment_cont.id,contracts.contract,contracts.file,equipments.name,contracts.date,equipment_cont.prov
    FROM equipment_cont
    INNER JOIN `contracts` ON contracts.id=equipment_cont.id_con
    INNER JOIN `equipments` ON equipment_cont.id_equ=equipments.id'''
    cursor.execute(quary)
    result = cursor.fetchall()
    res = [i for i in result if
           (search in i[1].lower()) or (search in i[3].lower())]
    connection.commit()
    cursor.close()
    connection.close()
    return res


def equipment_upset(s):
    connection = data_con()
    cursor = connection.cursor()
    for i in s:
        quary = f'''UPDATE equipment_cont SET prov={s[i]} WHERE id={i} '''
        cursor.execute(quary)
    connection.commit()
    cursor.close()
    connection.close()


def type_reference():
    connection = data_con()
    cursor = connection.cursor()
    quary = f'''SELECT id,name FROM type_reference'''
    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def reference_input(f):
    connection = data_con()
    cursor = connection.cursor()
    quary = '''INSERT INTO reference (id_res,id_type,file,date) VALUE (%s,%s,%s,%s)'''
    cursor.execute(quary, f)
    connection.commit()
    cursor.close()
    connection.close()


def reference():
    connection = data_con()
    cursor = connection.cursor()
    quary = f'''SELECT reference.id,reference.file,residents.surname,residents.name,residents.fatherland,type_reference.name,reference.date
        FROM reference
        INNER JOIN `residents` ON residents.id=reference.id_res
        INNER JOIN `type_reference` ON reference.id_type=type_reference.id'''
    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def disciplinary_input(f):
    connection = data_con()
    cursor = connection.cursor()
    quary = '''INSERT INTO disciplinary (id_rez,reason,date) VALUE (%s,%s,%s)'''
    cursor.execute(quary, f)
    connection.commit()
    cursor.close()
    connection.close()


def disciplinary():
    connection = data_con()
    cursor = connection.cursor()
    quary = f'''SELECT disciplinary.id,residents.surname,residents.name,residents.fatherland,disciplinary.reason,disciplinary.date
        FROM disciplinary
        INNER JOIN `residents` ON residents.id=disciplinary.id_rez'''
    cursor.execute(quary)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def disciplinary_search(search):
    connection = data_con()
    cursor = connection.cursor()
    search = search.lower()
    quary = f'''SELECT disciplinary.id,residents.surname,residents.name,residents.fatherland,disciplinary.reason,disciplinary.date
        FROM disciplinary
        INNER JOIN `residents` ON residents.id=disciplinary.id_rez'''
    cursor.execute(quary)
    result = cursor.fetchall()
    res = [i for i in result if
           (search in i[1].lower()) or (search in i[2].lower()) or (search in i[3].lower()) or (
                   search in i[4].lower()) or (search.lower() in (i[2] + " " + i[3] + " " + i[4]).lower())]
    connection.commit()
    cursor.close()
    connection.close()
    return res


def reference_search(search):
    connection = data_con()
    cursor = connection.cursor()
    search = search.lower()
    quary = f'''SELECT reference.id,reference.file,residents.surname,residents.name,residents.fatherland,type_reference.name,reference.date
        FROM reference
        INNER JOIN `residents` ON residents.id=reference.id_res
        INNER JOIN `type_reference` ON reference.id_type=type_reference.id'''
    cursor.execute(quary)
    result = cursor.fetchall()
    res = [i for i in result if
           (search in i[2].lower()) or (search in i[3].lower()) or (search in i[4].lower()) or (
                   search.lower() in i[5].lower()) or (search.lower() in (i[2] + " " + i[3] + " " + i[4]).lower())]
    connection.commit()
    cursor.close()
    connection.close()
    return res


print(disciplinary())
print(reference())

print(rooms_selctor())
