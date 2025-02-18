import requests
import polka
from hashlib import sha256
from gen_token import generate_token


class Pow:
    @staticmethod
    def digestToHex(c):
        return "".join([format(b, "02x") for b in c])

    @staticmethod
    def checkPrefix(challenge: str, difficulty: int) -> int:
        s = 0
        d = "0" * difficulty
        while True:
            n = (str(s) + challenge).encode("utf-8")
            if Pow.digestToHex(sha256(n).digest()).startswith(d):
                return s
            s += 1


class Prosopo:
    def __init__(self, site_key: str, user_key: str):
        self.site_key = site_key
        self.user_key = user_key
        self.base_url = "https://pronode9.prosopo.io/v1/prosopo"
        self.default_headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://prosopo.io",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "prosopo-site-key": self.site_key,
            "prosopo-user": self.user_key,
            "referer": "https://prosopo.io/",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        }

    def get_session_id(self):
        response = requests.request(
            method="POST",
            url=f'{self.base_url}/provider/client/captcha/frictionless',
            headers=self.default_headers,
            json={
                "token": generate_token(),
                "dapp": self.site_key,
                "user": self.user_key
            }
        )

        resp_body = response.json()

        if resp_body.get("captchaType") != "pow":
            raise Exception("bad captchaType received: ", resp_body)

        return resp_body.get("sessionId")

    def get_challenge(self, session_id: str):
        response = requests.request(
            method="POST",
            url=f'{self.base_url}/provider/client/captcha/pow',
            headers=self.default_headers,
            json={
                "user": self.user_key,
                "dapp": self.site_key,
                "sessionId": session_id,
            }
        )

        resp_body = response.json()

        if resp_body.get('status') != "ok":
            raise Exception("bad challenge received: ", resp_body)

        return resp_body

    def submit_challenge(self, challenge_str: str, provider: str, signature: str, nonce: int):
        response = requests.request(
            method="POST",
            url="https://pronode9.prosopo.io/v1/prosopo/provider/client/pow/solution",
            headers=self.default_headers,
            json={
                "challenge": challenge_str,
                "difficulty": 4,
                "signature": {
                    "user": {
                        "timestamp": '0x'+signature,
                    },
                    "provider": {
                        "challenge": provider
                    },
                },
                "user": self.user_key,
                "dapp": self.site_key,
                "nonce": nonce,
                "verifiedTimeout": 120000,
            },
        )

        print(response.json())


def main(site_key: str, visitor_id: str):
    signer = polka.create_signer(visitor_id)
    print(f'Your (ss58) address: {signer.address()}')

    captcha = Prosopo(
        site_key=site_key,
        user_key=signer.address(),
    )
    session_id = captcha.get_session_id()
    challenge = captcha.get_challenge(session_id)
    nonce = Pow.checkPrefix(challenge['challenge'], challenge['difficulty'])

    captcha.submit_challenge(
        challenge['challenge'],
        challenge['signature']['provider']['challenge'],
        signer.sign(challenge['timestamp']),
        nonce
    )


if __name__ == "__main__":
    main('5C7bfXYwachNuvmasEFtWi9BMS41uBvo6KpYHVSQmad4nWzw', 'visitor id')
