#!/usr/bin/env python
import random
import gmpy
import os
import asyncio
import base64
import shutil
import traceback
import tempfile
import argparse
import aiopg
import logging
import collections
import pyasn1_modules.rfc3447
import pyasn1.codec.ber.encoder
import concurrent.futures


TARGET_USERNAME = "deputies"
DB = {'database': 'wiener', 'user': TARGET_USERNAME}
ADMIN_NAME = "sheriff"
AUTH_KEYS_PATH = os.path.join(
    "/", "home", TARGET_USERNAME, ".ssh", "authorized_keys")
EXECUTOR = concurrent.futures.ProcessPoolExecutor()

auth_keys_lock = asyncio.Lock()
logging.getLogger('asyncio').setLevel(logging.ERROR)
prng = random.SystemRandom()
messages = {
    'welcome': ("Well if it isn't another one of those shave tails again. "
                "Don't you dare think this is gonna be an easy job here, we "
                "take no coffee boilers just so ya' know. If you're sure you "
                "want to join our deputy ranks, just apply here. If you got "
                "any problems just lemme know by typing 'h'."),
    'access': ('Oh and you can find all lockers by going '
               'to the "Secure Sheriff\'s Huddle" with the number 1427 on the '
               'door and tell the doorman you are a "deputies". Of course you '
               'are not a "sheriff"!'),
    'new_private_key': ("Here is your locker code. Don't you dare loose it or "
                        "I'm gonna knock you galley west!"),
    'new_public_key': "And that's your lock.",
    'key_validity': ("Your locker code is only valid for 30 minutes. If you "
                     "don't need it, I'm gonna trash your lock, boy!"),
    'new_username': ("I'm gonna call you %s from now on. I don't wanna hear "
                     "any bellyaching about it!"),
    'get_public_get': "Here this is %s's lock. Why do you need it, hmm?",
    'get_pubkey_query': "So whose lock do you wanna see? ",
    'invalid_user': "Don't know him, get lost!",
    'cmd_unknwown': "What? No way you get THAT!",
    'unkown_error': "We seem to be having some problems here. We'll fix it.",
    'help_prefix': "These are the questions you can ask me:",
}


def get_message(key, *params, with_newline=True):
    nl = '\n' if with_newline else ''
    return ((messages[key] % params) + nl).encode('utf-8')

#
# Actions
#


@asyncio.coroutine
def do_help(reader, writer, conn):
    """
    Ask the sheriff for help. He might not react too friendly...
    """
    writer.write(get_message('help_prefix'))
    out = []
    for key, handler in actions.items():
        out.append("%s: %s" % (key, handler.__doc__.strip()))
    writer.writelines([(s + '\n').encode("utf-8") for s in out])


@asyncio.coroutine
def do_register(reader, writer, conn):
    """
    Get a lock and a locker code. This way you can also unlock the shared locker for everyone!
    """
    uname, id_ = yield from new_username(conn)
    priv_key, pub_key = yield from get_keypair(uname)
    with (yield from auth_keys_lock):
        with open(AUTH_KEYS_PATH, "ab") as f:
            f.seek(0, 2)
            f.write(pub_key + b'\n')
    writer.write(get_message('new_private_key'))
    writer.write(priv_key)
    writer.write(get_message('new_public_key'))
    writer.write(pub_key + b"\n")
    writer.write(get_message('new_username', uname.lower()))
    writer.write(get_message('key_validity'))
    writer.write(get_message('access'))
    cur = yield from conn.cursor()
    try:
        yield from cur.execute(
            'UPDATE users SET public_key=%s, username=%s WHERE id=%s',
            (pub_key.decode("utf-8"), uname, id_))
    finally:
        cur.close()


@asyncio.coroutine
def do_list(reader, writer, conn):
    """
    Get a list of all guys that have locks.
    """
    cur = yield from conn.cursor()
    out = []
    try:
        yield from cur.execute('SELECT username FROM users')
        for username, in (yield from cur.fetchall()):
            out.append(("- %s\n" % username).encode("utf-8"))
    finally:
        cur.close()
    writer.write(b"".join(out))


@asyncio.coroutine
def do_get_pubkey(reader, writer, conn):
    """
    Get the lock for a particular guy. Why would you need that?
    """
    writer.write(get_message('get_pubkey_query', with_newline=False))
    uname = (yield from reader.readline()).decode("utf-8").strip().lower()
    cur = yield from conn.cursor()
    try:
        yield from cur.execute(
            'SELECT public_key FROM users WHERE username=%s',
            (uname,))
        result = yield from cur.fetchone()
    finally:
        cur.close()
    if result:
        pub_key, = result
        writer.write(get_message('get_public_get', uname))
        writer.write((pub_key + '\n').encode("utf-8"))
    else:
        writer.write(get_message('invalid_user'))


actions = collections.OrderedDict()
actions['h'] = do_help
actions['r'] = do_register
actions['l'] = do_list
actions['p'] = do_get_pubkey

#
# Helpers
#


@asyncio.coroutine
def new_username(conn):
    cur = yield from conn.cursor()
    try:
        yield from cur.execute(
            'INSERT INTO users DEFAULT VALUES RETURNING id')
        new_id = yield from cur.fetchone()
        new_user = 'user%d' % new_id
    finally:
        cur.close()
    return new_user, new_id


