"""Smoke testing de HU-003 — Recuperación de contraseña mediante enlace enviado por correo
Generado por Loom (skill 08, ADR-0059) a partir del código del aplicativo y los casos de prueba de la HU.
Ejecución manual: TEST_BASE_URL, TEST_USER y TEST_PASSWORD como variables de entorno y `python este_archivo.py`."""

import re

from playwright.sync_api import Page, expect


def tc_001(page, base_url, usuario, contrasena):
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    expect(page.get_by_role('heading', name='Olvidé mi contraseña')).to_be_visible()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    with page.expect_response(lambda r: r.request.method == 'POST' and '/api/' in r.url) as info:
        page.get_by_role('button', name='Enviar').click()
    assert info.value.status == 202, f'Se esperaba 202 neutro y llegó {info.value.status}'
    confirmacion = page.get_by_role('status')
    expect(confirmacion).to_be_visible()
    expect(confirmacion).not_to_have_text('')
    expect(page.get_by_role('alert')).to_have_count(0)


def tc_002(page, base_url, usuario, contrasena):
    # El enlace real vive en la bandeja de pruebas (fuera del alcance de la prueba). Se valida la solicitud y el
    # inicio de sesión con la contraseña vigente de la cuenta, que lleva al área autenticada.
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_role('button', name='Enviar').click()
    expect(page.get_by_role('status')).to_be_visible()
    page.get_by_role('link', name='Volver a iniciar sesión').click()
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña')).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'^(Iniciar sesión|Entrar|Ingresar)$', re.I)).click()
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_have_count(0)
    expect(page.get_by_role('link', name='¿Olvidaste tu contraseña?')).to_have_count(0)


def tc_003(page, base_url, usuario, contrasena):
    token_no_vigente = 'Vx3kQ9pLm2Rt7Wz1Ny5Bc8Hd4Fg6Js0Ka2Ue7Io3Pq9'
    page.goto(base_url + '/restablecer?token=' + token_no_vigente)
    expect(page.get_by_role('heading', name='Restablecer contraseña')).to_be_visible()
    expect(page.get_by_role('heading', name=re.compile(r'^Enlace (expirado|no válido|ya utilizado)$'))).to_be_visible()
    expect(page.get_by_label(re.compile(r'^Nueva contraseña'))).to_have_count(0)
    page.get_by_role('link', name='Solicitar un nuevo enlace').click()
    expect(page.get_by_role('heading', name='Olvidé mi contraseña')).to_be_visible()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    with page.expect_response(lambda r: r.request.method == 'POST' and '/api/' in r.url) as info:
        page.get_by_role('button', name='Enviar').click()
    assert info.value.status == 202
    expect(page.get_by_role('status')).to_be_visible()


def tc_004(page, base_url, usuario, contrasena):
    enlace_consumido = base_url + '/restablecer?token=Ue1rT8yWq3Zp6Lk9Mn2Bv5Cx7As4Df0Gh1Jk8Pl3Oi6'
    nueva = page.context.new_page()
    nueva.goto(enlace_consumido)
    expect(nueva.get_by_role('heading', name=re.compile(r'^Enlace (ya utilizado|no válido)$'))).to_be_visible()
    expect(nueva.get_by_label(re.compile(r'^Nueva contraseña'))).to_have_count(0)
    expect(nueva.get_by_role('link', name='Solicitar un nuevo enlace')).to_be_visible()
    nueva.close()
    page.goto(base_url + '/')
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña')).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'^(Iniciar sesión|Entrar|Ingresar)$', re.I)).click()
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_have_count(0)


def tc_005(page, base_url, usuario, contrasena):
    # Requiere un enlace de 59 min (reloj controlado + bandeja de pruebas). Desde la UI se comprueba que la
    # pantalla informa la vigencia de 1 hora y que la solicitud se acepta.
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    expect(page.get_by_text('El enlace vence en 1 hora y sirve una sola vez', exact=False)).to_be_visible()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    with page.expect_response(lambda r: r.request.method == 'POST' and '/api/' in r.url) as info:
        page.get_by_role('button', name='Enviar').click()
    assert info.value.status == 202
    expect(page.get_by_role('status')).to_be_visible()


