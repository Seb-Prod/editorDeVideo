import flet as ft


def TextField(label: str, value: str = "", multiline: bool = False, min_lines: int = 1, max_lines: int = 1, height=30) -> ft.TextField:
    return ft.TextField(label=label.capitalize(),
                        value=value, 
                        height=height, 
                        text_vertical_align=ft.VerticalAlignment.START,
                        text_size=12,
                        multiline=multiline,
                        min_lines=min_lines,
                        max_lines=max_lines,
                        read_only=True,
                        label_style=ft.TextStyle(
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            size=12)
                        )
