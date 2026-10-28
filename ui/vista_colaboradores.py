"""Pestaña «Colaboradores»: eventos con colaboradores."""

from __future__ import annotations

import flet as ft

from core import cruzar_colaboradores as colaboradores

from .comunes import VistaBase, bloque_titulo, mostrar_dialogo
from .seleccion import CampoArchivo


class VistaColaboradores(VistaBase):
    """Genera ``DATOS/colaboradores.xlsx`` desde el archivo maestro."""

    titulo = "Colaboradores"
    icono = ft.Image(
        src="/Users/alexisjankowicz/Python/flet_scoring_poli/src/icons/colaborar.png",  # Ruta relativa dentro de la carpeta assets
        width=32,
        height=32,
        fit=ft.BoxFit.CONTAIN,
    )
    etiqueta_registro = "Registro — Agregar Colaboradores al archivo Maestro"

    def __init__(self, page: ft.Page) -> None:
        super().__init__(page)
        self.archivo = CampoArchivo(
            page, "Archivo maestro (CMU):", "Seleccionar archivo maestro (CMU)"
        )
        self.btn_procesar = ft.Button(
            "Procesar archivo",
            icon=ft.Icons.PLAY_ARROW,
            bgcolor="#2196F3",
            color=ft.Colors.WHITE,
            on_click=self.on_procesar,
        )

    def build(self) -> ft.Control:
        ayuda = ft.Container(
            bgcolor="#F1F5F9",
            border_radius=8,
            alignment=ft.Alignment.CENTER_LEFT,
            padding=4,
            expand=1,
            content=ft.Column(
                [
                    ft.Text("Reglas aplicadas", size=13, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "  • Al archivo maestro se incrustan 5 columnas seguidas al 'Operador' con titulo 'Colaborador' y el número de colaborador (1 a 5).",
                        size=12,
                    ),
                    ft.Text(
                        f"Salida: {colaboradores.DATOS_DIR / colaboradores.ARCHIVO_SALIDA}",
                        size=12,
                        italic=True,
                    ),
                ],
                spacing=3,
            ),
        )
        return ft.Column(
            [
                bloque_titulo(
                    "Colaboradores",
                    "Agrega información de colaboradores al archivo maestro.",
                ),
                self.archivo.build(),
                ft.Row([self.btn_procesar, self.progreso], spacing=12),
                ft.Row(
                    [ayuda, self.registro.campo],
                    spacing=10,
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            expand=True,
            spacing=10,
        )

    async def on_procesar(self, e: ft.Event[ft.Button]) -> None:
        self.progreso.visible = True
        self.btn_procesar.disabled = True
        self.registro.limpiar()
        self.page.update()
        try:
            ruta = validar_ruta(self.archivo.valor, "archivo maestro (CMU)")
            resultado = await self.registro.ejecutar(
                colaboradores.procesar, ruta, self.registro.log
            )
            self.log("")
            self.log(resultado.resumen())
            await mostrar_dialogo(self.page, "Proceso completado", resultado.resumen())
        except Exception as exc:  # noqa: BLE001 - se informa al usuario
            self.log(f"\n⛔ ERROR: {exc}")
            await mostrar_dialogo(self.page, "Error", str(exc), es_error=True)
        finally:
            self.progreso.visible = False
            self.btn_procesar.disabled = False
            self.page.update()
