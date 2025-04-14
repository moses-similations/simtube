import random
import time
import sqlite3
import streamlit as st

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("simtube.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS channel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            niche TEXT,
            subscribers INTEGER DEFAULT 0,
            watch_hours REAL DEFAULT 0,
            verified INTEGER DEFAULT 0,
            live_stream_active INTEGER DEFAULT 0,
            live_stream_views INTEGER DEFAULT 0,
            video_likes INTEGER DEFAULT 0,
            video_dislikes INTEGER DEFAULT 0,
            video_quality INTEGER DEFAULT 0 -- Add quality metric
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS wallet (
            id INTEGER PRIMARY KEY,
            usd REAL DEFAULT 0,
            rwf REAL DEFAULT 0
        )
    ''')
    cur.execute("INSERT OR IGNORE INTO wallet (id, usd, rwf) VALUES (1, 0, 0)")
    conn.commit()
    conn.close()

def create_channel(name, niche):
    conn = sqlite3.connect("simtube.db")
    cur = conn.cursor()
    # Set initial video quality to a random value between 1 and 10
    video_quality = random.randint(1, 10)
    cur.execute("INSERT INTO channel (name, niche, video_quality) VALUES (?, ?, ?)", (name, niche, video_quality))
    conn.commit()
    conn.close()

def get_all_channels():
    conn = sqlite3.connect("simtube.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM channel")
    data = cur.fetchall()
    conn.close()
    return data

def get_channel_by_id(channel_id):
    conn = sqlite3.connect("simtube.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM channel WHERE id = ?", (channel_id,))
    data = cur.fetchone()
    conn.close()
    return data

def get_wallet():
    conn = sqlite3.connect("simtube.db")
    cur = conn.cursor()
    cur.execute("SELECT usd, rwf FROM wallet WHERE id = 1")
    data = cur.fetchone()
    conn.close()
    return data

def is_monetized(channel):
    return channel[3] >= 1000 and channel[4] >= 4000  # subscribers and watch_hours

# --- AD REVENUE SIMULATION ---
def calculate_ad_revenue(channel):
    if not is_monetized(channel):
        return 0  # Not monetized, no ad revenue

    # Basic calculation factors: video views, video quality, and engagement
    views = channel[7]
    quality = channel[10]  # Video quality factor (1 to 10)
    engagement = (channel[8] - channel[9]) / (channel[8] + channel[9])  # Like/Dislike ratio as engagement factor

    # Simulate ad revenue: higher views and quality = more revenue
    revenue = (views * quality * engagement) * 0.0001  # Simplified formula for ad revenue

    return revenue

# --- YOUTUBE UPDATES / ALGORITHM CHANGES ---
def algorithm_update(channel):
    # Simulate algorithm changes that impact video views or growth
    update_type = random.choice(["favor", "penalize", "neutral"])
    if update_type == "favor":
        # Increase views due to algorithm favor
        extra_views = random.randint(1000, 5000)
        new_views = channel[7] + extra_views
        st.write("🚀 Algorithm update: Your content is favored, and views increased!")
    elif update_type == "penalize":
        # Decrease views due to algorithm penalty
        extra_views = random.randint(-5000, -1000)
        new_views = max(0, channel[7] + extra_views)  # Ensure views don't go negative
        st.write("⚠️ Algorithm update: Your content is penalized, and views decreased!")
    else:
        # No change
        new_views = channel[7]

    # Update the views in the database
    conn = sqlite3.connect("simtube.db")
    cur = conn.cursor()
    cur.execute("UPDATE channel SET live_stream_views = ? WHERE id = ?", (new_views, channel[0]))
    conn.commit()
    conn.close()

# --- LIVE STREAM LOGIC ---
def start_live_stream(channel_id):
    conn = sqlite3.connect("simtube.db")
    cur = conn.cursor()
    cur.execute("UPDATE channel SET live_stream_active = 1, live_stream_views = 0 WHERE id = ?", (channel_id,))
    conn.commit()
    conn.close()

def end_live_stream(channel_id):
    conn = sqlite3.connect("simtube.db")
    cur = conn.cursor()
    cur.execute("UPDATE channel SET live_stream_active = 0 WHERE id = ?", (channel_id,))
    conn.commit()
    conn.close()

def generate_donations():
    return random.uniform(0, 10)  # Random donation between $0 and $10

# --- APP SETUP ---
init_db()
st.set_page_config(page_title="SimTube", layout="centered")
st.title("🎬 SimTube - Fake YouTube Simulator")

menu = st.sidebar.selectbox("Navigate", ["Home", "Create Channel", "Dashboard", "Wallet"])

if menu == "Home":
    st.subheader("🏠 Welcome to SimTube")
    st.write("Simulate YouTube channels, earnings, uploads, and more!")

elif menu == "Create Channel":
    st.subheader("🛠️ Create a New Channel")
    with st.form("channel_form"):
        name = st.text_input("Channel Name")
        niche = st.selectbox("Choose a Niche", ["Gaming", "Tech", "Education", "Entertainment", "Vlogs"])
        submitted = st.form_submit_button("Create Channel")
        if submitted:
            if name:
                create_channel(name, niche)
                st.success(f"Channel '{name}' created successfully!")
            else:
                st.warning("Please enter a channel name.")

elif menu == "Dashboard":
    st.subheader("📊 Channel Dashboard")
    channels = get_all_channels()
    if channels:
        channel_options = {f"{name} (ID: {id})": id for id, name in channels}
        selected_name = st.selectbox("Select a Channel", list(channel_options.keys()))
        selected_id = channel_options[selected_name]
        channel = get_channel_by_id(selected_id)

        st.markdown("---")
        st.text(f"📺 Name: {channel[1]}")
        st.text(f"🏷️ Niche: {channel[2]}")
        st.text(f"👥 Subscribers: {channel[3]}")
        st.text(f"⏱️ Watch Hours: {channel[4]}")
        st.text(f"✅ Verified: {'Yes' if channel[5] else 'No'}")

        # --- YOUTUBE PARTNER PROGRAM CHECK ---
        st.markdown("### 💼 Monetization Status")
        if is_monetized(channel):
            st.success("✅ Congratulations! You're now in the YouTube Partner Program!")
            st.markdown("💰 Earnings from videos will now go to your wallet.")
            # Show ad revenue after monetization
            ad_revenue = calculate_ad_revenue(channel)
            st.text(f"💸 Ad Revenue: ${ad_revenue:.2f}")
        else:
            st.warning("🔒 Not eligible for monetization yet.")
            st.info("To unlock monetization, you need:")
            st.markdown(f"- At least **1000 subscribers** (you have {channel[3]})")
            st.markdown(f"- At least **4000 watch hours** (you have {channel[4]})")

        # --- LIVE STREAM CONTROL ---
        st.markdown("### 🎥 Live Stream")
        if channel[6] == 1:  # Stream is active
            st.write(f"🕒 Stream has been live for: {int(time.time())} seconds!")
            st.write(f"👀 Views: {channel[7]}")
            st.write(f"💰 Donations: ${generate_donations():.2f} received!")
            end_stream_button = st.button("End Stream")
            if end_stream_button:
                end_live_stream(selected_id)
                st.success("Your live stream has ended!")
        else:
            st.write("🔴 Stream is currently offline.")
            start_stream_button = st.button("Start Live Stream")
            if start_stream_button and is_monetized(channel):
                start_live_stream(selected_id)
                st.success("Your live stream has started!")
            elif not is_monetized(channel):
                st.warning("You need to be monetized to start a live stream.")

        # --- LIKES/DISLIKES RATIO ---
        update_likes_dislikes(selected_id)
        likes, dislikes = get_likes_dislikes(selected_id)

        st.markdown("### 💬 Likes/Dislikes Ratio")
        total = likes + dislikes if likes + dislikes > 0 else 1  # Avoid division by zero
        like_percentage = (likes / total) * 100
        dislike_percentage = (dislikes / total) * 100
        
        st.write(f"👍 Likes: {likes} ({like_percentage:.2f}%)")
        st.write(f"👎 Dislikes: {dislikes} ({dislike_percentage:.2f}%)")

        if like_percentage > 70:
            st.success("This content is well-received by the viewers!")
        elif dislike_percentage > 30:
            st.warning("This content is not very popular.")

        # --- ALGORITHM UPDATE ---
        algorithm_update(channel)

    else:
        st.info("No channels found. Please create one.")

elif menu == "Wallet":
    st.subheader("💼 Your Wallet")
    wallet = get_wallet()
    st.text(f"USD: ${wallet[0]:,.2f}")
    st.text(f"RWF: {wallet[1]:,.2f} Frw")
