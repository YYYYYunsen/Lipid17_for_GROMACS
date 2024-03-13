import os
import subprocess

def extract_section(input_file_path, output_file_path):
    start_marker = "[ moleculetype ]"
    end_marker = "; Include Position restraint file"
    extract = False
    extracted_content = []

    with open(input_file_path, 'r') as file:
        for line in file:
            if start_marker in line:
                extract = True
                extracted_content.append(line)
            elif end_marker in line:
                extract = False
                break  
            elif extract:
                extracted_content.append(line)
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(extracted_content)

def convert_molecule_formats(directory):
    os.chdir(directory)
    for filename in os.listdir('.'):
        if filename.endswith('.gro'):  
            base_filename = filename[:-4]
            output_filename = base_filename
            # replace the "amber14SB_ROC_lipid17" to your forcefield
            command = f"gmx pdb2gmx -f {base_filename} -water spc -ff amber14SB_ROC_lipid17 -p {output_filename}.top"
            subprocess.run(command, shell=True)
            input_file_path = f'{output_filename}.top'
            output_file_path = f'{output_filename}.itp'
            # Execute the function
            extract_section(input_file_path, output_file_path)
            try:
                with open(output_file_path, 'r') as file:
                    content = file.read()
                updated_content = content.replace('Other', f"{output_filename}")
                with open(output_file_path, 'w') as file:
                    file.write(updated_content)

                print("File updated successfully.")
            except FileNotFoundError:
                print("The file was not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

convert_molecule_formats('path')

