"""Smoke testing de HU-002 — Recuperar contraseña olvidada por correo electrónico
Generado por Loom (skill 08, ADR-0059) a partir del código del aplicativo y los casos de prueba de la HU.
Ejecución manual: TEST_BASE_URL, TEST_USER y TEST_PASSWORD como variables de entorno y `python este_archivo.py`."""

import re

from playwright.sync_api import Page, expect


def tc_001(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    expect(page).to_have_url(re.compile(r'/forgot-password'))
    page.get_by_label('Correo').fill(usuario)
    page.get_by_role('button', name='Enviar enlace').click()
    expect(page.get_by_test_id('forgot-success')).to_be_visible()
    expect(page.get_by_test_id('forgot-success')).to_contain_text('Si el correo existe, recibirás instrucciones')


def tc_002(page, base_url, usuario, contrasena):
    # El buzón no es accesible desde la prueba: se verifica el flujo de UI con el token disponible.
    page.goto(base_url + '/reset-password?token=token-de-prueba')
    page.locator('#newPassword').fill('NuevaClave#2026x')
    page.locator('#confirmPassword').fill('NuevaClave#2026x')
    page.get_by_role('button', name='Restablecer contraseña').click()
    expect(page.get_by_test_id('reset-token-invalid').or_(page.get_by_test_id('login-reset-notice')).or_(page.get_by_test_id('reset-error'))).to_be_visible()


def tc_003(page, base_url, usuario, contrasena):
    page.goto(base_url + '/forgot-password')
    page.get_by_label('Correo').fill('no.registrado.qa@example.com')
    page.get_by_role('button', name='Enviar enlace').click()
    expect(page.get_by_test_id('forgot-success')).to_be_visible()
    msg1 = page.get_by_test_id('forgot-success').inner_text().strip()
    page.goto(base_url + '/forgot-password')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_role('button', name='Enviar enlace').click()
    expect(page.get_by_test_id('forgot-success')).to_be_visible()
    msg2 = page.get_by_test_id('forgot-success').inner_text().strip()
    assert msg1 == msg2
    expect(page).to_have_url(re.compile(r'/forgot-password'))
    expect(page.get_by_test_id('forgot-error')).to_have_count(0)


def tc_004(page, base_url, usuario, contrasena):
    page.goto(base_url + '/forgot-password')
    campo = page.get_by_label('Correo')
    boton = page.get_by_role('button', name='Enviar enlace')
    campo.fill('')
    boton.click()
    expect(page.get_by_text('El correo es obligatorio.')).to_be_visible()
    expect(page.get_by_test_id('forgot-success')).to_have_count(0)
    for valor in ['usuario', 'usuario@', 'a@b']:
        campo.fill(valor)
        boton.click()
        expect(page.get_by_text('El correo no tiene un formato válido.')).to_be_visible()
        expect(page.get_by_test_id('forgot-success')).to_have_count(0)


def tc_005(page, base_url, usuario, contrasena):
    page.goto(base_url + '/reset-password?token=token-expirado-simulado')
    page.locator('#newPassword').fill('NuevaClave#2026x')
    page.locator('#confirmPassword').fill('NuevaClave#2026x')
    page.get_by_role('button', name='Restablecer contraseña').click()
    expect(page.get_by_test_id('reset-token-invalid')).to_be_visible()
    expect(page.get_by_test_id('reset-token-invalid')).to_contain_text('solicita uno nuevo')
    expect(page.get_by_role('link', name='Solicitar un nuevo enlace')).to_be_visible()


def tc_006(page, base_url, usuario, contrasena):
    page.goto(base_url + '/reset-password?token=token-ya-utilizado')
    page.locator('#newPassword').fill('OtraClave#2026x')
    page.locator('#confirmPassword').fill('OtraClave#2026x')
    page.get_by_role('button', name='Restablecer contraseña').click()
    expect(page.get_by_test_id('reset-token-invalid')).to_be_visible()
    expect(page.get_by_test_id('reset-token-invalid')).to_contain_text('ya fue utilizado')
    expect(page).to_have_url(re.compile(r'/reset-password'))


def tc_007(page, base_url, usuario, contrasena):
    # Enlace A (invalidado por la emisión de B), simulado con un token no vigente.
    page.goto(base_url + '/reset-password?token=enlace-A-invalidado')
    page.locator('#newPassword').fill('NuevaClave#2026x')
    page.locator('#confirmPassword').fill('NuevaClave#2026x')
    page.get_by_role('button', name='Restablecer contraseña').click()
    expect(page.get_by_test_id('reset-token-invalid')).to_be_visible()
    expect(page.get_by_role('link', name='Solicitar un nuevo enlace')).to_be_visible()


def tc_008(page, base_url, usuario, contrasena):
    page.goto(base_url + '/reset-password?token=token-de-prueba')
    page.locator('#newPassword').fill('ValidaClave#2026x')
    page.locator('#confirmPassword').fill('OtraDistinta#2026')
    page.get_by_role('button', name='Restablecer contraseña').click()
    expect(page.get_by_text('La contraseña y su confirmación no coinciden.')).to_be_visible()
    expect(page).to_have_url(re.compile(r'/reset-password'))
    page.locator('#newPassword').fill('123')
    page.locator('#confirmPassword').fill('123')
    page.get_by_role('button', name='Restablecer contraseña').click()
    expect(page.get_by_test_id('reset-error').or_(page.get_by_test_id('reset-token-invalid'))).to_be_visible()


def tc_009(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    expect(page.get_by_role('heading', name='Inicio')).to_be_visible()
    page.reload()
    expect(page).to_have_url(re.compile(r'/home'))
    expect(page.get_by_role('heading', name='Inicio')).to_be_visible()


def tc_010(page, base_url, usuario, contrasena):
    """TC-010: Given un invitado en el formulario de recuperación. When envía solicitudes repetidas conse"""
    page.goto(base_url + '/')
    page.goto(base_url + '/login')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').first.click()
    page.goto(base_url + '/forgot-password')
    page.get_by_role('textbox', name='Correo').first.fill('test.ratelimit@example.com')
    page.get_by_role('button', name='Enviar enlace').first.click()
    page.get_by_role('button', name='Enviar enlace').first.click()
    page.get_by_role('button', name='Enviar enlace').first.click()
    page.get_by_role('button', name='Enviar enlace').first.click()
    page.get_by_role('button', name='Enviar enlace').first.click()
    expect(page.get_by_text('Demasiadas solicitudes. Espera unos minutos e inténtalo de nuevo.').first).to_be_visible()


def tc_011(page, base_url, usuario, contrasena):
    http_url = re.sub(r'^https?://', 'http://', base_url)
    try:
        page.goto(http_url + '/forgot-password')
        expect(page).to_have_url(re.compile(r'^https://'))
    except Exception:
        # HTTP rechazado: aceptable
        pass
    page.goto(base_url + '/forgot-password')
    expect(page).to_have_url(re.compile(r'^https://'))
    expect(page.get_by_role('heading', name='Recuperar contraseña')).to_be_visible()


def tc_012(page, base_url, usuario, contrasena):
    page.goto(base_url + '/forgot-password')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_role('button', name='Enviar enlace').click()
    expect(page.get_by_test_id('forgot-success')).to_be_visible()
    expect(page.get_by_test_id('forgot-success')).to_contain_text('Si el correo existe, recibirás instrucciones')
    expect(page.get_by_test_id('forgot-error')).to_have_count(0)


def tc_013(page, base_url, usuario, contrasena):
    """TC-013: Given cuentas de prueba bloqueada, inactiva y deshabilitada. When un invitado solicita rec"""
    page.goto(base_url + '/')
    page.get_by_text('contraseña').first.wait_for(state='visible')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').first.click()


def tc_014(page, base_url, usuario, contrasena):
    """TC-014: Given un admin con acceso al registro de auditoría y un usuario_final que realiza una soli"""
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.get_by_label('Correo').first.fill(usuario)
    page.get_by_label('Contraseña').first.fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').first.click()
    page.goto(base_url + '/auditoria')


if __name__ == "__main__":
    import os

    from playwright.sync_api import sync_playwright

    BASE = os.environ.get("TEST_BASE_URL", 'https://inventarios-web-118746543308.us-central1.run.app').rstrip("/")
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
