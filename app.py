import streamlit as st
from supabase import create_client
import re
import pandas as pd

# ✅ Supabase credentials (replace with your real project values)
SUPABASE_URL = "https://lsxzkmydgkfopkfnurhn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxzeHprbXlkZ2tmb3BrZm51cmhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM2MTc1MTMsImV4cCI6MjA2OTE5MzUxM30.9667x3VLGw799MrNPLVcAQ5FxZiAvQh0ulcuPdJNU4g"

# ✅ Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📘 Mid Marks Entry Form (Supabase)")

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
                # ✅ Insert data into Supabase table
               result = supabase.table("mid_marks").insert({
                    "id": id,
                    "name": name,
                    "roll_no": roll,
                    "daa": daa,
                    "dld": dld,
                    "flat": flat,
                    "dbms": dbms,
                    "ps": ps
                }).execute()
               

               if result.data and isinstance(result.data, list):
                    # print("result:\n\n",result)
                    # print('resukt[0]\n\n',result[0])
                    # print('dict instance\n\n\n:',isinstance(result, dict))
                    # print('list instance\n\n:',isinstance(result, list))
                    st.success("✅ Data submitted successfully!")
               else:
                    st.warning("⚠ Data submitted, but no confirmation received.")

            except Exception as e:
                st.error(f"❌ Error inserting data: {e}")

            # ✅ Show all records
            try:
                records = supabase.table("mid_marks").select("*").execute()
                print(records)
                if isinstance(records.data, list):
                    st.subheader("📄 All Mid Marks Records")
                    df=pd.DataFrame(records.data)
                    st.dataframe(df)
      
                else:
                    st.warning("⚠ Could not fetch records.")
            except Exception as e:
                st.error(f"❌ Error fetching records: {e}")