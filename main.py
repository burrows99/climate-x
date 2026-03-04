"""
Climate Risk Analysis Tool - Parallel execution for speed
Entry point - orchestrates API, analysis, reporting
"""

import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from api_client import ClimateAPI
from analyzer import RiskAnalyzer
from reporter import ReportGenerator
from portfolio_data import PORTFOLIO
from logger import get_logger
import config

logger = get_logger()


def fetch_asset_parallel(api, asset_data, index, total):
    """Worker function for parallel API calls"""
    logger.info(f"[{index}/{total}] Processing {asset_data['name']}...")
    response = api.fetch_risk(asset_data)
    
    if response["success"]:
        logger.info(f"  {asset_data['name']}: Success")
    else:
        logger.error(f"  {asset_data['name']}: {response.get('error', 'Failed')}")
    
    return asset_data['name'], response


def main():
    """Execute portfolio risk analysis with parallel processing"""
    logger.info("="*60)
    logger.info("Climate Risk Portfolio Analysis (Parallel)")
    logger.info("="*60)
    
    api = ClimateAPI()
    analyzer = RiskAnalyzer()
    reporter = ReportGenerator()
    
    Path("output").mkdir(exist_ok=True)
    
    # Parallel execution with ThreadPoolExecutor
    logger.info(f"Analyzing {len(PORTFOLIO)} assets in parallel...")
    
    assets = []
    raw_responses = []
    failed_count = 0
    start_time = time.time()
    
    # Execute API calls in parallel (max 5 concurrent)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(fetch_asset_parallel, api, asset_data, i, len(PORTFOLIO)): asset_data
            for i, asset_data in enumerate(PORTFOLIO, 1)
        }
        
        for future in as_completed(futures):
            asset_name, response = future.result()
            raw_responses.append(response)
            
            if response["success"]:
                asset = analyzer.parse_response(response["data"], asset_name)
                assets.append(asset)
            else:
                failed_count += 1
    
    duration = time.time() - start_time
    
    # Analyze portfolio
    logger.info("\n" + "="*60)
    logger.info("Portfolio Analysis Complete")
    logger.info("="*60)
    
    portfolio = analyzer.analyze_portfolio(assets, len(PORTFOLIO), failed_count)
    
    logger.info(f"Success: {portfolio.successful}/{portfolio.total}")
    logger.info(f"Average Risk: {portfolio.avg_risk:.2f}/5.0")
    logger.info(f"Total Annual Loss: £{portfolio.total_loss:,.2f}")
    logger.info(f"Execution Time: {duration:.2f}s ({duration/len(PORTFOLIO):.2f}s avg)")
    
    # Generate report
    logger.info("\nGenerating executive report...")
    report = reporter.generate(portfolio)
    
    # Save outputs
    with open(config.REPORT_FILE, "w") as f:
        f.write(report)
    logger.info(f"  Report saved: {config.REPORT_FILE}")
    
    with open(config.RAW_DATA_FILE, "w") as f:
        json.dump(raw_responses, f, indent=2)
    logger.info(f"  Raw data saved: {config.RAW_DATA_FILE}")
    
    logger.info("\n✓ Analysis complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\nAnalysis interrupted by user")
    except Exception as e:
        logger.error(f"\nFatal error: {e}", exc_info=True)
