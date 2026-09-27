"""Smoke testing de HU-002 — Inicio y cierre de sesión con correo y contraseña, con redirección por rol
Generado por Loom (skill 08, ADR-0059) a partir del código del aplicativo y los casos de prueba de la HU.
Ejecución manual: TEST_BASE_URL, TEST_USER y TEST_PASSWORD como variables de entorno y `python este_archivo.py`."""

import re

from playwright.sync_api import Page, expect


def tc_001(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    expect(page.get_by_role('heading', name='Iniciar sesión')).to_be_visible()
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
        page.get_by_role('button', name='Iniciar sesión').click()
    assert info.value.status == 200
    expect(page).not_to_have_url(re.compile(r'/login'))
    expect(page.get_by_role('button', name='Iniciar sesión')).to_have_count(0)
    page.get_by_role('button', name='Menú de usuario').click()
    expect(page.get_by_role('menuitem', name='Cerrar sesión')).to_be_visible()


def tc_002(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
        page.get_by_role('button', name='Iniciar sesión').click()
    assert info.value.status == 200
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_role('heading', name='Mis vehículos')).to_be_visible()
    expect(page.get_by_text('Agenda del día')).to_have_count(0)


def tc_003(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
        page.get_by_role('button', name='Iniciar sesión').click()
    assert info.value.status == 200
    expect(page).to_have_url(re.compile(r'/interno'))
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    expect(page.get_by_text('Mis vehículos')).to_have_count(0)


def tc_004(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena + '#Err0r')
    with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
        page.get_by_role('button', name='Iniciar sesión').click()
    assert info.value.status == 401
    assert 'accessToken' not in info.value.text()
    alerta = page.get_by_role('alert')
    expect(alerta).to_contain_text('Correo o contraseña incorrectos')
    expect(alerta).not_to_contain_text(re.compile(r'no existe|no registrado|contraseña es incorrecta', re.I))
    expect(page).to_have_url(re.compile(r'/login'))
    nombres = [c['name'] for c in page.context.cookies()]
    assert 'refreshToken' not in nombres
    almacen = page.evaluate('() => JSON.stringify(Object.assign({}, localStorage)) + JSON.stringify(Object.assign({}, sessionStorage))')
    assert 'eyJ' not in almacen


def tc_005(page, base_url, usuario, contrasena):
    def entrar(clave):
        page.get_by_label('Correo').fill(usuario)
        page.get_by_label('Contraseña').fill(clave)
        with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
            page.get_by_role('button', name='Iniciar sesión').click()
        return info.value
    page.goto(base_url + '/login')
    for _ in range(5):
        r = entrar(contrasena + '#Err0r')
        assert r.status == 401
        expect(page.get_by_role('alert')).to_contain_text('Correo o contraseña incorrectos')
    r6 = entrar(contrasena + '#Err0r')
    assert r6.status == 423
    assert 'accessToken' not in r6.text()
    alerta = page.get_by_role('alert')
    expect(alerta).to_contain_text(re.compile(r'bloqueada temporalmente', re.I))
    expect(alerta).not_to_contain_text('Correo o contraseña incorrectos')
    expect(page).to_have_url(re.compile(r'/login'))
    assert 'refreshToken' not in [c['name'] for c in page.context.cookies()]


def tc_006(page, base_url, usuario, contrasena):
    def entrar(clave):
        page.get_by_label('Correo').fill(usuario)
        page.get_by_label('Contraseña').fill(clave)
        with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
            page.get_by_role('button', name='Iniciar sesión').click()
        return info.value
    page.goto(base_url + '/login')
    bloqueo = re.compile(r'bloqueada temporalmente', re.I)
    for _ in range(4):
        r = entrar(contrasena + '#Err0r')
        assert r.status == 401
        expect(page.get_by_role('alert')).to_contain_text('Correo o contraseña incorrectos')
        expect(page.get_by_text(bloqueo)).to_have_count(0)
    r5 = entrar(contrasena + '#Err0r')
    assert r5.status in (401, 423)
    if r5.status == 401:
        expect(page.get_by_role('alert')).to_contain_text('Correo o contraseña incorrectos')
        r6 = entrar(contrasena + '#Err0r')
        assert r6.status == 423
    expect(page.get_by_role('alert')).to_contain_text(bloqueo)
    expect(page).to_have_url(re.compile(r'/login'))


def tc_007(page, base_url, usuario, contrasena):
    # Requiere que el reloj del servidor del entorno de prueba se adelante 15 min; page.clock adelanta el navegador.
    def entrar(clave):
        page.get_by_label('Correo').fill(usuario)
        page.get_by_label('Contraseña').fill(clave)
        with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
            page.get_by_role('button', name='Iniciar sesión').click()
        return info.value
    page.clock.install()
    page.goto(base_url + '/login')
    for _ in range(5):
        entrar(contrasena + '#Err0r')
    assert entrar(contrasena + '#Err0r').status == 423
    page.clock.fast_forward('15:00')
    r = entrar(contrasena)
    assert r.status == 200
    expect(page.get_by_text(re.compile(r'bloqueada temporalmente', re.I))).to_have_count(0)
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_role('heading', name='Mis vehículos')).to_be_visible()


def tc_008(page, base_url, usuario, contrasena):
    def entrar(clave):
        page.get_by_label('Correo').fill(usuario)
        page.get_by_label('Contraseña').fill(clave)
        with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
            page.get_by_role('button', name='Iniciar sesión').click()
        return info.value
    page.clock.install()
    page.goto(base_url + '/login')
    for _ in range(5):
        entrar(contrasena + '#Err0r')
    page.clock.fast_forward('14:00')
    r = entrar(contrasena)
    assert r.status == 423
    assert 'accessToken' not in r.text()
    expect(page.get_by_role('alert')).to_contain_text(re.compile(r'bloqueada temporalmente', re.I))
    expect(page).to_have_url(re.compile(r'/login'))


def tc_009(page, base_url, usuario, contrasena):
    """TC-009: Given un cliente autenticado en 'Mis vehículos'"""
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.get_by_role('textbox', name='Correo').first.fill(usuario)
    page.get_by_role('textbox', name='Contraseña').first.fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').first.click()
    page.get_by_text('Mis vehículos').first.wait_for(state='visible')
    page.get_by_role('button', name='Menú de usuario').first.click()
    page.get_by_role('menuitem', name='Cerrar sesión').first.click()
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    expect(page.get_by_text('Ingresa con tu correo y contraseña.').first).to_be_visible()
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')


def tc_010(page, base_url, usuario, contrasena):
    """TC-010: Given personal interno autenticado en 'Agenda del día'"""
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.get_by_role('textbox', name='Correo').first.fill(usuario)
    page.get_by_role('textbox', name='Contraseña').first.fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').first.click()
    page.get_by_text('Agenda del día').first.wait_for(state='visible')
    page.get_by_role('button', name='Menú de usuario').first.click()
    page.get_by_role('menuitem', name='Cerrar sesión').first.click()
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    expect(page.get_by_text('Ingresa con tu correo y contraseña.').first).to_be_visible()
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')


def tc_011(page, base_url, usuario, contrasena):
    # La expiración la decide el backend: requiere también el reloj del servidor adelantado en el entorno de prueba.
    page.clock.install()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    page.clock.fast_forward('30:00')
    with page.expect_response(lambda r: '/auth/refresh' in r.url) as ref:
        page.goto(base_url + '/interno')
    assert ref.value.status == 401
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_role('button', name='Iniciar sesión')).to_be_visible()
    expect(page.get_by_role('heading', name='Agenda del día')).to_have_count(0)


