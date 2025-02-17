// reversing how to generate ("token") key for /frictionless endpoint
const Ax = (...e) => {
    const currTime = Date.now().toString().slice(-3);
    const pie = ((Number(currTime) + e[0]) / (999) * Math.PI) - Math.PI / 2
    const sinner = Math.sin(pie) * 1000;
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

const token = await encryptPlainText(
    JSON.stringify(
        Ax(Math.min(Math.random() * 0.3, 1))
    )
);
console.log(token)
