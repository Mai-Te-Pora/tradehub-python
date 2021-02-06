<p align="center">
    <a href="https://scrutinizer-ci.com/g/Mai-Te-Pora/tradehub-python/">
        <img src="https://img.shields.io/scrutinizer/quality/g/mai-te-pora/tradehub-python/main" alt="Code Quality"></a>
    <a href="https://app.codecov.io/gh/Mai-Te-Pora/tradehub-python/">
        <img src="https://img.shields.io/codecov/c/github/mai-te-pora/tradehub-python" alt="Code Coverage"></a>
    <a href="https://libraries.io/github/Mai-Te-Pora/tradehub-python" alt="Dependcy Status">
        <img src="https://img.shields.io/librariesio/github/Mai-Te-Pora/tradehub-python">
    <a href="https://pypi.org/project/tradehub/">
        <img src="https://img.shields.io/pypi/v/tradehub" alt="PyPi Version"/></a>
    <a href="https://pypi.org/project/tradehub/#history">
        <img src="https://img.shields.io/pypi/pyversions/tradehub"/></a>
</p>
<p align="center">
    <a href="https://github.com/Mai-Te-Pora/tradehub-python/blob/main/LICENSE" alt="License">
        <img src="https://img.shields.io/github/license/mai-te-pora/tradehub-python" /></a>
    <a href="https://github.com/Mai-Te-Pora/tradehub-python/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/contributors/Mai-Te-Pora/tradehub-python" /></a>
    <a href="https://github.com/Mai-Te-Pora/tradehub-python/pulse" alt="Commit Activity">
        <img src="https://img.shields.io/github/commit-activity/m/mai-te-pora/tradehub-python" /></a>
    <a href="https://github.com/Mai-Te-Pora/tradehub-python/issues">
        <img src="https://img.shields.io/github/issues/mai-te-pora/tradehub-python" alt="Open Issues"></a>
    <a href="">
        <img src="https://img.shields.io/pypi/dm/tradehub" alt="Downloads"></a>
</p>

# Tradehub Python API

This repository is designed to easily integrate your Python code or application with the Switcheo Tradehub Blockchain. This API is designed to interact with the decentralized network of Validators designed to keep the blockchain running and secure. This allows you to choose trusted endpoints or select random endpoints to interact with.

This project has been submitted on the Switcheo Foundation forums as part of the wider Switcheo community and you can follow official progress in this thread: https://forum.switcheo.foundation/topic/49/python-sdk-for-tradehub

**NOTE:** This repository and underlying blockchain is under active development and may change drastically from each update.

If you have ideas or contributions we are accepting Pull Requests.

## Getting Started

```
pip install tradehub
```

Or Using Poetry - https://python-poetry.org/

```
poetry add tradehub
```

### Demex Client

This client utilizes all the other clients and can call wallet, authenticated, and public endpoints.

```
dmx = DemexClient(mnemonic=mnemonic, network="mainnet")
print(dmx.tradehub.get_account_details())
dmx.limit_sell(pair="swth_eth1", quantity="200", price="0.000021"))
dmx.limit_buy(pair="swth_eth1", quantity="200", price="0.0000165"))
dmx.market_sell(pair="swth_eth1", quantity="200"))
dmx.market_buy(pair="swth_eth1", quantity="200"))
```

### Wallet and Tradehub Authenticated Client

```
from tradehub.authenticated_client import AuthenticatedClient as TradehubAuthenticatedClient
from tradehub.wallet import Wallet
mnemonic = 'ENTER'
wallet = Wallet(mnemonic = mnemonic, network = "mainnet")
pk = TradehubAuthenticatedClient(wallet = wallet, node_ip = validator_ip, network = "mainnet")

profile_update_dict = {
    "username": "pythonapi",
    "twitter": "test3",
}
print(pk.update_profile(message = profile_update_dict))
```

### Tradehub Public Client

```
from tradehub.utils import validator_crawler_mp
from tradehub.public_client import PublicClient as TradehubPublicClient
import random

validator_dict = validator_crawler_mp(network = 'main')
active_peers = validator_dict["active_peers"]
decentralized_client = TradehubPublicClient(validator_ip=active_peers[random.randint(a=0, b=len(active_peers)-1)])

print(decentralized_client.get_tokens())
```
