def test_input_length():
    # Ask user for input
    phrase = input("Set a phrase")

    # Determine length of input
    input_length = len(phrase)

    # Compare input length with determined length
    input_length = 15
    assert input_length == len(phrase), "Length of input doesn't match the determined length"

    print("Input length matches determined length")

if __name__ == "__main__":
    test_input_length()
