"""Smoke testing de HU-003 — Cerrar sesión manualmente y expirar sesión por inactividad
Generado por Loom (skill 08, ADR-0059) a partir del código del aplicativo y los casos de prueba de la HU.
Ejecución manual: TEST_BASE_URL, TEST_USER y TEST_PASSWORD como variables de entorno y `python este_archivo.py`."""

import re

from playwright.sync_api import Page, expect


def tc_001(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    page.get_by_test_id('logout-button').click()
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
    page.goto(base_url + '/perfil')
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
    expect(page.get_by_test_id('logout-button')).to_have_count(0)


def tc_002(page, base_url, usuario, contrasena):
    page.clock.install()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    page.clock.fast_forward('01:00:00')
    expect(page).to_have_url(re.compile(r'/login'))
    page.goto(base_url + '/home')
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()


def tc_003(page, base_url, usuario, contrasena):
    page.clock.install()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    page.clock.fast_forward('00:10')
    expect(page).to_have_url(re.compile(r'/home'))
    expect(page.get_by_test_id('logout-button')).to_be_visible()
    expect(page.get_by_test_id('login-expired-notice')).to_have_count(0)


def tc_004(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    page.get_by_test_id('logout-button').click()
    expect(page).to_have_url(re.compile(r'/login'))
    for ruta in ['/home', '/perfil', '/historial']:
        page.goto(base_url + ruta)
        expect(page).to_have_url(re.compile(r'/login'))
        expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
        expect(page.get_by_test_id('logout-button')).to_have_count(0)
    expect(page.get_by_label('Correo')).to_have_value('')
    expect(page.get_by_label('Contraseña')).to_have_value('')


def tc_005(page, base_url, usuario, contrasena):
    page.clock.install()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    page.clock.fast_forward('01:00:00')
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_label('Correo')).to_have_value('')
    expect(page.get_by_label('Contraseña')).to_have_value('')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    expect(page.get_by_test_id('logout-button')).to_be_visible()
    expect(page.get_by_test_id('login-expired-notice')).to_have_count(0)


def tc_006(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    with page.expect_response(re.compile(r'/api/v1/auth/login')) as resp_info:
        page.get_by_role('button', name='Iniciar sesión').click()
    login_url = resp_info.value.url
    api_base = login_url.split('/api/v1/auth/login')[0]
    expect(page).to_have_url(re.compile(r'/home'))
    token = page.evaluate("() => sessionStorage.getItem('auth.token')")
    assert token
    with page.expect_response(re.compile(r'/api/v1/auth/logout')):
        page.get_by_test_id('logout-button').click()
    expect(page).to_have_url(re.compile(r'/login'))
    respuesta = page.request.get(
        api_base + '/api/v1/users/me',
        headers={'Authorization': 'Bearer ' + token},
    )
    assert respuesta.status == 401


def tc_007(page, base_url, usuario, contrasena):
    """TC-007: Given un usuario autenticado que navegó por varias pantallas protegidas. When cierra sesió"""
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.get_by_label('Correo').first.fill(usuario)
    page.get_by_label('Contraseña').first.fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').first.click()
    page.get_by_text('Cerrar sesión').first.wait_for(state='visible')
    page.get_by_role('button', name='Cerrar sesión').first.click()
    page.keyboard.press('Alt+ArrowLeft')
    expect(page.get_by_text('Iniciar sesión').first).to_be_visible()


def tc_008(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    assert page.evaluate("() => sessionStorage.getItem('auth.token')") is not None
    page.get_by_test_id('logout-button').click()
    expect(page).to_have_url(re.compile(r'/login'))
    claves_session = page.evaluate("() => Object.keys(sessionStorage).filter(k => k.startsWith('auth.'))")
    claves_local = page.evaluate("() => Object.keys(localStorage).filter(k => k.startsWith('auth.'))")
    assert claves_session == []
    assert claves_local == []
    assert page.evaluate("() => sessionStorage.getItem('auth.token')") is None
    cookies = page.context.cookies()
    assert not [c for c in cookies if 'token' in c['name'].lower() or 'session' in c['name'].lower()]


def tc_009(page, base_url, usuario, contrasena):
    page.clock.install()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    page.clock.fast_forward('00:20')
    page.mouse.click(10, 300)
    page.clock.fast_forward('00:20')
    page.keyboard.press('Shift')
    page.clock.fast_forward('00:20')
    expect(page).to_have_url(re.compile(r'/home'))
    expect(page.get_by_test_id('logout-button')).to_be_visible()


def tc_010(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    expect(page.get_by_test_id('logout-button')).to_be_visible()

    def vencida(route):
        route.fulfill(
            status=401,
            content_type='application/json',
            body='{"detail": "La sesión venció por inactividad."}',
        )

    page.route(re.compile(r'/api/v1/(?!auth/login|auth/logout).*'), vencida)
    page.evaluate("() => sessionStorage.setItem('auth.token', sessionStorage.getItem('auth.token'))")
    page.reload()
    page.mouse.click(10, 300)
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_test_id('login-expired-notice')).to_be_visible()
    expect(page.get_by_test_id('login-expired-notice')).to_contain_text('venció por inactividad')


def tc_011(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    token = page.evaluate("() => sessionStorage.getItem('auth.token')")
    page2 = page.context.new_page()
    page2.goto(base_url + '/login')
    page2.evaluate("t => sessionStorage.setItem('auth.token', t)", token)
    page2.goto(base_url + '/home')
    expect(page2.get_by_test_id('logout-button')).to_be_visible()
    page.bring_to_front()
    page.get_by_test_id('logout-button').click()
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page2).to_have_url(re.compile(r'/login'))
    expect(page2.get_by_test_id('logout-button')).to_have_count(0)
    expect(page2.get_by_role('heading', name='Iniciar sesión')).to_be_visible()


def tc_012(page, base_url, usuario, contrasena):
    page.clock.install()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    token = page.evaluate("() => sessionStorage.getItem('auth.token')")
    page2 = page.context.new_page()
    page2.clock.install()
    page2.goto(base_url + '/login')
    page2.evaluate("t => sessionStorage.setItem('auth.token', t)", token)
    page2.goto(base_url + '/home')
    expect(page2.get_by_test_id('logout-button')).to_be_visible()
    page.clock.fast_forward('01:00:00')
    page2.clock.fast_forward('01:00:00')
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page2).to_have_url(re.compile(r'/login'))
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
    expect(page2.get_by_role('heading', name='Iniciar sesión')).to_be_visible()


def tc_013(page, base_url, usuario, contrasena):
    page.clock.install()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    page.clock.fast_forward('01:00:00')
    expect(page).to_have_url(re.compile(r'/login'))
    aviso = page.get_by_test_id('login-expired-notice')
    expect(aviso).to_be_visible()
    expect(aviso).to_contain_text('La sesión venció por inactividad')
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()


def tc_014(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    expect(page.get_by_test_id('logout-button')).to_be_visible()
    expect(page.get_by_test_id('logout-button')).to_have_text('Cerrar sesión')
    page.get_by_test_id('logout-button').click()
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()


def tc_015(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    with page.expect_response(re.compile(r'/api/v1/auth/login')) as resp_info:
        page.get_by_role('button', name='Iniciar sesión').click()
    api_base = resp_info.value.url.split('/api/v1/auth/login')[0]
    expect(page).to_have_url(re.compile(r'/home'))
    token = page.evaluate("() => sessionStorage.getItem('auth.token')")
    page2 = page.context.new_page()
    page2.goto(base_url + '/login')
    page2.evaluate("t => sessionStorage.setItem('auth.token', t)", token)
    page2.goto(base_url + '/home')
    expect(page2.get_by_test_id('logout-button')).to_be_visible()
    page.bring_to_front()
    page.get_by_test_id('logout-button').click()
    expect(page).to_have_url(re.compile(r'/login'))
    respuesta = page.request.post(
        api_base + '/api/v1/auth/logout',
        headers={'Authorization': 'Bearer ' + token},
    )
    assert respuesta.status < 500
    expect(page2).to_have_url(re.compile(r'/login'))
    expect(page2.get_by_role('heading', name='Iniciar sesión')).to_be_visible()


def tc_016(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/home'))
    enlace = page.get_by_role('link', name=re.compile(r'Bit[áa]cora|Auditor[íi]a', re.I))
    expect(enlace.first).to_be_visible()
    enlace.first.click()
    expect(page.get_by_text(re.compile(r'cierre manual|logout', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'inactividad', re.I)).first).to_be_visible()


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