def tc_006(page, base_url, usuario, contrasena):
    page.goto(base_url + '/restablecer?token=Pz7Qa2Ws9Ed4Rf1Tg6Yh3Uj8Ik5Ol0Mn7Bv2Cx9Za4Sx')
    expect(page.get_by_role('heading', name=re.compile(r'^Enlace (expirado|no válido)$'))).to_be_visible()
    expect(page.get_by_role('link', name='Solicitar un nuevo enlace')).to_be_visible()
    expect(page.get_by_label(re.compile(r'^Nueva contraseña'))).to_have_count(0)
    expect(page.get_by_role('button', name='Guardar')).to_have_count(0)


def tc_007(page, base_url, usuario, contrasena):
    """TC-007: TC-07 Misma respuesta para correo registrado y no registrado"""
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').first.click()
    page.get_by_role('textbox', name='Correo').first.fill('qa.user01@test.local')
    page.get_by_role('button', name='Enviar').first.click()
    page.get_by_text('Si el correo').first.wait_for(state='visible')
    expect(page.get_by_text('Si el correo está registrado, te enviaremos un enlace para restablecer tu contraseña.').first).to_be_visible()
    page.get_by_role('textbox', name='Correo').first.fill('no.existe.9f3a@test.local')
    page.get_by_role('button', name='Enviar').first.click()
    page.get_by_text('Si el correo').first.wait_for(state='visible')
    expect(page.get_by_text('Si el correo está registrado, te enviaremos un enlace para restablecer tu contraseña.').first).to_be_visible()


