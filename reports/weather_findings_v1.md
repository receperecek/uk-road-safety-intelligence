# Weather Findings v1

## Key Insights
- Fine weather with no high winds accounted for the largest collision volume, with 400,956 collisions, representing 79.64% of decoded weather-condition records.
- Raining with no high winds was the second-largest weather segment by volume, with 57,187 collisions.
- Higher-severity outcomes appear more concentrated in lower-volume adverse weather contexts such as fog or mist, fine weather with high winds, and raining with high winds.
- This indicates that the most common weather condition is not necessarily the most severe one from a collision-outcome perspective.

## Analyst Interpretation
Weather should be interpreted through both exposure and severity. Fine weather dominates total collision volume, likely reflecting overall traffic exposure. However, adverse weather segments such as fog or mist and high-wind conditions show stronger severity signals despite much lower frequency. This means weather-driven risk prioritization should separate common exposure environments from rarer but more severe operating conditions.

## Business Relevance
This finding supports a more nuanced road safety strategy:
- common weather conditions drive operational collision volume
- adverse weather conditions may drive disproportionate severity risk
- weather context is a strong candidate feature for downstream severity scoring and intervention prioritization

## Scope Note
The 'Unknown' category should not be prioritized in policy-facing interpretation.
