# Static Gantt Chart
    st.subheader("📊 Gantt Chart (Static)")
    fig = plot_gantt_chart(result)
    st.pyplot(fig)

    # Animated Gantt Chart
    st.subheader("🎞️ Animated Gantt Chart")
    animate_gantt_chart(result, delay=0.6)