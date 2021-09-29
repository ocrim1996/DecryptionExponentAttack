import random
import time
import PublicKeyCryptography as Rsa


# Shows the list of main functions that can be run, and the user chooses one of them.
def option_menu():
    print("---- DECRYPTION EXPONENT ATTACK (EXERCISE 3.2) " + "-" * 100 + "\n")
    print("List of available functions:")
    print("1) Execute Decryption Exponent Attack.")
    print("2) Test Decryption Exponent Attack.")
    print("3) Exit.\n")
    try:
        chosen_function = int(input("\U0000270F Select the number of the function to run: "))
        if 1 <= chosen_function <= 3:
            return chosen_function
        else:
            print("\nYou must enter a number from 1 to 3\n")
    except ValueError:
        print("\nYou must enter a number from 1 to 3\n")


# Gets input from the user and executes.
def get_input(message):
    choice = int(input(message))
    return choice


# Implements the decryption exponent attack, take in input the modulo n, the exponent e and the exponent d and
# returns a non trivial factor of n and the total number of iterations.
def decryption_exponent_attack(n, d, e):
    # Calculate m from (e*d)-1 = (2^r)*m with r>1 and m odd, and initializes the iterations parameter.
    m = e*d - 1
    iteration = 0
    while m % 2 == 0:
        m //= 2
    while True:
        iteration += 1
        # Randomly chooses x in the range [1, n-1].
        x = random.randint(1, n-1)

        n_factor, _, _ = Rsa.extended_euclidean(x, n)
        while n_factor != 1:
            x = random.randint(1, n - 1)
            n_factor, _, _ = Rsa.extended_euclidean(x, n)

        # Calculates x^m mod n
        xj = Rsa.fast_modular_exponentiation(x, m, n)

        # If xj=1 --> changes x value.
        if xj == 1:
            continue
        xj_prev = 0
        while xj != 1:
            xj_prev = xj
            xj = Rsa.fast_modular_exponentiation(xj, 2, n)
        if xj_prev != -1 and xj_prev != n-1:
            n_factor, _, _ = Rsa.extended_euclidean(xj_prev + 1, n)
            return [n_factor, iteration]


# Sets the input values for decryption exponent attack.
def set_decryption_exponential_attack():
    n = get_input("\n\U0000270F Insert the modulo n: ")
    while n <= 0:
        print("\nYou must enter a positive value for the modulo n")
        n = get_input("\n\U0000270F Insert the modulo n: ")
    d = get_input("\U0000270F Insert the exponent d of the private key: ")
    e = get_input("\U0000270F Insert the exponent e of the public key: ")
    factor, iterations = decryption_exponent_attack(n, d, e)
    print("\n\U00002022 Non-Trivial Factor of n:", factor)
    print("\U00002022 Total Algorithm Iterations:", iterations, "\n")


# Sets the function decryption_exponential_attack() on rsa random modules and returns the average algorithm iterations,
# the average and variance of the execution time.
def set_random_modules_test():
    # Takes input values.
    k = get_input("\n\U0000270F Insert the size of modules to be randomly generated (number of bits): ")
    while k <= 0:
        print("\nYou must enter a positive value for the number of bits")
        k = get_input("\n\U0000270F Insert the size of modules to be randomly generated (number of bits): ")

    iterations = get_input("\U0000270F Insert the total number of random modules to be tested: ")
    while iterations <= 0:
        print("\nYou must enter a positive value for the number of random modules\n")
        iterations = get_input("\U0000270F Insert the total number of random modules to be tested: ")

    iteration_sum = 0
    decryption_exp_exec_time = []

    print("\nTest is Started.")
    for i in range(iterations):
        # Calculate Public and Private key
        public_key, private_key = Rsa.generate_rsa_keys(k)

        start = time.perf_counter()
        _, algorithm_iterations = decryption_exponent_attack(public_key[1], private_key[0], public_key[0])
        end = time.perf_counter()
        decryption_exp_exec_time.append(end - start)

        iteration_sum += algorithm_iterations
        print("\rCurrently Tested Modules:", i + 1, end="", flush=True)
    print("\nTest is completed.\n")

    # Calculates average execution time.
    avg_exec_time = sum(decryption_exp_exec_time) / iterations
    # Calculates variance execution time.
    var_exec_time = sum([(j - avg_exec_time) ** 2 for j in decryption_exp_exec_time]) / iterations

    # Print the test results.
    print("----- Test Results -----")
    print("\U00002022 Average Algorithm Iterations Number:", iteration_sum / iterations)
    print("\U00002022 Average Execution Time:", avg_exec_time, "seconds")
    print("\U00002022 Variance of Execution Time:", var_exec_time, "seconds^2\n")


# Exposes all the functions for the various choices.
def main():
    while True:
        # Asks the user what function wants to run.
        choice = option_menu()

        # Executes the function requested by the user.
        try:
            if choice == 1:
                set_decryption_exponential_attack()
            elif choice == 2:
                set_random_modules_test()
            elif choice == 3:
                exit(0)
        except ValueError:
            print("\nYou must enter an integer\n")
        input("Press Enter to return to the Main menu.\n")


if __name__ == '__main__':
    main()