def tc_012(page, base_url, usuario, contrasena):
    page.clock.install()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    page.clock.fast_forward('29:00')
    with page.expect_response(lambda r: '/auth/refresh' in r.url) as ref:
        page.goto(base_url + '/interno')
    assert ref.value.status == 200
    expect(page).to_have_url(re.compile(r'/interno'))
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    expect(page.get_by_text('Tu sesión expiró')).to_have_count(0)


def tc_013(page, base_url, usuario, contrasena):
    """TC-013: Given una cuenta en estado inactivo y el navegador en la pantalla de login"""
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.get_by_role('textbox', name='Correo').first.fill(usuario)
    page.get_by_role('textbox', name='Contraseña').first.fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').first.click()
    expect(page.get_by_text('Tu cuenta no está habilitada').first).to_be_visible()


def tc_014(page, base_url, usuario, contrasena):
    """TC-014: Given una cuenta pendiente de verificación y el navegador en la pantalla de login"""
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.get_by_role('textbox', name='Correo').first.fill(usuario)
    page.get_by_role('textbox', name='Contraseña').first.fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').first.click()
    page.get_by_text('verific').first.wait_for(state='visible')
    expect(page.get_by_text('Tu cuenta aún no está activa: verifica tu correo con el enlace que te enviamos para poder iniciar sesión.').first).to_be_visible()


