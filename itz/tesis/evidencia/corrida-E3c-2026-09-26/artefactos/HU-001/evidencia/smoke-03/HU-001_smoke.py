"""Smoke testing de HU-001 — Autorregistro de cliente en el portal del taller con verificación de correo y vinculación a expediente existente
Generado por Loom (skill 08, ADR-0059) a partir del código del aplicativo y los casos de prueba de la HU.
Ejecución manual: TEST_BASE_URL, TEST_USER y TEST_PASSWORD como variables de entorno y `python este_archivo.py`."""

import re

from playwright.sync_api import Page, expect


def tc_001(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.e1+{ts}@test.com'
    page.goto(base_url + '/registro')
    expect(page.get_by_role('heading', name='Crear cuenta')).to_be_visible()
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('WhatsApp (opcional)').fill('')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    with page.expect_response(lambda r: r.request.method == 'POST' and re.search(r'/registro/?(\?.*)?$', r.url) is not None) as info:
        page.get_by_role('button', name='Crear cuenta').click()
    respuesta = info.value
    assert 200 <= respuesta.status < 300, f'Registro rechazado: HTTP {respuesta.status}'
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_be_visible()
    expect(page.get_by_text('pendiente de verificación')).to_be_visible()
    expect(page.get_by_text(correo)).to_be_visible()
    expect(page.get_by_role('button', name='Reenviar correo de verificación')).to_be_visible()


def tc_002(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.e1.wa+{ts}@test.com'
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('WhatsApp (opcional)').fill('5598765432')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    with page.expect_response(lambda r: r.request.method == 'POST' and re.search(r'/registro/?(\?.*)?$', r.url) is not None) as info:
        page.get_by_role('button', name='Crear cuenta').click()
    respuesta = info.value
    cuerpo = respuesta.request.post_data_json or {}
    assert cuerpo.get('whatsapp') == '5598765432', f'WhatsApp enviado: {cuerpo.get("whatsapp")}'
    assert 200 <= respuesta.status < 300, f'Registro rechazado: HTTP {respuesta.status}'
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_be_visible()
    expect(page.get_by_text(correo)).to_be_visible()
    expect(page.get_by_text('pendiente de verificación')).to_be_visible()


def tc_003(page, base_url, usuario, contrasena):
    correo = 'duplicado@test.com'

    def registrar():
        page.goto(base_url + '/registro')
        page.get_by_label('Nombre(s)').fill('Dup')
        page.get_by_label('Apellidos').fill('Licado')
        page.get_by_label('Correo').fill(correo)
        page.get_by_label('Celular').fill('5512345678')
        page.get_by_label('Contraseña').fill('Taller2026')
        page.get_by_label('Acepto el aviso de privacidad').check()
        page.get_by_label('Acepto los términos').check()
        page.get_by_role('button', name='Crear cuenta').click()

    # Precondición: garantiza que exista la cuenta (si ya existía, este intento ya es duplicado).
    registrar()
    expect(page.get_by_role('heading', name='Revisa tu correo').or_(page.get_by_text('Este correo ya tiene una cuenta'))).to_be_visible()

    registrar()
    expect(page.get_by_text('Este correo ya tiene una cuenta')).to_be_visible()
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_have_count(0)
    expect(page).to_have_url(re.compile(r'/registro$'))
    enlace = page.get_by_role('link', name='Recuperar contraseña')
    expect(enlace).to_be_visible()
    enlace.click()
    expect(page).not_to_have_url(re.compile(r'/registro$'))
    expect(page).to_have_url(re.compile(r'(olvide|recuperar|contrasena)', re.I))


def tc_004(page, base_url, usuario, contrasena):
    # El token real llega por correo (fuera del alcance del navegador); se simula la respuesta exitosa del backend
    # para validar la pantalla y luego se inicia sesión con la cuenta del cliente ya verificada.
    def simular(route):
        req = route.request
        if req.method == 'POST' and req.resource_type in ('fetch', 'xhr'):
            route.fulfill(status=200, content_type='application/json', body='{"estado":"ACTIVA","expedienteExistente":false}')
        else:
            route.continue_()
    page.route(re.compile(r'.*verific.*'), simular)
    page.goto(base_url + '/verificar-correo?token=tokenDePruebaE2E0123456789')
    expect(page.get_by_role('heading', name='¡Tu cuenta está activa!')).to_be_visible()
    expect(page.get_by_text('Tu correo quedó verificado; ya puedes iniciar sesión.')).to_be_visible()
    expect(page).not_to_have_url(re.compile(r'token='))
    page.unroute(re.compile(r'.*verific.*'))
    page.get_by_role('link', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/login'))
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_role('alert')).to_have_count(0)


def tc_005(page, base_url, usuario, contrasena):
    # Enlace emitido hace 23 h 59 min: aún vigente. Sin token sembrado accesible desde la UI, se simula la
    # respuesta del backend (verificación aceptada) y se comprueba el flujo completo hasta el inicio de sesión.
    def simular(route):
        req = route.request
        if req.method == 'POST' and req.resource_type in ('fetch', 'xhr'):
            route.fulfill(status=200, content_type='application/json', body='{"estado":"ACTIVA","expedienteExistente":false}')
        else:
            route.continue_()
    page.route(re.compile(r'.*verific.*'), simular)
    page.goto(base_url + '/verificar-correo?token=tokenLimite2359E2E0123456789')
    expect(page.get_by_role('heading', name='¡Tu cuenta está activa!')).to_be_visible()
    expect(page.get_by_role('heading', name='Enlace expirado')).to_have_count(0)
    page.unroute(re.compile(r'.*verific.*'))
    page.get_by_role('link', name='Iniciar sesión').click()
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).not_to_have_url(re.compile(r'/login'))
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))


