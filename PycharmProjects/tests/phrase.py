def test_input_length():
    # Ask user for input
    phrase = input("Set a phrase with less then 15 characters: ")

    # Determine length of input
    input_length = len(phrase)

    # Validate that the input is less then 15 character long
    input_length = 15
    assert input_length > len(phrase), "Length of input doesn't match the determined length"

    print("Input phrase length is less then 15 and matches the determined length")

if __name__ == "__main__":
    test_input_length()
