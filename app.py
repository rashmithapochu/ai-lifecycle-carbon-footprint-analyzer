import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import base64
import platform
from datetime import datetime, date   # ✔ FIX ADDED

# ----------------------------------------------------------
# ✅ PAGE CONFIGURATION
# ----------------------------------------------------------
st.set_page_config(
    page_title="🌿 AI Lifecycle Carbon Footprint Dashboard",
    layout="wide",
    page_icon="🌍"
)

# ----------------------------------------------------------
# 🔐 USER DATABASE
# ----------------------------------------------------------
if "user_db" not in st.session_state:
    st.session_state.user_db = {"rashmitha": "password123", "admin": "admin123"}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ----------------------------------------------------------
# 🎨 LOGIN PAGE STYLING
# ----------------------------------------------------------
login_css = """
<style>
    .login-box {
        background-color: #f9f9f9;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: auto;
    }
    .login-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
</style>
"""
st.markdown(login_css, unsafe_allow_html=True)


# ----------------------------------------------------------
# 🔐 SIGN IN FORM
# ----------------------------------------------------------
def sign_in():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Login to Dashboard</div>', unsafe_allow_html=True)
    username = st.text_input("👤 Username", key="signin_username")
    password = st.text_input("🔑 Password", type="password", key="signin_password")
    
    if st.button("Login", key="login_btn"):
        if username in st.session_state.user_db and st.session_state.user_db[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.nav = "🏠 Home"
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")
    
    # 👉 Forget Password option
    if st.button("Forgot Password?", key="forgot_btn"):
        st.session_state.show_reset = True
    
    # 👉 Show reset form if triggered
    if st.session_state.get("show_reset", False):
        new_password = st.text_input("🔑 New Password", type="password", key="reset_new")
        confirm_password = st.text_input("🔁 Confirm Password", type="password", key="reset_confirm")
        if st.button("Update Password", key="reset_update"):
            if new_password == confirm_password and len(new_password) >= 4:
                st.session_state.user_db[username] = new_password
                st.success("✅ Password updated successfully! Please login again.")
                st.session_state.show_reset = False
            else:
                st.error("❌ Passwords do not match or too short.")
    
    st.markdown('</div>', unsafe_allow_html=True)



# ----------------------------------------------------------
# 🔐 SIGN UP FORM
# ----------------------------------------------------------
def sign_up():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🆕 Create Account</div>', unsafe_allow_html=True)
    new_username = st.text_input("👤 Choose a Username", key="signup_username")
    new_password = st.text_input("🔑 Choose a Password", type="password", key="signup_password")
    confirm_password = st.text_input("🔁 Confirm Password", type="password", key="signup_confirm")
    if st.button("Register", key="signup_btn"):
        if new_username in st.session_state.user_db:
            st.error("⚠️ Username already exists.")
        elif new_password != confirm_password:
            st.error("❌ Passwords do not match.")
        elif len(new_username) < 3 or len(new_password) < 4:
            st.warning("⚠️ Username must be ≥ 3 chars, password ≥ 4 chars.")
        else:
            st.session_state.user_db[new_username] = new_password
            st.success("✅ Account created! You can now sign in.")
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------------------------------------
# 🚀 AUTH
# ----------------------------------------------------------
auth_mode = st.sidebar.radio("🔐 Authentication Mode", ["Sign In", "Sign Up"])

if not st.session_state.authenticated:
    if auth_mode == "Sign In":
        sign_in()
    else:
        sign_up()
    st.stop()
else:
    st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.update({"authenticated": False}))

