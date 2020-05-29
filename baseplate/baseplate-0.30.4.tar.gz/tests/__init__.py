try:
    from unittest import mock
except ImportError:
    import mock

AUTH_TOKEN_PUBLIC_KEY = """\
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtzMnDEQPd75QZByogNlB
NY2auyr4sy8UNTDARs79Edq/Jw5tb7ub412mOB61mVrcuFZW6xfmCRt0ILgoaT66
Tp1RpuEfghD+e7bYZ+Q2pckC1ZaVPIVVf/ZcCZ0tKQHoD8EpyyFINKjCh516VrCx
KuOm2fALPB/xDwDBEdeVJlh5/3HHP2V35scdvDRkvr2qkcvhzoy0+7wUWFRZ2n6H
TFrxMHQoHg0tutAJEkjsMw9xfN7V07c952SHNRZvu80V5EEpnKw/iYKXUjCmoXm8
tpJv5kXH6XPgfvOirSbTfuo+0VGqVIx9gcomzJ0I5WfGTD22dAxDiRT7q7KZnNgt
TwIDAQAB
-----END PUBLIC KEY-----
"""


AUTH_TOKEN_PRIVATE_KEY = """\
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAtzMnDEQPd75QZByogNlBNY2auyr4sy8UNTDARs79Edq/Jw5t
b7ub412mOB61mVrcuFZW6xfmCRt0ILgoaT66Tp1RpuEfghD+e7bYZ+Q2pckC1ZaV
PIVVf/ZcCZ0tKQHoD8EpyyFINKjCh516VrCxKuOm2fALPB/xDwDBEdeVJlh5/3HH
P2V35scdvDRkvr2qkcvhzoy0+7wUWFRZ2n6HTFrxMHQoHg0tutAJEkjsMw9xfN7V
07c952SHNRZvu80V5EEpnKw/iYKXUjCmoXm8tpJv5kXH6XPgfvOirSbTfuo+0VGq
VIx9gcomzJ0I5WfGTD22dAxDiRT7q7KZnNgtTwIDAQABAoIBAEjzXJw8yfAD391N
sCfG23mozrGzdd9cYu6fYCGSMSIX+kBiNV/l1DigxRzZ1bSggv4Am5H4LUj5HrAc
xTLLoMLHUIlkYfiYLc4zzE7qiHxR5AgLc5fq/FX9Uz8c0Kvgr3j+kVbrBOa7QONh
6SJ2L8aFap6kQMULbyFrSnaBY0omCZVV1tgyHwH2glZqm+0YjW4K0QU9KdE9YxLm
LXo8kXv5gZrPLtRzKrKo8WVscLGxSI0+x/ca9FjonGkZxUgfNZ61pu0sdXlpYCM/
yTjgtl35bFRcLsA1ZTxSI53y8iZUMljSg+oO6PEYrqzJh050khf/cP9GaSos00cJ
CUUx46kCgYEA8+GT8uIxLBTLQVvJMbvmK0enl1tvnQsSw6BKs1Gzprmk+7NRBeQg
6IuMAwMqgGgYq2MHPCt+/xEYlywyls37ME/JRlu0273lxK1jLcDAKgzHlCaMukzb
YyXdswRjkM0vzwljrjytUhO2Y8Bn8Y5LDR3ZP3XsZnx619NhHnWhPXMCgYEAwE2l
DNFXB6IZKzoBSrvG01yKxUjNoDDc6RaC1YciXJIDrya1EvJSsL0B7SOh2S2KWK4S
NdOMn3FlXGJU8CEwD67xDxWnRNFr26IMAOQAflxMiaooDBZevIY5wGBVUGU/45eo
fJK8+TmAbLMJWXT0PmY0HRI9Z9G8LLvbkTPqmbUCgYBQNz4mgWeTDDPeh4YhqaAH
VEY3bofDq8S8O5jWamUgzacKcuyPd32rf1rKEtyD57lVhfj3PYdD9ieUcaEiIRYh
ydx2G+vc6xUMH8ujXObX7eQnQpa/IFB4yBenriXhltvGyVvUD3kiqgEvxjVqKldd
NRgj23GqM/9jxc8H6cDjKQKBgBcOuEWLLDY8F2x5bgI59aMOK41wJ0eX1EUWb+WO
aG5VC6AKshdtesC6SOrYJOXXcgkkBgbyMKBFhnPHTovkTtDylvDKFd5Ihfg1u963
d9+uzXaMMnUQkZdlOLN6WYBkQ37Uhl05cvMnE+D0rqBNR6PbuU/rCfXSzg9HDxKf
+PcpAoGBAIu7BGSFmQpuL8OOcoap5moT2DHiatcDcsQGUg05kQxjWQPqkqUKk5Ms
Szq8xEe5u6rKLGFd1oPGB1/P6yiSxModVOGW0ALSlPNzHITtVEXLz27l3yXjBZeg
UNIHRjPq0YEdP4hwn2DxgZdgjm/RobXNz4DWfzRVqHR+hxMso5QQ
-----END RSA PRIVATE KEY-----
"""

