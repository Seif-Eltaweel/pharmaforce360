import os

target_dir = r"d:\portfolio2026\02_PharmaForce360\powerbi"
bom = b'\xef\xbb\xbf'
fixed_files = []
checked_files = 0

for root, dirs, files in os.walk(target_dir):
    for f in files:
        filepath = os.path.join(root, f)
        checked_files += 1
        with open(filepath, 'rb') as fp:
            data = fp.read()
        if data.startswith(bom):
            with open(filepath, 'wb') as fp:
                fp.write(data[len(bom):])
            fixed_files.append(filepath)

print("Checked {0} files.".format(checked_files))
print("Stripped UTF-8 BOM from {0} files:".format(len(fixed_files)))
for path in fixed_files:
    print(" - {0}".format(path))

# Double check if any BOM remains
remaining_bom = []
for root, dirs, files in os.walk(target_dir):
    for f in files:
        filepath = os.path.join(root, f)
        with open(filepath, 'rb') as fp:
            data = fp.read(3)
        if data == bom:
            remaining_bom.append(filepath)

if not remaining_bom:
    print("\nSUCCESS: All files in powerbi/ are completely free of UTF-8 BOM!")
else:
    print("\nWARNING: Found {0} files still with BOM:".format(len(remaining_bom)))
    for path in remaining_bom:
        print(" - {0}".format(path))

