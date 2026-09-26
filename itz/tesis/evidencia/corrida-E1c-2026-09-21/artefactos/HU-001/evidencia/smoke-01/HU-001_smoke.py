"""Smoke testing de HU-001 — Iniciar sesión con correo y contraseña
Generado por Loom (skill 08, ADR-0059) a partir del código del aplicativo y los casos de prueba de la HU.
Ejecución manual: TEST_BASE_URL, TEST_USER y TEST_PASSWORD como variables de entorno y `python este_archivo.py`."""

import re

from playwright.sync_api import Page, expect


def tc_001(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.locator('#email').fill(usuario)
    page.locator('#password').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home$'))
    expect(page.get_by_text('Bienvenido,')).to_be_visible()
    expect(page.get_by_role('button', name=re.compile('Cerrar sesión', re.I))).to_be_visible()
    expect(page.get_by_test_id('login-error')).to_have_count(0)


def tc_002(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.locator('#email').fill(usuario)
    page.locator('#password').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home$'))
    expect(page.get_by_text('Bienvenido,')).to_be_visible()
    # Solo aparece el correo de la cuenta autenticada
    expect(page.locator('dd').first).to_have_text(re.compile(re.escape(usuario), re.I))
    expect(page.locator('dd')).to_have_count(2)
    expect(page.get_by_test_id('home-error')).to_have_count(0)


def tc_003(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.locator('#email').fill(usuario)
    page.locator('#password').fill(contrasena + '_incorrecta')
    page.get_by_role('button', name='Iniciar sesión').click()
    error = page.get_by_test_id('login-error')
    expect(error).to_be_visible()
    expect(error).to_have_text(re.compile(r'Correo o contraseña incorrectos'))
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.locator('#email')).to_be_visible()


def tc_004(page, base_url, usuario, contrasena):
    """TC-004: Given un correo que no existe en el sistema. When ingresa ese correo con cualquier contras"""
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.get_by_label('Correo').first.fill('noexiste.qa.9731@example.com')
    page.get_by_role('textbox', name='Contraseña').first.fill('ClaveIncorrecta#123')
    page.get_by_role('button', name='Iniciar sesión').first.click()
    page.get_by_text('incorrect').first.wait_for(state='visible')
    expect(page.get_by_text('Correo o contraseña incorrectos.').first).to_be_visible()


def tc_005(page, base_url, usuario, contrasena):
    peticiones = []
    page.on('request', lambda r: peticiones.append(r.url) if r.url.endswith('/api/v1/auth/login') else None)
    boton = page.get_by_role('button', name='Iniciar sesión')

    # (a) correo vacío
    page.goto(base_url + '/login')
    page.locator('#password').fill('Alguna123!')
    boton.click()
    expect(page.get_by_text('El correo es obligatorio.')).to_be_visible()

    # (b) contraseña vacía
    page.goto(base_url + '/login')
    page.locator('#email').fill(usuario)
    boton.click()
    expect(page.get_by_text('La contraseña es obligatoria.')).to_be_visible()

    # (c) correo con formato inválido
    page.goto(base_url + '/login')
    page.locator('#email').fill('usuario@')
    page.locator('#password').fill('Alguna123!')
    boton.click()
    expect(page.get_by_text('El correo no tiene un formato válido.')).to_be_visible()

    expect(page).to_have_url(re.compile(r'/login'))
    assert len(peticiones) == 0


def tc_006(page, base_url, usuario, contrasena):
    otro_id = '00000000-0000-0000-0000-00000000b0b0'
    with page.expect_request(re.compile(r'/api/v1/auth/login$')) as info:
        page.goto(base_url + '/login')
        page.locator('#email').fill(usuario)
        page.locator('#password').fill(contrasena)
        page.get_by_role('button', name='Iniciar sesión').click()
    api_base = info.value.url[:-len('/api/v1/auth/login')]
    expect(page).to_have_url(re.compile(r'/home$'))
    token = page.evaluate("sessionStorage.getItem('auth.token')")

    resp = page.request.get(
        api_base + '/api/v1/users/' + otro_id,
        headers={'Authorization': 'Bearer ' + token},
    )
    assert resp.status in (403, 404)

    page.goto(base_url + '/users/' + otro_id)
    expect(page.get_by_text('Bienvenido,')).to_be_visible()
    expect(page.get_by_text(otro_id)).to_have_count(0)


def tc_007(page, base_url, usuario, contrasena):
    """TC-007: Given un visitante sin sesión. When navega directamente a una URL protegida y consulta un """
    page.goto(base_url + '/')
    page.goto(base_url + '/dashboard')
    page.goto(base_url + '/api/users')
    expect(page.get_by_text('Iniciar sesión').first).to_be_visible()
    page.goto(base_url + '/api/users')


def tc_008(page, base_url, usuario, contrasena):
    with page.expect_request(re.compile(r'/api/v1/auth/login$')) as info:
        page.goto(base_url + '/login')
        page.locator('#email').fill(usuario)
        page.locator('#password').fill(contrasena)
        page.get_by_role('button', name='Iniciar sesión').click()
    api_base = info.value.url[:-len('/api/v1/auth/login')]
    expect(page).to_have_url(re.compile(r'/home$'))

    # Invalida el token de sesión
    page.evaluate("sessionStorage.setItem('auth.token', 'token.expirado.invalido')")
    resp = page.request.get(
        api_base + '/api/v1/users/me',
        headers={'Authorization': 'Bearer token.expirado.invalido'},
    )
    assert resp.status == 401

    page.reload()
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_text('Bienvenido,')).to_have_count(0)


def tc_009(page, base_url, usuario, contrasena):
    """TC-009: Given la página de login cargada. When escribe una contraseña en el campo y envía el formu"""
    page.goto(base_url + '/')
    page.get_by_text('Contraseña').first.wait_for(state='visible')
    page.get_by_label('Contraseña').first.fill('TextoPrueba123')
    page.get_by_role('button', name='Iniciar sesión').first.click()
    expect(page.get_by_text('Contraseña').first).to_be_visible()
    page.locator('input[type=password]').first.click()


def tc_010(page, base_url, usuario, contrasena):
    with page.expect_request(re.compile(r'/api/v1/auth/login$')) as info:
        page.goto(base_url + '/login')
        page.locator('#email').fill(usuario)
        page.locator('#password').fill(contrasena)
        page.get_by_role('button', name='Iniciar sesión').click()
    api_base = info.value.url[:-len('/api/v1/auth/login')]
    expect(page).to_have_url(re.compile(r'/home$'))
    token = page.evaluate("sessionStorage.getItem('auth.token')")
    assert token

    page.get_by_role('button', name=re.compile('Cerrar sesión', re.I)).click()
    expect(page).to_have_url(re.compile(r'/login'))

    page.go_back()
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_text('Bienvenido,')).to_have_count(0)

    resp = page.request.get(
        api_base + '/api/v1/users/me',
        headers={'Authorization': 'Bearer ' + token},
    )
    assert resp.status == 401


