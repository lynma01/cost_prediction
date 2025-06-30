# Pricing Analysis for Common Dental Codes

Analyzes the Common Dental Terminology codes (CDTs) and their prices from a variety of health insurance providers to determine which procedures would utilize UCleaner LLC's products.

## Dental Insurance Providers

- [Aetna Dental](https://health1.aetna.com/app/public/#/one/insurerCode=AETNACVS_I&brandCode=ALICFI/machine-readable-transparency-in-coverage)
- [Cigna](https://www.cigna.com/legal/compliance/machine-readable-files)
- [Delta Dental Oregon](https://deltadentalor.org/idaho/privacy-center/machine-readable-files)
- [Kaiser Permanente](https://healthy.kaiserpermanente.org/maryland-virginia-washington-dc/front-door/machine-readable)
  - Liberty Dental

## Methods

1. The [script](main.py) ingests the [legally required, machine readable, cost transparency files](https://www.cms.gov/CCIIO/Resources/Regulations-and-Guidance/Downloads/CMS-Transparency-in-Coverage-9915F.pdf) from the insurer's website into a duckdb database for local analytics.

2. The script then establishes database functions for sending rows of ingested data to Large Language Models (LLMs) for determining whether each CDT procedure would utilize UCleaner LLC's product(s).

3. 
