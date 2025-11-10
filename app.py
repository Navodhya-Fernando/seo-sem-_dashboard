import streamlit as st
import pandas as pd
from datetime import date, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ---------- CONFIGURE THIS ----------
# Must match EXACTLY your Search Console property.
# Example: "https://dreamshift.lk/" or "https://www.dreamshift.lk/"
PROPERTY_URI = "https://dreamshift.net/"  # TODO: change this

# Blog URL filter. Adjust if needed (e.g. "/blog/", "/insights/", etc).
BLOG_PATH_KEYWORD = "/blog/"
# ------------------------------------


SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

st.set_page_config(
    page_title="Blog SEO Dashboard",
    layout="wide",
)

# ---------- AUTH & API CLIENT ----------

@st.cache_resource
def get_sc_service():
    """
    Build a Search Console service client using the service account
    stored in .streamlit/secrets.toml under [gcp_service_account].
    """
    service_account_info = st.secrets["gcp_service_account"]
    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES,
    )
    service = build("searchconsole", "v1", credentials=creds)
    return service


@st.cache_data(show_spinner=True)
def fetch_search_console_data(start_date: date, end_date: date) -> pd.DataFrame:
    """
    Fetch date+page level data from Search Console Search Analytics.
    """
    service = get_sc_service()

    body = {
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "dimensions": ["date", "page"],
        "rowLimit": 25000,  # increase if you have tons of URLs
    }

    response = (
        service.searchanalytics()
        .query(siteUrl=PROPERTY_URI, body=body)
        .execute()
    )

    rows = response.get("rows", [])
    if not rows:
        return pd.DataFrame()

    records = []
    for row in rows:
        keys = row.get("keys", [])
        if len(keys) != 2:
            continue
        d, page = keys
        records.append(
            {
                "date": pd.to_datetime(d),
                "page": page,
                "clicks": row.get("clicks", 0),
                "impressions": row.get("impressions", 0),
                "ctr": row.get("ctr", 0.0),
                "position": row.get("position", 0.0),
            }
        )

    df = pd.DataFrame(records)

    # Filter only blog URLs if needed
    if BLOG_PATH_KEYWORD:
        df = df[df["page"].str.contains(BLOG_PATH_KEYWORD)]

    return df.reset_index(drop=True)


def get_preset_range(option: str):
    """
    Return (start, end) for the chosen preset.
    Note: GSC data is usually available up to yesterday.
    """
    today = date.today()
    end = today - timedelta(days=1)

    if option == "Last 7 days":
        start = end - timedelta(days=6)
    elif option == "Last 30 days":
        start = end - timedelta(days=29)
    elif option == "Last 90 days":
        start = end - timedelta(days=89)
    elif option == "Last 365 days":
        start = end - timedelta(days=364)
    else:
        # default if something goes weird
        start = end - timedelta(days=29)

    return start, end


# ---------- UI LAYOUT ----------

st.title("Blog SEO Performance Dashboard")

with st.sidebar:
    st.header("Filters")

    range_option = st.selectbox(
        "Date range",
        ["Last 7 days", "Last 30 days", "Last 90 days", "Last 365 days", "Custom"],
        index=1,
    )

    if range_option == "Custom":
        default_start, default_end = get_preset_range("Last 30 days")
        date_range = st.date_input(
            "Select custom range",
            value=(default_start, default_end),
        )

        # Streamlit returns (start, end) as a tuple
        if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date, end_date = default_start, default_end
    else:
        start_date, end_date = get_preset_range(range_option)

    st.caption(
        f"Showing data from **{start_date}** to **{end_date}**"
    )

# ---------- DATA FETCH ----------

df = fetch_search_console_data(start_date, end_date)

if df.empty:
    st.warning(
        "No Search Console data found for this date range/property. "
        "Check PROPERTY_URI, permissions, and date range."
    )
    st.stop()

# ---------- KPIs ----------

total_articles = df["page"].nunique()
total_clicks = int(df["clicks"].sum())
total_impr = int(df["impressions"].sum())

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
kpi_col1.metric("Articles with activity", total_articles)
kpi_col2.metric("Total Clicks", f"{total_clicks:,}")
kpi_col3.metric("Total Impressions", f"{total_impr:,}")

st.markdown("---")

# ---------- TRENDS OVER TIME ----------

trend = (
    df.groupby("date")[["clicks", "impressions"]]
    .sum()
    .sort_index()
)

st.subheader("Clicks & Impressions Over Time")
st.line_chart(trend)

st.markdown("---")

# ---------- TOP ARTICLES: CLICKS ----------

st.subheader("Top 5 Articles by Clicks")

top_clicks = (
    df.groupby("page")[["clicks", "impressions"]]
    .sum()
    .sort_values("clicks", ascending=False)
    .head(5)
    .reset_index()
)

st.dataframe(top_clicks, use_container_width=True)
st.bar_chart(
    data=top_clicks.set_index("page")["clicks"]
)

# ---------- TOP ARTICLES: IMPRESSIONS ----------

st.subheader("Top 5 Articles by Impressions")

top_impr = (
    df.groupby("page")[["clicks", "impressions"]]
    .sum()
    .sort_values("impressions", ascending=False)
    .head(5)
    .reset_index()
)

st.dataframe(top_impr, use_container_width=True)
st.bar_chart(
    data=top_impr.set_index("page")["impressions"]
)

# ---------- OPTIONAL: DETAIL TABLE ----------

with st.expander("View detailed data"):
    st.dataframe(
        df.sort_values(["date", "clicks"], ascending=[False, False]),
        use_container_width=True,
    )
