"""
Bansos AI Hunter - Main CLI Application Entry Point.
"""

import sys
import argparse
import asyncio
from typing import List

from bansos_ai import __version__
from bansos_ai.config import CHINESE_KEYWORDS, GLOBAL_KEYWORDS
from bansos_ai.core.scraper import BansosAIScraper
from bansos_ai.core.validator import BansosAIValidator
from bansos_ai.core.reporter import BansosAIReporter
from bansos_ai.core.models import ScanSummary, RelayTarget
from bansos_ai.utils.logger import logger, console

async def run_scan(args):
    """Menjalankan alur kerja pemindaian lengkap (Scrape -> Validate -> Report)."""
    console.print(f"[bold cyan]Memulai Bansos AI Hunter v{__version__}[/bold cyan]")
    
    custom_kws = args.keywords.split(",") if args.keywords else None
    scraper = BansosAIScraper(max_results_per_query=args.limit)
    
    # Step 1: Scrape
    targets = await scraper.scrape_all(
        include_chinese=not args.no_chinese,
        custom_keywords=custom_kws
    )
    
    if not targets:
        logger.warning("Tidak ada target relay yang ditemukan dari pemindaian web.")
        return

    # Step 2: Validate
    start_time = asyncio.get_event_loop().time()
    validator = BansosAIValidator(timeout=args.timeout)
    results = await validator.validate_batch(targets, max_concurrency=args.concurrency)
    duration = round(asyncio.get_event_loop().time() - start_time, 2)
    
    # Step 3: Filter & Summarize
    valid_results = [r for r in results if r.is_valid]
    agent_ready = [r for r in results if r.is_agent_working]
    
    summary = ScanSummary(
        total_found=len(targets),
        total_valid=len(valid_results),
        total_agent_ready=len(agent_ready),
        duration_seconds=duration,
        valid_endpoints=valid_results
    )

    # Step 4: Report / Output
    BansosAIReporter.display_terminal_table(results)
    
    out_dir = args.output_dir
    if args.format in ["html", "all"]:
        BansosAIReporter.generate_html_dashboard(summary, f"{out_dir}/bansos_dashboard.html")
    if args.format in ["json", "all"]:
        BansosAIReporter.export_json(summary, f"{out_dir}/bansos_summary.json")
    if args.format in ["csv", "all"]:
        BansosAIReporter.export_csv(results, f"{out_dir}/bansos_report.csv")

async def run_direct_test(args):
    """Menjalankan pengujian langsung terhadap satu Base URL / API Key."""
    console.print(f"[cyan]Menguji langsung endpoint:[/cyan] [bold]{args.url}[/bold]")
    target = RelayTarget(
        url=args.url,
        base_url=args.url,
        api_key=args.key,
        source="Direct Test"
    )
    
    validator = BansosAIValidator(timeout=args.timeout)
    res = await validator.validate_target(target)
    
    BansosAIReporter.display_terminal_table([res])

def main():
    parser = argparse.ArgumentParser(
        description='Bansos AI Hunter - Pemindai & Validator Automated Endpoint AI Relay ("AI中转站") & Kuota Gratis.'
    )
    parser.add_argument("--version", "-v", action="version", version=f"Bansos AI Hunter v{__version__}")

    
    subparsers = parser.add_subparsers(dest="command", help="Perintah yang tersedia")
    
    # Sub-command 'scan'
    scan_parser = subparsers.add_parser("scan", help="Menjalankan pemindaian otomatis dari web & forum")
    scan_parser.add_argument("--no-chinese", action="store_true", help="Nonaktifkan kata kunci bahasa Mandarin")
    scan_parser.add_argument("--keywords", type=str, help="Kata kunci kustom (dipisahkan koma)")
    scan_parser.add_argument("--limit", type=int, default=10, help="Batas pencarian per kata kunci (default: 10)")
    scan_parser.add_argument("--timeout", type=float, default=8.0, help="Timeout koneksi HTTP dalam detik (default: 8.0)")
    scan_parser.add_argument("--concurrency", type=int, default=15, help="Jumlah thread pengujian paralel (default: 15)")
    scan_parser.add_argument("--output-dir", type=str, default="output_reports", help="Direktori hasil ekspor (default: output_reports)")
    scan_parser.add_argument("--format", choices=["table", "html", "json", "csv", "all"], default="all", help="Format laporan (default: all)")

    # Sub-command 'test'
    test_parser = subparsers.add_parser("test", help="Menguji endpoint relay tunggal secara langsung")
    test_parser.add_argument("--url", required=True, help="Base URL endpoint relay (misal: https://api.example.com)")
    test_parser.add_argument("--key", help="API Key jika ada (misal: sk-...)")
    test_parser.add_argument("--timeout", type=float, default=8.0, help="Timeout koneksi HTTP")

    args = parser.parse_args()

    if args.command == "scan":
        asyncio.run(run_scan(args))
    elif args.command == "test":
        asyncio.run(run_direct_test(args))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
