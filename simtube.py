import streamlit as st

st.set_page_config(page_title="SimTube", layout="centered")

# --- Sidebar Navigation ---
st.sidebar.title("SimTube Menu")
menu_option = st.sidebar.radio("Choose an action:", ["Upload Regular Video", "Upload Shorts", "Go Live", "My Channel", "Analytics"])

# --- Title ---
st.title("🎬 SimTube: YouTube Simulator")

# --- Upload Regular Video ---
if menu_option == "Upload Regular Video":
    st.header("📤 Upload Regular Video")
    title = st.text_input("Enter video title")
    description = st.text_area("Enter description")
    quality = st.slider("Select video quality (affects performance)", 1, 10, 5)
    if st.button("Upload Video"):
        st.success(f"Video '{title}' uploaded as a regular video with quality level {quality}!")

# --- Upload Shorts ---
elif menu_option == "Upload Shorts":
    st.header("📱 Upload YouTube Short")
    title = st.text_input("Enter short title")
    caption = st.text_area("Enter short caption")
    if st.button("Upload Short"):
        st.success(f"Short '{title}' uploaded successfully!")

# --- Go Live ---
elif menu_option == "Go Live":
    st.header("🔴 Start a Livestream")
    stream_title = st.text_input("Enter livestream title")
    stream_category = st.selectbox("Select category", ["Gaming", "Music", "Education", "Chat", "Other"])
    is_streaming = st.button("Start Live Stream")
    if is_streaming:
        st.success(f"You're now live: {stream_title} in {stream_category}")
        st.info("Click 'End Stream' below when you're ready to finish.")
        if st.button("End Stream"):
            st.warning("Livestream ended.")

# --- My Channel ---
elif menu_option == "My Channel":
    st.header("📺 My Channel")
    st.text("Channel Name: SimGamer123")
    st.text("Subscribers: 1,204")
    st.text("Total Videos: 27")
    st.text("Verified: ✅")

# --- Analytics ---
elif menu_option == "Analytics":
    st.header("📊 Channel Analytics")
    st.metric("Total Views", "124,200")
    st.metric("Watch Hours", "4,500")
    st.metric("Estimated Revenue", "$892.50")
    st.metric("Shorts Uploaded", "10")
    st.metric("Livestreams", "3")