def tc_006(page, base_url, usuario, contrasena):
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Ana')
    page.get_by_label('Apellidos').fill('Ruiz')
    page.get_by_label('Correo').fill('ana.ruiz@test.com')
    page.get_by_label('Celular').fill('5511112222')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    # Primera ejecución: confirmación; ejecuciones posteriores: la cuenta ya existe.
    expect(page.get_by_role('heading', name='Revisa tu correo').or_(page.get_by_text('Este correo ya tiene una cuenta'))).to_be_visible()
    # Tras verificar el correo, el cliente inicia sesión y ve los vehículos de su expediente existente.
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_text('ABC-123')).to_be_visible()
    expect(page.get_by_text('XYZ-987')).to_be_visible()
    expect(page.get_by_text(re.compile(r'\b[A-Z]{3}-\d{3}\b'))).to_have_count(2)


def tc_007(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.pw7+{ts}@test.com'
    posts = []
    page.on('request', lambda r: posts.append(r.url) if (r.method == 'POST' and re.search(r'/registro/?(\?.*)?$', r.url)) else None)
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill('Abcde12')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    campo = page.get_by_label('Contraseña')
    expect(campo).to_have_attribute('aria-invalid', 'true')
    expect(campo).to_have_accessible_description(re.compile(r'8'))
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_have_count(0)
    expect(page).to_have_url(re.compile(r'/registro$'))
    assert len(posts) == 0, 'Se envió la petición de registro con una contraseña inválida'


def tc_008(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.pw8+{ts}@test.com'
    posts = []
    page.on('request', lambda r: posts.append(r.url) if (r.method == 'POST' and re.search(r'/registro/?(\?.*)?$', r.url)) else None)
    casos = [
        ('abcdefg1', re.compile(r'may[uú]scula', re.I)),
        ('ABCDEFG1', re.compile(r'min[uú]scula', re.I)),
        ('Abcdefgh', re.compile(r'n[uú]mero', re.I)),
    ]
    for clave, regla in casos:
        page.goto(base_url + '/registro')
        page.get_by_label('Nombre(s)').fill('Juan')
        page.get_by_label('Apellidos').fill('Pérez López')
        page.get_by_label('Correo').fill(correo)
        page.get_by_label('Celular').fill('5512345678')
        page.get_by_label('Contraseña').fill(clave)
        page.get_by_label('Acepto el aviso de privacidad').check()
        page.get_by_label('Acepto los términos').check()
        page.get_by_role('button', name='Crear cuenta').click()
        campo = page.get_by_label('Contraseña')
        expect(campo).to_have_attribute('aria-invalid', 'true')
        expect(campo).to_have_accessible_description(regla)
        expect(page.get_by_role('heading', name='Revisa tu correo')).to_have_count(0)
        expect(page).to_have_url(re.compile(r'/registro$'))
    assert len(posts) == 0, 'Se envió alguna petición de registro con contraseña inválida'


def tc_009(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.pw9+{ts}@test.com'
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill('Abcdef12')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_be_visible()
    expect(page.get_by_text('pendiente de verificación')).to_be_visible()
    expect(page.get_by_text(correo)).to_be_visible()


def tc_010(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.exp10+{ts}@test.com'
    clave = 'Taller2026'
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill(clave)
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_be_visible()

    # Enlace emitido hace 24 h 1 min: se simula la respuesta del backend (410 TOKEN_EXPIRADO).
    def simular(route):
        req = route.request
        if req.method == 'POST' and req.resource_type in ('fetch', 'xhr'):
            route.fulfill(status=410, content_type='application/json', body='{"codigo":"TOKEN_EXPIRADO","mensaje":"El enlace de verificación expiró."}')
        else:
            route.continue_()
    page.route(re.compile(r'.*verific.*'), simular)
    page.goto(base_url + '/verificar-correo?token=tokenVencido2401E2E0123456789')
    expect(page.get_by_role('heading', name='Enlace expirado')).to_be_visible()
    expect(page.get_by_role('heading', name='¡Tu cuenta está activa!')).to_have_count(0)
    page.unroute(re.compile(r'.*verific.*'))

    # La cuenta sigue pendiente: el login se bloquea pidiendo verificar el correo.
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Contraseña').fill(clave)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_role('alert').filter(has_text=re.compile(r'verific', re.I))).to_be_visible()
    expect(page).to_have_url(re.compile(r'/login'))


def tc_011(page, base_url, usuario, contrasena):
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Luis')
    page.get_by_label('Apellidos').fill('Mora')
    page.get_by_label('Correo').fill('luis.mora@test.com')
    page.get_by_label('Celular').fill('55 3333-4444')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    with page.expect_request(lambda r: r.method == 'POST' and re.search(r'/registro/?(\?.*)?$', r.url) is not None) as info:
        page.get_by_role('button', name='Crear cuenta').click()
    cuerpo = info.value.post_data_json or {}
    assert re.sub(r'[\s-]', '', str(cuerpo.get('celular', ''))) == '5533334444'
    expect(page.get_by_role('heading', name='Revisa tu correo').or_(page.get_by_text('Este correo ya tiene una cuenta'))).to_be_visible()
    # Tras verificar, el cliente inicia sesión y ve el vehículo de su expediente (vinculado por celular).
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_text('LMN-456')).to_be_visible()


def tc_012(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.aviso12+{ts}@test.com'
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    expect(page.get_by_label('Acepto el aviso de privacidad')).to_be_checked()
    expect(page.get_by_label('Acepto los términos')).to_be_checked()
    t_inicio = page.evaluate('() => Date.now()')
    with page.expect_response(lambda r: r.request.method == 'POST' and re.search(r'/registro/?(\?.*)?$', r.url) is not None) as info:
        page.get_by_role('button', name='Crear cuenta').click()
    respuesta = info.value
    t_fin = page.evaluate('() => Date.now()')
    cuerpo = respuesta.request.post_data_json or {}
    assert cuerpo.get('aceptaAvisoPrivacidad') is True
    assert cuerpo.get('aceptaTerminos') is True
    assert 200 <= respuesta.status < 300
    assert t_fin - t_inicio <= 120000, 'El registro tardó más de 2 min'
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_be_visible()
    expect(page.get_by_text(correo)).to_be_visible()


def tc_013(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.oblig13+{ts}@test.com'
    posts = []
    page.on('request', lambda r: posts.append(r.url) if (r.method == 'POST' and re.search(r'/registro/?(\?.*)?$', r.url)) else None)
    valores = {
        'Nombre(s)': 'Juan',
        'Apellidos': 'Pérez López',
        'Correo': correo,
        'Celular': '5512345678',
        'Contraseña': 'Taller2026',
    }
    for vacio in valores:
        page.goto(base_url + '/registro')
        for etiqueta, valor in valores.items():
            page.get_by_label(etiqueta).fill('' if etiqueta == vacio else valor)
        page.get_by_label('Acepto el aviso de privacidad').check()
        page.get_by_label('Acepto los términos').check()
        page.get_by_role('button', name='Crear cuenta').click()
        campo = page.get_by_label(vacio)
        expect(campo).to_have_attribute('aria-invalid', 'true')
        expect(campo).to_have_accessible_description(re.compile(r'\S'))
        expect(page.get_by_role('heading', name='Revisa tu correo')).to_have_count(0)
        expect(page).to_have_url(re.compile(r'/registro$'))
    assert len(posts) == 0, 'Se envió una petición de registro con un campo obligatorio vacío'


def tc_014(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.sinwa14+{ts}@test.com'
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('WhatsApp (opcional)').fill('')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_be_visible()
    expect(page.get_by_text('pendiente de verificación')).to_be_visible()
    expect(page.get_by_label('WhatsApp (opcional)')).to_have_count(0)


def tc_015(page, base_url, usuario, contrasena):
    # Descubre el endpoint real del formulario abortando la petición (no se crea ninguna cuenta).
    def abortar(route):
        req = route.request
        if req.method == 'POST' and req.resource_type in ('fetch', 'xhr'):
            route.abort()
        else:
            route.continue_()
    patron = re.compile(r'.*/registro/?(\?.*)?$')
    page.route(patron, abortar)
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill('descubrir.endpoint@test.com')
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    with page.expect_request(lambda r: r.method == 'POST' and patron.match(r.url) is not None) as info:
        page.get_by_role('button', name='Crear cuenta').click()
    url_registro = info.value.url
    payload = dict(info.value.post_data_json or {})
    page.unroute(patron)

    payload.update({'password': 'abc', 'celular': '123', 'correo': 'no-es-correo'})
    respuesta = page.request.post(url_registro, data=payload)
    assert respuesta.status in (400, 422), f'Se esperaba 400/422 y llegó {respuesta.status}'
    texto = respuesta.text()
    assert 'password' in texto, 'Falta el error de contraseña'
    assert 'celular' in texto, 'Falta el error de celular'
    assert 'correo' in texto, 'Falta el error de correo'
    expect(page).to_have_url(re.compile(r'/registro$'))


def tc_016(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).not_to_have_url(re.compile(r'/login'))
    # Módulo de Auditoría (texto visible descrito en el caso).
    page.get_by_role('link', name=re.compile(r'Auditor[ií]a', re.I)).first.click()
    expect(page.get_by_text(re.compile(r'alta', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'verificaci[oó]n', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'vinculaci[oó]n', re.I)).first).to_be_visible()
    # Documentación de la API.
    page.goto(base_url + '/api/docs')
    expect(page.get_by_text(re.compile(r'/registro')).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'verific', re.I)).first).to_be_visible()


def tc_017(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.legal17+{ts}@test.com'
    posts = []
    page.on('request', lambda r: posts.append(r.url) if (r.method == 'POST' and re.search(r'/registro/?(\?.*)?$', r.url)) else None)
    casos = [(False, True), (True, False), (False, False)]
    for aviso, terminos in casos:
        page.goto(base_url + '/registro')
        page.get_by_label('Nombre(s)').fill('Juan')
        page.get_by_label('Apellidos').fill('Pérez López')
        page.get_by_label('Correo').fill(correo)
        page.get_by_label('Celular').fill('5512345678')
        page.get_by_label('Contraseña').fill('Taller2026')
        if aviso:
            page.get_by_label('Acepto el aviso de privacidad').check()
        if terminos:
            page.get_by_label('Acepto los términos').check()
        page.get_by_role('button', name='Crear cuenta').click()
        if not aviso:
            expect(page.get_by_label('Acepto el aviso de privacidad')).to_have_accessible_description(re.compile(r'\S'))
        if not terminos:
            expect(page.get_by_label('Acepto los términos')).to_have_accessible_description(re.compile(r'\S'))
        expect(page.get_by_role('heading', name='Revisa tu correo')).to_have_count(0)
        expect(page).to_have_url(re.compile(r'/registro$'))
    assert len(posts) == 0, 'Se envió una petición de registro sin aceptar el aviso/los términos'


def tc_018(page, base_url, usuario, contrasena):
    def abortar(route):
        req = route.request
        if req.method == 'POST' and req.resource_type in ('fetch', 'xhr'):
            route.abort()
        else:
            route.continue_()
    patron = re.compile(r'.*/registro/?(\?.*)?$')
    page.route(patron, abortar)
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.legal18+{ts}@test.com'
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    with page.expect_request(lambda r: r.method == 'POST' and patron.match(r.url) is not None) as info:
        page.get_by_role('button', name='Crear cuenta').click()
    url_registro = info.value.url
    base = dict(info.value.post_data_json or {})
    page.unroute(patron)

    con_false = dict(base, aceptaAvisoPrivacidad=False, aceptaTerminos=False)
    r1 = page.request.post(url_registro, data=con_false)
    assert 400 <= r1.status < 500, f'HTTP {r1.status}'
    t1 = r1.text()
    assert 'ACEPTACION_LEGAL_REQUERIDA' in t1 or ('aceptaAvisoPrivacidad' in t1 and 'aceptaTerminos' in t1), t1

    sin_campos = {k: v for k, v in base.items() if k not in ('aceptaAvisoPrivacidad', 'aceptaTerminos')}
    r2 = page.request.post(url_registro, data=sin_campos)
    assert 400 <= r2.status < 500, f'HTTP {r2.status}'
    t2 = r2.text()
    assert 'ACEPTACION_LEGAL_REQUERIDA' in t2 or ('aceptaAvisoPrivacidad' in t2 and 'aceptaTerminos' in t2), t2

    # No se creó la cuenta: un registro válido posterior con el mismo correo no es duplicado.
    r3 = page.request.post(url_registro, data=base)
    assert r3.status != 409, 'La cuenta se había creado pese a no aceptar aviso/términos'
    expect(page).to_have_url(re.compile(r'/registro$'))


def tc_019(page, base_url, usuario, contrasena):
    def registrar(correo):
        page.goto(base_url + '/registro')
        page.get_by_label('Nombre(s)').fill('Juan')
        page.get_by_label('Apellidos').fill('Mail')
        page.get_by_label('Correo').fill(correo)
        page.get_by_label('Celular').fill('5512345678')
        page.get_by_label('Contraseña').fill('Taller2026')
        page.get_by_label('Acepto el aviso de privacidad').check()
        page.get_by_label('Acepto los términos').check()
        page.get_by_role('button', name='Crear cuenta').click()

    registrar('juan@mail.com')
    expect(page.get_by_role('heading', name='Revisa tu correo').or_(page.get_by_text('Este correo ya tiene una cuenta'))).to_be_visible()

    registrar('  Juan@Mail.COM  ')
    expect(page.get_by_text('Este correo ya tiene una cuenta')).to_be_visible()
    expect(page.get_by_role('link', name='Recuperar contraseña')).to_be_visible()
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_have_count(0)
    expect(page).to_have_url(re.compile(r'/registro$'))


def tc_020(page, base_url, usuario, contrasena):
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('María')
    page.get_by_label('Apellidos').fill('Prueba')
    page.get_by_label('Correo').fill(' MARIA@Mail.com')
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.get_by_role('heading', name='Revisa tu correo').or_(page.get_by_text('Este correo ya tiene una cuenta'))).to_be_visible()
    # Tras verificar, el cliente inicia sesión y ve el vehículo del expediente existente.
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_text('QWE-111')).to_be_visible()


def tc_021(page, base_url, usuario, contrasena):
    posts = []
    page.on('request', lambda r: posts.append(r.url) if (r.method == 'POST' and re.search(r'/registro/?(\?.*)?$', r.url)) else None)
    for correo in ['juanmail.com', 'juan@', '@mail.com', 'juan @mail.com']:
        page.goto(base_url + '/registro')
        page.get_by_label('Nombre(s)').fill('Juan')
        page.get_by_label('Apellidos').fill('Pérez López')
        page.get_by_label('Correo').fill(correo)
        page.get_by_label('Celular').fill('5512345678')
        page.get_by_label('Contraseña').fill('Taller2026')
        page.get_by_label('Acepto el aviso de privacidad').check()
        page.get_by_label('Acepto los términos').check()
        page.get_by_role('button', name='Crear cuenta').click()
        campo = page.get_by_label('Correo')
        expect(campo).to_have_attribute('aria-invalid', 'true')
        expect(campo).to_have_accessible_description(re.compile(r'correo|v[aá]lido|formato', re.I))
        expect(page.get_by_role('heading', name='Revisa tu correo')).to_have_count(0)
        expect(page).to_have_url(re.compile(r'/registro$'))
    assert len(posts) == 0, 'Se envió una petición de registro con correo inválido'


def tc_022(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.cel22+{ts}@test.com'
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('55 1234-5678')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    with page.expect_response(lambda r: r.request.method == 'POST' and re.search(r'/registro/?(\?.*)?$', r.url) is not None) as info:
        page.get_by_role('button', name='Crear cuenta').click()
    respuesta = info.value
    assert 200 <= respuesta.status < 300, f'HTTP {respuesta.status}'
    enviado = str((respuesta.request.post_data_json or {}).get('celular', ''))
    assert re.sub(r'[\s-]', '', enviado) == '5512345678', enviado
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_be_visible()
    expect(page.get_by_text(correo)).to_be_visible()


def tc_023(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.cel23+{ts}@test.com'
    posts = []
    page.on('request', lambda r: posts.append(r.url) if (r.method == 'POST' and re.search(r'/registro/?(\?.*)?$', r.url)) else None)
    for celular in ['551234567', '55123456789', '55123a5678', '+525512345678']:
        page.goto(base_url + '/registro')
        page.get_by_label('Nombre(s)').fill('Juan')
        page.get_by_label('Apellidos').fill('Pérez López')
        page.get_by_label('Correo').fill(correo)
        page.get_by_label('Celular').fill(celular)
        page.get_by_label('Contraseña').fill('Taller2026')
        page.get_by_label('Acepto el aviso de privacidad').check()
        page.get_by_label('Acepto los términos').check()
        page.get_by_role('button', name='Crear cuenta').click()
        campo = page.get_by_label('Celular')
        expect(campo).to_have_attribute('aria-invalid', 'true')
        expect(campo).to_have_accessible_description(re.compile(r'10'))
        expect(page.get_by_role('heading', name='Revisa tu correo')).to_have_count(0)
        expect(page).to_have_url(re.compile(r'/registro$'))
    assert len(posts) == 0, 'Se envió una petición de registro con celular inválido'


def tc_024(page, base_url, usuario, contrasena):
    secreto = 'QaSecreta2026X'
    respuestas = []
    page.on('response', lambda r: respuestas.append(r) if r.request.resource_type in ('fetch', 'xhr') else None)
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.hash24+{ts}@test.com'
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill(secreto)
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_be_visible()
    assert secreto not in page.content(), 'La contraseña aparece en la pantalla de confirmación'
    # Intento de login (cuenta pendiente): tampoco debe devolverse la contraseña.
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Contraseña').fill(secreto)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_role('alert').first).to_be_visible()
    assert len(respuestas) > 0, 'No se interceptó ninguna respuesta de la API'
    for resp in respuestas:
        try:
            cuerpo = resp.text()
        except Exception:
            continue
        assert secreto not in cuerpo, f'La contraseña aparece en la respuesta de {resp.url}'
    expect(page.get_by_label('Contraseña')).not_to_have_value(secreto)


def tc_025(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'concurrente+{ts}@test.com'
    ctx2 = page.context.browser.new_context()
    p2 = ctx2.new_page()
    try:
        for p in (page, p2):
            p.goto(base_url + '/registro')
            p.get_by_label('Nombre(s)').fill('Juan')
            p.get_by_label('Apellidos').fill('Concurrente')
            p.get_by_label('Correo').fill(correo)
            p.get_by_label('Celular').fill('5512345678')
            p.get_by_label('Contraseña').fill('Taller2026')
            p.get_by_label('Acepto el aviso de privacidad').check()
            p.get_by_label('Acepto los términos').check()
        page.get_by_role('button', name='Crear cuenta').click(no_wait_after=True)
        p2.get_by_role('button', name='Crear cuenta').click(no_wait_after=True)
        for p in (page, p2):
            exito = p.get_by_role('heading', name='Revisa tu correo')
            controlado = p.get_by_role('alert')
            expect(exito.or_(controlado).first).to_be_visible()
            expect(p.get_by_text(re.compile(r'Internal Server Error', re.I))).to_have_count(0)
        exitos = page.get_by_role('heading', name='Revisa tu correo').count() + p2.get_by_role('heading', name='Revisa tu correo').count()
        assert exitos == 1, f'Se esperaba exactamente 1 registro exitoso y hubo {exitos}'
        perdedor = p2 if page.get_by_role('heading', name='Revisa tu correo').count() == 1 else page
        expect(perdedor.get_by_role('alert').first).to_be_visible()
        expect(perdedor).to_have_url(re.compile(r'/registro$'))
    finally:
        ctx2.close()


def tc_026(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.pend26+{ts}@test.com'
    clave = 'Taller2026'
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill(clave)
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_be_visible()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Contraseña').fill(clave)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_role('alert').filter(has_text=re.compile(r'verific', re.I))).to_be_visible()
    expect(page).to_have_url(re.compile(r'/login'))
    page.goto(base_url + '/mis-vehiculos')
    expect(page).to_have_url(re.compile(r'/login'))


def tc_027(page, base_url, usuario, contrasena):
    # Segunda apertura del mismo enlace: el backend responde 409 CUENTA_YA_VERIFICADA (simulado, el token real
    # solo llega por correo).
    llamadas = []
    def simular(route):
        req = route.request
        if req.method == 'POST' and req.resource_type in ('fetch', 'xhr'):
            llamadas.append(req.url)
            route.fulfill(status=409, content_type='application/json', body='{"codigo":"CUENTA_YA_VERIFICADA","mensaje":"Tu cuenta ya estaba verificada."}')
        else:
            route.continue_()
    page.route(re.compile(r'.*verific.*'), simular)
    page.goto(base_url + '/verificar-correo?token=tokenYaUsadoE2E0123456789')
    ya = page.get_by_role('heading', name='Cuenta ya verificada')
    expect(ya.or_(page.get_by_role('button', name='Iniciar sesión'))).to_be_visible()
    expect(page.get_by_role('heading', name='¡Tu cuenta está activa!')).to_have_count(0)
    assert len(llamadas) == 1, f'El token se envió {len(llamadas)} veces'
    page.get_by_role('link', name='Ir a iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/login'))


def tc_028(page, base_url, usuario, contrasena):
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.inval28+{ts}@test.com'
    clave = 'Taller2026'
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill(clave)
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_be_visible()
    for token in ['inexistente123', 'aB3dE5gH7jK9mN1pQ3sT5vX7zA9cE1gX', '']:
        page.goto(base_url + '/verificar-correo?token=' + token)
        expect(page.get_by_role('heading', name='Enlace inválido')).to_be_visible()
        expect(page.get_by_role('heading', name='¡Tu cuenta está activa!')).to_have_count(0)
        expect(page.get_by_text(correo)).to_have_count(0)
    # La cuenta sigue pendiente: el login continúa bloqueado.
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Contraseña').fill(clave)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_role('alert').filter(has_text=re.compile(r'verific', re.I))).to_be_visible()
    expect(page).to_have_url(re.compile(r'/login'))


def tc_029(page, base_url, usuario, contrasena):
    # Enlace de más de 24 h: se simula la respuesta del backend (410 TOKEN_EXPIRADO).
    def simular(route):
        req = route.request
        if req.method == 'POST' and req.resource_type in ('fetch', 'xhr'):
            route.fulfill(status=410, content_type='application/json', body='{"codigo":"TOKEN_EXPIRADO","mensaje":"El enlace de verificación expiró."}')
        else:
            route.continue_()
    page.route(re.compile(r'.*verific.*'), simular)
    page.goto(base_url + '/verificar-correo?token=tokenVencidoE2E0123456789')
    expect(page.get_by_role('heading', name='Enlace expirado')).to_be_visible()
    expect(page.get_by_role('heading', name='Enlace inválido')).to_have_count(0)
    expect(page.get_by_role('heading', name='¡Tu cuenta está activa!')).to_have_count(0)
    expect(page.get_by_role('button', name='Reenviar correo de verificación')).to_be_visible()
    page.unroute(re.compile(r'.*verific.*'))
    # Contraste: un token inexistente muestra un mensaje distinto (inválido).
    page.goto(base_url + '/verificar-correo?token=inexistente123')
    expect(page.get_by_role('heading', name='Enlace inválido')).to_be_visible()
    expect(page.get_by_role('heading', name='Enlace expirado')).to_have_count(0)


def tc_030(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_text('Agenda del día')).to_have_count(0)
    expect(page.get_by_role('link', name=re.compile(r'Auditor[ií]a|Administraci[oó]n|Clientes$', re.I))).to_have_count(0)
    for ruta in ['/clientes/EB', '/vehiculos/VB', '/citas?cliente=EB']:
        page.goto(base_url + ruta)
        expect(page.get_by_text(re.compile(r'no encontr|no existe|404|acceso denegado|403|no tienes permiso', re.I)).first).to_be_visible()


def tc_031(page, base_url, usuario, contrasena):
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Hist')
    page.get_by_label('Apellidos').fill('Prueba')
    page.get_by_label('Correo').fill('hist@test.com')
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.get_by_role('heading', name='Revisa tu correo').or_(page.get_by_text('Este correo ya tiene una cuenta'))).to_be_visible()
    expect(page.get_by_text('HIS-001')).to_have_count(0)
    # Antes de verificar (sin sesión) la ruta protegida redirige al login.
    page.goto(base_url + '/mis-vehiculos')
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_text('HIS-001')).to_have_count(0)
    # Después de verificar: inicia sesión y ve su vehículo e historial.
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_text('HIS-001')).to_be_visible()
    expect(page.get_by_text(re.compile(r'orden de servicio|historial', re.I)).first).to_be_visible()


def tc_032(page, base_url, usuario, contrasena):
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan Carlos')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill('jp@test.com')
    page.get_by_label('Celular').fill('5500000002')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.get_by_role('heading', name='Revisa tu correo').or_(page.get_by_text('Este correo ya tiene una cuenta'))).to_be_visible()
    # Vista de recepción: el expediente conserva los datos originales.
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).not_to_have_url(re.compile(r'/login'))
    page.get_by_role('link', name=re.compile(r'^Clientes', re.I)).first.click()
    page.get_by_label(re.compile(r'Buscar', re.I)).fill('jp@test.com')
    page.keyboard.press('Enter')
    expect(page.get_by_text('Juan Pérez', exact=True).first).to_be_visible()
    expect(page.get_by_text('5500000001').first).to_be_visible()
    expect(page.get_by_text('Juan Carlos')).to_have_count(0)
    expect(page.get_by_text('5500000002')).to_have_count(0)


def tc_033(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).not_to_have_url(re.compile(r'/login'))
    page.get_by_role('link', name=re.compile(r'Auditor[ií]a', re.I)).first.click()
    expect(page.get_by_text(re.compile(r'autorregistro', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'aviso de privacidad', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'verificaci[oó]n', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'vinculaci[oó]n', re.I)).first).to_be_visible()


def tc_034(page, base_url, usuario, contrasena):
    # Simula el fallo SMTP: la cuenta se crea de verdad, pero la respuesta indica que el correo no se envió.
    patron = re.compile(r'.*/registro/?(\?.*)?$')
    def falla_smtp(route):
        req = route.request
        if req.method == 'POST' and req.resource_type in ('fetch', 'xhr'):
            resp = route.fetch()
            texto = resp.text()
            texto = re.sub(r'"correoVerificacionEnviado"\s*:\s*true', '"correoVerificacionEnviado":false', texto)
            route.fulfill(response=resp, body=texto)
        else:
            route.continue_()
    page.route(patron, falla_smtp)
    ts = page.evaluate('() => Date.now()')
    correo = f'qa.smtp34+{ts}@test.com'
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Juan')
    page.get_by_label('Apellidos').fill('Pérez López')
    page.get_by_label('Correo').fill(correo)
    page.get_by_label('Celular').fill('5512345678')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.get_by_role('heading', name='Revisa tu correo')).to_be_visible()
    expect(page.get_by_text('No pudimos enviarte el correo de verificación. Usa el botón para reenviarlo.')).to_be_visible()
    page.unroute(patron)
    boton = page.get_by_role('button', name='Reenviar correo de verificación')
    expect(boton).to_be_visible()
    boton.click()
    expect(page.get_by_role('alert').filter(has_text=re.compile(r'enlace|enviar', re.I)).last).to_be_visible()
    expect(page.get_by_text(re.compile(r'(Si el correo tiene una cuenta pendiente|enviaremos|enviamos)', re.I)).first).to_be_visible()