def asn1_encode_priv_key(N, e, d, p, q):
    key = pyasn1_modules.rfc3447.RSAPrivateKey()
    dp = d % (p - 1)
    dq = d % (q - 1)
    qInv = gmpy.invert(q, p)
    assert (qInv * q) % p == 1
    key.setComponentByName('version', 0)
    key.setComponentByName('modulus', N)
    key.setComponentByName('publicExponent', e)
    key.setComponentByName('privateExponent', d)
    key.setComponentByName('prime1', p)
    key.setComponentByName('prime2', q)
    key.setComponentByName('exponent1', dp)
    key.setComponentByName('exponent2', dq)
    key.setComponentByName('coefficient', qInv)
    ber_key = pyasn1.codec.ber.encoder.encode(key)
    pem_key = base64.b64encode(ber_key).decode("ascii")
    out = ['-----BEGIN RSA PRIVATE KEY-----']
    out += [pem_key[i:i + 64] for i in range(0, len(pem_key), 64)]
    out.append('-----END RSA PRIVATE KEY-----\n')
    out = "\n".join(out)
    return out.encode("ascii")


@asyncio.coroutine
def ssh_encode_pub_key(keypath, uname):
    p = yield from asyncio.create_subprocess_exec(
        "ssh-keygen", "-y", "-f", keypath, stdout=asyncio.subprocess.PIPE)
    out = yield from p.stdout.read()
    return out.strip() + b' ' + uname.encode("ascii")


def get_prime(size):
    while True:
        val = prng.getrandbits(size)
        if gmpy.is_prime(val):
            return val


def test_key(N, e, d):
    msg = (N - 1) >> 1
    c = pow(msg, e, N)
    if pow(c, d, N) != msg:
        return False
    else:
        return True


def create_parameters(size=2048):
    p = get_prime(size // 2)
    q = get_prime(size // 2)
    N = p * q
    phi_N = (p - 1) * (q - 1)
    while True:
        d = prng.getrandbits(size // 5)
        e = int(gmpy.invert(d, phi_N))
        if (e * d) % phi_N == 1:
            break

    assert test_key(N, e, d)
    return N, e, d, p, q


@asyncio.coroutine
def get_keypair(uname):
    loop = asyncio.get_event_loop()
    params_coro = loop.run_in_executor(EXECUTOR, create_parameters)
    N, e, d, p, q = yield from params_coro
    priv_key = asn1_encode_priv_key(N, e, d, p, q)
    with tempfile.NamedTemporaryFile() as priv_file:
        priv_file.write(priv_key)
        priv_file.flush()
        pub_key = yield from ssh_encode_pub_key(priv_file.name, uname)
    return priv_key, pub_key


@asyncio.coroutine
def cleanup_old_users(conn):
    print("Cleanup task is running now.")
    while True:
        cur = yield from conn.cursor()
        yield from cur.execute("BEGIN")
        try:
            yield from cur.execute('SELECT COUNT(*) FROM users')
            old_count, = yield from cur.fetchone()
            yield from cur.execute(
                "DELETE FROM users WHERE creation_date < "
                "CURRENT_TIMESTAMP - interval '30 minutes' "
                "AND username != %s OR public_key IS NULL",
                (ADMIN_NAME,))
            yield from cur.execute('SELECT COUNT(*) FROM users')
            new_count, = yield from cur.fetchone()
            yield from cur.execute(
                'SELECT public_key FROM users WHERE username != %s',
                (ADMIN_NAME,))
            with (yield from auth_keys_lock):
                AUTH_KEYS_PATH_NEW = AUTH_KEYS_PATH + '.new'
                with open(AUTH_KEYS_PATH_NEW, "wb") as f:
                    for public_key, in (yield from cur.fetchall()):
                        f.write(public_key.encode("utf-8"))
                        f.write(b'\n')
                shutil.move(AUTH_KEYS_PATH_NEW, AUTH_KEYS_PATH)
            print("Deleted %d old keys" % (old_count - new_count))
        except Exception:
            yield from cur.execute("ROLLBACK")
            raise
        else:
            yield from cur.execute("COMMIT")
        finally:
            cur.close()
        yield from asyncio.sleep(15 * 60)


def cleanup_done(t, conn):
    POOL.release(conn)
    e = t.exception()
    if e:
        traceback.print_exception(e.__class__, e, e.__traceback__)


@asyncio.coroutine
def handle(reader, writer):
    conn = yield from POOL.acquire()
    cur = yield from conn.cursor()
    yield from cur.execute("BEGIN")
    try:
        writer.write(get_message('welcome'))
        while True:
            writer.write(b"Command: ")
            cmd = (yield from reader.readline()).decode("utf-8").strip()
            if not cmd and reader.at_eof():
                writer.close()
                break
            try:
                yield from (actions[cmd](reader, writer, conn))
            except KeyError:
                writer.write(get_message('cmd_unknwown'))
            except Exception as e:
                writer.write(get_message('unkown_error'))
                traceback.print_exception(e.__class__, e, e.__traceback__)
    except Exception:
        yield from cur.execute("ROLLBACK")
    else:
        yield from cur.execute("COMMIT")
    finally:
        cur.close()
        POOL.release(conn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', metavar='PORT', type=int,
                        required=True)
    args = parser.parse_args()
    server = asyncio.start_server(handle, port=args.port)
    server_task = asyncio.Task(server)
    loop = asyncio.get_event_loop()

    # Initialize connection pool
    POOL = loop.run_until_complete(aiopg.create_pool(maxsize=100, **DB))

    # Cleanup task setup
    cleanup_conn = loop.run_until_complete(POOL.acquire())
    cleaner_task = asyncio.Task(cleanup_old_users(cleanup_conn))
    cleaner_task.add_done_callback(lambda t: cleanup_done(t, cleanup_conn))
    try:
        print("Starting main loop, accepting connections now.")
        loop.run_forever()
    finally:
        EXECUTOR.shutdown()
        server.close()
        loop.run_until_complete(POOL.clear())
