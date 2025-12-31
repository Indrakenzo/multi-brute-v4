import itertools

class WordlistArchitect:
    def __init__(self):
        self.leets = {'a': '@', 'i': '1', 'e': '3', 'o': '0', 's': '$', 'g': '9'}
    
    def get_permutations(self, word):
        # Mengubah kata menjadi variasi case (lower, upper, title)
        base = {word, word.lower(), word.upper(), word.title()}
        results = set(base)
        
        # Leetspeak transformation
        leet_word = ""
        for char in word.lower():
            leet_word += self.leets.get(char, char)
        results.add(leet_word)
        return list(results)

    def generate(self):
        print("[*] --- TARGET PROFILING INTERFACE ---")
        base_name = input("Nama Depan Target : ").strip()
        last_name = input("Nama Belakang/Nick: ").strip()
        birth_year = input("Tahun Lahir (YYYY): ").strip()
        extra_key = input("Kata Kunci (Hobi/Hewan/Pacar): ").strip()
        
        # Kumpulkan elemen dasar
        elements = [x for x in [base_name, last_name, extra_key] if x]
        years = [birth_year, birth_year[-2:]] if birth_year else []
        symbols = ['!', '@', '#', '123', '123!', '?']

        final_list = set()

        # Level 1: Permutasi Dasar
        for item in elements:
            perms = self.get_permutations(item)
            for p in perms:
                final_list.add(p)
                # Level 2: Append Tahun & Simbol
                for y in years:
                    final_list.add(f"{p}{y}")
                    final_list.add(f"{p}{y}!")
                for s in symbols:
                    final_list.add(f"{p}{s}")

        # Level 3: Kombinasi Kompleks (Nama+Marga)
        if base_name and last_name:
            final_list.add(f"{base_name}{last_name}")
            final_list.add(f"{base_name}.{last_name}")
            final_list.add(f"{base_name}_{last_name}")

        # Output File
        filename = f"{base_name}_target.txt"
        with open(filename, "w") as f:
            for pwd in final_list:
                f.write(pwd + "\n")
        
        print(f"\n[SUCCESS] Wordlist cerdas berhasil dibuat: {filename}")
        print(f"[INFO] Total Payload: {len(final_list)} kombinasi password.")

if __name__ == "__main__":
    WordlistArchitect().generate()