# ----------------------------------------------------------
# 🎨 THEME MODE
# ----------------------------------------------------------
theme = st.sidebar.selectbox("🎨 Theme Mode:", ["Light", "Dark"], key="theme_select")
if theme == "Dark":
    st.markdown("""
        <style>
        body { background-color:#111; color:#eee; }
        .stApp { background-color:#111; color:#eee; }
        </style>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------
# 💡 DAILY TIP
# ----------------------------------------------------------
tips = [
    "💧 Unplug chargers after use to save up to 10% power.",
    "🌞 Solar charging can reduce your carbon footprint by 80%.",
    "🖥️ Lower your screen brightness — it cuts energy instantly!",
    "♻️ Recycle your old devices responsibly.",
    "🌿 Switching to renewable energy reduces 90% of CO₂ emissions."
]
st.sidebar.info("💡 **Tip of the Day:**\n" + random.choice(tips))


# ----------------------------------------------------------
# 📂 SIDEBAR NAVIGATION
# ----------------------------------------------------------
nav = st.sidebar.radio("📂 Navigation", [
    "🏠 Home",
    "📱 Device Carbon Estimation",
    "🤖 AI Model Lifecycle Analysis",
    "🌍 Lifestyle Footprint",   # merged section
    "👤 Profile"
])

# ----------------------------------------------------------
# ❄ SEASONAL ANIMATION ON HOME ONLY
# ----------------------------------------------------------
def seasonal_animation():
    month = datetime.now().month

    if month in [12, 1]:      # Snow season
        animation_url = "https://i.gifer.com/Yg7R.gif"
    elif month in [8, 9, 10]:  # Falling leaves
        animation_url = "https://i.gifer.com/7VE.gif"
    else:                    # Eco floating particles
        animation_url = "https://i.gifer.com/76YS.gif"

    st.markdown(f"""
        <style>
        .stApp {{
            background: url('{animation_url}') center/cover fixed no-repeat;
        }}
        </style>
    """, unsafe_allow_html=True)




# ==========================================================
# 🏠 HOME PAGE
# ==========================================================
if nav == "🏠 Home":
    seasonal_animation()
    st.markdown("""
        <div style="background-color:#000000; padding:40px; border-radius:12px; text-align:center; box-shadow: 0 0 20px #00ff99;">
            <h1 style="color:#00ff99; font-size:40px; font-weight:bold; margin-bottom:10px;">
                🌍 Welcome to the <span style="color:#ffffff;">AI Carbon Footprint Dashboard</span>
            </h1>
            <p style="color:#cccccc; font-size:22px;">
                Analyze and reduce <span style="color:#00ff99;">CO₂ emissions</span> from devices & AI models
            </p>
            <p style="color:#00ff99; font-size:18px; margin-top:30px;">
                Use the sidebar to begin your analysis.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.image("https://advertisingweek.com/wp-content/uploads/2023/01/carbon-neutral-and-esg-concepts-carbon-emission-clean-energy-globe-balancing-between-a-green.jpg_s1024x1024wisk20cUZjMAOHpGtWFVw7D3JgEpa2RWgw4gL0OQFSV2AkPD1c.jpg",
             use_container_width=True)

    st.success("Use the sidebar to begin your analysis.")


# ==========================================================
# 👤 PROFILE SECTION
# ==========================================================
elif nav == "👤 Profile":
    from datetime import date

    # Initialize states
    if "profile_image" not in st.session_state:
        st.session_state.profile_image = None
    if "image_mode" not in st.session_state:
        st.session_state.image_mode = "menu"
    if "show_image_menu" not in st.session_state:
        st.session_state.show_image_menu = False
    if "profile_data" not in st.session_state:
        st.session_state.profile_data = {
            "first_name": "",
            "last_name": "",
            "gender": "Female",
            "birth_date": date(2000, 1, 1)
        }

    st.markdown("""
        <style>
        .profile-frame { position: relative; width: 160px; height: 160px; margin: auto; border-radius: 50%; overflow: hidden; border: 4px solid #2ecc71; }
        .profile-frame img { width: 100%; height: 100%; object-fit: cover; }
        .profile-header { text-align: center; font-size: 1.6rem; font-weight: bold; margin-bottom: 1rem; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="profile-header">👤 Edit Profile</div>', unsafe_allow_html=True)

    # Display profile image with toggle pencil
    if st.session_state.profile_image:
        image_bytes = st.session_state.profile_image.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode()
        st.markdown(f"""
            <div class="profile-frame">
                <img src="data:image/png;base64,{image_base64}">
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="profile-frame">
            <img src="https://cdn-icons-png.flaticon.com/512/149/149071.png">
        </div>
        """, unsafe_allow_html=True)

    # Image edit menu
    if st.button("✏️", help="Edit Photo", key="edit_photo_btn"):
        st.session_state.show_image_menu = not st.session_state.show_image_menu

    if st.session_state.show_image_menu:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📤 Upload New Photo", key="upload_menu_btn"):
                st.session_state.image_mode = "upload"
                st.session_state.show_image_menu = False
        with col2:
            if st.button("👁️ View Photo", key="view_menu_btn") and st.session_state.profile_image:
                st.session_state.image_mode = "view"
                st.session_state.show_image_menu = False
        with col3:
            if st.button("🗑️ Remove Photo", key="remove_menu_btn"):
                st.session_state.profile_image = None
                st.session_state.show_image_menu = False
                st.success("✅ Photo removed.")

    # View / Upload
    if st.session_state.image_mode == "upload":
        uploaded = st.file_uploader("Choose an image", type=["png","jpg","jpeg"], key="file_upload")
        if uploaded:
            st.image(uploaded, caption="Crop Preview", use_container_width=True)
            if st.button("Save", key="save_upload"):
                st.session_state.profile_image = uploaded
                st.session_state.image_mode = "menu"
            if st.button("Cancel", key="cancel_upload"):
                st.session_state.image_mode = "menu"

    elif st.session_state.image_mode == "view":
        st.image(st.session_state.profile_image, caption="Your Profile Photo", use_container_width=True)
        if st.button("Back", key="back_view_btn"):
            st.session_state.image_mode = "menu"

    # Profile details with saved defaults
    st.session_state.profile_data["first_name"] = st.text_input(
        "First Name",
        value=st.session_state.profile_data["first_name"],
        key="first_name_input"
    )
    st.session_state.profile_data["last_name"] = st.text_input(
        "Last Name",
        value=st.session_state.profile_data["last_name"],
        key="last_name_input"
    )
    st.selectbox(
        "Gender",
        ["Female","Male","Other"],
        index=["Female","Male","Other"].index(st.session_state.profile_data["gender"]),
        key="gender_select"
    )
    st.session_state.profile_data["gender"] = st.session_state["gender_select"]
    st.session_state.profile_data["birth_date"] = st.date_input(
        "Birth Date",
        value=st.session_state.profile_data["birth_date"],
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        key="birth_date_input"
    )

    # Save button
    if st.button("💾 Save Profile", key="save_profile_btn"):
        st.success("✅ Profile updated successfully!")

    if st.button("🔙 Back to Home", key="back_home_btn"):
        st.session_state.nav = "🏠 Home"
        st.rerun()



# ==========================================================
# 🌱 HELPER FUNCTION — ECO SCORE
# ==========================================================
def eco_score(emission):
    if emission < 50:
        return 95, "🌟 Excellent! Ultra-low footprint."
    elif emission < 200:
        return 80, "✅ Good! Moderate sustainability."
    elif emission < 500:
        return 60, "⚠️ Can be improved — consider optimizations."
    else:
        return 30, "🚨 High footprint! Take action soon."

# ----------------------------------------------------------
# Emission Factors
# ----------------------------------------------------------
emission_factors = {
    "Solar ☀️": 0.02, "Wind 🌬️": 0.01, "Hydro 💧": 0.08, "Geothermal 🌋": 0.06, "Biomass 🌱": 0.12,
    "Coal 🪨": 0.70, "Oil ⛽": 0.65, "Natural Gas 🔥": 0.50, "Nuclear ⚡": 0.10
}

renewable_sources = ["Solar ☀️","Wind 🌬️","Hydro 💧","Geothermal 🌋","Biomass 🌱"]
nonrenewable_sources = ["Coal 🪨","Oil ⛽","Natural Gas 🔥","Nuclear ⚡"]

renewable_avg = sum([emission_factors[s] for s in renewable_sources])/len(renewable_sources)
nonrenewable_avg = sum([emission_factors[s] for s in nonrenewable_sources])/len(nonrenewable_sources)

# ----------------------------------------------------------
# 🌍 Standardized Lifestyle Emission Factors (EPA/IPCC style)
# ----------------------------------------------------------
standard_factors = {
    "Electricity (kWh)": 0.82,       # India avg ~0.82 kg CO₂/kWh
    "Gasoline (litre)": 2.31,        # kg CO₂ per litre
    "Diesel (litre)": 2.68,          # kg CO₂ per litre
    "Flight (km)": 0.115,            # kg CO₂ per km
    "Food (kg meat)": 27.0,          # kg CO₂ per kg beef
    "Food (kg vegetables)": 2.0,     # kg CO₂ per kg vegetables
    "Waste (kg)": 1.9                # kg CO₂ per kg municipal waste
}

# ==========================================================
# 📱 DEVICE CARBON ESTIMATION
# ==========================================================
if nav == "📱 Device Carbon Estimation":
    st.header("📱 Device Carbon Estimation")

    col1, col2 = st.columns(2)
    with col1:
        device = st.selectbox("Device Type", ["Android Phone", "iPhone", "Laptop"], key="device_select")
        power = st.number_input("Power (Watts):", min_value=1, value=15, step=1, key="power_input")
        hours = st.number_input("Usage per Day (Hours):", min_value=0.0, value=5.0, step=0.5, key="hours_input")
    with col2:
        days = st.slider("Days used per year:", 1, 365, 300, key="days_slider")
        energy_category = st.radio("Energy Category:", ["Renewable", "Non-renewable"], key="energy_radio")
        if energy_category == "Renewable":
            energy_source = st.selectbox(
                "Select Renewable Source:",
                renewable_sources + ["Above All 🌍"],
                key="energy_source_renew"
            )
        else:
            energy_source = st.selectbox(
                "Select Non-renewable Source:",
                nonrenewable_sources + ["Above All 🌍"],
                key="energy_source_nonrenew"
            )
        cost_per_kwh = st.number_input("Electricity Cost (₹/kWh):", min_value=1.0, value=6.5, key="cost_input")

    # Assign emission factor
    if energy_source=="Above All 🌍":
        emission_factor = renewable_avg if energy_category=="Renewable" else nonrenewable_avg
    else:
        emission_factor = emission_factors.get(energy_source, 0.5)

    energy_kwh = (power * hours * days)/1000
    carbon_emission = energy_kwh * emission_factor
    annual_cost = energy_kwh * cost_per_kwh

    score, msg = eco_score(carbon_emission)
    st.subheader(f"🌱 Eco Score: {score}/100")
    st.info(msg)

    # ========================
    # 🌳 Carbon Offset Calculator
    # ========================
    st.subheader("🌳 Carbon Offset Calculator")
    emission_value = carbon_emission
    trees_needed = emission_value / 21
    credits_needed = emission_value / 1000
    st.write(f"🌲 Trees needed to offset: **{trees_needed:.1f}**")
    st.write(f"💵 Carbon credits needed: **{credits_needed:.2f}**")

    # ========================
    # 🎯 Gamified Eco Challenges
    # ========================
    st.subheader("🎯 Weekly Eco Challenge")
    if emission_value < 200:
        st.success("🏅 Badge Earned: Eco Saver — Keep your footprint ultra-low this week!")
    elif emission_value < 500:
        st.info("🎖️ Challenge: Reduce your usage by 10% to earn the Green Optimizer badge.")
    else:
        st.warning("🔥 Challenge: Cut your footprint by 20% this week to unlock the Carbon Warrior badge.")

    # ========================
    # 📊 Results & Charts (Collapsible)
    # ========================
    with st.expander("📊 Results & Charts"):
        st.metric("Energy Used (kWh/year)", f"{energy_kwh:.2f}")
        st.metric("Carbon Footprint (kg CO₂/year)", f"{carbon_emission:.2f}")
        st.metric("Annual Energy Cost (₹)", f"{annual_cost:.2f}")

        # Device Comparison Bar Chart
        data = {
            "Device": ["Android Phone", "iPhone", "Laptop"],
            "Power (W)": [15, 18, 60],
            "Usage (hrs/day)": [5, 4, 8]
        }
        df = pd.DataFrame(data)
        df["Energy (kWh/Year)"] = (df["Power (W)"] * df["Usage (hrs/day)"] * days)/1000
        df["Carbon (kg CO₂/Year)"] = df["Energy (kWh/Year)"] * emission_factor
        fig, ax = plt.subplots()
        ax.bar(df["Device"], df["Carbon (kg CO₂/Year)"], color=["green","blue","orange"])
        ax.set_ylabel("CO₂ Emission (kg/year)")
        ax.set_title("Carbon Footprint Comparison by Device")
        st.pyplot(fig)

        # Device vs Global Average
        global_avg = 400
        compare_df = pd.DataFrame({
            "Category": ["Your Device","Global Average"],
            "Carbon (kg CO₂/year)":[carbon_emission, global_avg]
        })
        fig2, ax2 = plt.subplots()
        ax2.bar(compare_df["Category"], compare_df["Carbon (kg CO₂/year)"], color=["#27ae60","#e74c3c"])
        ax2.set_ylabel("CO₂ Emission (kg/year)")
        ax2.set_title("Your Device vs Global Average Emissions")
        st.pyplot(fig2)

        # Additional Pie Chart: Renewable vs Non-renewable
        if energy_source=="Above All 🌍":
            fig3, ax3 = plt.subplots()
            ax3.pie([renewable_avg, nonrenewable_avg], labels=["Renewable (Above All)","Non-renewable (Above All)"],
                    autopct="%1.1f%%", startangle=90, colors=["#2ecc71","#e74c3c"])
            ax3.axis("equal")
            st.subheader("🔄 Renewable vs Non-renewable (Above All)")
            st.pyplot(fig3)


# ==========================================================
# 🤖 AI MODEL LIFECYCLE ANALYSIS
# ==========================================================
elif nav == "🤖 AI Model Lifecycle Analysis":
    st.header("🤖 AI Model Lifecycle Carbon Footprint Analysis")

    col1, col2 = st.columns(2)
    with col1:
        gpu_power = st.number_input("GPU Power (Watts):", min_value=50, value=250, step=5, key="gpu_power_input")
        training_hours = st.number_input("Training Hours:", min_value=1, value=10, step=1, key="training_hours_input")
        num_gpus = st.number_input("Number of GPUs:", min_value=1, value=1, step=1, key="num_gpus_input")
    with col2:
        inference_hours = st.number_input("Daily Inference Hours:", min_value=0.0, value=5.0, step=0.5, key="inference_hours_input")
        inference_days = st.slider("Days per Year:",1,365,300,key="inference_days_slider")
        ai_energy_category = st.radio("Energy Category:", ["Renewable","Non-renewable"], key="ai_energy_radio")
        if ai_energy_category=="Renewable":
            ai_energy_source = st.selectbox("Select Renewable Source:", renewable_sources+["Above All 🌍"], key="ai_energy_source_renew")
        else:
            ai_energy_source = st.selectbox("Select Non-renewable Source:", nonrenewable_sources+["Above All 🌍"], key="ai_energy_source_nonrenew")
        cost_per_kwh_ai = st.number_input("Electricity Cost (₹/kWh):", min_value=1.0, value=6.5, key="ai_cost_input")

    # Emission factor
    if ai_energy_source=="Above All 🌍":
        emission_factor_ai = renewable_avg if ai_energy_category=="Renewable" else nonrenewable_avg
    else:
        emission_factor_ai = emission_factors.get(ai_energy_source,0.5)

    train_energy = (gpu_power*num_gpus*training_hours)/1000
    inference_energy = (gpu_power*num_gpus*inference_hours*inference_days)/1000
    total_energy = train_energy + inference_energy
    total_carbon = total_energy * emission_factor_ai
    total_cost = total_energy * cost_per_kwh_ai

    score_ai, msg_ai = eco_score(total_carbon)
    st.subheader(f"🌱 Eco Score: {score_ai}/100")
    st.info(msg_ai)

    # ========================
    # 🌳 Carbon Offset Calculator
    # ========================
    st.subheader("🌳 Carbon Offset Calculator")
    emission_value = total_carbon
    trees_needed = emission_value / 21
    credits_needed = emission_value / 1000
    st.write(f"🌲 Trees needed to offset: **{trees_needed:.1f}**")
    st.write(f"💵 Carbon credits needed: **{credits_needed:.2f}**")

    # ========================
    # 🎯 Gamified Eco Challenges
    # ========================
    st.subheader("🎯 Weekly Eco Challenge")
    if emission_value < 200:
        st.success("🏅 Badge Earned: Eco Saver — Keep your footprint ultra-low this week!")
    elif emission_value < 500:
        st.info("🎖️ Challenge: Reduce your usage by 10% to earn the Green Optimizer badge.")
    else:
        st.warning("🔥 Challenge: Cut your footprint by 20% this week to unlock the Carbon Warrior badge.")

    # ========================
    # 📊 Results & Charts (Collapsible)
    # ========================
    with st.expander("📊 Results & Charts"):
        st.metric("Training Energy (kWh)", f"{train_energy:.2f}")
        st.metric("Inference Energy (kWh)", f"{inference_energy:.2f}")
        st.metric("Total Carbon (kg CO₂)", f"{total_carbon:.2f}")
        st.metric("Electricity Cost (₹)", f"{total_cost:.2f}")

        # AI Lifecycle Pie Chart
        fig, ax = plt.subplots()
        stages = ["Training","Inference"]
        emissions = [train_energy*emission_factor_ai, inference_energy*emission_factor_ai]
        ax.pie(emissions, labels=stages, autopct="%1.1f%%", startangle=90, colors=["#4CAF50","#2196F3"])
        ax.axis("equal")
        st.pyplot(fig)

        # Bar Chart: AI vs Global Average
        global_avg_ai = 500
        compare_df = pd.DataFrame({
            "Category":["Your Model","Global AI Avg"],
            "Carbon (kg CO₂/year)":[total_carbon, global_avg_ai]
        })
        fig2, ax2 = plt.subplots()
        ax2.bar(compare_df["Category"], compare_df["Carbon (kg CO₂/year)"], color=["#16a085","#e74c3c"])
        ax2.set_title("AI Model vs Global AI Average")
        st.pyplot(fig2)

        # Additional Pie Chart: Renewable vs Non-renewable
        if ai_energy_source=="Above All 🌍":
            fig3, ax3 = plt.subplots()
            ax3.pie([renewable_avg, nonrenewable_avg], labels=["Renewable (Above All)","Non-renewable (Above All)"],
                    autopct="%1.1f%%", startangle=90, colors=["#2ecc71","#e74c3c"])
            ax3.axis("equal")
            st.subheader("🔄 Renewable vs Non-renewable (Above All)")
            st.pyplot(fig3)

    # ========================
    # 🤖 AI Assistant Panel
    # ========================
    st.sidebar.subheader("🤖 AI Assistant")
    user_question = st.sidebar.text_input("Ask about your results:", key="ai_assistant_input")
    if user_question:
        if "reduce" in user_question.lower():
            st.sidebar.info("💡 Try switching to renewable sources or lowering daily usage hours.")
        elif "offset" in user_question.lower():
            st.sidebar.info("🌳 Plant trees or buy carbon credits to offset your footprint.")
        else:
            st.sidebar.info("📘 I can help explain emissions, offsets, and eco tips — try asking about 'renewables'.")
# ==========================================================
# 🌍 Lifestyle Footprint
# ==========================================================
elif nav == "🌍 Lifestyle Footprint":
    st.header("🌍 Lifestyle Carbon Footprint")

    # 🚗 Transport
    st.subheader("🚗 Transport")
    km = st.number_input("Kilometers driven per year", min_value=0, value=12000)
    fuel = st.selectbox("Fuel Type", ["Gasoline", "Diesel"])
    transport_emission = km * (standard_factors["Gasoline (litre)"] if fuel=="Gasoline" else standard_factors["Diesel (litre)"])

    # 🍽️ Food
    st.subheader("🍽️ Food")
    meat = st.number_input("Meat consumption (kg/year)", min_value=0, value=50)
    veg = st.number_input("Vegetable consumption (kg/year)", min_value=0, value=200)
    food_emission = meat*standard_factors["Food (kg meat)"] + veg*standard_factors["Food (kg vegetables)"]

    # 🗑️ Waste
    st.subheader("🗑️ Waste")
    waste = st.number_input("Waste generated (kg/year)", min_value=0, value=500)
    waste_emission = waste * standard_factors["Waste (kg)"]

    # 🏠 Household Energy
    st.subheader("🏠 Household Energy")
    kwh = st.number_input("Electricity used (kWh/year)", min_value=0, value=3000)
    energy_emission = kwh * standard_factors["Electricity (kWh)"]

    # 🌍 Total Lifestyle Footprint
    total_lifestyle = transport_emission + food_emission + waste_emission + energy_emission
    st.metric("Total Lifestyle Footprint (kg CO₂/year)", f"{total_lifestyle:.2f}")

    # Personalized Recommendations
    if transport_emission > 2000:
        st.info("💡 Consider carpooling or switching to public transport.")
    if meat > 100:
        st.info("💡 Reduce red meat intake to cut food emissions.")
    if waste > 1000:
        st.info("♻️ Try composting or recycling to reduce waste emissions.")
    if kwh > 5000:
        st.info("💡 Switch to LED bulbs and energy-efficient appliances.")

    # Benchmark Comparison
    compare_df = pd.DataFrame({
        "Category": ["Your Lifestyle", "India Avg", "Global Avg"],
        "Carbon (tons CO₂/year)": [total_lifestyle/1000, 1.9, 4.7]
    })
    st.bar_chart(compare_df.set_index("Category"))

    # Export Report
    report = f"Total Lifestyle Footprint: {total_lifestyle:.2f} kg CO₂/year"
    st.download_button("📥 Download Lifestyle Report", report, file_name="lifestyle_report.txt")

    # Net Zero Progress
    target = 1000  # kg CO₂/year
    progress = max(0, 1 - (total_lifestyle/target))
    st.progress(progress)
    st.write(f"🎯 Progress toward Net Zero: {progress*100:.1f}%")