def tc_015(page, base_url, usuario, contrasena):
    peticiones = []
    page.on('request', lambda r: peticiones.append(r.url) if '/auth/login' in r.url else None)
    page.goto(base_url + '/login')
    page.get_by_label('Contraseña').fill('ClaveCualquiera1')
    page.get_by_role('button', name='Iniciar sesión').click()
    correo = page.get_by_label('Correo')
    expect(correo).to_have_attribute('aria-invalid', 'true')
    expect(page.get_by_text(re.compile(r'correo es obligatorio|obligatori', re.I)).first).to_be_visible()
    expect(page).to_have_url(re.compile(r'/login'))
    assert peticiones == []


def tc_016(page, base_url, usuario, contrasena):
    peticiones = []
    page.on('request', lambda r: peticiones.append(r.url) if '/auth/login' in r.url else None)
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill('persona.qa@example.com')
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_label('Contraseña')).to_have_attribute('aria-invalid', 'true')
    expect(page.get_by_text(re.compile(r'contraseña es obligatoria|obligatori', re.I)).first).to_be_visible()
    expect(page).to_have_url(re.compile(r'/login'))
    assert peticiones == []


def tc_017(page, base_url, usuario, contrasena):
    # Se descubre la URL real del endpoint con un intento desde la UI con un correo no registrado.
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill('no.registrado.qa017@example.com')
    page.get_by_label('Contraseña').fill('ClaveCualquiera1')
    with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
        page.get_by_role('button', name='Iniciar sesión').click()
    url_login = info.value.url
    cuerpos = [
        {'correo': '', 'password': 'ClaveCualquiera1'},
        {'correo': 'persona.qa@example.com', 'password': ''},
        {'password': 'ClaveCualquiera1'},
        {'correo': 'persona.qa@example.com'},
        {},
    ]
    for cuerpo in cuerpos:
        r = page.request.post(url_login, data=cuerpo)
        assert r.status in (400, 422), (cuerpo, r.status)
        texto = r.text()
        assert 'accessToken' not in texto
        assert 'refreshToken' not in r.headers.get('set-cookie', '')
    expect(page).to_have_url(re.compile(r'/login'))


def tc_018(page, base_url, usuario, contrasena):
    peticiones = []
    page.on('request', lambda r: peticiones.append(r.url) if '/auth/login' in r.url else None)
    page.goto(base_url + '/login')
    for correo_invalido in ['usuario@', 'usuario.dominio.com']:
        page.get_by_label('Correo').fill(correo_invalido)
        page.get_by_label('Contraseña').fill('ClaveCualquiera1')
        page.get_by_role('button', name='Iniciar sesión').click()
        expect(page.get_by_label('Correo')).to_have_attribute('aria-invalid', 'true')
        expect(page.get_by_text(re.compile(r'correo.*(v[aá]lido|formato)|formato', re.I)).first).to_be_visible()
        expect(page.get_by_text('Correo o contraseña incorrectos')).to_have_count(0)
        expect(page).to_have_url(re.compile(r'/login'))
    assert peticiones == []


