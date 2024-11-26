import streamlit as st
import requests

def check_server(client):
    if not client.ping():
        st.toast("Elastic Search Server Is Not Running!")

def display_results(client, query, searchtype):
    check_server(client)
    getreq = {
        searchtype: {"tags": query}
    }
    results = client.search(index="flickrphotos", query=getreq)

    # Create four columns for displaying images
    cols = st.columns(4)
    col_heights = [0, 0, 0, 0]  # Track heights of each column to balance image distribution
    displayed_images = 0

    for hit in results["hits"]['hits']:
        if displayed_images >= 10:
            break

        image_data = hit["_source"]
        image_url = (
            "http://farm" + image_data['flickr_farm'] + ".staticflickr.com/"
            + image_data['flickr_server'] + "/" + image_data["id"] + "_"
            + image_data['flickr_secret'] + ".jpg"
        )

        col_id = col_heights.index(min(col_heights))  # Find the shortest column to place the image
        with st.spinner("Loading Image"):
            response = requests.get(image_url)
            if response.status_code == 200:
                cols[col_id].image(image_url)
                col_heights[col_id] += 1
                displayed_images += 1


