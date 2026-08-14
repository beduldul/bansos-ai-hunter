"""
Modul Reporter untuk Memformat & Mengekspor Hasil Pemindaian (Rich Terminal Table, JSON, CSV, HTML Dashboard).
"""

import json
import csv
import os
from typing import List
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from bansos_ai.core.models import ValidationResult, ScanSummary
from bansos_ai.utils.logger import console, logger

class BansosAIReporter:
    """Reporter untuk menyajikan dan menyimpan data hasil pemindaian AI Relay."""

    @staticmethod
    def display_terminal_table(results: List[ValidationResult]):
        """Menampilkan tabel hasil validasi di terminal menggunakan Rich Table."""
        table = Table(title="✨ HASIL PEMINDAIAN BANSOS AI (RELAY ENDPOINT) ✨", show_lines=True)
        
        table.add_column("No", style="dim", width=4)
        table.add_column("Base URL", style="cyan", no_wrap=True)
        table.add_column("Status Endpoint", style="bold")
        table.add_column("Agent Status", style="bold", justify="center")
        table.add_column("Latency", justify="right")
        table.add_column("API Key Extracted", style="yellow")
        table.add_column("Supported Models", style="green")


        for idx, res in enumerate(results, start=1):
            target = res.target
            
            # Status styling
            if res.is_agent_working:
                agent_status = "[bold green]WORK ✅[/bold green]"
            elif res.is_valid:
                agent_status = "[yellow]ONLINE ⚠️[/yellow]"
            else:
                agent_status = "[red]DEAD ❌[/red]"
                
            status_style = "green" if res.is_valid else "red"
            status_text = f"[{status_style}]{res.status_message}[/{status_style}]"
            
            latency_str = f"{res.latency_ms} ms" if res.latency_ms > 0 else "-"
            key_str = f"{target.api_key[:12]}..." if target.api_key else "[dim]Tidak Ada[/dim]"
            models_str = ", ".join(res.supported_models[:3]) if res.supported_models else "-"
            if len(res.supported_models) > 3:
                models_str += f" (+{len(res.supported_models)-3})"

            table.add_row(
                str(idx),
                target.base_url,
                status_text,
                agent_status,
                latency_str,
                key_str,
                models_str
            )

        console.print(table)

    @staticmethod
    def export_json(summary: ScanSummary, filepath: str):
        """Mengekspor laporan ringkasan ke format JSON."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json.dumps(summary.model_dump(), indent=2, ensure_ascii=False))
        logger.info(f"💾 Laporan JSON berhasil disimpan di: [green]{filepath}[/green]")

    @staticmethod
    def export_csv(results: List[ValidationResult], filepath: str):
        """Mengekspor laporan ke format CSV."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        fieldnames = [
            "base_url", "source", "status_code", "is_valid", "is_agent_working",
            "latency_ms", "api_key", "status_message", "supported_models", "title"
        ]
        
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow({
                    "base_url": r.target.base_url,
                    "source": r.target.source,
                    "status_code": r.status_code,
                    "is_valid": r.is_valid,
                    "is_agent_working": r.is_agent_working,
                    "latency_ms": r.latency_ms,
                    "api_key": r.target.api_key or "",
                    "status_message": r.status_message,
                    "supported_models": "|".join(r.supported_models),
                    "title": r.target.title or ""
                })
        logger.info(f"💾 Laporan CSV berhasil disimpan di: [green]{filepath}[/green]")

    @staticmethod
    def generate_html_dashboard(summary: ScanSummary, filepath: str):
        """Menghasilkan Dashboard HTML modern interaktif untuk melihat daftar Bansos AI."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        cards_html = ""
        for idx, res in enumerate(summary.valid_endpoints, start=1):
            t = res.target
            agent_badge = '<span class="badge badge-success">AGENT WORK ✅</span>' if res.is_agent_working else '<span class="badge badge-warning">ONLINE ⚠️</span>'
            key_html = f'<code>{t.api_key}</code> <button onclick="navigator.clipboard.writeText(\'{t.api_key}\')" class="btn-copy">Copy Key</button>' if t.api_key else '<span class="text-muted">No Direct Key (Free Reg)</span>'
            
            # Rendering Status Per Model
            model_status_tags = ""
            if res.tested_models_status:
                for m_name, is_ok in res.tested_models_status.items():
                    m_cls = "tag-success" if is_ok else "tag-fail"
                    m_icon = "✅" if is_ok else "❌"
                    model_status_tags += f'<span class="tag {m_cls}">{m_name} {m_icon}</span>'
            elif res.supported_models:
                for m_name in res.supported_models[:6]:
                    model_status_tags += f'<span class="tag">{m_name}</span>'
            else:
                model_status_tags = '<span class="text-muted">Standard LLM Endpoint</span>'


            cards_html += f"""
            <div class="card" data-source="{t.source}">
                <div class="card-header">
                    <h3>#{idx} {t.base_url}</h3>
                    {agent_badge}
                </div>
                <div class="card-body">
                    <p><strong>Status:</strong> {res.status_message} ({res.latency_ms} ms)</p>
                    <p><strong>Sumber:</strong> <span class="badge-source">{t.source}</span> | Keyword: <code>{t.matched_keyword or '-'}</code></p>
                    <p><strong>API Key:</strong> {key_html}</p>
                    <div class="models-container">
                        <strong>Status Pengujian Model:</strong>
                        <div class="tags-wrapper">{model_status_tags}</div>
                    </div>
                </div>
                <div class="card-footer">
                    <button onclick="navigator.clipboard.writeText(\'{t.base_url}\')" class="btn-primary">Copy Base URL</button>
                    <a href="{t.base_url}" target="_blank" rel="noopener" class="btn-outline">Buka Web Relay</a>
                </div>
            </div>
            """


        html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Bansos AI & Relay Validator</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --success: #22c55e;
            --warning: #eab308;
            --border: #334155;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 2rem;
        }}
        .header {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        .header h1 {{
            color: var(--accent);
            margin-bottom: 0.5rem;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .stat-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.2rem;
            text-align: center;
        }}
        .stat-card h2 {{
            font-size: 2rem;
            margin: 0;
            color: var(--accent);
        }}
        .stat-card p {{
            margin: 0.5rem 0 0 0;
            color: var(--text-muted);
        }}
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
        }}
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}
        .card-header h3 {{
            margin: 0;
            font-size: 1.1rem;
            color: var(--accent);
            word-break: break-all;
        }}
        .badge {{
            padding: 0.3rem 0.6rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
        }}
        .badge-success {{ background: #166534; color: #4ade80; }}
        .badge-warning {{ background: #854d0e; color: #fef08a; }}
        .card-body p {{
            margin: 0.4rem 0;
            font-size: 0.9rem;
        }}
        .tags-wrapper {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin-top: 0.4rem;
        }}
        .tag-success {{
            background: #14532d !important;
            color: #86efac !important;
            border: 1px solid #22c55e;
        }}
        .tag-fail {{
            background: #451a03 !important;
            color: #fca5a5 !important;
            border: 1px solid #ef4444;
        }}
        .badge-source {{
            background: #1e1b4b;
            color: #a5b4fc;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            border: 1px solid #4338ca;
        }}


        .tag {{
            background: #092635;
            color: #9cdcf0;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
        }}
        .card-footer {{
            margin-top: 1.2rem;
            display: flex;
            gap: 0.5rem;
        }}
        button, .btn-primary, .btn-outline {{
            cursor: pointer;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            border: none;
            font-size: 0.85rem;
            text-decoration: none;
        }}
        .btn-primary {{ background: var(--accent); color: #0f172a; font-weight: bold; }}
        .btn-outline {{ background: transparent; border: 1px solid var(--border); color: var(--text-main); }}
        .btn-copy {{ background: #334155; color: #fff; padding: 0.2rem 0.5rem; font-size: 0.75rem; }}
        code {{ background: #0f172a; padding: 0.2rem 0.4rem; border-radius: 4px; font-family: monospace; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Dashboard Bansos AI & Relay Hunter</h1>
        <p class="text-muted">Hasil pemindaian endpoint AI Proxy publik & pengujian status agen AI</p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <h2>{summary.total_found}</h2>
            <p>Total Ditemukan</p>
        </div>
        <div class="stat-card">
            <h2>{summary.total_valid}</h2>
            <p>Endpoint Online</p>
        </div>
        <div class="stat-card">
            <h2>{summary.total_agent_ready}</h2>
            <p>Agent Ready (Work)</p>
        </div>
        <div class="stat-card">
            <h2>{summary.duration_seconds}s</h2>
            <p>Waktu Pemindaian</p>
        </div>
    </div>

    <div class="cards-grid">
        {cards_html or '<p>Tidak ada endpoint valid ditemukan dalam pemindaian ini.</p>'}
    </div>
</body>
</html>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info(f"🌐 Dashboard HTML interaktif berhasil dibuat di: [green]{filepath}[/green]")