def tc_019(page, base_url, usuario, contrasena):
    """TC-019: Given una cuenta activa con 4 intentos fallidos consecutivos"""
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.get_by_role('textbox', name='Correo').first.fill('correo-invalido')
    page.get_by_role('textbox', name='Contraseña').first.fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').first.click()
    expect(page.get_by_text('El correo no tiene un formato válido.').first).to_be_visible()
    page.get_by_role('textbox', name='Correo').first.fill(usuario)
    page.get_by_role('textbox', name='Contraseña').first.fill('ClaveErronea123!')
    page.get_by_role('button', name='Iniciar sesión').first.click()
    page.get_by_text('bloquead').first.wait_for(state='visible')


def tc_020(page, base_url, usuario, contrasena):
    """TC-020: Given el navegador en la pantalla de login"""
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.get_by_role('textbox', name='Correo').first.fill('noregistrado.tc020@example.com')
    page.get_by_role('textbox', name='Contraseña').first.fill('ClaveCualquiera123!')
    page.get_by_role('button', name='Iniciar sesión').first.click()
    page.get_by_text('incorrect').first.wait_for(state='visible')
    expect(page.get_by_text('Correo o contraseña incorrectos.').first).to_be_visible()


def tc_021(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill('no.registrado.qa021@example.com')
    page.get_by_label('Contraseña').fill('ClaveCualquiera1')
    with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
        page.get_by_role('button', name='Iniciar sesión').click()
    url_login = info.value.url
    # N=7 por grupo para no superar el límite de 20 logins/min por IP; un login correcto cada 4 fallos evita el bloqueo.
    resultado = page.evaluate(
        '''async ({url, correo, clave}) => {
            const post = async (c, p) => {
                const t = performance.now();
                await fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({correo: c, password: p}), credentials: 'include'});
                return performance.now() - t;
            };
            const inexistente = [], existente = [];
            let fallos = 0;
            for (let i = 0; i < 7; i++) {
                inexistente.push(await post('no.registrado.qa021@example.com', 'ClaveCualquiera1'));
                if (fallos === 4) { await post(correo, clave); fallos = 0; }
                existente.push(await post(correo, clave + '#Err0r'));
                fallos++;
            }
            await post(correo, clave);
            const mediana = (xs) => { const s = [...xs].sort((a, b) => a - b); return s[Math.floor(s.length / 2)]; };
            return {a: mediana(inexistente), b: mediana(existente)};
        }''',
        {'url': url_login, 'correo': usuario, 'clave': contrasena},
    )
    assert abs(resultado['a'] - resultado['b']) < 100, resultado
    expect(page).to_have_url(re.compile(r'/login'))


def tc_022(page, base_url, usuario, contrasena):
    def entrar(clave):
        page.get_by_label('Correo').fill(usuario)
        page.get_by_label('Contraseña').fill(clave)
        with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
            page.get_by_role('button', name='Iniciar sesión').click()
        return info.value
    def salir():
        page.get_by_role('button', name='Menú de usuario').click()
        page.get_by_role('menuitem', name='Cerrar sesión').click()
        expect(page).to_have_url(re.compile(r'/login'))
    bloqueo = re.compile(r'bloqueada temporalmente', re.I)
    page.goto(base_url + '/login')
    for _ in range(4):
        assert entrar(contrasena + '#Err0r').status == 401
    assert entrar(contrasena).status == 200
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_role('heading', name='Mis vehículos')).to_be_visible()
    salir()
    for _ in range(4):
        assert entrar(contrasena + '#Err0r').status == 401
        expect(page.get_by_role('alert')).to_contain_text('Correo o contraseña incorrectos')
        expect(page.get_by_text(bloqueo)).to_have_count(0)
    assert entrar(contrasena).status == 200
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_role('heading', name='Mis vehículos')).to_be_visible()