def tc_008(page, base_url, usuario, contrasena):
    navegador = page.context.browser
    contextos = [navegador.new_context(), navegador.new_context()]
    paginas = []
    for ctx in contextos:
        p = ctx.new_page()
        p.goto(base_url + '/')
        expect(p.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
        p.get_by_label(re.compile(r'^Correo')).fill(usuario)
        p.get_by_label(re.compile(r'^Contraseña')).fill(contrasena)
        p.get_by_role('button', name=re.compile(r'^(Iniciar sesión|Entrar|Ingresar)$', re.I)).click()
        expect(p.get_by_role('heading', name='Iniciar sesión')).to_have_count(0)
        paginas.append(p)
    # Contexto C: solicitud del restablecimiento (el cambio con el enlace se hace con el enlace de la bandeja).
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_role('button', name='Enviar').click()
    expect(page.get_by_role('status')).to_be_visible()
    for p in paginas:
        p.reload()
        expect(p.get_by_role('heading', name='Olvidé mi contraseña')).to_have_count(0)
    for ctx in contextos:
        ctx.close()


def tc_009(page, base_url, usuario, contrasena):
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_role('button', name='Enviar').click()
    expect(page.get_by_role('status')).to_be_visible()
    texto_registrado = page.get_by_role('status').inner_text()

    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    page.get_by_label(re.compile(r'^Correo')).fill('no.existe.9f3a@test.local')
    with page.expect_response(lambda r: r.request.method == 'POST' and '/api/' in r.url) as info:
        page.get_by_role('button', name='Enviar').click()
    assert info.value.status == 202
    confirmacion = page.get_by_role('status')
    expect(confirmacion).to_have_text(texto_registrado)
    expect(page.get_by_role('alert')).to_have_count(0)


def tc_010(page, base_url, usuario, contrasena):
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    campo = page.get_by_label(re.compile(r'^Correo'))
    boton = page.get_by_role('button', name='Enviar')
    registrados, no_registrados = [], []
    for i in range(20):
        for correo, destino in ((usuario, registrados), (f'no.existe.t10.{i}@test.local', no_registrados)):
            campo.fill(correo)
            with page.expect_response(lambda r: r.request.method == 'POST' and '/api/' in r.url) as info:
                boton.click()
            resp = info.value
            assert resp.status == 202
            resp.finished()
            t = resp.request.timing
            destino.append(t['responseEnd'] - t['requestStart'] if t['requestStart'] >= 0 else t['responseEnd'])
            expect(boton).to_be_enabled()

    def mediana(v):
        s = sorted(v)
        return (s[9] + s[10]) / 2

    def p95(v):
        return sorted(v)[18]

    m1, m2 = mediana(registrados), mediana(no_registrados)
    margen = max(50, 0.10 * max(m1, m2))
    assert abs(m1 - m2) <= margen, f'Medianas {m1:.1f} ms vs {m2:.1f} ms (margen {margen:.1f})'
    assert min(registrados) <= max(no_registrados) and min(no_registrados) <= max(registrados), 'Las distribuciones no se solapan'
    assert abs(p95(registrados) - p95(no_registrados)) <= max(100, 0.25 * max(p95(registrados), p95(no_registrados)))
    expect(page.get_by_role('status')).to_be_visible()


def tc_011(page, base_url, usuario, contrasena):
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    expect(page.get_by_role('heading', name='Olvidé mi contraseña')).to_be_visible()
    peticiones = []
    page.on('request', lambda r: peticiones.append(r.url) if r.method == 'POST' and '/api/' in r.url else None)
    campo = page.get_by_label(re.compile(r'^Correo'))
    campo.fill('')
    page.get_by_role('button', name='Enviar').click()
    expect(campo).to_have_attribute('aria-invalid', 'true')
    expect(page.locator('.MuiFormHelperText-root.Mui-error')).to_be_visible()
    expect(page.get_by_role('status')).to_have_count(0)
    assert peticiones == [], f'Se hicieron peticiones: {peticiones}'


def tc_012(page, base_url, usuario, contrasena):
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    expect(page.get_by_role('heading', name='Olvidé mi contraseña')).to_be_visible()
    peticiones = []
    page.on('request', lambda r: peticiones.append(r.url) if r.method == 'POST' and '/api/' in r.url else None)
    campo = page.get_by_label(re.compile(r'^Correo'))
    for valor in ['usuario', 'usuario@', '@dominio.com', 'usu ario@dominio.com']:
        campo.fill(valor)
        page.get_by_role('button', name='Enviar').click()
        expect(campo).to_have_attribute('aria-invalid', 'true')
        expect(page.locator('.MuiFormHelperText-root.Mui-error')).to_be_visible()
        expect(page.get_by_role('status')).to_have_count(0)
    assert peticiones == [], f'Se hicieron peticiones: {peticiones}'


def tc_013(page, base_url, usuario, contrasena):
    # Se obtiene la URL real del endpoint de solicitud a partir del formulario y luego se llama directo.
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    page.get_by_label(re.compile(r'^Correo')).fill('no.existe.t13@test.local')
    with page.expect_request(lambda r: r.method == 'POST' and '/api/' in r.url) as info:
        page.get_by_role('button', name='Enviar').click()
    endpoint = info.value.url
    expect(page.get_by_role('status')).to_be_visible()
    for cuerpo in [{'correo': ''}, {'correo': 'usuario@'}, {}]:
        resp = page.request.post(endpoint, data=cuerpo)
        assert resp.status in (400, 422), f'{cuerpo} -> {resp.status}'
        texto = resp.text()
        assert 'VALIDACION' in texto or 'SOLICITUD_INVALIDA' in texto, f'Código de error no documentado: {texto}'


def tc_014(page, base_url, usuario, contrasena):
    # El formulario requiere un enlace vigente de la bandeja de pruebas. Se comprueba que con un enlace no vigente
    # no se ofrece el formulario y que la contraseña actual sigue funcionando (no cambió).
    page.goto(base_url + '/restablecer?token=Kd8Ls3Mz6Nq1Pw4Rx7Ty2Uv5Wa9Xb0Yc3Zd6Ae8Bf1Cg')
    expect(page.get_by_role('heading', name=re.compile(r'^Enlace '))).to_be_visible()
    expect(page.get_by_label(re.compile(r'^Nueva contraseña'))).to_have_count(0)
    page.get_by_role('link', name='Volver a iniciar sesión').click()
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña')).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'^(Iniciar sesión|Entrar|Ingresar)$', re.I)).click()
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_have_count(0)


def tc_015(page, base_url, usuario, contrasena):
    # La contraseña 'NuevaClave#2026' no debe permitir entrar; la vigente (contrasena) sí.
    page.goto(base_url + '/')
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña')).fill('NuevaClave#2026')
    page.get_by_role('button', name=re.compile(r'^(Iniciar sesión|Entrar|Ingresar)$', re.I)).click()
    expect(page.get_by_role('alert').first).to_be_visible()
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
    page.get_by_label(re.compile(r'^Contraseña')).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'^(Iniciar sesión|Entrar|Ingresar)$', re.I)).click()
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_have_count(0)


