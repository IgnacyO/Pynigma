# TODO:AAAAAA
# - multi rotor Enigma machine
import argparse
import string


parser = argparse.ArgumentParser(description="A program that simulates 3 rotor Enigma machine")
parser.add_argument("--encrypt", "-e", action="store_true", help="Encrypt given text")
parser.add_argument("--decrypt", "-d", action="store_true", help="Decrypt given cipher text")
parser.add_argument("--position", "-p", type=str, help="Rotors position: R1R2R3 where each R is a letter for ex. AVF", default="AAA")
parser.add_argument("text", type=str, help="Text to be encrypted or decrypted")
parser.add_argument("--types", "-t", type=str, help="Rotor types({1-5}[3] for ex. 153)", default="123")
parser.add_argument("--indentations", "-i", type=str, help="Rotors indentations: R1R2R3 where each R is a letter for ex. BEG", default="AAA")
args = vars(parser.parse_args())
# TODO:
# - load params from file
# - encrypt or decrypt whole file

ALPHABET = list(string.ascii_uppercase) 
REVERSING_ROTOR_SCHEMA = {pair[0]: pair[1] for pair in "AF  BV  CP  DJ  EI  GO  HY  KR  LZ  MX  NW  QT  SU".split("  ")} # UKW C STAŁY
ROTOR_TYPES = {
    "1": "E K M F L G D Q V Z N T O W Y H X U S P A I B R C J".split(" "),
    "2": "A J D K S I R U X B L H W T M C Q G Z N P Y F V O E".split(" "),
    "3": "B D F H J L C P R T X V Z N Y E I W G A K M U S Q O".split(" "),
    "4": "E S O V P Z J A Y Q U I R H X L N F T G K D C M W B".split(" "),
    "5": "V Z B R G I T Y U P S D N H L X A W M J Q O F E C K".split(" ")
}
rotors = [ROTOR_TYPES[i] for i in args["types"]]
steps = [0, 0, 0]

def shift(rotor_i):
    rotors[rotor_i] = [rotors[rotor_i][l + 1] if l < len(rotors[rotor_i]) - 1 else rotors[rotor_i][-(l + 1)] for l in range(len(rotors[rotor_i]))]
    steps[rotor_i] += 1

def index(iterable, letter):
    return iterable.index(letter)

def rotations():
    shift(0)
    if steps[0] >= 26:
        shift(1)
        steps[0] = 0
    if steps[1] >= 26:
        shift(1)
        shift(2)
        steps[1] = 0

def set_at(positions):
    for i in range(len(rotors)):
        while rotors[i][0] != positions[i]:
            shift(i)

def count_steps(indents):
    global steps
    steps =  [26 - rotors[i].index(indent) for i, indent in enumerate(indents)]

def encrypt_forward(letter, rotor_i):
    res = rotors[rotor_i][index(ALPHABET, letter)]
    if rotor_i < 2:
        return encrypt_forward(res, rotor_i + 1)
    else:
        return res

def encrypt_backward(letter, rotor_i):
    res = rotors[rotor_i][index(ALPHABET, letter)]
    if rotor_i > 0:
        return encrypt_backward(res, rotor_i - 1)
    else:
        return res

def decrypt_forward(letter, rotor_i):
    res = ALPHABET[index(rotors[rotor_i], letter)]
    if rotor_i < 2:
        return decrypt_forward(res, rotor_i + 1)
    else:
        return res

def decrypt_backward(letter, rotor_i):
    res = ALPHABET[index(rotors[rotor_i], letter)]
    if rotor_i > 0:
        return decrypt_backward(res, rotor_i - 1)
    else:
        return res

def reverse(result):
    try:
        return REVERSING_ROTOR_SCHEMA[result]
    except:
        for key_letter, letter_ in REVERSING_ROTOR_SCHEMA.items():
            if result == letter_:
                return key_letter

def encrypt_text(text):
    res = ""
    for letter in text:
        ef = encrypt_forward(letter, 0)
        er = reverse(ef)
        res += encrypt_backward(er, 2)
    print(f"[+] Encrypted text: {res} Position: {args['position']} Indentation: {args['indentations']} Types: {args['types']}")

def decrypt_text(text):
    res = ""
    for letter in text:
        df = decrypt_forward(letter, 0)
        dr = reverse(df)
        res += decrypt_backward(dr, 2)
    print(f"[+] Decrypted text: {res} Position: {args['position']} Indentation: {args['indentations']} Types: {args['types']}")

def main():
    
    set_at(args["position"])
    count_steps(args["indentations"])

    if args["encrypt"]:
        encrypt_text(args["text"].upper().replace(" ", "").strip().replace("/n", ""))
    elif args["decrypt"]:
        decrypt_text(args["text"].upper().replace(" ", "").strip().replace("/n", ""))
    elif args["encrypt"] and args["decrypt"]:
        raise argparse.ArgumentError("You can only set one action to perform: encrypt or decrypt. You can't set both.")
    else:
        raise argparse.ArgumentError("You must specify action to perform: encrypt or decrypt.")
main()