def tc_023(page, base_url, usuario, contrasena):
    def entrar(clave):
        page.get_by_label('Correo').fill(usuario)
        page.get_by_label('Contraseña').fill(clave)
        with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
            page.get_by_role('button', name='Iniciar sesión').click()
        return info.value
    bloqueo = re.compile(r'bloqueada temporalmente', re.I)
    page.goto(base_url + '/login')
    assert entrar(contrasena + '#Err0r').status == 401
    assert entrar(contrasena).status == 200
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    page.get_by_role('button', name='Menú de usuario').click()
    page.get_by_role('menuitem', name='Cerrar sesión').click()
    expect(page).to_have_url(re.compile(r'/login'))
    for _ in range(4):
        assert entrar(contrasena + '#Err0r').status == 401
        expect(page.get_by_role('alert')).to_contain_text('Correo o contraseña incorrectos')
    expect(page.get_by_text(bloqueo)).to_have_count(0)
    expect(page).to_have_url(re.compile(r'/login'))


def tc_024(page, base_url, usuario, contrasena):
    def entrar(clave):
        page.get_by_label('Correo').fill(usuario)
        page.get_by_label('Contraseña').fill(clave)
        with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
            page.get_by_role('button', name='Iniciar sesión').click()
        return info.value
    page.goto(base_url + '/login')
    for _ in range(5):
        entrar(contrasena + '#Err0r')
    r = entrar(contrasena)
    assert r.status == 423
    assert 'accessToken' not in r.text()
    expect(page.get_by_role('alert')).to_contain_text(re.compile(r'bloqueada temporalmente', re.I))
    expect(page).to_have_url(re.compile(r'/login'))
    assert 'refreshToken' not in [c['name'] for c in page.context.cookies()]


def tc_025(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    campo = page.get_by_label('Contraseña')
    expect(campo).to_have_attribute('type', 'password')
    campo.fill('SecretoVisible123')
    expect(campo).to_have_attribute('type', 'password')
    expect(page.locator('body')).not_to_contain_text('SecretoVisible123')


def tc_026(page, base_url, usuario, contrasena):
    respuestas = []
    page.on('response', lambda r: respuestas.append(r))
    erronea = contrasena + '#Err0r'
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(erronea)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_role('alert')).to_contain_text('Correo o contraseña incorrectos')
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_role('heading', name='Mis vehículos')).to_be_visible()
    page.reload()
    expect(page.get_by_role('heading', name='Mis vehículos')).to_be_visible()
    for r in respuestas:
        cabeceras = ' '.join(r.all_headers().values())
        assert contrasena not in cabeceras and erronea not in cabeceras
        assert contrasena not in r.url
        if '/api/' in r.url:
            try:
                cuerpo = r.text()
            except Exception:
                cuerpo = ''
            assert contrasena not in cuerpo, r.url
            assert '"password"' not in cuerpo, r.url
    assert contrasena not in page.url
    almacen = page.evaluate('() => JSON.stringify(Object.assign({}, localStorage)) + JSON.stringify(Object.assign({}, sessionStorage))')
    assert contrasena not in almacen
    assert all(contrasena not in c['value'] for c in page.context.cookies())
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))


def tc_027(page, base_url, usuario, contrasena):
    """TC-027: Given un cliente que inició sesión, navegó a 'Mis vehículos' y luego cerró sesión"""
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.get_by_role('textbox', name='Correo').first.fill(usuario)
    page.get_by_role('textbox', name='Contraseña').first.fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').first.click()
    page.get_by_text('Mis vehículos').first.wait_for(state='visible')
    page.get_by_role('button', name='Menú de usuario').first.click()
    page.get_by_role('menuitem', name='Cerrar sesión').first.click()
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.keyboard.press('Alt+ArrowLeft')
    expect(page.get_by_text('Ingresa con tu correo y contraseña.').first).to_be_visible()