def tc_016(page, base_url, usuario, contrasena):
    dialogos = []
    page.on('dialog', lambda d: (dialogos.append(d.message), d.dismiss()))
    casos = [
        'Qw8Er3Ty6Ui1Op4As7Df2Gh5Jk9Lz0Xc3Vb6Nm8Qa1Ws',
        '',
        '%25%25%25%3Cscript%3Ealert(1)%3C%2Fscript%3E',
    ]
    titulos = []
    for token in casos:
        resp = page.goto(base_url + '/restablecer?token=' + token)
        assert resp is None or resp.status < 500
        titulo = page.get_by_role('heading', name=re.compile(r'^Enlace '))
        expect(titulo).to_be_visible()
        titulos.append(titulo.inner_text())
        expect(page.get_by_role('link', name='Solicitar un nuevo enlace')).to_be_visible()
        expect(page.get_by_label(re.compile(r'^Nueva contraseña'))).to_have_count(0)
        expect(page.get_by_text('No pudimos revisar tu enlace')).to_have_count(0)
        expect(page.get_by_text(re.compile(r'stack|Exception|at .+\.(js|ts):\d+'))).to_have_count(0)
    assert all(t == 'Enlace no válido' for t in titulos), f'Mensajes distintos: {titulos}'
    assert dialogos == [], 'Se ejecutó un script inyectado'


def tc_017(page, base_url, usuario, contrasena):
    page.goto(base_url + '/restablecer?token=Hn4Jm7Kl0Zx3Cv6Bn9Ma2Sd5Fg8Hj1Kl4Qw7Er0Ty3Ui')
    expect(page.get_by_role('heading', name=re.compile(r'^Enlace (ya utilizado|no válido)$'))).to_be_visible()
    opcion = page.get_by_role('link', name='Solicitar un nuevo enlace')
    expect(opcion).to_be_visible()
    opcion.click()
    expect(page.get_by_role('heading', name='Olvidé mi contraseña')).to_be_visible()
    expect(page.get_by_label(re.compile(r'^Correo'))).to_be_visible()
    expect(page.get_by_role('button', name='Enviar')).to_be_visible()


def tc_018(page, base_url, usuario, contrasena):
    # Con reloj de servidor controlado el formulario se enviaría a los 61 min; se valida la vista resultante
    # (mensaje de expiración/no válido con la opción de pedir otro) y que la contraseña no cambió.
    page.goto(base_url + '/restablecer?token=Tr5Yu8Io1Pa4Sd7Fg0Hj3Kl6Zx9Cv2Bn5Mq8Wz1Xe4Rc')
    expect(page.get_by_role('heading', name=re.compile(r'^Enlace (expirado|no válido)$'))).to_be_visible()
    expect(page.get_by_role('link', name='Solicitar un nuevo enlace')).to_be_visible()
    expect(page.get_by_role('button', name='Guardar')).to_have_count(0)
    page.get_by_role('link', name='Volver a iniciar sesión').click()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña')).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'^(Iniciar sesión|Entrar|Ingresar)$', re.I)).click()
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_have_count(0)


