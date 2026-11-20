import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Industrial Machine Monitoring",
    page_icon="⚙️",
    layout="wide"
)

# =====================================================
# LOGIN
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔒 Machine Monitoring Login")

    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if password == st.secrets["APP_PASSWORD"]:
            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Wrong password")

    st.stop()

# Auto-refresh every 5 seconds
st_autorefresh(
    interval=5000,
    limit=None,
    key="machine_dashboard_refresh"
)

# API_URL = "http://127.0.0.1:8000"
API_URL = "https://machine-monitoring-project.onrender.com"  # Alternative URL

# =====================================================
# DASHBOARD HEADER
# =====================================================

st.title("⚙️ Industrial Machine Monitoring System")

st.markdown(
    "Real-Time Production Monitoring | Machine Performance Analytics"
)

st.divider()

# =====================================================
# FETCH DATA FROM FASTAPI
# =====================================================

try:

    latest_response = requests.get(
        f"{API_URL}/latest", timeout=5
    )

    summary_response = requests.get(
        f"{API_URL}/summary", timeout=5
    )

    readings_response = requests.get(
        f"{API_URL}/readings", timeout=5
    )

    latest_response.raise_for_status()
    summary_response.raise_for_status()
    readings_response.raise_for_status()

    latest = latest_response.json()
    summary = summary_response.json()
    readings = readings_response.json()

    df = pd.DataFrame(readings["readings"])

    # =================================================
    # MACHINE STATUS
    # =================================================

    st.subheader("🚦 Machine Status")

    if not df.empty and "timestamp" in df.columns:

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            utc=True,
            format="ISO8601"
        )

        local_timezone = datetime.now().astimezone().tzinfo

        df["timestamp"] = df["timestamp"].dt.tz_convert(
            local_timezone
        )

        latest_timestamp = df["timestamp"].max()

        time_difference = (
            pd.Timestamp.now(tz="UTC")
            - latest_timestamp.tz_convert("UTC")
        ).total_seconds()

        if time_difference <= 90:

            st.success("🟢 MACHINE STATUS: RUNNING")

        else:

            st.error("🔴 MACHINE STATUS: STOPPED")

            st.warning(
                f"No new readings for approximately "
                f"{int(time_difference)} seconds."
            )

    else:

        st.warning("🟡 MACHINE STATUS: NO DATA")

    st.caption(
        "Machine status is based on the latest database reading. "
        "Dashboard refreshes every 5 seconds."
    )

    st.divider()

    # =================================================
    # MACHINE OVERVIEW
    # =================================================

    st.subheader("📊 Machine Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏭 Total Production",
        f"{summary.get('total_production', 0):,}"
    )

    col2.metric(
        "🔢 Current Counter",
        f"{latest.get('counter', 0):,}"
    )

    col3.metric(
        "📋 Total Readings",
        f"{summary.get('total_records', 0):,}"
    )

    col4.metric(
        "📦 Latest Total",
        f"{latest.get('total', 0):,}"
    )

    st.divider()

    # =================================================
    # DATE FILTER
    # =================================================

    st.subheader("📅 Filter Machine Readings")

    if not df.empty:

        min_date = df["timestamp"].min().date()
        max_date = df["timestamp"].max().date()

        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if len(date_range) == 2:

            start_date, end_date = date_range

            filtered_df = df[
                (df["timestamp"].dt.date >= start_date)
                &
                (df["timestamp"].dt.date <= end_date)
            ].copy()

        else:

            filtered_df = df[
                df["timestamp"].dt.date == date_range[0]
            ].copy()

        st.info(
            f"Showing {len(filtered_df)} readings."
        )

        st.divider()

        # =============================================
        # CSV DOWNLOAD
        # =============================================

        st.subheader("📥 Export Machine Data")

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Readings as CSV",
            data=csv_data,
            file_name="machine_readings.csv",
            mime="text/csv"
        )

        st.divider()

        # =============================================
        # FILTERED ANALYTICS
        # =============================================

        st.subheader("📈 Filtered Production Analytics")

        if not filtered_df.empty:

            chart1, chart2 = st.columns(2)

            with chart1:

                production_fig = px.line(
                    filtered_df,
                    x="timestamp",
                    y="total",
                    title="Production Trend",
                    markers=True,
                    template="plotly_white"
                )

                production_fig.update_layout(
                    xaxis_title="Time",
                    yaxis_title="Total Production",
                    hovermode="x unified"
                )

                st.plotly_chart(
                    production_fig,
                    use_container_width=True
                )

            with chart2:

                counter_fig = px.line(
                    filtered_df,
                    x="timestamp",
                    y="counter",
                    title="Machine Counter Trend",
                    markers=True,
                    template="plotly_white"
                )

                counter_fig.update_layout(
                    xaxis_title="Time",
                    yaxis_title="Counter",
                    hovermode="x unified"
                )

                st.plotly_chart(
                    counter_fig,
                    use_container_width=True
                )

            # =========================================
            # PRODUCTION STATISTICS
            # =========================================

            st.subheader("📊 Production Statistics")

            stat1, stat2, stat3 = st.columns(3)

            stat1.metric(
                "Maximum Production",
                f"{filtered_df['total'].max():,}"
            )

            stat2.metric(
                "Minimum Production",
                f"{filtered_df['total'].min():,}"
            )

            stat3.metric(
                "Average Production",
                f"{filtered_df['total'].mean():,.2f}"
            )

            st.divider()

            # =========================================
            # ANOMALY DETECTION
            # =========================================

            st.subheader("🚨 Machine Anomaly Detection")

            if len(filtered_df) >= 5:

                anomaly_df = filtered_df.sort_values(
                    "timestamp"
                ).copy()

                anomaly_df["production_change"] = (
                    anomaly_df["total"].diff()
                )

                changes = anomaly_df[
                    "production_change"
                ].dropna()

                q1 = changes.quantile(0.25)
                q3 = changes.quantile(0.75)

                iqr = q3 - q1

                lower_limit = q1 - (1.5 * iqr)
                upper_limit = q3 + (1.5 * iqr)

                anomaly_df["anomaly"] = (
                    (anomaly_df["production_change"] < lower_limit)
                    |
                    (anomaly_df["production_change"] > upper_limit)
                )

                anomalies = anomaly_df[
                    anomaly_df["anomaly"]
                ]

                if anomalies.empty:

                    st.success(
                        "✅ No unusual production changes detected."
                    )

                else:

                    st.warning(
                        f"⚠️ {len(anomalies)} unusual production "
                        "changes detected!"
                    )

                    st.dataframe(
                        anomalies[
                            ["timestamp", "production_change"]
                        ],
                        use_container_width=True,
                        hide_index=True
                    )

            else:

                st.info(
                    "At least 5 readings are required "
                    "for anomaly detection."
                )

            st.divider()

            # =========================================
            # DOWNTIME ANALYSIS
            # =========================================

            st.subheader("⏱️ Machine Downtime Analysis")

            if len(filtered_df) >= 2:

                downtime_df = filtered_df.sort_values(
                    "timestamp"
                ).copy()

                downtime_df["time_gap"] = (
                    downtime_df["timestamp"]
                    .diff()
                    .dt.total_seconds()
                )

                downtime_events = downtime_df[
                    downtime_df["time_gap"] > 90
                ].copy()

                downtime_events["estimated_downtime"] = (
                    downtime_events["time_gap"] - 30
                )

                total_downtime = downtime_events[
                    "estimated_downtime"
                ].sum()

                downtime_minutes = total_downtime / 60

                down_col1, down_col2 = st.columns(2)

                down_col1.metric(
                    "Downtime Events",
                    len(downtime_events)
                )

                down_col2.metric(
                    "Estimated Downtime",
                    f"{downtime_minutes:.2f} minutes"
                )

                if not downtime_events.empty:

                    st.warning(
                        "⚠️ Possible machine downtime detected."
                    )

                    st.dataframe(
                        downtime_events[
                            [
                                "timestamp",
                                "time_gap",
                                "estimated_downtime"
                            ]
                        ],
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.success(
                        "✅ No significant reading gaps detected."
                    )

            else:

                st.info(
                    "At least 2 readings are required "
                    "for downtime analysis."
                )

            st.divider()

            # =========================================
            # PRODUCTION EFFICIENCY
            # =========================================

            st.subheader("📈 Production Efficiency")

            if len(filtered_df) >= 2:

                efficiency_df = filtered_df.sort_values(
                    "timestamp"
                ).copy()

                first_reading = efficiency_df.iloc[0]
                last_reading = efficiency_df.iloc[-1]

                production_difference = (
                    last_reading["total"]
                    - first_reading["total"]
                )

                elapsed_seconds = (
                    last_reading["timestamp"]
                    - first_reading["timestamp"]
                ).total_seconds()

                if elapsed_seconds > 0:

                    elapsed_minutes = elapsed_seconds / 60
                    elapsed_hours = elapsed_seconds / 3600

                    production_per_minute = (
                        production_difference / elapsed_minutes
                    )

                    production_per_hour = (
                        production_difference / elapsed_hours
                    )

                    eff1, eff2, eff3 = st.columns(3)

                    eff1.metric(
                        "Production Per Minute",
                        f"{production_per_minute:.2f}"
                    )

                    eff2.metric(
                        "Production Per Hour",
                        f"{production_per_hour:.2f}"
                    )

                    eff3.metric(
                        "Total Production Change",
                        f"{production_difference:,.0f}"
                    )

                else:

                    st.info(
                        "Not enough elapsed time to calculate efficiency."
                    )

            else:

                st.info(
                    "At least 2 readings are required "
                    "for production efficiency."
                )

            st.divider()

            # =========================================
            # HISTORICAL READINGS
            # =========================================

            st.subheader("📋 Historical Machine Readings")

            display_df = filtered_df.sort_values(
                "timestamp",
                ascending=False
            )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No readings available for the selected date range."
            )

    else:

        st.info("No machine readings available yet.")

except requests.exceptions.RequestException as e:

    st.error(
        f"🔴 Unable to connect to Machine Monitoring API: {e}"
    )

except Exception as e:

    st.error(
        f"Unexpected error: {e}"
    )