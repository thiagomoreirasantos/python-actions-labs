#!/usr/bin/env python3
"""
Script para rodar no GitHub Actions:
- Mostra informações do workflow/run
- Lista arquivos na raiz do repositório
- Gera output/run_info.json com um resumo
"""
from __future__ import annotations
import os
from pathlib import Path
from datetime import datetime, timezone
import json

def main() -> None:
    repo = os.getenv("GITHUB_REPOSITORY", "desconhecido")
    sha = (os.getenv("GITHUB_SHA") or "")[:7]
    ref = os.getenv("GITHUB_REF_NAME") or os.getenv("GITHUB_REF", "")
    run_id = os.getenv("GITHUB_RUN_ID", "")
    workflow = os.getenv("GITHUB_WORKFLOW", "")
    runner_os = os.getenv("RUNNER_OS", "")

    print("Olá, GitHub Actions (Python)!")
    print(f"Repositório: {repo}")
    print(f"Workflow: {workflow} | Run ID: {run_id}")
    print(f"Branch/Ref: {ref} | Commit: {sha}")
    print(f"Runner: {runner_os}")

    root = Path(".").resolve()
    print("\nArquivos no repositório (nível raiz):")
    for p in sorted(root.iterdir()):
        if p.name.startswith(".git"):
            continue
        print(f" - {p.name}/" if p.is_dir() else f" - {p.name}")

    # Gera um JSON com resumo do run
    out = {
        "repository": repo,
        "workflow": workflow,
        "run_id": run_id,
        "ref": ref,
        "commit": sha,
        "runner_os": runner_os,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    Path("output").mkdir(exist_ok=True)
    Path("output/run_info.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("\nResumo salvo em output/run_info.json")

if __name__ == "__main__":
    main()
