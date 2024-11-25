import flet as ft


def TextField(label: str) -> ft.TextField:
    return ft.TextField(label=label.capitalize(),
                        height=30, 
                        text_vertical_align=ft.VerticalAlignment.START,
                        text_size=12,
                        read_only=True,
                        label_style=ft.TextStyle(
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            size=12)
                        )

def TextFieldMultiLine(label:str, value:str="")->ft.TextField:
    return ft.TextField(label=label.capitalize(),
                        value=value,
                        height=90, 
                        text_vertical_align=ft.VerticalAlignment.START,
                        text_size=12,
                        multiline=True,
                        min_lines=3,
                        max_lines=3,
                        read_only=True,
                        label_style=ft.TextStyle(
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            size=12)
                        )

def ListDropDown()->ft.dropdown:
    return ft.Dropdown(
            width=70,
            text_size=12,
            autofocus=True,
            options=[],
        )
 
def ButtonDate(on_change, page:ft.Page)-> ft.ElevatedButton:
    return ft.ElevatedButton(
        "15-04-1977",
        icon=ft.icons.CALENDAR_MONTH,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=30,
        width=160,
        on_click=lambda e: page.open(
            ft.DatePicker(
                on_change=on_change,
            )
        ),
    )
    
def Button(label:str, icon:ft.icons = ft.icons.FIND_IN_PAGE_OUTLINED)-> ft.ElevatedButton:
    return ft.ElevatedButton(
        label,
        icon=icon,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=30,
        width=165,
    )