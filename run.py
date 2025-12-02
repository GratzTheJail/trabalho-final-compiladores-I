import os
import subprocess
import sys

def run_compiler_for_all_obsact():
    # Diretório atual (onde analisador.py está)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Subpasta onde estão os arquivos .obsact
    test_dir = os.path.join(current_dir, "testes")
    
    # Verifica se a pasta testes existe
    if not os.path.exists(test_dir):
        print(f"Erro: Diretório 'testes' não encontrado em {current_dir}")
        sys.exit(1)
    
    # Caminho completo para analisador.py
    analisador_path = os.path.join(current_dir, "analisador.py")

    # Lista todos os arquivos .obsact na pasta testes
    obsact_files = [f for f in os.listdir(test_dir) if f.endswith('.obsact')]
    
    if not obsact_files:
        print("Nenhum arquivo .obsact encontrado na pasta 'testes'")
        return
    
    print(f"Encontrados {len(obsact_files)} arquivo(s) .obsact:")
    
    # Processa cada arquivo .obsact
    for obsact_file in obsact_files:
        # Remove a extensão .obsact para passar como argumento
        file_name_without_ext = obsact_file[:-7]  # Remove '.obsact'
        file_path = os.path.join(test_dir, file_name_without_ext)
        
        print(f"\n--- Processando: {obsact_file} ---")
        
        # Executa o analisador.py com o nome do arquivo como argumento
        try:
            # Usa o mesmo interpretador Python que está executando este script
            result = subprocess.run(
                [sys.executable, analisador_path, file_name_without_ext],
                cwd=test_dir,  # Muda o diretório de trabalho para a pasta testes
                capture_output=True,
                text=True,
                timeout=10  # Timeout de 10 segundos por arquivo
            )
            
            # Exibe a saída
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("Erros:", result.stderr)
            
            print(f"Status: {'Sucesso' if result.returncode == 0 else 'Falhou'}")
            
        except subprocess.TimeoutExpired:
            print(f"Timeout ao processar {obsact_file}")
        except Exception as e:
            print(f"Erro ao executar o compilador: {e}")

if __name__ == "__main__":
    run_compiler_for_all_obsact()
    print("\nProcessamento concluído!")