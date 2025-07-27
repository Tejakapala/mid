import streamlit as st
import pymysql
import re

# ✅ Replace with your actual MySQL credentials
conn = pymysql.connect(
    host="localhost",            # ✅ localhost since you're using MySQL Workbench locally
    user="root",                 # ✅ your MySQL username (default is usually 'root')
    password="moTher@123",   # 🔁 replace with your actual password
    database="mid_marks"        # ✅ this is the database you created as per your screenshot
)

cursor = conn.cursor()

st.title("📘 Mid Marks Entry Form (MySQL)")

with st.form("marks_form"):
    id = st.text_input("ID (e.g., N220123)")
    name = st.text_input("Name")
    roll = st.text_input("Roll Number")

    st.markdown("### 📚 Enter Mid Marks")
    daa = st.number_input("DAA", min_value=0, max_value=100)
    dld = st.number_input("DLD", min_value=0, max_value=100)
    flat = st.number_input("FLAT", min_value=0, max_value=100)
    dbms = st.number_input("DBMS", min_value=0, max_value=100)
    ps = st.number_input("P&S", min_value=0, max_value=100)

    submitted = st.form_submit_button("Submit")

    if submitted:
        if not re.match(r'^N220\d{3}$', id):
            st.error("❌ ID must start with N220 followed by 3 digits (e.g., N220123)")
        elif name.strip() == "" or roll.strip() == "":
            st.error("❌ Name and Roll Number cannot be empty")
        elif 0 in [daa, dld, flat, dbms, ps]:
            st.error("❌ All subject marks must be greater than 0")
        else:
            try:
                # ✅ Insert into MySQL
                cursor.execute('''
                    INSERT INTO mid_marks (id, name, roll_no, daa, dld, flat, dbms, ps)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (id, name, roll, daa, dld, flat, dbms, ps))
                conn.commit()
                st.success("✅ Marks submitted successfully!")

                # ✅ Display current table
                cursor.execute("SELECT * FROM mid_marks")
                rows = cursor.fetchall()
                st.subheader("📄 Stored Records")
                st.dataframe(rows)

            except mysql.connector.Error as e:
                st.error(f"❌ Error inserting data: {e}")