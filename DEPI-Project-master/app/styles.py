def get_custom_css():
    return """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        /* ===================== IOS-INSPIRED GLASSMORPHIC DESIGN ===================== */
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes scaleIn {
            from {
                opacity: 0;
                transform: scale(0.95);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }

        /* ===================== BASE BACKGROUND ===================== */
        
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
            color: #ffffff;
        }
        
        /* Add subtle overlay pattern */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }

        /* ===================== GLASSMORPHISM CONTAINERS ===================== */
        
        .block-container {
            padding: 3rem 2rem !important;
            max-width: 1400px !important;
        }
        
        /* Main content wrapper */
        .main .block-container {
            animation: fadeInUp 0.6s ease-out;
        }

        /* ===================== GLASSMORPHIC CARDS ===================== */
        
        .neon-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 24px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            animation: scaleIn 0.5s ease-out;
        }
        
        .neon-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            transition: left 0.5s;
        }
        
        .neon-card:hover::before {
            left: 100%;
        }
        
        .neon-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                0 16px 48px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.4);
            border-color: rgba(255, 255, 255, 0.5);
        }

        /* ===================== TYPOGRAPHY ===================== */
        
        h1 {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
            font-weight: 800 !important;
            font-size: 3.5rem !important;
            color: #ffffff !important;
            margin-bottom: 1rem !important;
            letter-spacing: -2px !important;
            text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            animation: fadeInUp 0.8s ease-out;
        }
        
        h2 {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
            font-weight: 700 !important;
            font-size: 2rem !important;
            color: #ffffff !important;
            margin: 2.5rem 0 1.5rem 0 !important;
            letter-spacing: -1px !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }
        
        h3 {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.5rem !important;
            color: #ffffff !important;
            margin: 2rem 0 1rem 0 !important;
            letter-spacing: -0.5px !important;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        
        p, span, div, label {
            color: rgba(255, 255, 255, 0.9) !important;
            line-height: 1.6;
        }

        /* ===================== GLASSMORPHIC METRICS ===================== */
        
        .metric-value {
            font-size: 3.5rem !important;
            font-weight: 900 !important;
            background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 16px 0;
            letter-spacing: -3px;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
            animation: scaleIn 0.6s ease-out;
        }

        .metric-label {
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.8);
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
            margin-bottom: 12px;
        }
        
        .metric-desc {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
            margin-top: 12px;
            font-weight: 500;
        }

        /* ===================== IOS-STYLE BUTTONS ===================== */
        
        .stButton > button {
            background: rgba(255, 255, 255, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            color: white !important;
            padding: 16px 36px !important;
            border-radius: 16px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 
                0 4px 16px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
            letter-spacing: 0.5px !important;
        }

        .stButton > button:hover {
            transform: translateY(-3px) scale(1.05) !important;
            background: rgba(255, 255, 255, 0.3) !important;
            box-shadow: 
                0 8px 24px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
            border-color: rgba(255, 255, 255, 0.5) !important;
        }
        
        .stButton > button:active {
            transform: translateY(-1px) scale(1.02) !important;
        }

        /* ===================== GLASSMORPHIC SIDEBAR ===================== */
        
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(30px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(30px) saturate(180%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.1) !important;
        }
        
        [data-testid="stSidebar"] h1 {
            font-size: 1.75rem !important;
            padding: 1.5rem 0;
            color: #ffffff !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        [data-testid="stSidebar"] h3 {
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 1.1rem !important;
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            color: rgba(255, 255, 255, 0.95) !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
        }
        
        [data-testid="stSidebar"] [data-baseweb="radio"] {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 14px;
            padding: 14px 18px;
            margin: 8px 0;
            transition: all 0.3s ease;
        }
        
        [data-testid="stSidebar"] [data-baseweb="radio"]:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.4);
            transform: translateX(4px);
        }
        
        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.2) !important;
            margin: 1.5rem 0 !important;
        }

        /* ===================== GLASSMORPHIC INPUTS ===================== */
        
        .stSelectbox label, .stMultiSelect label, .stSlider label, 
        .stNumberInput label, .stTextInput label {
            color: rgba(255, 255, 255, 0.95) !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }
        
        .stSelectbox > div > div, .stMultiSelect > div > div,
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 14px !important;
            color: white !important;
            transition: all 0.3s ease !important;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stSelectbox > div > div:hover, .stMultiSelect > div > div:hover,
        .stTextInput > div > div > input:hover {
            background: rgba(255, 255, 255, 0.2) !important;
            border-color: rgba(255, 255, 255, 0.5) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stSelectbox > div > div:focus-within, .stMultiSelect > div > div:focus-within,
        .stTextInput > div > div > input:focus {
            background: rgba(255, 255, 255, 0.25) !important;
            border-color: rgba(255, 255, 255, 0.6) !important;
            box-shadow: 
                0 4px 16px rgba(0, 0, 0, 0.15),
                0 0 0 3px rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Dropdown options */
        [data-baseweb="popover"] {
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(20px) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        }
        
        [data-baseweb="popover"] li {
            color: #1e293b !important;
            border-radius: 8px !important;
            margin: 4px 8px !important;
            transition: all 0.2s ease !important;
        }
        
        [data-baseweb="popover"] li:hover {
            background: rgba(102, 126, 234, 0.2) !important;
        }
        
        .stNumberInput input {
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 14px !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 14px !important;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stNumberInput input:focus {
            border-color: rgba(255, 255, 255, 0.6) !important;
            box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1) !important;
        }
        
        .stSlider > div > div > div > div {
            background: rgba(255, 255, 255, 0.9) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }
        
        .stSlider > div > div > div {
            background: rgba(255, 255, 255, 0.2) !important;
        }

        /* ===================== GLASSMORPHIC TABS ===================== */
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 12px;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 600;
            padding: 12px 24px;
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(255, 255, 255, 0.15);
            color: white;
        }
        
        .stTabs [aria-selected="true"] {
            background: rgba(255, 255, 255, 0.25) !important;
            color: white !important;
            border-color: rgba(255, 255, 255, 0.3);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        /* ===================== GLASSMORPHIC DATA TABLES ===================== */
        
        [data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(20px) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            overflow: hidden !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
        }
        
        .dataframe {
            font-size: 0.95rem !important;
            color: rgba(255, 255, 255, 0.95) !important;
        }
        
        .dataframe thead tr th {
            background: rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            font-weight: 700 !important;
            padding: 18px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 1.5px;
        }
        
        .dataframe tbody tr {
            transition: all 0.2s ease;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
            background-color: transparent !important;
        }
        
        .dataframe tbody tr:hover {
            background: rgba(255, 255, 255, 0.15) !important;
        }
        
        .dataframe tbody td {
            padding: 16px !important;
            color: rgba(255, 255, 255, 0.9) !important;
            background-color: transparent !important;
        }
        
        /* Force all table elements to have visible text */
        [data-testid="stDataFrame"] table {
            color: white !important;
        }
        
        [data-testid="stDataFrame"] td,
        [data-testid="stDataFrame"] th {
            color: white !important;
            background-color: transparent !important;
        }
        
        [data-testid="stDataFrame"] tbody td {
            color: rgba(255, 255, 255, 0.95) !important;
        }
        
        /* AG Grid specific styling for newer Streamlit versions */
        .ag-theme-streamlit {
            --ag-foreground-color: rgb(255, 255, 255) !important;
            --ag-background-color: transparent !important;
            --ag-header-foreground-color: rgb(255, 255, 255) !important;
            --ag-header-background-color: rgba(255, 255, 255, 0.2) !important;
            --ag-odd-row-background-color: transparent !important;
            --ag-row-hover-color: rgba(255, 255, 255, 0.15) !important;
        }
        
        .ag-theme-streamlit .ag-root-wrapper {
            border: none !important;
        }
        
        .ag-theme-streamlit .ag-header {
            color: white !important;
        }
        
        .ag-theme-streamlit .ag-cell {
            color: rgba(255, 255, 255, 0.95) !important;
        }
        
        .ag-theme-streamlit .ag-row {
            color: rgba(255, 255, 255, 0.95) !important;
        }
        
        /* For any white backgrounds that might appear */
        [data-testid="stDataFrame"] div[style*="background-color: white"],
        [data-testid="stDataFrame"] div[style*="background-color: rgb(255, 255, 255)"],
        [data-testid="stDataFrame"] div[style*="background: white"] {
            background-color: transparent !important;
            color: rgba(255, 255, 255, 0.95) !important;
        }
        
        /* Cell content divs */
        [data-testid="stDataFrame"] div[data-testid="stDataFrameResizable"] *,
        [data-testid="stDataFrame"] .element-container * {
            color: rgba(255, 255, 255, 0.95) !important;
        }

        /* ===================== GLASSMORPHIC ALERTS ===================== */
        
        .stAlert {
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(15px) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            padding: 20px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
            animation: scaleIn 0.4s ease-out;
        }
        
        .stAlert p {
            color: rgba(255, 255, 255, 0.95) !important;
            font-weight: 500;
        }
        
        .stSuccess {
            background: rgba(34, 197, 94, 0.2) !important;
            border-color: rgba(34, 197, 94, 0.4) !important;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.2) !important;
            border-color: rgba(239, 68, 68, 0.4) !important;
        }
        
        .stWarning {
            background: rgba(245, 158, 11, 0.2) !important;
            border-color: rgba(245, 158, 11, 0.4) !important;
        }
        
        .stInfo {
            background: rgba(59, 130, 246, 0.2) !important;
            border-color: rgba(59, 130, 246, 0.4) !important;
        }

        /* ===================== PLOTLY CHARTS GLASSMORPHISM ===================== */
        
        .js-plotly-plot {
            border-radius: 16px !important;
            overflow: hidden !important;
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            animation: scaleIn 0.5s ease-out;
        }
        
        .js-plotly-plot .plotly {
            border-radius: 12px;
        }

        /* ===================== CUSTOM SCROLLBAR ===================== */
        
        ::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            border: 2px solid transparent;
            background-clip: padding-box;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
            background-clip: padding-box;
        }

        /* ===================== FLOATING ANIMATIONS ===================== */
        
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.8;
            }
        }
        
        .metric-value {
            animation: pulse 2s ease-in-out infinite;
        }

        /* ===================== COLUMN SPACING ===================== */
        
        [data-testid="column"] {
            padding: 0 12px;
            animation: fadeInUp 0.6s ease-out;
            animation-fill-mode: both;
        }
        
        [data-testid="column"]:nth-child(1) { animation-delay: 0.1s; }
        [data-testid="column"]:nth-child(2) { animation-delay: 0.2s; }
        [data-testid="column"]:nth-child(3) { animation-delay: 0.3s; }
        [data-testid="column"]:nth-child(4) { animation-delay: 0.4s; }
        
        /* ===================== DIVIDER ===================== */
        
        hr {
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            margin: 3rem 0;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }
        
        /* ===================== DOWNLOAD BUTTON ===================== */
        
        .stDownloadButton > button {
            background: rgba(34, 197, 94, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(34, 197, 94, 0.4) !important;
            color: white !important;
            border-radius: 14px !important;
            padding: 14px 32px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        .stDownloadButton > button:hover {
            background: rgba(34, 197, 94, 0.3) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(34, 197, 94, 0.3) !important;
        }
        
        /* ===================== EXPANDER ===================== */
        
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 14px !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 16px !important;
        }
        
        .streamlit-expanderHeader:hover {
            background: rgba(255, 255, 255, 0.15) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
        }
        
        .streamlit-expanderContent {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 0 0 14px 14px !important;
            border-top: none !important;
        }
        
        /* ===================== METRIC CONTAINERS ===================== */
        
        [data-testid="stMetricValue"] {
            font-size: 2.5rem !important;
            font-weight: 900 !important;
            color: white !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: rgba(255, 255, 255, 0.8) !important;
            font-weight: 600 !important;
        }
        
        /* ===================== SPECIAL GRADIENT HEADERS ===================== */
        
        .gradient-header {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.05) 100%);
            backdrop-filter: blur(20px);
            padding: 32px;
            border-radius: 20px;
            margin-bottom: 32px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            animation: scaleIn 0.5s ease-out;
        }
        
        .gradient-header h3 {
            margin: 0 !important;
            color: white !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .gradient-header p {
            margin: 12px 0 0 0 !important;
            color: rgba(255, 255, 255, 0.85) !important;
            font-size: 1.05rem;
        }
        
        /* ===================== LOADING SPINNER ===================== */
        
        .stSpinner > div {
            border-color: rgba(255, 255, 255, 0.3) !important;
            border-top-color: white !important;
        }
        
        /* ===================== RESPONSIVE DESIGN ===================== */
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2.5rem !important;
            }
            
            .neon-card {
                padding: 24px;
            }
            
            .metric-value {
                font-size: 2.5rem !important;
            }
        }
    </style>
    """

def card_component(title, value, description=""):
    return f"""
    <div class="neon-card" style="animation-delay: 0.2s;">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-desc">{description}</div>
    </div>
    """
