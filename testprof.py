import os
import subprocess

def compile_latex(tex_content, output_dir="static/mes_fichiers"):
    tex_content = tex_content.replace('<<LOGO_PATH>>', "static/img/logo2.png")

    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Name for the LaTeX file (e.g., main.tex)
        tex_file = os.path.join(output_dir, 'main.tex')

        # Write the LaTeX content to the file in the output directory
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(tex_content)

        # Change the working directory to the output directory
        os.chdir(output_dir)

        # Compile the LaTeX file into a PDF with nonstopmode
        subprocess.run(['pdflatex', '-interaction=nonstopmode', 'main.tex'], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error during LaTeX compilation: {e}")
    except OSError as e:
        print(f"OS error: {e}")
    else:
        print("LaTeX compilation completed successfully.")