def tc_028(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
        page.get_by_role('button', name='Iniciar sesión').click()
    assert info.value.status == 200
    token = info.value.json()['accessToken']
    url_me = re.sub(r'/auth/login.*$', '/auth/me', info.value.url)
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    antes = page.request.get(url_me, headers={'Authorization': 'Bearer ' + token})
    assert antes.status == 200
    page.get_by_role('button', name='Menú de usuario').click()
    with page.expect_response(lambda r: '/auth/logout' in r.url):
        page.get_by_role('menuitem', name='Cerrar sesión').click()
    expect(page).to_have_url(re.compile(r'/login'))
    despues = page.request.get(url_me, headers={'Authorization': 'Bearer ' + token})
    assert despues.status == 401
    cuerpo = despues.text()
    assert usuario.lower() not in cuerpo.lower()
    assert 'rutaInicial' not in cuerpo


def tc_029(page, base_url, usuario, contrasena):
    # La expiración la decide el backend: requiere también el reloj del servidor adelantado en el entorno de prueba.
    page.clock.install()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    page.clock.fast_forward('30:00')
    page.reload()
    expect(page).to_have_url(re.compile(r'/login'))
    aviso = page.get_by_role('status').filter(has_text='Tu sesión expiró')
    expect(aviso).to_be_visible()
    expect(aviso).not_to_contain_text('Correo o contraseña incorrectos')


def tc_030(page, base_url, usuario, contrasena):
    page.clock.install()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    page.clock.fast_forward('25:00')
    with page.expect_response(lambda r: '/auth/refresh' in r.url) as r1:
        page.goto(base_url + '/interno')
    assert r1.value.status == 200
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    page.clock.fast_forward('25:00')
    with page.expect_response(lambda r: '/auth/refresh' in r.url) as r2:
        page.goto(base_url + '/interno')
    assert r2.value.status == 200
    expect(page).to_have_url(re.compile(r'/interno'))
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    expect(page.get_by_text('Tu sesión expiró')).to_have_count(0)


def tc_031(page, base_url, usuario, contrasena):
    # La expiración la decide el backend: requiere también el reloj del servidor adelantado en el entorno de prueba.
    page.clock.install()
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    page.clock.fast_forward('25:00')
    page.goto(base_url + '/interno')
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    page.clock.fast_forward('30:00')
    page.reload()
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page.get_by_text('Tu sesión expiró')).to_be_visible()


def tc_032(page, base_url, usuario, contrasena):
    """TC-032: Given un cliente autenticado"""
    page.goto(base_url + '/')
    page.get_by_text('Iniciar sesión').first.wait_for(state='visible')
    page.get_by_role('textbox', name='Correo').first.fill(usuario)
    page.get_by_role('textbox', name='Contraseña').first.fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').first.click()
    page.get_by_text('Mis vehículos').first.wait_for(state='visible')
    page.goto(base_url + '/agenda')
    expect(page.get_by_text('Página no encontrada').first).to_be_visible()


