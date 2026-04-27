import json
import csv
import os
from connect import get_connection


# получить список всех групп из базы
def get_groups():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM groups ORDER BY name;")
    groups = cur.fetchall()
    cur.close()
    conn.close()
    return groups


# найти или создать группу, вернуть её id
def get_or_create_group(conn, group_name):
    cur = conn.cursor()
    cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
    row = cur.fetchone()
    if row:
        cur.close()
        return row[0]
    cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id;", (group_name,))
    group_id = cur.fetchone()[0]
    cur.close()
    return group_id


# найти id контакта по имени (вернёт None если не найден)
def get_contact_id(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
    row = cur.fetchone()
    cur.close()
    return row[0] if row else None


# вывести список контактов в виде таблицы
def print_contacts(rows):
    if not rows:
        print("Контакты не найдены.")
        return
    print(f"\n{'ID':<4} {'Имя':<20} {'Email':<25} {'День рождения':<14} {'Группа':<10} {'Телефон':<15} {'Тип'}")
    print("-" * 95)
    for row in rows:
        cid, name, email, birthday, group, phone, ptype = row
        print(f"{str(cid):<4} {str(name or ''):<20} {str(email or ''):<25} {str(birthday or ''):<14} {str(group or ''):<10} {str(phone or ''):<15} {str(ptype or '')}")


# ── добавить новый контакт ─────────────────────────────────────

def add_contact():
    print("\n-- Добавить контакт --")
    name = input("Имя: ").strip()
    if not name:
        print("Имя не может быть пустым.")
        return

    email = input("Email (Enter чтобы пропустить): ").strip() or None
    birthday = input("День рождения ГГГГ-ММ-ДД (Enter чтобы пропустить): ").strip() or None

    groups = get_groups()
    print("Группы:")
    for gid, gname in groups:
        print(f"  {gname}")
    group_name = input("Группа (Enter = Other): ").strip() or "Other"

    conn = get_connection()
    group_id = get_or_create_group(conn, group_name)

    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id;",
            (name, email, birthday, group_id)
        )
        contact_id = cur.fetchone()[0]
        conn.commit()
        print(f"Контакт '{name}' добавлен.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
        cur.close()
        conn.close()
        return

    # добавляем номера телефонов
    while True:
        phone = input("Добавить телефон (Enter чтобы закончить): ").strip()
        if not phone:
            break
        phone_type = input("Тип (home / work / mobile): ").strip().lower()
        if phone_type not in ("home", "work", "mobile"):
            phone_type = "mobile"
        try:
            cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))
            conn.commit()
            print(f"Телефон {phone} добавлен.")
        except Exception as e:
            conn.rollback()
            print(f"Ошибка: {e}")

    cur.close()
    conn.close()


# ── поиск контактов ───────────────────────────────────────────

