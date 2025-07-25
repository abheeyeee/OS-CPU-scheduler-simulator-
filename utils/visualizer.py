import matplotlib.pyplot as plt
import time
import streamlit as st

def plot_gantt_chart(schedule_result):
    
    gantt = schedule_result["gantt"]
    fig, ax = plt.subplots()

    for pid, start, end in gantt:
        ax.broken_barh([(start, end - start)], (10, 9), facecolors='tab:blue')
        ax.text(start + (end - start) / 2, 14, f'P{pid}', ha='center', va='center', color='white')

    ax.set_ylim(5, 25)
    ax.set_xlim(0, gantt[-1][2] + 2)
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title('Gantt Chart')
    ax.grid(True)
    plt.tight_layout()

    return fig


def animate_gantt_chart(schedule_result, delay=0.5):
     
    gantt = schedule_result["gantt"]
    fig, ax = plt.subplots()
    
    ax.set_ylim(5, 25)
    ax.set_xlim(0, gantt[-1][2] + 2)
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title('Animated Gantt Chart')
    ax.grid(True)

    chart_placeholder = st.empty()

    for pid, start, end in gantt:
        ax.broken_barh([(start, end - start)], (10, 9), facecolors='tab:blue')
        ax.text(start + (end - start) / 2, 14, f'P{pid}', ha='center', va='center', color='white')

        chart_placeholder.pyplot(fig)
        time.sleep(delay)

    return fig