def tc_033(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/interno'))
    page.goto(base_url + '/mis-vehiculos')
    expect(page).to_have_url(re.compile(r'/interno'))
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    expect(page.get_by_text('Mis vehículos')).to_have_count(0)


def tc_034(page, base_url, usuario, contrasena):
    # Supuesto: el endpoint de la agenda del personal es <api>/agenda (no aparece en el código provisto).
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as info:
        page.get_by_role('button', name='Iniciar sesión').click()
    assert info.value.status == 200
    token = info.value.json()['accessToken']
    url_agenda = re.sub(r'/auth/login.*$', '/agenda', info.value.url)
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    r = page.request.get(url_agenda, headers={'Authorization': 'Bearer ' + token})
    assert r.status == 403, r.status
    cuerpo = r.text()
    assert re.search(r'"(citas|agenda|items)"\s*:\s*\[', cuerpo) is None


def tc_035(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    page.goto(base_url + '/login')
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_role('heading', name='Mis vehículos')).to_be_visible()
    expect(page.get_by_role('button', name='Iniciar sesión')).to_have_count(0)


def tc_036(page, base_url, usuario, contrasena):
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/interno'))
    page.goto(base_url + '/login')
    expect(page).to_have_url(re.compile(r'/interno'))
    expect(page.get_by_role('heading', name='Agenda del día')).to_be_visible()
    expect(page.get_by_role('button', name='Iniciar sesión')).to_have_count(0)


def tc_037(page, base_url, usuario, contrasena):
    # No hay vista ni endpoint de auditoría en el código provisto: se ejecutan las acciones auditables y se verifica
    # lo observable desde la UI. La comprobación de los EventoAuditoria (correo, fecha, resultado, IP) requiere backend.
    respuestas = []
    page.on('response', lambda r: respuestas.append(r) if '/auth/' in r.url else None)
    erronea = contrasena + '#Err0r'
    page.goto(base_url + '/login')
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(erronea)
    with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as fallo:
        page.get_by_role('button', name='Iniciar sesión').click()
    assert fallo.value.status == 401
    page.get_by_label('Contraseña').fill(contrasena)
    with page.expect_response(lambda r: '/auth/login' in r.url and r.request.method == 'POST') as exito:
        page.get_by_role('button', name='Iniciar sesión').click()
    assert exito.value.status == 200
    expect(page).to_have_url(re.compile(r'/interno'))
    page.get_by_role('button', name='Menú de usuario').click()
    with page.expect_response(lambda r: '/auth/logout' in r.url) as salida:
        page.get_by_role('menuitem', name='Cerrar sesión').click()
    assert salida.value.status in (200, 204)
    expect(page).to_have_url(re.compile(r'/login'))
    for r in respuestas:
        try:
            cuerpo = r.text()
        except Exception:
            cuerpo = ''
        assert contrasena not in cuerpo and erronea not in cuerpo
    expect(page.get_by_role('button', name='Iniciar sesión')).to_be_visible()


def tc_038(page, base_url, usuario, contrasena):
    urls = []
    page.on('request', lambda r: urls.append(r.url) if '/api/' in r.url or '/auth/' in r.url else None)
    page.goto(base_url.replace('https://', 'http://', 1) + '/login')
    expect(page).to_have_url(re.compile(r'^https://.*/login'))
    page.get_by_label('Correo').fill(usuario)
    page.get_by_label('Contraseña').fill(contrasena)
    page.get_by_role('button', name='Iniciar sesión').click()
    expect(page).to_have_url(re.compile(r'/mis-vehiculos'))
    expect(page.get_by_role('heading', name='Mis vehículos')).to_be_visible()
    cookie = [c for c in page.context.cookies() if c['name'] == 'refreshToken']
    assert cookie and all(c['secure'] for c in cookie)
    page.reload()
    expect(page.get_by_role('heading', name='Mis vehículos')).to_be_visible()
    page.get_by_role('button', name='Menú de usuario').click()
    page.get_by_role('menuitem', name='Cerrar sesión').click()
    expect(page).to_have_url(re.compile(r'^https://.*/login'))
    assert any('/auth/login' in u for u in urls) and any('/auth/logout' in u for u in urls)
    for u in urls:
        assert u.startswith('https://'), u


def tc_039(page, base_url, usuario, contrasena):
    # Supuesto: Swagger UI de NestJS publicado en /api/docs.
    page.goto(base_url + '/api/docs')
    login = page.get_by_text(re.compile(r'/auth/login$')).first
    logout = page.get_by_text(re.compile(r'/auth/logout$')).first
    expect(login).to_be_visible()
    expect(logout).to_be_visible()
    login.click()
    expect(page.get_by_text('Inicio de sesión con correo y contraseña').first).to_be_visible()
    for codigo in ['200', '400', '401', '403', '423']:
        expect(page.get_by_role('cell', name=codigo, exact=True).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'Correo o contraseña incorrectos')).first).to_be_visible()
    expect(page.get_by_text(re.compile(r'bloqueada temporalmente')).first).to_be_visible()
    login.click()
    logout.click()
    expect(page.get_by_text(re.compile(r'SESION_INVALIDA|SESION_EXPIRADA|NO_AUTENTICADO')).first).to_be_visible()


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
