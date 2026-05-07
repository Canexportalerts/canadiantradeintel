# CTI Accuracy Review Schedule

## What this covers
Every specific claim on canadiantradeintel.ca — every dollar 
figure, percentage, index score, bilateral trade value, programme 
funding amount, leadership name, or date-specific fact — is 
subject to scheduled review. This document defines when and how.

## Review tiers

### Weekly (pipeline automated)
- Market scoring in weekly sector reports
- Commodity prices and FX rates
- Procurement tender data
- Sanctions list updates (OFAC, GACC, UN)
- Spotlight stories

### Quarterly (manual + audit script)
Run: python3 accuracy_audit.py --page-type country_dossier --limit 50
Covers:
- All 45+ country dossiers — bilateral trade figures, 
  GDP data, leadership references, bilateral status
- Dashboard static content — all context rows in sector tabs
- Canada Forward analysis pieces — policy claims, fund amounts
- CUSMA tracker — negotiation status, tariff rates

Next quarterly audit due: August 2026

### Semi-annual (full site)
Run: python3 accuracy_audit.py --page-type all --limit 200
Covers all 139 pages on the site.
Includes enrichment pass to update country dossiers with:
- World Bank GDP, B-READY scores
- UN Human Development Index
- StatCan bilateral trade figures
- EDC country risk ratings
- IMF economic outlook data

Next full audit due: November 2026

## Source standards
1. Primary government sources are authoritative
2. Major established news organizations for recent events
3. International organizations (World Bank, IMF, OECD, UN) 
   for standardized international data
4. Wikipedia is acceptable as a starting point — always 
   follow to the primary source Wikipedia cites
5. Single-source claims are flagged but not blocked; 
   two independent sources is the target standard

## Claim types that require immediate re-verification
- Any named political leader or CEO
- Any programme funding amount (budgets change)
- Any bilateral trade figure older than 18 months
- Any tariff rate (active US tariff environment)
- Any index score older than 12 months

## Error correction protocol
- Inaccurate claims: corrected within 48 hours of detection
- Outdated claims: updated at next scheduled quarterly review
- Unverifiable claims: flagged with "approximate" or 
  "as of [year]" qualifier added inline

## Contact
Found a factual error? Email hello@canadiantradeintel.ca
We correct verified errors within 48 hours.
