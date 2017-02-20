import urllib.request, urllib.error
import primality
import random

def check_quota():
    url = 'https://www.random.org/quota/?format=plain'
    try:
        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8')
            return text
    except urllib.error.HTTPError as e:
            print("Error checking quota: " + str(e.code))
            return -1

def get_max_bits(pseudo=False):
    '''
    gets the maximum number of random bits from random.org and returns them as a hex string.
    when pseudo is enabled, if unable to get random bits from random.org (quota is full, etc),
    it will use python's pseudo random bit generator to make a string in the same format
    '''
    url = 'https://www.random.org/cgi-bin/randbyte?nbytes=16384&format=h'
    if int(check_quota()) > 0:
        try:
            with urllib.request.urlopen(url) as response:
                text = response.read().decode('utf-8').replace(' ', '').replace('\n', '')
                return text
        except urllib.error.HTTPError as e:
                print("Error: " + str(e.code))
                if pseudo:
                    return '%x' % random.getrandbits(16384)
    elif pseudo:
        return '%x' % random.getrandbits(16384)
    else:
        print("Quota full, try again later")


def get_keys(num_bits=1024, num_keys=2, pseudo=False):
    '''
    returns a list of num_keys prime numbers with num_bits bits. Default is 1024
    because of limit to number of bytes we can get from Random.org
    experts recommend 2048 for security
    pseudo enables python's pseudorng if unable to get random bits
    TODO: allow kwarg to choose primality test
    '''
    bits = get_max_bits(pseudo)
    if not bits:
        print("Unable to get bits")
        return
    keys = []

    for i in range(0, 16394, num_bits // 16):
        current_string = bits[i : i + num_bits // 16]
        if not current_string:
            break
        if primality.miller_rabin(int(current_string, 16)):
            keys.append(int(current_string, 16))

    if len(keys) < num_keys:
        keys.extend(get_keys(num_bits, num_keys - len(keys), pseudo))
    if len(keys) > num_keys:
        keys = random.sample(keys, num_keys)
    return keys
get_keys(pseudo=True)
