from datetime import datetime

input_path = "us-counties-max-new.txt"
# output_path = "us-counties-max-new.txt"


def check_and_fix_line(line):
    parts = line.strip().split("\t")
    if len(parts) != 5:
        return False, "Column count mismatch", line
    try:
        datetime.strptime(parts[0], "%Y-%m-%d")
    except ValueError as e:
        return False, f"Invalid date format: {e}", line

    try:
        parts[3] = int(parts[3]) if parts[3] else 0
        parts[4] = int(parts[4]) if parts[4] else 0
    except ValueError as e:
        return False, f"Invalid value for cases or deaths: {e}", line

    return True, None, "\t".join(map(str, parts))


invalid_lines = []
valid_lines = []

with open(input_path, "r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        is_valid, error_message, processed_line = check_and_fix_line(line)
        if is_valid:
            valid_lines.append(processed_line.strip())
        else:
            invalid_lines.append((line_number, line.strip(), error_message))

print(f"Invalid data lines: {len(invalid_lines)}")

if invalid_lines:
    print("Invalid lines found:")
    for line_number, line, error in invalid_lines:
        print(f"Line {line_number}: {repr(line)} | Error: {error}")
else:
    print("No invalid lines found.")

'''
# save
if valid_lines:
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(valid_lines))
    print(f"Valid data saved to: {output_path}")
'''