import math
import time
import random


# Shows the list of main functions that can be run, and the user chooses one of them.
def option_menu():
    print("---- PUBLIC KEY CRYPTOGRAPHY (EXERCISE 3.1) " + "-" * 100 + "\n")
    print("List of available functions:")
    print("1) Extended Euclidean Algorithm.")
    print("2) Fast Modular Exponentiation.")
    print("3) Miller-Rabin Test.")
    print("4) Prime Number Generator.")
    print("5) RSA SCHEMA.")
    print("6) Exit.\n")
    try:
        chosen_function = int(input("\U0000270F Select the number of the function to run: "))
        if 1 <= chosen_function <= 6:
            return chosen_function
        else:
            print("\nYou must enter a number from 1 to 6\n")
    except ValueError:
        print("\nYou must enter a number from 1 to 6\n")


# Shows the sub-list of RSA schema functions that can be run, and the user chooses one of them.
def sub_option_menu():
    print("\n**** RSA SCHEMA " + "*" * 100 + "\n")
    print("List of available functions:")
    print("1) RSA Keys Generator (Public and Private Key).")
    print("2) RSA Encryption.")
    print("3) RSA Decryption.")
    print("4) Test RSA Decryption With and Without CRT.")
    print("5) Return to the Main Menu.\n")
    try:
        chosen_sub_function = int(input("\U0000270F Select the number of the function to run: "))
        if 1 <= chosen_sub_function <= 5:
            return chosen_sub_function
        else:
            print("\nYou must enter a number from 1 to 5\n")
    except ValueError:
        print("\nYou must enter a number from 1 to 5\n")


# Gets input from the user and executes.
def get_input(message):
    choice = int(input(message))
    return choice


# Executes the extended euclidean algorithm, returns the GCD and the Bezout Identity coefficients.
def extended_euclidean(a, b):
    a, b = abs(a), abs(b)
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


# Converts a decimal number to a binary number.
def decimal_to_binary(x):
    return int(bin(x)[2:])


# Fast modular exponentiation algorithm.
# Complexity of the algorithm: proportional complexity of a k^3 [O(k^3) = c * k^3  then  k = log_2 (n)].
def fast_modular_exponentiation(a, exp, n):
    # Partial sums accumulator (d).
    d = 1
    # Counter (c) (c is used only for correctness).
    c = 0
    exp_bin = decimal_to_binary(exp)
    for i in str(exp_bin):
        d = (d * d) % n
        c = 2 * c
        if int(i) == 1:
            d = (d * a) % n
            c = c + 1
    return d


