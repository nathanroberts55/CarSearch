from nicegui import ui, App
from constants import MAKES_LIST
from get_data import get_car_df, convert_to_excel
from logger import logger

logger.name = __name__

# Set to Dark Mode
ui.dark_mode().enable()

ui.add_head_html(
    """
<style>
.ag-theme-balham {
    --ag-header-height: 30px;
    --ag-header-foreground-color: white;
    --ag-header-background-color: black;
    --ag-header-cell-hover-background-color: rgb(80, 40, 140);
    --ag-header-cell-moving-background-color: rgb(80, 40, 140);
}
.ag-grid-container {
    height: 80vh;
}

</style>
"""
)

# Initial Data
car_data_list, car_data_df = get_car_df()


def set_data():
    global car_data_list, car_data_df
    try:
        logger.info(
            f"Updating Data with New Inputs - Makes: {makes.value}, Zip: {zip.value}, Radius: {radius.value}, Max Price: {maxPrice.value}, Min Year: {minYear.value}"
        )
        car_data_list, car_data_df = get_car_df(
            makes=makes.value,
            zip=zip.value,
            radius=radius.value,
            priceMax=maxPrice.value,
            yearMin=minYear.value,
        )
        CarDataTable.refresh()
    except Exception as e:
        logger.exception(
            f"Was unable to Update Data with Input- Makes: {makes.value}, Zip: {zip.value}, Radius: {radius.value}, Max Price: {maxPrice.value}, Min Year: {minYear.value}, Exception: {e}"
        )


@ui.refreshable
def CarDataTable():
    for car in car_data_list:
        car.url = f'<a href="{car.url}" target="_blank">Link</a>'

    my_table: ui.aggrid = (
        ui.aggrid(
            {
                "defaultColDef": {"flex": 1},
                "columnDefs": [
                    {
                        "headerName": "Make",
                        "field": "make",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "Model",
                        "field": "model",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "Year",
                        "field": "year",
                        "filter": "agNumberColumnFilter",
                        "sortable": True,
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "Mileage",
                        "field": "mileage",
                        "filter": "agNumberColumnFilter",
                        "sortable": True,
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "Price",
                        "field": "price",
                        "valueFormatter": "'$' + value",
                        "filter": "agNumberColumnFilter",
                        "sortable": True,
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "Dealer",
                        "field": "dealership",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "Dealer Address",
                        "field": "dealer_address",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "City",
                        "field": "dealer_city",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "State",
                        "field": "dealer_state",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "Zip Code",
                        "field": "dealer_zip",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "Distance",
                        "field": "distance",
                        "filter": "agNumberColumnFilter",
                        "sortable": True,
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "link",
                        "field": "url",
                    },
                ],
                "multiSortKey": "ctrl",
                "rowSelection": "multiple",
                "rowData": car_data_list,
            },
            html_columns=[11],
        )
        .classes("min-h-max")
        .style("height: 80vh;")
    )

    my_table.call_api_method("setDomLayout", "autoHeight")
    my_table.call_api_method("setRowCount", 50)

    return my_table


with ui.row().classes("justify-center"):
    with ui.row().classes("w-full justify-center"):
        ui.label("Carfax Data Scrape").classes("text-4xl")

    with ui.row().classes("items-center justify-center w-full") as data_input:
        makes = ui.select(
            MAKES_LIST, multiple=True, value=MAKES_LIST[:5], label="Makes"
        ).classes("w-64")
        zip = ui.input(label="Zip Code", value="22030")
        radius = ui.number(label="Radius", value=50)
        maxPrice = ui.number(label="Max Price", value=17000)
        minYear = ui.number(label="Model Year Minimum", min=2004, max=2023, value=2008)

    with ui.row().classes("justify-center w-full") as submit_button:
        ui.button(
            "Submit",
            on_click=set_data,
        )

    ui.label("Cars for Sale").classes("text-4xl")
    CarDataTable()

    ui.button("Export", on_click=lambda: convert_to_excel(car_data_df))

ui.run(title="Custom Carfax Search")