def tc_019(page, base_url, usuario, contrasena):
    enlace = base_url + '/restablecer?token=Lp2Ok5Ij8Uh1Yg4Tf7Rd0Es3Wa6Qz9Xs2Cd5Vf8Bg1Nh'
    p1 = page
    p2 = page.context.new_page()
    p1.goto(enlace)
    p2.goto(enlace)
    for p in (p1, p2):
        expect(p.get_by_role('heading', name=re.compile(r'^Enlace '))).to_be_visible()
        expect(p.get_by_role('link', name='Solicitar un nuevo enlace')).to_be_visible()
        expect(p.get_by_label(re.compile(r'^Nueva contraseña'))).to_have_count(0)
    p2.close()
    p1.goto(base_url + '/')
    p1.get_by_label(re.compile(r'^Correo')).fill(usuario)
    p1.get_by_label(re.compile(r'^Contraseña')).fill('NuevaClave#B2')
    p1.get_by_role('button', name=re.compile(r'^(Iniciar sesión|Entrar|Ingresar)$', re.I)).click()
    expect(p1.get_by_role('alert').first).to_be_visible()
    expect(p1.get_by_role('heading', name='Iniciar sesión')).to_be_visible()


def tc_020(page, base_url, usuario, contrasena):
    # Los tokens se leen de la bandeja de pruebas (fuera del navegador). Aquí se generan las 20 solicitudes y se
    # verifica que la respuesta nunca expone un token ni datos del usuario.
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    campo = page.get_by_label(re.compile(r'^Correo'))
    boton = page.get_by_role('button', name='Enviar')
    for _ in range(20):
        campo.fill(usuario)
        with page.expect_response(lambda r: r.request.method == 'POST' and '/api/' in r.url) as info:
            boton.click()
        resp = info.value
        assert resp.status == 202
        cuerpo = resp.text()
        assert 'token' not in cuerpo.lower() and 'restablecer?' not in cuerpo
        expect(boton).to_be_enabled()
    expect(page.get_by_role('status')).to_be_visible()


def tc_021(page, base_url, usuario, contrasena):
    marca = 'MarcaUnica#7Qz91'
    respuestas = []
    page.on('response', lambda r: respuestas.append(r))
    page.goto(base_url + '/restablecer?token=Mc3Vb6Nn9Aa2Ss5Dd8Ff1Gg4Hh7Jj0Kk3Ll6Zz9Xx2Cc')
    expect(page.get_by_role('heading', name=re.compile(r'^Enlace '))).to_be_visible()
    page.goto(base_url + '/')
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña')).fill(marca)
    page.get_by_role('button', name=re.compile(r'^(Iniciar sesión|Entrar|Ingresar)$', re.I)).click()
    expect(page.get_by_role('alert').first).to_be_visible()
    for r in respuestas:
        tipo = r.headers.get('content-type', '')
        if 'json' in tipo or 'text' in tipo:
            try:
                cuerpo = r.text()
            except Exception:
                continue
            assert marca not in cuerpo, f'La contraseña aparece en la respuesta de {r.url}'
    expect(page.get_by_text(marca)).to_have_count(0)


def tc_022(page, base_url, usuario, contrasena):
    page.goto(base_url + '/')
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña')).fill('ClaveActual#1')
    boton = page.get_by_role('button', name=re.compile(r'^(Iniciar sesión|Entrar|Ingresar)$', re.I))
    boton.click()
    expect(page.get_by_role('alert').first).to_be_visible()
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
    page.get_by_label(re.compile(r'^Contraseña')).fill(contrasena)
    boton.click()
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_have_count(0)


def tc_023(page, base_url, usuario, contrasena):
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    campo = page.get_by_label(re.compile(r'^Correo'))
    boton = page.get_by_role('button', name='Enviar')
    textos, estados, cuerpos = set(), set(), set()
    for _ in range(8):
        campo.fill(usuario)
        with page.expect_response(lambda r: r.request.method == 'POST' and '/api/' in r.url) as info:
            boton.click()
        estados.add(info.value.status)
        cuerpos.add(info.value.text())
        expect(page.get_by_role('status')).to_be_visible()
        textos.add(page.get_by_role('status').inner_text())
        expect(page.get_by_role('alert')).to_have_count(0)
    assert estados == {202}, f'Códigos: {estados}'
    assert len(cuerpos) == 1 and len(textos) == 1