# Computes the Miller-Rabin test for a number given the number of rounds, returns True if the number is composite or
# returns False if the number is not composite (i.e. it is a prime number).
def miller_rabin_test(n, rounds=40):
    if n == 1 or n == 2 or n == 3:
        return False
    if n % 2 == 0:
        return True
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for i in range(rounds):
        a = random.randrange(2, n - 1)
        x = fast_modular_exponentiation(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(r - 1):
            x = fast_modular_exponentiation(x, 2, n)
            if x == n - 1:
                break
        else:
            return True
    return False


# Generates a random k-bit prime number.
def generate_prime(k, rounds=40):
    if k < 2:
        return None
    while True:
        number = random.randrange(pow(2, k - 1) + 1, pow(2, k), 2)
        if not miller_rabin_test(number, rounds):
            return number


# Generates a k-bit RSA public and private key pair (with or without the Chinese Remainder Theorem (CRT)).
def generate_rsa_keys(k, crt=False, rounds=40):
    # The least integer greater than or equal to k.
    k1 = int(math.ceil(k / 2))
    # The greatest integer less than or equal to k.
    k2 = int(math.floor(k / 2))
    p = q = 0

    while p == q:
        p = generate_prime(k1, rounds)
        q = generate_prime(k2, rounds)

    if crt and q > p:
        p, q = q, p
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        # Finds "e < phi".
        e = random.randrange(2, phi // 2)
        g, d, _ = extended_euclidean(e, phi)

        # Checks if "e" and "phi" are relatively prime numbers.
        if g == 1:
            public_key = (e, n)
            d = d % phi
            if d < 0:
                d += phi
            if crt:
                d_p, d_q, q_inv = crt_pre_computation(p, q, d)
                private_key = (p, q, d_p, d_q, q_inv)
            else:
                private_key = (d, n)
            return public_key, private_key


# Pre-computation for RSA with CRT (Chinese Remainder Theorem).
def crt_pre_computation(p, q, d):
    _, q_inv, _ = extended_euclidean(q, p)
    return d % (p - 1), d % (q - 1), q_inv % p


# RSA encryption.
def rsa_encryption(m, public_key):
    return fast_modular_exponentiation(m, public_key[0], public_key[1])


# RSA decryption.
def rsa_decryption(c, private_key, crt=False):
    if not crt:
        return rsa_encryption(c, private_key)
    else:
        m1 = fast_modular_exponentiation(c, private_key[2], private_key[0])
        m2 = fast_modular_exponentiation(c, private_key[3], private_key[1])
        h = (private_key[4] * (m1 - m2)) % private_key[0]
        return (m2 + h * private_key[1]) % (private_key[0] * private_key[1])


# ---------------------- Setting of All Functions ---------------------------------

# Sets Extended Euclidean Algorithm.
def set_extended_euclidean():
    a = get_input("\n\U0000270F Insert the first integer: ")
    b = get_input("\U0000270F Insert the second integer: ")
    gcd, x, y, = extended_euclidean(a, b)
    print("\n\U00002022 Greatest Common Divisor (GCD):", gcd)
    print("\U00002022 Bezout Identity Coefficients (x, y):", "(", x, ",", y, ")\n")


# Sets Fast Modular Exponentiation.
def set_fast_modular_exponentiation():
    # Base.
    a = get_input("\n\U0000270F Insert the base: ")

    # Exponent.
    exp = get_input("\U0000270F Insert the exponent: ")
    # Checks the the exponent value.
    while exp < 0:
        print("\nYou must enter a correct value for the exponent (exp>=0)\n")
        exp = get_input("\U0000270F Insert the exponent: ")

    # Modulo.
    n = get_input("\U0000270F Insert the modulo: ")
    # Checks the modulo value.
    while n < 1:
        print("\nYou must enter a correct value for the modulo (n>=1)\n")
        n = get_input("\U0000270FInsert the modulo: ")

    print("\n\U00002022 Fast Modular Exponentiation:", fast_modular_exponentiation(a, exp, n), "\n")


# Sets Miller-Rabin Test.
def set_miller_rabin_test():
    n = get_input("\n\U0000270F Insert an integer: ")
    if n > 0:
        rounds = get_input("\U0000270F Insert the number of rounds to execute (default=40): ")
        if miller_rabin_test(n, rounds):
            print("\n\U00002022 Miller-Rabin Test: composite number", "\n")
        else:
            print("\n\U00002022 Miller-Rabin Test: prime number", "\n")
    else:
        print("\nYou must enter a correct value for the parameter (n>0)")
        set_miller_rabin_test()


# Set Prime Number Generator.
def set_generate_prime():
    k = get_input("\n\U0000270F Insert number of bits (k>1): ")
    rounds = get_input("\U0000270F Insert the number of rounds for Miller-Rabin Test (default=40): ")
    print("\n\U00002022 Generated Prime Number:", generate_prime(k, rounds), "\n")


# Sets RSA keys Generator (Public Key and the Private Key for the RSA schema are set).
def set_rsa_keys():
    n = get_input("\n\U0000270F Insert the number of bits for the modulo n: ")
    while n < 5:
        print("\nYou must enter a correct value for the parameter n (n>4)")
        n = get_input("\n\U0000270F Insert the number of bits for the modulo n: ")
    crt = input("\U0000270F Do you want to use CRT optimization? (Y or N): ")
    if crt.upper() == 'Y':
        crt = True
    else:
        crt = False
    rounds = get_input("\U0000270F Insert the number of rounds for Miller-Rabin Test (default=40): ")
    public_key, private_key = generate_rsa_keys(n, crt, rounds)
    print("\n\U00002022 Public Key (e, n):", public_key)
    if crt:
        print("\U00002022 Private Key (p, q, d_p, d_q, q_inv):", private_key, "\n")
    else:
        print("\U00002022 Private Key (d, n):", private_key, "\n")


# Sets RSA encryption (m: message (plaintext), e: public key exponent, n: modulo)
def set_rsa_encryption():
    m = get_input("\n\U0000270F Insert the message m: ")
    e = get_input("\U0000270F Insert the exponent e of the public key: ")
    n = get_input("\U0000270F Insert the modulo n: ")
    print("\n\U00002022 Generated ciphertext c:", rsa_encryption(m, (e, n)), "\n")


# Sets RSA decryption (c: ciphertext, d: private key exponent, n: modulo).
def set_rsa_decryption():
    c = get_input("\n\U0000270F Insert the ciphertext c: ")
    d = get_input("\U0000270F Insert the exponent d of the private key: ")
    n = get_input("\U0000270F Insert the modulo n: ")
    print("\n\U00002022 Plaintext message m:", rsa_decryption(c, (d, n)), "\n")


# Sets RSA Decryption With and Without CRT (e.g. Total Execution Time on 100 random ciphertext of 1024 bits)
def set_rsa_with_without_crt():
    # Checks the value of the prime number p.
    p = get_input("\n\U0000270F Insert the first prime number p: ")
    while miller_rabin_test(p):
        print("\nThis number p is not a prime number, you must enter a prime number")
        p = get_input("\n\U0000270F Insert the first prime number p: ")

    # Checks the value of the prime number q.
    q = get_input("\U0000270F Insert the second prime number q: ")
    while miller_rabin_test(q):
        print("\nThis number q is not a prime number, you must enter a prime number")
        q = get_input("\n\U0000270F Insert the first prime number q: ")

    d = get_input("\U0000270F Insert the exponent d of the private key: ")
    if q > p:
        p, q = q, p
    n = p * q
    private_key = (d, n)
    d_p, d_q, q_inv = crt_pre_computation(p, q, d)
    crt_private_key = (p, q, d_p, d_q, q_inv)
    print("\n\U00002022 RSA without CRT - Private Key (d, n):", private_key)
    print("\U00002022 RSA with CRT - Private Key (p, q, d_p, d_q, q_inv):", crt_private_key, "\n")

    k = get_input("\U0000270F Insert the size of ciphertext to be randomly generated (number of bits): ")
    ciphertext_num = get_input("\U0000270F Insert the number of ciphertext to be tested: ")

    # Here begins the test.
    decryption_exec_time = 0
    crt_decryption_exec_time = 0
    print("\nTest is Started.")
    for i in range(ciphertext_num):
        ciphertext = random.getrandbits(k)

        # RSA Decryption without CRT (the "crt" parameter of the rsa_decryption() is by default False).
        start = time.perf_counter()
        rsa_decryption(ciphertext, private_key)
        end = time.perf_counter()
        decryption_exec_time += end - start

        # RSA Decryption with CRT (the "crt" parameter of the rsa_decryption() is set to True).
        start = time.perf_counter()
        rsa_decryption(ciphertext, crt_private_key, True)
        end = time.perf_counter()
        crt_decryption_exec_time += end - start

        print("\rCurrently Tested Ciphertexts:", i+1, end="", flush=True)

    print("\nTest is completed.\n")

    print("----- RSA Decryption without CRT -----")
    print("\U00002022 Total Execution Time on", ciphertext_num, "Random Ciphertext of", k, "bits:",
          decryption_exec_time, "seconds")
    print("\n----- RSA Decryption with CRT ------")
    print("\U00002022 Total Execution Time on", ciphertext_num, "Random Ciphertext of", k, "bits:",
          crt_decryption_exec_time, "seconds\n")


# Exposes all the functions for the various choices.
def main():
    while True:
        # Asks the user what function wants to run
        choice = option_menu()

        # Executes the function requested by the user
        # Main Menu options.
        try:
            if choice == 1:
                set_extended_euclidean()
            elif choice == 2:
                set_fast_modular_exponentiation()
            elif choice == 3:
                set_miller_rabin_test()
            elif choice == 4:
                set_generate_prime()
            elif choice == 5:
                while True:
                    sub_choice = sub_option_menu()
                    # RSA Schema Menu options.
                    try:
                        if sub_choice == 1:
                            set_rsa_keys()
                        elif sub_choice == 2:
                            set_rsa_encryption()
                        elif sub_choice == 3:
                            set_rsa_decryption()
                        elif sub_choice == 4:
                            set_rsa_with_without_crt()
                        elif sub_choice == 5:
                            break
                    except ValueError:
                        print("\nYou must enter an integer\n")
                    input("Press Enter to return to the RSA SCHEMA menu.\n")
            elif choice == 6:
                exit(0)
        except ValueError:
            print("\nYou must enter an integer\n")
        input("\nPress Enter to return to the Main menu.\n")


if __name__ == '__main__':
    main()
