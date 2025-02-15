# pip install py-sr25519-bindings
# pip install py-bip39-bindings
# pip install mnemonic

import bip39
import sr25519
import mnemonic
from hashlib import blake2b
from wordlist import words


# visitorId is given from fpjs
# found at: async createAccount(e){ or find it by ="sr25519"
# breakpoint n = await N() and the value of n is visitorId
visitorId = '654876d6cbb05449270e38d11bb1f9a6'

# received from the challenge
# ../provider/client/captcha/pow
timestamp = '1739428755367'

blakeHash = blake2b(visitorId.encode(), digest_size=16, key=bytes())
mnemo = mnemonic.Mnemonic(language="english", wordlist=words)
seed_phrase = mnemo.to_mnemonic(blakeHash.hexdigest().encode())
mini_secret = bip39.bip39_to_mini_secret(seed_phrase, "")
keypair = sr25519.pair_from_seed(mini_secret)

def create_signature(timestamp: str):
    signature = sr25519.sign(keypair, timestamp.encode())
    return signature.hex()

if __init__ == "__main__":
  message = create_signature(timestamp)
  print('Signed message:', message)
