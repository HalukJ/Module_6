#Game Pass
import streamlit as st
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="GamePass Management", layout="wide")
st.title("🎮 GamePass Management App")

# --- Initialize session state ---
if "account_created" not in st.session_state:
    st.session_state.account_created = False
if "package_selected" not in st.session_state:
    st.session_state.package_selected = False
if "df_users" not in st.session_state:
    st.session_state.df_users = pd.DataFrame()
if "simulation_done" not in st.session_state:
    st.session_state.simulation_done = False  # To simulate users only once

# --- Step 1: Account Creation ---
with st.expander("Step 1: Create Account", expanded=True):
    with st.form("account_form"):
        name = st.text_input("👤 Name")
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        payment_method = st.selectbox("💳 Payment Method", ["Credit Card", "PayPal", "Crypto"])
        submit = st.form_submit_button("Create Account")

    if submit:
        errors = []
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Invalid email format.")
        if len(password) < 6 or not any(char.isdigit() for char in password):
            errors.append("Password must be at least 6 characters and include a number.")

        # Simulate payment (10% chance failure)
        payment_success = np.random.choice([True, False], p=[0.9, 0.1])
        if not payment_success:
            errors.append("Payment failed. Please try again.")

        if errors:
            st.error("❌ Account creation failed:")
            for err in errors:
                st.write(f"- {err}")
        else:
            st.session_state.update({
                "name": name,
                "email": email,
                "payment_method": payment_method,
                "account_created": True
            })
            st.success("✅ Account created! Proceed to package selection below.")

# --- Step 2: Package Selection ---
if st.session_state.account_created:
    with st.expander("Step 2: Select Package", expanded=True):
        packages = {"Essential": 9.99, "Premium": 14.99, "Ultimate": 29.99}
        selected_package = st.radio("Select a package:", list(packages.keys()))
        subscribe = st.button("Subscribe")
        if subscribe:
            payment_success = np.random.choice([True, False], p=[0.9, 0.1])

            new_user = pd.DataFrame([{
                "UserID": f"{st.session_state['name'].lower().replace(' ', '_')}_001",
                "Name": st.session_state["name"],
                "Email": st.session_state["email"],
                "Package": selected_package,
                "PaymentMethod": st.session_state["payment_method"],
                "HoursPlayed": np.random.poisson(lam=25),
                "Paid": payment_success
            }])

            st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
            st.session_state.package_selected = True
            st.session_state.selected_package = selected_package
            st.success(f"🎉 {selected_package} package subscribed successfully!")

# --- Step 3: Boss Report / Simulation ---
if st.session_state.package_selected:
    with st.expander("Step 3: Boss Report / Simulation", expanded=True):
        packages = {"Essential": 9.99, "Premium": 14.99, "Ultimate": 29.99}

        # Simulate 1000 users only once
        if not st.session_state.simulation_done:
            np.random.seed(42)
            user_ids = [f"User_{i+1}" for i in range(1000)]
            package_probs = [0.5, 0.4, 0.1]
            assigned_packages = np.random.choice(list(packages.keys()), size=1000, p=package_probs)
            hours_played = np.random.poisson(lam=25, size=1000)
            payment_failed = np.random.choice([True, False], size=1000, p=[0.05, 0.95])

            simulated_users = pd.DataFrame({
                "UserID": user_ids,
                "Name": [f"SimUser_{i+1}" for i in range(1000)],
                "Email": [f"simuser{i+1}@example.com" for i in range(1000)],
                "Package": assigned_packages,
                "PaymentMethod": ["Credit Card"]*1000,
                "HoursPlayed": hours_played,
                "Paid": ~payment_failed
            })

            st.session_state.df_users = pd.concat([st.session_state.df_users, simulated_users], ignore_index=True)
            st.session_state.simulation_done = True

        df_users = st.session_state.df_users.copy()

        # Revenue calculations
        df_users["BasePrice"] = df_users["Package"].map(packages)
        df_users["FlatRevenue"] = df_users["BasePrice"]
        df_users["TieredRevenue"] = df_users["HoursPlayed"].apply(lambda h: 10 if h < 20 else 15 if h <= 50 else 20)
        df_users["PPURevenue"] = df_users["HoursPlayed"] * 0.5
        df_users["FinalFlatRevenue"] = np.where(df_users["Paid"], df_users["FlatRevenue"], 0)
        df_users["FinalTieredRevenue"] = np.where(df_users["Paid"], df_users["TieredRevenue"], 0)
        df_users["FinalPPURevenue"] = np.where(df_users["Paid"], df_users["PPURevenue"], 0)

        st.subheader("📊 Subscribers (Including Simulated 1000 Users)")
        st.dataframe(df_users)

        st.subheader("📈 Summary Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Users", len(df_users))
        col2.metric("Payment Failures", len(df_users[df_users["FinalFlatRevenue"] == 0]))
        col3.metric("Total Revenue (Flat)", f"${df_users['FinalFlatRevenue'].sum():,.2f}")
        col4.metric("Total Revenue (Tiered)", f"${df_users['FinalTieredRevenue'].sum():,.2f}")
        col5.metric("Total Revenue (PPU)", f"${df_users['FinalPPURevenue'].sum():,.2f}")

# --- Step 4: Z-Raport Dashboard ---
if st.session_state.package_selected:
    with st.expander("Step 4: Z-Raport Dashboard", expanded=True):
        df_users = st.session_state.df_users.copy()

        # Ensure revenues exist
        packages = {"Essential": 9.99, "Premium": 14.99, "Ultimate": 29.99}
        df_users["BasePrice"] = df_users["Package"].map(packages)
        df_users["FlatRevenue"] = df_users["BasePrice"]
        df_users["TieredRevenue"] = df_users["HoursPlayed"].apply(lambda h: 10 if h < 20 else 15 if h <= 50 else 20)
        df_users["PPURevenue"] = df_users["HoursPlayed"] * 0.5
        df_users["FinalFlatRevenue"] = np.where(df_users["Paid"], df_users["FlatRevenue"], 0)
        df_users["FinalTieredRevenue"] = np.where(df_users["Paid"], df_users["TieredRevenue"], 0)
        df_users["FinalPPURevenue"] = np.where(df_users["Paid"], df_users["PPURevenue"], 0)

        # Package distribution pie chart
        st.subheader("📊 Package Distribution")
        package_counts = df_users["Package"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(package_counts, labels=package_counts.index, autopct="%1.1f%%", startangle=90)
        ax.set_title("Package Share Among Users")
        st.pyplot(fig)

        # Z-Raport summary
        failures = len(df_users[df_users["FinalFlatRevenue"] == 0])
        z_report = pd.DataFrame({
            "Model": ["Flat", "Tiered", "Pay-Per-Use"],
            "Revenue": [
                df_users["FinalFlatRevenue"].sum(),
                df_users["FinalTieredRevenue"].sum(),
                df_users["FinalPPURevenue"].sum()
            ],
            "PaymentFailures": [failures] * 3
        })

        st.subheader("📄 Z-Raport Summary")
        st.dataframe(z_report)

        # --- Export CSVs ---
        subscriptions_csv = df_users.to_csv(index=False).encode("utf-8")
        st.download_button("Download Full Subscriptions CSV", subscriptions_csv, "subscriptions.csv", "text/csv")

        z_report_csv = z_report.to_csv(index=False).encode("utf-8")
        st.download_button("Download Z-Raport CSV", z_report_csv, "z_report.csv", "text/csv")
