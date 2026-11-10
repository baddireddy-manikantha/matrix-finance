# Matrix Finance — Multi-page Streamlit Website

A customer-facing bilingual (English/Telugu) Streamlit site with **separate URL pages** for Home, Gold Loan, Silver Loan, Personal Loan, Home Loan, Mortgage Loan and Contact. No admin dashboard or database.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501. Navigation uses separate Streamlit pages, e.g. `/gold`, `/silver`, `/personal`, `/housing`, `/mortgage`, `/contact`.

## Configure WhatsApp and business details

Set environment variables before launching:

- `MATRIX_WHATSAPP_NUMBER` — Indian WhatsApp business number, e.g. `919876543210` (example only).
- `MATRIX_PUBLIC_PHONE` — public phone displayed on Contact page.
- `MATRIX_BRANCH_ADDRESS` — public branch address.

For Render: create a **Web Service**, connect your private GitHub repository, build command `pip install -r requirements.txt`, start command `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`. Configure environment variables in Render. A GoDaddy domain can point to Render using its DNS records.

## Important

- The figures are illustrative only. Gold and silver rates are manually entered assumptions, **not live market data**. LTV settings are demonstrative and must be reviewed against applicable laws and lender policy before public launch.
- Personal data is not stored in this prototype. An enquiry opens WhatsApp with a prefilled message **only after user consent**; the user must press Send in WhatsApp.
- Do not launch as a real lending site without reviewing regulatory requirements, disclosures, privacy policy, accessibility, input validation and security.
- The navigation is multi-page, not a single-page loan tab layout. Streamlit's UI is responsive, though exact Figma pixel-perfect fidelity requires a custom frontend.

Per-loan routing: MATRIX_GOLD_WHATSAPP_NUMBER, MATRIX_SILVER_WHATSAPP_NUMBER, MATRIX_PERSONAL_WHATSAPP_NUMBER, MATRIX_HOUSING_WHATSAPP_NUMBER, MATRIX_MORTGAGE_WHATSAPP_NUMBER. Fallback: MATRIX_WHATSAPP_NUMBER. Enter Indian WhatsApp numbers with country code, e.g. 919876543210. The visitor must press Send in WhatsApp.