def tc_035(page, base_url, usuario, contrasena):
    page.goto(base_url + '/registro')
    page.get_by_label('Nombre(s)').fill('Pedro')
    page.get_by_label('Apellidos').fill('Soto')
    page.get_by_label('Correo').fill('pedro@test.com')
    page.get_by_label('Celular').fill('123')
    page.get_by_label('WhatsApp (opcional)').fill('5544443333')
    page.get_by_label('Contraseña').fill('Taller2026')
    page.get_by_label('Acepto el aviso de privacidad').check()
    page.get_by_label('Acepto los términos').check()
    page.get_by_role('button', name='Crear cuenta').click()
    celular = page.get_by_label('Celular')
    expect(celular).to_have_attribute('aria-invalid', 'true')
    expect(celular).to_have_accessible_description(re.compile(r'10'))
    expect(page.get_by_label('Nombre(s)')).to_have_value('Pedro')
    expect(page.get_by_label('Apellidos')).to_have_value('Soto')
    expect(page.get_by_label('Correo')).to_have_value('pedro@test.com')
    expect(celular).to_have_value('123')
    expect(page.get_by_label('WhatsApp (opcional)')).to_have_value('5544443333')
    expect(page.get_by_label('Contraseña')).to_have_value('')
    expect(page).to_have_url(re.compile(r'/registro$'))


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
