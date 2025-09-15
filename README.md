# Budget Optimization Analysis

## Overview
Comprehensive budget optimization analysis for digital advertising campaigns comparing TikTok vs Meta performance across 3 clients.

## Dataset
- **Time Period:** 12 months of weekly campaign data
- **Platforms:** Meta and TikTok
- **Clients:** 3 different advertisers
- **Metrics:** Spend, Revenue, Impressions, Clicks, Conversions

## Analysis Framework

### 5-Step Analysis Process:
1. **Performance Metrics Calculation**
   - CTR (Click-Through Rate)
   - CVR (Conversion Rate)
   - CPC (Cost Per Click)
   - CPA (Cost Per Acquisition)
   - ROAS (Return on Ad Spend)

2. **Platform Comparison**
   - Client-level performance analysis
   - Meta vs TikTok comparison
   - Budget allocation assessment

3. **Return Curves Analysis**
   - Diminishing returns identification
   - Marginal ROAS analysis
   - Saturation point detection

4. **Supporting Analysis**
   - Funnel analysis (CTR vs CVR)
   - Creative performance breakdown
   - Cross-platform insights

5. **Recommendations**
   - Budget reallocation guidance
   - Creative testing strategies
   - Performance optimization opportunities

## Key Findings

### Platform Performance
- **Meta ROAS:** 5.3-5.7x (all clients)
- **TikTok ROAS:** 5.0-5.6x (all clients)
- **Performance Gap:** ±6.6% range (minimal difference)

### Budget Allocation
- **Current Split:** ~50/50 Meta/TikTok
- **Recommendation:** Maintain current allocation
- **Rationale:** Both platforms deliver strong, comparable performance

### Risk Assessment
- **Both platforms:** Above target ROAS (1.5x)
- **Performance consistency:** High across all clients
- **Risk-adjusted returns:** Similar risk profiles

## Files Structure

```
├── budget_optimization_analysis.ipynb    # Main analysis notebook
├── bi_case_study_campaigns_12m.csv      # Original dataset
├── enhanced_campaign_data_for_looker_fixed.csv  # Looker Studio export
├── BI - Test Case.pdf                   # Original case study
└── README.md                           # This file
```

## Looker Studio Integration

### Dataset: `enhanced_campaign_data_for_looker_fixed.csv`

**Important:** Create calculated fields in Looker Studio instead of using pre-calculated metrics:

```sql
-- ROAS (correct aggregation)
ROAS = SUM(revenue) / SUM(spend)

-- Other KPIs
CTR = SUM(clicks) / SUM(impressions)
CVR = SUM(conversions) / SUM(clicks)
CPC = SUM(spend) / SUM(clicks)
CPA = SUM(spend) / SUM(conversions)
```

### ROAS Formatting Options:
1. **Custom Format:** `#,##0.00"x"` → displays as "11.80x"
2. **Percentage Format:** → displays as "1180%"

## Technical Notes

- **Environment:** Jupyter Notebook with Python
- **Libraries:** pandas, numpy, matplotlib, seaborn
- **Analysis Method:** Statistical comparison with marginal ROAS calculation
- **Visualization:** 20+ charts covering performance, trends, and optimization

## Recommendations Summary

1. **Budget Strategy:** Maintain 50/50 allocation - no major reallocation needed
2. **Optimization Focus:** Within-platform optimization over between-platform shifts  
3. **Creative Testing:** Cross-platform concept testing opportunities identified
4. **Monitoring:** Weekly performance tracking for dynamic adjustments
5. **Target ROAS:** Continue using 1.5x minimum threshold

---

*Analysis completed using comprehensive 5-step framework for budget optimization decision-making.*