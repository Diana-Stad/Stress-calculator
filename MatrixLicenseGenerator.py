import random
import string


class MatrixLicenseGenerator:
    def __init__(self):
        self.attempts_limit = 1000
        self.current_generated_code = None

    def random_values(self, count, max_val):
        return [random.randint(0, max_val) for _ in range(count)]

    def number_to_letter(self, num):
        return string.ascii_uppercase[num]

    def solve_matrix_system(self, a, b, c, d, matrix_type):
        if matrix_type == "letters":
            p = 2 * a + c + random.randint(1, 10)
            q = 2 * b + d + random.randint(1, 10)
            r = a + 3 * c + random.randint(1, 10)
            s = b + 3 * d + random.randint(1, 10)

            try:
                e = (3 * p - r) / 5
                f = (3 * q - s) / 5
                g = (2 * r - p) / 5
                h = (2 * s - q) / 5

                if all(x.is_integer() for x in [e, f, g, h]):
                    return int(e), int(f), int(g), int(h)
            except:
                pass

        elif matrix_type == "digits":
            p = 3 * a + 2 * c + random.randint(1, 5)
            q = 3 * b + 2 * d + random.randint(1, 5)
            r = 2 * a + 5 * c + random.randint(1, 5)
            s = 2 * b + 5 * d + random.randint(1, 5)

            try:
                e = (5 * p - 2 * r) / 11
                f = (5 * q - 2 * s) / 11
                g = (3 * r - 2 * p) / 11
                h = (3 * s - 2 * q) / 11

                if all(x.is_integer() for x in [e, f, g, h]):
                    e, f, g, h = int(e), int(f), int(g), int(h)
                    if all(0 <= x <= 9 for x in [e, f, g, h]):
                        return e, f, g, h
            except:
                pass

        return None

    def solution_valid(self, solution, max_val):
        if solution is None:
            return False
        return all(0 <= x <= max_val for x in solution)

    def generate_key_parts(self, max_val, matrix_type):
        attempts = 0
        while attempts < self.attempts_limit:
            a, b, c, d = self.random_values(4, max_val)
            solution = self.solve_matrix_system(a, b, c, d, matrix_type)
            if self.solution_valid(solution, max_val):
                return a, b, c, d, solution
            attempts += 1
        return self.generate_key_parts(max_val, matrix_type)

    def format_key(self, letters1, letters2, digits1, digits2):
        letters_part1 = ''.join(self.number_to_letter(x) for x in letters1)
        letters_part2 = ''.join(self.number_to_letter(x) for x in letters2)
        digits_part1 = ''.join(str(x) for x in digits1)
        digits_part2 = ''.join(str(x) for x in digits2)
        return f"{letters_part1}-{letters_part2}-{digits_part1}-{digits_part2}"

    def generate_key(self):
        a1, b1, c1, d1, (e1, f1, g1, h1) = self.generate_key_parts(25, "letters")
        a2, b2, c2, d2, (e2, f2, g2, h2) = self.generate_key_parts(9, "digits")
        self.current_generated_code = self.format_key([a1, b1, c1, d1], [e1, f1, g1, h1],
                                                      [a2, b2, c2, d2], [e2, f2, g2, h2])
        return self.current_generated_code

    def validate_code(self, entered_code):
        return entered_code == self.current_generated_code