# Matrix Finance — Premium multipage Streamlit website

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Pages
Home, Gold Loan, Silver Loan, Personal Loan, Home Loan, Mortgage Loan, Contact, FAQs. Language selector English / Telugu.

## Configure WhatsApp recipients
Set environment variables for the corresponding loan teams (digits only, country code 91):

```
MATRIX_GOLD_WHATSAPP_NUMBER=919XXXXXXXXX
MATRIX_SILVER_WHATSAPP_NUMBER=919XXXXXXXXX
MATRIX_PERSONAL_WHATSAPP_NUMBER=919XXXXXXXXX
MATRIX_HOUSING_WHATSAPP_NUMBER=919XXXXXXXXX
MATRIX_MORTGAGE_WHATSAPP_NUMBER=919XXXXXXXXX
```

Optional fallback `MATRIX_WHATSAPP_NUMBER`, public phone `MATRIX_PUBLIC_PHONE`, address `MATRIX_BRANCH_ADDRESS`.

On valid form submission with consent, the application creates a prefilled WhatsApp link. The customer must press **Send**. It does not send automatically or store leads.

## Important before production
- Replace screenshot-derived decorative crops with properly licensed original brand assets; the supplied image was used as design inspiration.
- Configure a privacy policy, actual contacts, product terms, accurate eligibility rules and legally required disclosures.
- Use a secure backend and verified WhatsApp Business API if you need guaranteed direct enquiry delivery and lead records.
- All rates are illustrative and not live. The calculator does not guarantee approval.
- Test layouts on mobile and across browsers; CSS is tailored to Streamlit and may need adjustments with Streamlit upgrades.
