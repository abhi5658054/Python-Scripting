def count_letters(word_list):
    """ See question description """
    
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    letter_count = {}
    for letter in ALPHABET:
        letter_count[letter] = 0
        
    # enter code here
    for word in word_list:
        for letter in word:
            letter_count[letter] += 1
    sorted_dict = sorted(letter_count.items())

    sorted_dict.sort(key = lambda x :x[1])
    print(sorted_dict[-1][1])



if __name__ == "__main__":
    print("This is main")
    monty_quote = "listen strange women lying in ponds distributing swords is no basis for a system of government supreme executive power derives from a mandate from the masses not from some farcical aquatic ceremony"
    monty_words = monty_quote.split(" ")
    count_letters(["hello", "world"])
    count_letters(monty_words)
