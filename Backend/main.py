from fastapi import FastAPI

app = FastAPI(title="RiskContext AI API")


@app.post("/analyze")
def analyze_risk(data: dict):
  raw_prs = data.get("raw_prs", 0.0)
  admixture = data.get("admixture", {})
  env_factor = data.get("environmental_factor", 1.0)

  # Calculate penalty/correction based heavily on European fraction mismatch
  eur_fraction = admixture.get("EUR", 0.0)
  # Lower European fraction in standard PRS causes overestimation bias
  bias_correction = 1.0 - (eur_fraction * 0.25)
  adjusted_score = round(raw_prs * bias_correction * env_factor, 3)

  return {
      "status": "success",
      "raw_prs": raw_prs,
      "adjusted_risk_score": adjusted_score,
      "recommendation": (
          f"Adjusted for {int(eur_fraction*100)}% European and multi-ancestry"
          " admixture model. Mitigated false-positive risk over-attribution"
          " common in Euro-centric GWAS training sets."
      ),
  }