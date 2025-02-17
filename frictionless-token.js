// reversing how to generate ("token") key for /frictionless endpoint

function l(x, y, a) {
    switch (a) {
        case -44:
            return x + y;
        case -28:
            return x - y;
        case 63:
            return x * y;
    }
}

const a = l(Math.random(), 0.3, 63);
const c = Math.min(l(0, a, -44), 1);

const Ax = (...e) => {
    const currTime = Date.now();
    const pie = l((Number(currTime.toString().slice(-3)) + e[0]) / (999) * Math.PI, Math.PI / 2, -28);
    const sinner = l(Math.sin(pie), 1000, 63);
    return [currTime, sinner]
};

async function encryptPlainText(...e) {
    const publicKeyBytes = atob(`MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoa1QCkVvFAfv+fgFpjfq
  9/YrtGzDYull6V0oiy1XPuTCQeb4uptHEmCepnZPmKaP/akp5wS7UTGYw+or//gd
  IER2Cs58q7tVvqxTe68mx901oSw61VOt7mqDVhIsnJlH6yo2Kd9a5rClU/xr618K
  Ry0wuoD2i6mq4fE3uKZZBNrxJ57Jg0EXEsMIvYHxk0kKO8i0YIxEVP84tUuZiq9T
  dcponzr4ny6lqn0YlOSu67kRVL8O0ryHvRJomNN4OcUgq/rUfzJxonqvvmHd75n4
  4r8n4Y7I8/DmVe9cpDWDgv6vk2djRkAQDiLfDEMfq8C7S+/8RPyLTCxXUrR2ouUG
  6QIDAQAB`);

    const publicKey = new Uint8Array(294);

    for (let a = 0; a < 294; a++)
        publicKey[a] = publicKeyBytes.charCodeAt(a);

    const cryptoKey = await crypto.subtle.importKey('spki', publicKey, {
        'name': 'RSA-OAEP',
        'hash': 'SHA-256'
    }, true, ['encrypt']);

    const cryptoText = await crypto.subtle.encrypt(
        { name: "RSA-OAEP" },
        cryptoKey,
        new TextEncoder().encode(e[0])
    );

    return btoa(String.fromCharCode(...new Uint8Array(cryptoText)));
}

const token = await encryptPlainText(JSON.stringify(Ax(c)));
console.log(token)
