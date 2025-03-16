import streamlit as st
import re
import random
import pandas as pd
import matplotlib.pyplot as plt

# App title
st.set_page_config(page_title="Up AI Follow-Up App (Demo)", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Dashboard", "Call Analysis", "Call History", "Performance Data", "Client Timeline", "Leaderboard", "Settings"])

# Brand Styling
st.markdown("""
    <style>
        body { 
            font-family: 'Roboto', sans-serif; 
            background-color: #121212; 
            color: #e0e0e0; 
        }
        .css-18e3th9 { padding-top: 20px; }
        .css-1d391kg { padding-top: 20px; }
        .stButton>button { 
            width: 100%; 
            margin-top: 5px; 
            transition: background-color 0.3s, transform 0.3s; 
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }
        .stButton>button:hover { 
            transform: scale(1.05); 
        }
        .lead-card {
            background: linear-gradient(135deg, #1e1e2f, #262730);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            color: white; 
        }
        .lead-name { font-weight: bold; font-size: 18px; color: #ffffff; }
        .status-badge { font-size: 14px; padding: 5px 10px; border-radius: 5px; color: white; }
        .status-new { background-color: #007bff; }
        .status-followup { background-color: #ffcc00; color: #000; }
        .status-closed { background-color: #28a745; }
        .red-button {
            background: linear-gradient(135deg, rgba(220, 53, 69, 0.8), rgba(220, 53, 69, 0.3));
            box-shadow: 0 4px 20px rgba(220, 53, 69, 0.5);
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            display: block;
            margin-top: 10px;
            color: white !important; 
        }
        .blue-button {
            background: #007bff;
            color: white !important; 
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            text-decoration: none;
            display: block;
            margin-top: 10px;
            border: none; 
            transition: background-color 0.3s, transform 0.3s;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }
        .blue-button:hover {
            transform: scale(1.05);
        }
        .sidebar .sidebar-content {
            background-color: #1e1e2f; 
            border-radius: 10px; 
            padding: 10px;
        }
        .sidebar .sidebar-title {
            color: #ffffff;
        }
        .sidebar .selectbox {
            background-color: #262730; 
            color: #ffffff; 
            border-radius: 5px; 
        }
        .sidebar .selectbox:hover {
            background-color: #007bff; 
        }
        .time-to-call-back {
            color: #ffcc00;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Estimator Performance Stats
performance_stats = {
    "Win Rate": 50,
    "Total Won": 5,
    "Total Lost": 5,
    "Avg Follow-Ups Before Close": 4
}

# AI Suggestions & Lead Data
leads = [
    {"name": "John Doe", "status": "New", "phone": "555-1234", "heat": "❄️", "last_call": "2 days ago", "suggestion": "Mention pricing details to encourage action.", "call_notes": "They mentioned wanting a discount—ask if an extended warranty would be a better value."},
    {"name": "Jane Smith", "status": "Follow-Up", "phone": "555-5678", "heat": "😐", "last_call": "1 week ago", "suggestion": "They had timing concerns—ask if adjusting the schedule helps.", "call_notes": "They mentioned wanting a discount—ask if an extended warranty would be a better value."},
    {"name": "Mike Johnson", "status": "Closed", "phone": "555-9876", "heat": "🔥", "last_call": "Yesterday", "suggestion": "They mentioned competitor bids—highlight unique value.", "call_notes": "They mentioned wanting a discount—ask if an extended warranty would be a better value."}
]

# 📌 Dashboard
if page == "Dashboard":
    st.markdown("<h2 style='text-align: center; color: white;'>📌 Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Welcome to Up AI's demo dashboard!</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)
    
    for lead in leads:
        button_color = "red-button" if lead['heat'] == "🔥" else "blue-button"
        note_key = f"show_notes_{lead['name'].replace(' ', '_')}"
        followup_key = f"show_followup_{lead['name'].replace(' ', '_')}"

        if note_key not in st.session_state:
            st.session_state[note_key] = False
        
        if followup_key not in st.session_state:
            st.session_state[followup_key] = False

        st.markdown(f"""
            <div class='lead-card' style="display: flex; justify-content: space-between;">
                <div>
                    <p class='lead-name'>{lead['name']} {lead['heat']}</p>
                    <p>Status: <span class='status-badge status-{lead['status'].lower().replace(' ', '')}'>{lead['status']}</span></p>
                    <p style="color: white;">📅 Last Call: {lead['last_call']}</p>
                    <p style="color: white;">💡 AI Suggestion: {lead['suggestion']}</p>
                    <a href="tel:{lead['phone']}" class="blue-button" style="width: 100%;">
                        📞 Call Now - {lead['phone']}
                    </a>
                </div>
                <div style="text-align: right; padding-right: 10px;">
                    <p class="time-to-call-back">⏰ Time to Call Back: <br> <span style="color: #ffcc00;">{random.choice(["Tomorrow at 10 AM", "In 2 days at 3 PM", "Next Monday at 9 AM"])}</span></p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button(f"📩 Send Follow-Up", key=f"toggle_followup_{lead['name']}"):
            followup_message = f"Hey {lead['name']}, just checking in to see if you had any thoughts on our last conversation. Let me know how you'd like to move forward!"
            st.text_area("AI-Generated Follow-Up Message", followup_message, key=f"followup_message_{lead['name']}", height=70)
            col1, col2 = st.columns(2)
            with col1:
                st.button("📩 Send Text", key=f"send_text_{lead['name']}")
            with col2:
                st.button("📧 Send Email", key=f"send_email_{lead['name']}")

        if st.button(f"📝 View Call Notes", key=f"toggle_notes_{lead['name']}"):
            st.session_state[note_key] = not st.session_state[note_key]

        if st.session_state[note_key]:
            updated_note = st.text_area(f"Edit Notes for {lead['name']}", lead['call_notes'], key=f"edit_notes_{lead['name']}")

        st.markdown("</div>", unsafe_allow_html=True)

# 📌 Performance Data Page
if page == "Performance Data":
    st.markdown("<h2 style='text-align: center; color: white;'>📊 Performance Data</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        labels = ["Won Deals", "Lost Deals"]
        sizes = [performance_stats["Total Won"], performance_stats["Total Lost"]]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#28a745', '#dc3545'])
        ax.axis("equal")
        st.pyplot(fig)
        st.markdown("### Win/Loss Ratio", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Avg Follow-Ups Before Close", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.bar(["Avg Follow-Ups"], [performance_stats["Avg Follow-Ups Before Close"]], color="#007bff")
        ax.set_ylim(0, 10)
        ax.set_ylabel("Follow-Ups")
        st.pyplot(fig)

    st.markdown("### Summary", unsafe_allow_html=True)
    st.write(f"<p style='color: white;'>✅ **Win Rate:** {performance_stats['Win Rate']}%</p>", unsafe_allow_html=True)
    st.write(f"<p style='color: white;'>🏆 **Total Won:** {performance_stats['Total Won']}</p>", unsafe_allow_html=True)
    st.write(f"<p style='color: white;'>❌ **Total Lost:** {performance_stats['Total Lost']}</p>", unsafe_allow_html=True)
    st.write(f"<p style='color: white;'>📌 **Avg Follow-Ups Before Close:** {performance_stats['Avg Follow-Ups Before Close']}</p>", unsafe_allow_html=True)

# 📌 Call History Page
if page == "Call History":
    st.markdown("<h2 style='color: white;'>📞 Call History</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>View your previous call interactions here.</p>", unsafe_allow_html=True)

# 📌 Settings Page (Mockup)
if page == "Settings":
    st.markdown("<h2 style='color: white;'>⚙️ Settings (Mockup)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>Settings page is under construction.</p>", unsafe_allow_html=True)
    st.button("Back to Dashboard", on_click=lambda: st.experimental_set_query_params(page="Dashboard"))

# 📌 Call Analysis Page
if page == "Call Analysis":
    st.markdown("<h2 style='text-align: center; color: white;'>📞 Call Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Review key insights from previous calls to refine your sales approach.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)
    
    st.markdown("### Good Phrases Used Often:")
    st.write("• 'Absolutely, I can help with that!'\n• 'Let’s explore the best options together.'\n• 'I understand your needs perfectly.'")
    
    st.markdown("### Phrases to Avoid:")
    st.write("• 'I don’t know if this will work for you.'\n• 'Maybe you should consider other options.'\n• 'It might be too expensive.'")
    
    st.markdown("### Areas for Improvement:")
    st.write("• Objection handling\n• Creating urgency\n• Closing technique")
    
    st.markdown("### Sales Personality Type:")
    st.write("Based on recent interactions, your sales personality type is **The Consultant**.")
    
    st.markdown("### Recommended Phrases for Future Calls:")
    st.write("• 'Based on our discussion, I believe this option aligns perfectly with your needs.'\n• 'Let’s take the next step together to ensure you get the best value.'\n• 'I’m here to provide you with all the insights you need to make an informed decision.'")
    
    st.markdown("### Most Effective Closing Lines:")
    st.write("• 'Clients have responded well to: \"Let’s move forward and lock in your pricing today!\"'\n• 'Another strong closer: \"Is there anything stopping us from getting started now?\"'")
    
    st.markdown("### Sales Pitfalls:")
    st.write("• 'Clients tend to disengage when pricing is hesitated on.'\n• 'Avoid saying: \"I understand if you need more time\"—it often delays deals.'")
    
    st.markdown("### Historical Trends:")
    st.write("• 'Win rates improved when objections were handled confidently.'\n• 'Following up within 48 hours of initial contact increases close rates by 20%.''")

# 📌 Client Timeline Page
if page == "Client Timeline":
    st.markdown("<h2 style='text-align: center; color: white;'>📍 Client Interaction Timeline</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Visual summary of past interactions for better follow-up planning.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)

    st.markdown("""
    - 📅 **March 1st, 2024:** John Doe - Initial Inquiry Call  
    - 📩 **March 3rd, 2024:** John Doe - Sent Follow-Up Email  
    - 📞 **March 5th, 2024:** John Doe - Follow-Up Call (Client requested more details)  
    - 📩 **March 7th, 2024:** John Doe - Sent Proposal via Email  
    - ✅ **March 10th, 2024:** John Doe - Client Accepted Proposal - Deal Closed!  

    - 📅 **March 2nd, 2024:** Jane Smith - Initial Inquiry Call  
    - 📩 **March 4th, 2024:** Jane Smith - Sent Follow-Up Email  
    - 📞 **March 6th, 2024:** Jane Smith - Follow-Up Call (Client requested more details)  
    - 📩 **March 8th, 2024:** Jane Smith - Sent Proposal via Email  
    - ❌ **March 12th, 2024:** Jane Smith - Client Declined Proposal  
    """)

# 📌 AI-Powered Leaderboard & Gamification
if page == "Leaderboard":
    st.markdown("<h2 style='text-align: center; color: #FFD700;'>🏆 Top Sales Performers</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Track top-performing estimators and gamify follow-ups!</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)

    # Sample leaderboard data
    leaderboard_data = pd.DataFrame({
        "Estimator": ["John Doe", "Jane Smith", "Mike Johnson", "Emily Davis", "Mark Lee"],
        "Closing Rate (%)": [75, 68, 60, 55, 50],
        "Follow-Up Efficiency (%)": [90, 85, 78, 72, 65],
        "AI Sales Score": [95, 88, 80, 75, 70]
    })

    # Rank estimators based on AI Sales Score
    leaderboard_data = leaderboard_data.sort_values(by="AI Sales Score", ascending=False)
    
    # Display leaderboard
    st.markdown("<h3 style='text-align: center; color: white;'>🔥 Competitive Rankings</h3>", unsafe_allow_html=True)
    
    def highlight_leaderboard(row):
        return ['background-color: #262730; color: white' if i % 2 == 0 else 'background-color: #1e1e2f; color: white' for i in range(len(row))]
    
    st.table(leaderboard_data.style.apply(highlight_leaderboard, axis=1))
    
    st.markdown("<p style='text-align: center; color: #FFD700; font-size: 16px;'>💡 Keep pushing—every call gets you closer to the top! 🚀</p>", unsafe_allow_html=True)