def search_contacts():
    print("\n-- Поиск --")
    print("1. По имени / email / телефону")
    print("2. По группе")
    choice = input("Выбор: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        query = input("Введи текст для поиска: ").strip()
        cur.execute("SELECT * FROM search_contacts(%s);", (query,))
        print_contacts(cur.fetchall())

    elif choice == "2":
        groups = get_groups()
        print("Группы:")
        for gid, gname in groups:
            print(f"  {gname}")
        group_name = input("Название группы: ").strip()

        print("Сортировка: 1=имя  2=день рождения  3=дата добавления")
        sort_choice = input("Выбор (Enter = по имени): ").strip()
        sort_col = {"2": "c.birthday", "3": "c.created_at"}.get(sort_choice, "c.name")

        cur.execute(
            f"""
            SELECT c.id, c.name, c.email, c.birthday, g.name, ph.phone, ph.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones ph ON ph.contact_id = c.id
            WHERE g.name ILIKE %s
            ORDER BY {sort_col};
            """,
            (group_name,)
        )
        print_contacts(cur.fetchall())

    cur.close()
    conn.close()
    input("\nEnter для продолжения...")


# ── постраничный просмотр ─────────────────────────────────────

def browse_contacts():
    page_size = 5
    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT c.id, c.name, c.email, c.birthday, g.name, ph.phone, ph.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones ph ON ph.contact_id = c.id
            ORDER BY c.name
            LIMIT %s OFFSET %s;
            """,
            (page_size, offset)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()

        os.system("cls" if os.name == "nt" else "clear")
        page = offset // page_size + 1
        print(f"\n-- Контакты (страница {page}) --")
        print_contacts(rows)
        print("\n[n] следующая  [p] предыдущая  [q] выход")
        cmd = input("> ").strip().lower()

        if cmd == "n":
            if len(rows) < page_size:
                print("Это последняя страница.")
                input("Enter...")
            else:
                offset += page_size
        elif cmd == "p":
            offset = max(0, offset - page_size)
        elif cmd == "q":
            break


# ── переместить контакт в группу ─────────────────────────────

def move_contact():
    print("\n-- Переместить в группу --")
    name = input("Имя контакта: ").strip()
    group = input("Новая группа: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s);", (name, group))
        conn.commit()
        print(f"'{name}' перемещён в группу '{group}'.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
    cur.close()
    conn.close()
    input("\nEnter для продолжения...")


# ── экспорт в JSON ────────────────────────────────────────────

def export_json():
    print("\n-- Экспорт в JSON --")
    filename = input("Имя файла (Enter = contacts_export.json): ").strip() or "contacts_export.json"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT c.id, c.name, c.email, c.birthday::text, g.name FROM contacts c LEFT JOIN groups g ON c.group_id = g.id ORDER BY c.name;"
    )
    contacts = cur.fetchall()

    result = []
    for cid, name, email, birthday, group in contacts:
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s;", (cid,))
        phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]
        result.append({
            "name": name,
            "email": email,
            "birthday": birthday,
            "group": group,
            "phones": phones
        })

    cur.close()
    conn.close()

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Экспортировано {len(result)} контактов в '{filename}'.")
    input("\nEnter для продолжения...")


# ── импорт из JSON ────────────────────────────────────────────

def import_json():
    print("\n-- Импорт из JSON --")
    filename = input("Имя файла (Enter = contacts_export.json): ").strip() or "contacts_export.json"

    if not os.path.exists(filename):
        print(f"Файл '{filename}' не найден.")
        input("\nEnter...")
        return

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = get_connection()
    inserted = skipped = overwritten = 0

    for item in data:
        name = (item.get("name") or "").strip()
        if not name:
            continue

        email    = item.get("email")
        birthday = item.get("birthday")
        group    = item.get("group") or "Other"
        phones   = item.get("phones", [])

        existing_id = get_contact_id(conn, name)

        if existing_id:
            print(f"'{name}' уже существует. [s] пропустить / [o] перезаписать")
            ans = input("> ").strip().lower()
            if ans == "o":
                group_id = get_or_create_group(conn, group)
                cur = conn.cursor()
                cur.execute(
                    "UPDATE contacts SET email=%s, birthday=%s, group_id=%s WHERE id=%s;",
                    (email, birthday, group_id, existing_id)
                )
                cur.execute("DELETE FROM phones WHERE contact_id=%s;", (existing_id,))
                for ph in phones:
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                        (existing_id, ph["phone"], ph.get("type", "mobile"))
                    )
                conn.commit()
                cur.close()
                overwritten += 1
            else:
                skipped += 1
        else:
            group_id = get_or_create_group(conn, group)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id;",
                (name, email, birthday, group_id)
            )
            new_id = cur.fetchone()[0]
            for ph in phones:
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                    (new_id, ph["phone"], ph.get("type", "mobile"))
                )
            conn.commit()
            cur.close()
            inserted += 1

    conn.close()
    print(f"Готово: добавлено {inserted}, перезаписано {overwritten}, пропущено {skipped}.")
    input("\nEnter для продолжения...")


# ── импорт из CSV ─────────────────────────────────────────────

def import_csv():
    print("\n-- Импорт из CSV --")
    filename = input("Имя файла (Enter = contacts.csv): ").strip() or "contacts.csv"

    if not os.path.exists(filename):
        print(f"Файл '{filename}' не найден.")
        input("\nEnter...")
        return

    conn = get_connection()
    inserted = skipped = errors = 0

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name      = (row.get("name") or "").strip()
            email     = (row.get("email") or "").strip() or None
            birthday  = (row.get("birthday") or "").strip() or None
            group     = (row.get("group") or "Other").strip()
            phone     = (row.get("phone") or "").strip() or None
            phone_type = (row.get("phone_type") or "mobile").strip().lower()

            if not name:
                errors += 1
                continue

            if get_contact_id(conn, name):
                print(f"'{name}' уже существует — пропускаем.")
                skipped += 1
                continue

            try:
                group_id = get_or_create_group(conn, group)
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id;",
                    (name, email, birthday, group_id)
                )
                cid = cur.fetchone()[0]
                if phone:
                    if phone_type not in ("home", "work", "mobile"):
                        phone_type = "mobile"
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                        (cid, phone, phone_type)
                    )
                conn.commit()
                cur.close()
                inserted += 1
            except Exception as e:
                conn.rollback()
                print(f"Ошибка на '{name}': {e}")
                errors += 1

    conn.close()
    print(f"Готово: добавлено {inserted}, пропущено {skipped}, ошибок {errors}.")
    input("\nEnter для продолжения...")


# ── главное меню ──────────────────────────────────────────────

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== PhoneBook ===")
        print("1. Добавить контакт")
        print("2. Поиск")
        print("3. Просмотр (по страницам)")
        print("4. Переместить в группу")
        print("5. Импорт из CSV")
        print("6. Импорт из JSON")
        print("7. Экспорт в JSON")
        print("0. Выход")

        choice = input("\nВыбор: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            search_contacts()
        elif choice == "3":
            browse_contacts()
        elif choice == "4":
            move_contact()
        elif choice == "5":
            import_csv()
        elif choice == "6":
            import_json()
        elif choice == "7":
            export_json()
        elif choice == "0":
            print("Пока!")
            break
        else:
            input("Неверный выбор. Enter...")


main()