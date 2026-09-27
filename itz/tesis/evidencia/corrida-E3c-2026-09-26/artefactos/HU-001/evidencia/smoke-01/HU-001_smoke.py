"""Smoke testing de HU-001 — Autorregistro de cliente en el portal del taller con verificación de correo y vinculación a expediente existente
Generado por Loom (skill 08, ADR-0059) a partir del código del aplicativo y los casos de prueba de la HU.
Ejecución manual: TEST_BASE_URL, TEST_USER y TEST_PASSWORD como variables de entorno y `python este_archivo.py`."""

import re

from playwright.sync_api import Page, expect


def tc_016(page, base_url, usuario, contrasena):
    # Inicio de sesión (pantalla de acceso del portal)
    page.goto(base_url + '/login')
    page.get_by_label(re.compile(r'^Correo', re.I)).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña', re.I)).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'iniciar sesión', re.I)).click()
    expect(page).not_to_have_url(re.compile(r'/login'))

    # Módulo de Auditoría (no hay ruta en el router provisto: se usa el texto visible del menú)
    page.get_by_role('link', name=re.compile(r'auditor[ií]a', re.I)).first.click()
    expect(page.get_by_role('heading', name=re.compile(r'auditor[ií]a', re.I)).first).to_be_visible()
    filtro = page.get_by_label(re.compile(r'correo|buscar|filtr', re.I)).first
    expect(filtro).to_be_visible()
    filtro.fill('autorregistro')
    filtro.press('Enter')

    # Los 3 eventos: alta de la cuenta, verificación y vinculación
    expect(page.get_by_text(re.compile(r'alta|registro', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'verificaci[oó]n', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'vinculaci[oó]n', re.I)).first).to_be_visible()

    # Documentación de la API con los endpoints de registro y verificación
    page.goto(base_url + '/api/docs')
    expect(page.get_by_text(re.compile(r'/registro')).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'verificar', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'reenviar-verificacion', re.I)).first).to_be_visible()


def tc_030(page, base_url, usuario, contrasena):
    # Inicio de sesión del cliente A
    page.goto(base_url + '/login')
    page.get_by_label(re.compile(r'^Correo', re.I)).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña', re.I)).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'iniciar sesión', re.I)).click()
    expect(page).not_to_have_url(re.compile(r'/login'))

    # Menú del cliente: solo sus opciones, sin recepción ni admin
    expect(page.get_by_text(re.compile(r'Mis veh[ií]culos', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'Agenda del d[ií]a', re.I))).to_have_count(0)
    expect(page.get_by_role('link', name=re.compile(r'auditor[ií]a|usuarios|recepci[oó]n', re.I))).to_have_count(0)

    # URLs de otro cliente (ids de B no conocidos en el código: se usan identificadores ajenos)
    for ruta in ['/clientes/EB', '/vehiculos/VB', '/citas?cliente=EB']:
        page.goto(base_url + ruta)
        expect(page.get_by_text(re.compile(r'no encontrad|no existe|acceso denegado|no tienes permiso|403|404', re.I)).first).to_be_visible()
        expect(page.get_by_text(re.compile(r'placas', re.I))).to_have_count(0)


def tc_033(page, base_url, usuario, contrasena):
    # Inicio de sesión del admin
    page.goto(base_url + '/login')
    page.get_by_label(re.compile(r'^Correo', re.I)).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña', re.I)).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'iniciar sesión', re.I)).click()
    expect(page).not_to_have_url(re.compile(r'/login'))

    # Auditoría (texto visible del menú)
    page.get_by_role('link', name=re.compile(r'auditor[ií]a', re.I)).first.click()
    expect(page.get_by_role('heading', name=re.compile(r'auditor[ií]a', re.I)).first).to_be_visible()
    filtro = page.get_by_label(re.compile(r'correo|cuenta|buscar|filtr', re.I)).first
    expect(filtro).to_be_visible()
    filtro.fill('autorregistro')
    filtro.press('Enter')

    # Evento de alta con origen y aceptación del aviso
    expect(page.get_by_text(re.compile(r'autorregistro en el portal|AUTORREGISTRO', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'aviso de privacidad|aceptaci[oó]n', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'\d{1,2}[/:-]\d{2}')).first).to_be_visible()
    # Evento de verificación
    expect(page.get_by_text(re.compile(r'verificaci[oó]n', re.I)).first).to_be_visible()
    # Evento de vinculación con el identificador del expediente
    expect(page.get_by_text(re.compile(r'vinculaci[oó]n', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'expediente', re.I)).first).to_be_visible()


if __name__ == "__main__":
    import os

    from playwright.sync_api import sync_playwright

    BASE = os.environ.get("TEST_BASE_URL", 'https://taller-web-118746543308.us-central1.run.app').rstrip("/")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for nombre, funcion in sorted((n, f) for n, f in globals().items() if n.startswith("tc_") and callable(f)):
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            try:
                funcion(page, BASE, os.environ.get("TEST_USER", ""), os.environ.get("TEST_PASSWORD", ""))
                print(nombre, "pasa")
            except Exception as error:
                print(nombre, "FALLA", str(error).splitlines()[0][:160])
            page.close()
        browser.close()
