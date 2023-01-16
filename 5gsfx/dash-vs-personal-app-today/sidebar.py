from dash import html


def SideBar():
    return html.Div(
        [
            html.Img(
                src="assets/shocked.jpg",
                width=120,
                height=120,
                className="rounded-circle",
            ),
            html.H3("Admin", className="mt-4"),  # Name
            html.P("Good morning"),  # Des
        ],
        className="text-white d-flex flex-column align-items-center pt-4",
    )