AUTH_TOKEN_VALID = b"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0Ml9leGFtcGxlIiwiZXhwIjoyNTI0NjA4MDAwfQ.dRzzfc9GmzyqfAbl6n_C55JJueraXk9pp3v0UYXw0ic6W_9RVa7aA1zJWm7slX9lbuYldwUtHvqaSsOpjF34uqr0-yMoRDVpIrbkwwJkNuAE8kbXGYFmXf3Ip25wMHtSXn64y2gJN8TtgAAnzjjGs9yzK9BhHILCDZTtmPbsUepxKmWTiEX2BdurUMZzinbcvcKY4Rb_Fl0pwsmBJFs7nmk5PvTyC6qivCd8ZmMc7dwL47mwy_7ouqdqKyUEdLoTEQ_psuy9REw57PRe00XCHaTSTRDCLmy4gAN6J0J056XoRHLfFcNbtzAmqmtJ_D9HGIIXPKq-KaggwK9I4qLX7g"
SERIALIZED_EDGECONTEXT_WITH_NO_AUTH = b"\x0c\x00\x01\x0b\x00\x01\x00\x00\x00\x0bt2_deadbeef\n\x00\x02\x00\x00\x00\x00\x00\x01\x86\xa0\x00\x0c\x00\x02\x0b\x00\x01\x00\x00\x00\x08beefdead\x00\x00"
SERIALIZED_EDGECONTEXT_WITH_VALID_AUTH = b"\x0c\x00\x01\x0b\x00\x01\x00\x00\x00\x0bt2_deadbeef\n\x00\x02\x00\x00\x00\x00\x00\x01\x86\xa0\x00\x0c\x00\x02\x0b\x00\x01\x00\x00\x00\x08beefdead\x00\x0b\x00\x03\x00\x00\x01\xaeeyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0Ml9leGFtcGxlIiwiZXhwIjoyNTI0NjA4MDAwfQ.dRzzfc9GmzyqfAbl6n_C55JJueraXk9pp3v0UYXw0ic6W_9RVa7aA1zJWm7slX9lbuYldwUtHvqaSsOpjF34uqr0-yMoRDVpIrbkwwJkNuAE8kbXGYFmXf3Ip25wMHtSXn64y2gJN8TtgAAnzjjGs9yzK9BhHILCDZTtmPbsUepxKmWTiEX2BdurUMZzinbcvcKY4Rb_Fl0pwsmBJFs7nmk5PvTyC6qivCd8ZmMc7dwL47mwy_7ouqdqKyUEdLoTEQ_psuy9REw57PRe00XCHaTSTRDCLmy4gAN6J0J056XoRHLfFcNbtzAmqmtJ_D9HGIIXPKq-KaggwK9I4qLX7g\x00"
SERIALIZED_EDGECONTEXT_WITH_EXPIRED_AUTH = b"\x0c\x00\x01\x0b\x00\x01\x00\x00\x00\x0bt2_deadbeef\n\x00\x02\x00\x00\x00\x00\x00\x01\x86\xa0\x00\x0c\x00\x02\x0b\x00\x01\x00\x00\x00\x08beefdead\x00\x0b\x00\x03\x00\x00\x01\xaeeyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0Ml9leGFtcGxlIiwiZXhwIjoxMjYyMzA0MDAwfQ.iUD0J2blW-HGtH86s66msBXymCRCgyxAZJ6xX2_SXD-kegm-KjOlIemMWFZtsNv9DJI147cNP81_gssewvUnhIHLVvXWCTOROasXbA9Yf2GUsjxoGSB7474ziPOZquAJKo8ikERlhOOVk3r4xZIIYCuc4vGZ7NfqFxjDGKAWj5Tt4VUiWXK1AdxQck24GyNOSXs677vIJnoD8EkgWqNuuwY-iFOAPVcoHmEuzhU_yUeQnY8D-VztJkip5-YPEnuuf-dTSmPbdm9ZTOP8gjTsG0Sdvb9NdLId0nEwawRy8CfFEGQulqHgd1bqTm25U-NyXQi7zroi1GEdykZ3w9fVNQ\x00"
SERIALIZED_EDGECONTEXT_WITH_ANON_AUTH = b"\x0c\x00\x01\x0b\x00\x01\x00\x00\x00\x0bt2_deadbeef\n\x00\x02\x00\x00\x00\x00\x00\x01\x86\xa0\x00\x0c\x00\x02\x0b\x00\x01\x00\x00\x00\x08beefdead\x00\x0b\x00\x03\x00\x00\x01\xc0eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlcyI6WyJhbm9ueW1vdXMiXSwic3ViIjpudWxsLCJleHAiOjI1MjQ2MDgwMDB9.gQDiVzOUh70mKKK-YBTnLHWBOEuQyRllEE1-EIMfy3x5K8PsH9FB6Oy9S5HbILjfGFNrIBeux9HyW6hBDikoZDhn5QWyPNitL1pzMNONGGrXzSfaDoDbFy4MLD03A7zjG3qWBn_wLjgzUXX6qVX6W_gWO7dMqrq0iFvEegue-xQ1HGiXfPgnTrXRRovUO3JHy1LcZsmOjltYj5VGUTWXodBM8ObKEealDxg8yskEPy0IuujNMmb9eIyuHB8Ozzpg-lr790lxP37s5HCf18vrZ-IhRmLcLCqm5WSFyq_Ld2ByblBKL9pPst1AZYZTXNRIqovTAqr6v0-xjUeJ1iho9A\x00"


__all__ = [
    "mock",
    "AUTH_TOKEN_PUBLIC_KEY",
    "AUTH_TOKEN_PRIVATE_KEY",
    "AUTH_TOKEN_VALID",
    "SERIALIZED_EDGECONTEXT_WITH_NO_AUTH",
    "SERIALIZED_EDGECONTEXT_WITH_VALID_AUTH",
    "SERIALIZED_EDGECONTEXT_WITH_EXPIRED_AUTH",
]
