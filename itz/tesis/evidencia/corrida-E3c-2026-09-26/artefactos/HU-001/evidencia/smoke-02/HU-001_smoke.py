"""Smoke testing de HU-001 — Autorregistro de cliente en el portal del taller con verificación de correo y vinculación a expediente existente
Generado por Loom (skill 08, ADR-0059) a partir del código del aplicativo y los casos de prueba de la HU.
Ejecución manual: TEST_BASE_URL, TEST_USER y TEST_PASSWORD como variables de entorno y `python este_archivo.py`."""

import re

from playwright.sync_api import Page, expect


def tc_016(page, base_url, usuario, contrasena):
    # Correo del cliente que se autorregistró, se vinculó a su expediente y verificó su correo (dato de prueba)
    correo_cliente = 'cliente.vinculado@example.com'

    # Inicio de sesión del admin
    page.goto(base_url + '/login')
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña')).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'iniciar sesi[oó]n|entrar', re.I)).click()
    expect(page).not_to_have_url(re.compile(r'/login'))

    # Módulo de Auditoría
    page.get_by_role('link', name=re.compile(r'Auditor[ií]a', re.I)).first.click()
    expect(page.get_by_role('heading', name=re.compile(r'Auditor[ií]a', re.I)).first).to_be_visible()

    filtro = page.get_by_label(re.compile(r'correo|usuario|cuenta', re.I)).first
    filtro.fill(correo_cliente)
    boton_filtrar = page.get_by_role('button', name=re.compile(r'filtrar|buscar|aplicar', re.I))
    if boton_filtrar.count() > 0:
        boton_filtrar.first.click()
    else:
        filtro.press('Enter')

    # Tres eventos: alta, verificación y vinculación
    filas = page.get_by_role('row').filter(has_text=correo_cliente)
    expect(filas).to_have_count(3)
    expect(page.get_by_text(re.compile(r'alta|registro|cuenta creada', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'verificaci[oó]n|verificad', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'vinculaci[oó]n|vinculad', re.I)).first).to_be_visible()

    # Documentación de la API
    page.goto(base_url + '/api/docs')
    expect(page.get_by_text(re.compile(r'/registro\b')).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'/registro/.*verific', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'reenviar-verificacion')).first).to_be_visible()

    # Campos y códigos de respuesta del endpoint de registro
    page.get_by_text(re.compile(r'^/registro$')).first.click()
    expect(page.get_by_text('correo').first).to_be_visible()
    expect(page.get_by_text(re.compile(r'aceptaAvisoPrivacidad')).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'^201$')).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'^409$')).first).to_be_visible()


def tc_030(page, base_url, usuario, contrasena):
    # Identificadores del cliente B (datos de prueba)
    expediente_b = 'EB'
    vehiculo_b = 'VB'
    nombre_b = 'Cliente B'
    placas_b = 'PLACAS-B'

    # El cliente A inicia sesión
    page.goto(base_url + '/login')
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña')).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'iniciar sesi[oó]n|entrar', re.I)).click()
    expect(page).not_to_have_url(re.compile(r'/login'))

    # Menú del cliente: solo sus opciones, sin recepción ni admin
    expect(page.get_by_text(re.compile(r'Mis veh[ií]culos', re.I)).first).to_be_visible()
    expect(page.get_by_role('link', name=re.compile(r'Agenda del d[ií]a', re.I))).to_have_count(0)
    expect(page.get_by_role('link', name=re.compile(r'Auditor[ií]a', re.I))).to_have_count(0)
    expect(page.get_by_role('link', name=re.compile(r'Usuarios|Administraci[oó]n|Recepci[oó]n', re.I))).to_have_count(0)

    denegado = re.compile(r'no encontrad|acceso denegado|no tienes permiso|403|404', re.I)
    for ruta in ['/clientes/' + expediente_b, '/vehiculos/' + vehiculo_b, '/citas?cliente=' + expediente_b]:
        page.goto(base_url + ruta)
        expect(page.get_by_text(denegado).first).to_be_visible()
        expect(page.get_by_text(nombre_b)).to_have_count(0)
        expect(page.get_by_text(placas_b)).to_have_count(0)


def tc_033(page, base_url, usuario, contrasena):
    # Datos de prueba: cuenta autorregistrada y expediente preexistente EX
    correo_cliente = 'cliente.preexistente@example.com'
    expediente_ex = 'EX'

    page.goto(base_url + '/login')
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña')).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'iniciar sesi[oó]n|entrar', re.I)).click()
    expect(page).not_to_have_url(re.compile(r'/login'))

    page.get_by_role('link', name=re.compile(r'Auditor[ií]a', re.I)).first.click()
    expect(page.get_by_role('heading', name=re.compile(r'Auditor[ií]a', re.I)).first).to_be_visible()

    filtro = page.get_by_label(re.compile(r'correo|usuario|cuenta', re.I)).first
    filtro.fill(correo_cliente)
    boton_filtrar = page.get_by_role('button', name=re.compile(r'filtrar|buscar|aplicar', re.I))
    if boton_filtrar.count() > 0:
        boton_filtrar.first.click()
    else:
        filtro.press('Enter')

    fecha_hora = re.compile(r'\d{1,4}[-/]\d{1,2}[-/]\d{1,4}.*\d{1,2}:\d{2}')

    # Alta con origen autorregistro y fecha de aceptación del aviso
    alta = page.get_by_role('row').filter(has_text=re.compile(r'alta|registro|cuenta creada', re.I)).first
    expect(alta).to_be_visible()
    expect(alta).to_contain_text(re.compile(r'autorregistro', re.I))
    expect(alta).to_contain_text(re.compile(r'aviso', re.I))
    expect(alta).to_contain_text(fecha_hora)

    # Verificación con fecha y hora
    verificacion = page.get_by_role('row').filter(has_text=re.compile(r'verificaci[oó]n|verificad', re.I)).first
    expect(verificacion).to_be_visible()
    expect(verificacion).to_contain_text(fecha_hora)

    # Vinculación con el identificador del expediente
    vinculacion = page.get_by_role('row').filter(has_text=re.compile(r'vinculaci[oó]n|vinculad', re.I)).first
    expect(vinculacion).to_be_visible()
    expect(vinculacion).to_contain_text(expediente_ex)


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
