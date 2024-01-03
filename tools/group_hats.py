import os
import string

HATS_DIR = "static/HatsV1"

SERIES = [
    list(string.ascii_letters),
    list(string.digits[1:]),
    ["(" + d + ")" for d in string.digits[1:]],
]


def strip_hat(s):
    prefixes = ("Hat ", "hat ")
    for prefix in prefixes:
        if s.startswith(prefix):
            s = s[len(prefix):]
    return s

def get_common_and_diff(a, b):
    """Get common start and seperate suffixes of a, b."""

    def normalize(name):
        return os.path.splitext(strip_hat(name.lower()))[0]

    a = normalize(a)
    b = normalize(b)

    common = os.path.commonprefix([a, b])

    diff_a = a[len(common):]
    diff_b = b[len(common):]

    return common, diff_a, diff_b


def group():
    names = sorted(os.listdir(HATS_DIR))
    assert names
    # Check for sequential photos with common prefix

    groups = []
    group = [names[0]]
    for name in names[1:]:
        common, diff_a, diff_b = get_common_and_diff(group[0], name)

        is_match = common and len(diff_a) < 5 and len(diff_b) < 5
        # Fix this name and rever this hack
        is_match = is_match and not ("L" in diff_a or "L" in diff_b)

        if is_match:
            group.append(name)
        else:
            groups.append(group)
            group = [name]

    if group:
        groups.append(group)

    for group in groups:
        if len(group) > 1:
            print(group)
            common = get_common_and_diff(group[0], group[1])[0]
            dir_path = os.path.join(HATS_DIR, common)
            if not os.path.isdir(dir_path):
                assert not os.path.exists(dir_path)
                os.mkdir(dir_path)

            for fn in group:
                old_fn = os.path.join(HATS_DIR, fn)
                new_fn = os.path.join(dir_path, fn)
                assert os.path.isfile(old_fn)
                assert not os.path.exists(new_fn)
                os.rename(old_fn, new_fn)

if __name__ == "__main__":
    group()
