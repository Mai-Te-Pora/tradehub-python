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

## Documentation

The documentation site can be found at: https://mai-te-pora.github.io/tradehub-python/

### Examples and Tests

We have provided examples and tests (unittests) for the majority of the functions available across this project. We are always looking for help with this because having tests pass has proven to be the most difficult part of this project.

## Usage

There are many clients to choose from and depending on your needs there are only one or two you should mainly interact with because most of these inheret from the building blocks.

Traders should use the `Demex Client`
Validators could use the `Demex Client` but combining the `Wallet` Client and `Authenticated Client` together is effectively the same.

The way these classes inheret from each other is as follows (top level first):

<p style="text-align: center;">
Demex Client</br>
:arrow_up:</br>
Authenticated Client     +     Wallet</br>
:arrow_up:</br>
Transactions Client</br>
:arrow_up:</br>
Public Client</br>
:arrow_up:</br>
Public Blockchain Client</br>
:arrow_up:</br>
Network Crawler Client</br>
</p>

### Demex Client

This client utilizes all the other clients and can call wallet, authenticated, and public endpoints.

```
from tradehub.demex_client import DemexClient

demex_crawl = DemexClient(mnemonic=mnemonic, network="mainnet", trusted_ips=None, trusted_uris=None)
demex_ips = DemexClient(mnemonic=mnemonic, network="mainnet", trusted_ips=["54.255.5.46", "175.41.151.35"], trusted_uris=None)
demex_uris = DemexClient(mnemonic=mnemonic, network="mainnet", trusted_ips=None, trusted_uris=["http://54.255.5.46:5001", "http://175.41.151.35:5001"])
```

`demex_crawl` will crawl the Tradehub network for active validators to interact with. There is ~5 second startup time to perform this but if you are running a long running process this should be acceptable.
`demex_ips` will respond very quickly as we are assuming trust and only checking that they have their persistence service turned on, can be used for quick interaction or lookups.
`demex_uris` similar to `demex_ips`, can be used for quick interaction or lookups.

#### Wallet

```
demex_ips.wallet.address
```

#### Authenticated Client

```
demex_ips.tradehub.send_tokens()
```

#### Public Client

```
demex_ips.tradehub.get_all_validators()
```