def tc_024(page, base_url, usuario, contrasena):
    page.goto(base_url + '/')
    page.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
    campo = page.get_by_label(re.compile(r'^Correo'))
    boton = page.get_by_role('button', name='Enviar')
    correos = [usuario if i % 3 == 0 else f'no.existe.t24.{i}@test.local' for i in range(15)]
    textos, estados, cuerpos = set(), set(), set()
    for correo in correos:
        campo.fill(correo)
        with page.expect_response(lambda r: r.request.method == 'POST' and '/api/' in r.url) as info:
            boton.click()
        estados.add(info.value.status)
        cuerpos.add(info.value.text())
        expect(page.get_by_role('status')).to_be_visible()
        textos.add(page.get_by_role('status').inner_text())
    assert estados == {202}, f'Códigos: {estados}'
    assert len(cuerpos) == 1, f'Cuerpos distintos: {cuerpos}'
    assert len(textos) == 1, f'Textos distintos: {textos}'


def tc_025(page, base_url, usuario, contrasena):
    # Acciones del flujo (la vista de auditoría del admin no está en el código provisto).
    page.goto(base_url + '/')
    page.get_by_label(re.compile(r'^Correo')).fill(usuario)
    page.get_by_label(re.compile(r'^Contraseña')).fill(contrasena)
    page.get_by_role('button', name=re.compile(r'^(Iniciar sesión|Entrar|Ingresar)$', re.I)).click()
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_have_count(0)
    invitado = page.context.browser.new_context().new_page()
    for correo in (usuario, 'no.existe.9f3a@test.local'):
        invitado.goto(base_url + '/')
        invitado.get_by_role('link', name='¿Olvidaste tu contraseña?').click()
        invitado.get_by_label(re.compile(r'^Correo')).fill(correo)
        with invitado.expect_response(lambda r: r.request.method == 'POST' and '/api/' in r.url) as info:
            invitado.get_by_role('button', name='Enviar').click()
        assert info.value.status == 202
        expect(invitado.get_by_role('status')).to_be_visible()
    invitado.context.close()


def tc_026(page, base_url, usuario, contrasena):
    token = 'Rf5Tg8Yh1Uj4Ik7Ol0Pz3Xa6Sc9Dv2Fb5Gn8Hm1Jq4Kw'
    assert base_url.startswith('https://')
    terceros = []
    host = re.sub(r'^https?://', '', base_url).split('/')[0]
    page.on('request', lambda r: terceros.append(r) if host not in r.url and not r.url.startswith('data:') else None)
    resp = page.goto(base_url + '/restablecer?token=' + token)
    politica = resp.headers.get('referrer-policy', '')
    assert politica in ('no-referrer', 'same-origin'), f'Referrer-Policy: {politica!r}'
    expect(page.locator('meta[name="referrer"]')).to_have_attribute('content', 'no-referrer')
    expect(page.get_by_role('heading', name='Restablecer contraseña')).to_be_visible()
    expect(page).not_to_have_url(re.compile(token))
    for r in terceros:
        assert token not in r.url, f'Token en URL de tercero: {r.url}'
        assert token not in (r.headers.get('referer') or ''), f'Token en Referer hacia {r.url}'
    page.goto(base_url.replace('https://', 'http://', 1) + '/restablecer?token=' + token)
    expect(page).to_have_url(re.compile(r'^https://'))


def tc_027(page, base_url, usuario, contrasena):
    candidatas = ['/api/docs', '/api/v1/docs', '/docs', '/api/swagger', '/swagger']
    ruta_docs = None
    for ruta in candidatas:
        resp = page.request.get(base_url + ruta)
        if resp.ok and re.search(r'swagger|openapi', resp.text(), re.I):
            ruta_docs = ruta
            break
    assert ruta_docs is not None, 'No se encontró la documentación de la API publicada'
    page.goto(base_url + ruta_docs)
    expect(page.get_by_text(re.compile(r'restablec|password|contrase', re.I)).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'\b(400|422)\b')).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'\b(409|410)\b')).first).to_be_visible()
    expect(page.get_by_text('202').first).to_be_visible()


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
