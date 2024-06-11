import os
import requests
import streamlit as st
import pandas as pd

API_BASE_URL = os.getenv("TRMM_BASE_URL")
HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": os.getenv("TRMM_NP"),
}

@st.cache_data
def fetch_clients():
    """Fetch the list of clients."""
    response = requests.get(f'{API_BASE_URL}/clients/', headers=HEADERS)
    if response.status_code == 200:
        clients = response.json()
        return clients
    else:
        st.error(f'Failed to fetch clients: {response.status_code}')
        return []


def fetch_workstations(client_id):
    """Fetch the list of workstations for the specified client ID and return the response."""
    response = requests.get(f'{API_BASE_URL}/agents/?client={client_id}', headers=HEADERS)
    if response.status_code == 200:
        workstations = response.json()
        return workstations
    else:
        print(f'Failed to fetch workstations: {response.status_code}')
        return []

def page1():
    if "clients" not in st.session_state:
        st.session_state.clients = None
    if "workstations" not in st.session_state:
        st.session_state.workstations = None

    st.title("App za pristup podacima iz Tactical RMM-a 💻")

    with st.expander("Instrukcije za korišćenje"):
        st.write("""
        ... kada bude bilo potrebe...
        """)

    st.divider()

    col1, _, col2 = st.columns([3, 1, 5])

    with col1:
        st.session_state.clients = pd.DataFrame(fetch_clients())

        if st.session_state.clients is not None:
            df = st.session_state.clients
            display_df = df[['name', 'id', 'agent_count']]
            st.write("### Client Data")
            st.dataframe(display_df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8-sig')

            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name='clients.csv',
                mime='text/csv',
            )

    with col2:
        col21, _ = st.columns([1, 6])
        client_id = col21.text_input("Unesi ID klijenta")

        if client_id:
            if client_id.isdigit():
                client_id_int = int(client_id)
                if client_id_int in st.session_state.clients['id'].values:
                    workstations = fetch_workstations(int(client_id))

                    if workstations != []:
                        if workstations:
                            st.session_state.workstations = pd.DataFrame(workstations)

                        if st.session_state.workstations is not None:
                            df = st.session_state.workstations
                            display_df = df[['hostname', 'logged_username']]
                            st.write("### Workstation Data")
                            st.dataframe(display_df, use_container_width=True)
                            csv = df.to_csv(index=False).encode('utf-8-sig')

                            st.download_button(
                                label="Download Workstations as CSV",
                                data=csv,
                                file_name='workstations.csv',
                                mime='text/csv',
                            )
                    else:
                        st.warning("Nema radnih stanica za ovog klijenta.")
                else:
                    st.warning("Ne postoji klijent sa tim ID-jem.")
            else:
                st.warning("Samo intedžeri!")

def page2():
    st.title("Page 2")
    st.write("Random text")