def tc_011(page, base_url, usuario, contrasena):
    boton = page.get_by_role('button', name='Iniciar sesión')
    for i in range(7):
        page.goto(base_url + '/login')
        page.locator('#email').fill(usuario)
        page.locator('#password').fill('Incorrecta_' + str(i))
        boton.click()
        expect(page.get_by_test_id('login-error')).to_be_visible()

    page.goto(base_url + '/login')
    page.locator('#email').fill(usuario)
    page.locator('#password').fill(contrasena)
    boton.click()
    expect(page.get_by_test_id('login-error')).to_have_text(re.compile(r'Demasiados intentos'))
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_text('Bienvenido,')).to_have_count(0)


def tc_012(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.locator('#email').fill('  ' + usuario.upper() + '  ')
    page.locator('#password').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home$'))
    expect(page.get_by_text('Bienvenido,')).to_be_visible()
    expect(page.locator('dd').first).to_have_text(re.compile(re.escape(usuario), re.I))


def tc_013(page, base_url, usuario, contrasena):
    page.route(re.compile(r'/api/v1/auth/login$'), lambda route: route.fulfill(status=503, body='{}', content_type='application/json'))
    page.goto(base_url + '/login')
    page.locator('#email').fill(usuario)
    page.locator('#password').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    error = page.get_by_test_id('login-error')
    expect(error).to_be_visible()
    expect(error).to_contain_text('El servicio no está disponible en este momento')
    expect(page.locator('#email')).to_have_value(usuario)
    expect(page).to_have_url(re.compile(r'/login'))


def tc_014(page, base_url, usuario, contrasena):
    # Intento fallido y luego exitoso; la consulta del registro de auditoría no tiene pantalla en el código provisto,
    # por lo que se verifica el flujo de acceso del admin y que la contraseña no se expone en la UI.
    page.goto(base_url + '/login')
    page.locator('#email').fill(usuario)
    page.locator('#password').fill('Incorrecta_audit_1')
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_test_id('login-error')).to_be_visible()

    page.locator('#email').fill(usuario)
    page.locator('#password').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home$'))
    expect(page.get_by_text('Bienvenido,')).to_be_visible()
    expect(page.get_by_text(contrasena, exact=True)).to_have_count(0)


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
