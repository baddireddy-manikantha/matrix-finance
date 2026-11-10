import os, re, base64, html, json
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from pathlib import Path
from urllib.parse import quote
import streamlit as st

st.set_page_config(page_title='Matrix Finance | Loans', page_icon='💠', layout='wide', initial_sidebar_state='collapsed')
NAVY='#08274e'; GOLD='#d9a531'
PAGES=['home','gold','silver','personal','housing','mortgage','contact','faq']
WORDS={
'en':{
'home':'Home','gold':'Gold Loan','silver':'Silver Loan','personal':'Personal Loan','housing':'Home Loan','mortgage':'Mortgage Loan','contact':'Contact Us','faq':'FAQs','language':'Language / భాష','tagline':'Your Trusted Financial Partner','apply':'Apply Now','calculate':'Calculate Estimate','your_details':'Your Details','full_name':'Full Name','phone':'Phone Number','email':'Email (optional)','city':'City','state':'State','weight':'Weight (grams)','purity':'Purity','rate':'Assumed pure metal rate per gram (₹)','ltv':'Illustrative loan-to-value (%)','requested':'Requested loan amount (₹)','annual':'Illustrative annual interest rate (%)','tenure':'Tenure (months)','property':'Estimated property value (₹)','estimate':'Indicative Loan Estimate','collateral':'Indicative Collateral Value','emi':'Estimated monthly EMI','interest':'Estimated total interest','consent':'I consent to share my details with Matrix Finance through WhatsApp for a loan enquiry.','open_whatsapp':'Open WhatsApp Enquiry','missing':'Set MATRIX_WHATSAPP_NUMBER to the business WhatsApp number to enable enquiries.','validation':'Enter your full name, a valid 10-digit Indian mobile number, and your city.','note':'Illustrative estimate only. Rates are editable assumptions, not live quotes. Final valuation, eligibility, approval and terms depend on verification and applicable rules.','intro':'Simple financial solutions, designed around your needs.','explore':'Explore Our Loan Products','start':'Find a loan that fits your plans','apply_heading':'Enquire About This Loan','calc_heading':'Loan Estimator','submitted':'Review the prefilled message in WhatsApp and press Send to submit your enquiry.','no_data':'Calculate an estimate above, then complete your enquiry.','how':'How it works','step1':'Choose your loan','step2':'Calculate an estimate','step3':'Send your enquiry','home_desc':'Gold, silver, personal, home and property-backed loans — all in one place.','contact_desc':'Talk to our team about the right loan for you.','contact_phone':'Business phone','contact_address':'Branch address','home_cta':'Explore loans','gold_desc':'Explore an indicative loan against eligible gold jewellery.','silver_desc':'Estimate borrowing against eligible silver collateral.','personal_desc':'Plan a personal loan with a simple monthly EMI estimate.','housing_desc':'Explore monthly payments for your dream home.','mortgage_desc':'Estimate a property-backed loan based on property value.','loan_info':'Loan Details','disclaimer':'We do not guarantee loan approval. Please confirm terms with Matrix Finance.'},
 'te':{
'home':'హోమ్','gold':'బంగారు రుణం','silver':'వెండి రుణం','personal':'వ్యక్తిగత రుణం','housing':'గృహ రుణం','mortgage':'తనఖా రుణం','contact':'సంప్రదించండి','faq':'తరచుగా అడిగే ప్రశ్నలు','language':'భాష / Language','tagline':'మీ విశ్వసనీయ ఆర్థిక భాగస్వామి','apply':'ఇప్పుడే దరఖాస్తు చేయండి','calculate':'అంచనా లెక్కించండి','your_details':'మీ వివరాలు','full_name':'పూర్తి పేరు','phone':'ఫోన్ నంబర్','email':'ఇమెయిల్ (ఐచ్ఛికం)','city':'నగరం','state':'రాష్ట్రం','weight':'బరువు (గ్రాములు)','purity':'స్వచ్ఛత','rate':'స్వచ్ఛమైన లోహం గ్రాము ఊహించిన ధర (₹)','ltv':'ఉదాహరణ రుణ విలువ నిష్పత్తి (%)','requested':'కావలసిన రుణ మొత్తం (₹)','annual':'ఉదాహరణ వార్షిక వడ్డీ రేటు (%)','tenure':'కాలవ్యవధి (నెలలు)','property':'ఆస్తి అంచనా విలువ (₹)','estimate':'రుణ మొత్తం అంచనా','collateral':'తాకట్టు అంచనా విలువ','emi':'నెలవారీ EMI అంచనా','interest':'మొత్తం వడ్డీ అంచనా','consent':'రుణ విచారణ కోసం నా వివరాలను వాట్సాప్ ద్వారా మ్యాట్రిక్స్ ఫైనాన్స్‌తో పంచుకోవడానికి అంగీకరిస్తున్నాను.','open_whatsapp':'వాట్సాప్ విచారణ తెరవండి','missing':'విచారణలను ప్రారంభించడానికి MATRIX_WHATSAPP_NUMBER లో వ్యాపార వాట్సాప్ నంబర్‌ను సెట్ చేయండి.','validation':'పూర్తి పేరు, సరైన 10 అంకెల భారతీయ మొబైల్ నంబర్ మరియు నగరం నమోదు చేయండి.','note':'ఇది కేవలం ఉదాహరణ అంచనా. ధరలు ప్రత్యక్ష మార్కెట్ ధరలు కావు. తుది విలువ, అర్హత, ఆమోదం మరియు షరతులు ధృవీకరణ, వర్తించే నియమాలపై ఆధారపడతాయి.','intro':'మీ అవసరాలకు అనుగుణంగా సులభమైన ఆర్థిక పరిష్కారాలు.','explore':'మా రుణ ఎంపికలు','start':'మీ ప్రణాళికలకు తగిన రుణాన్ని ఎంచుకోండి','apply_heading':'ఈ రుణం గురించి విచారించండి','calc_heading':'రుణ అంచనా కాలిక్యులేటర్','submitted':'వాట్సాప్‌లో ముందుగా నింపిన సందేశాన్ని చూసి, విచారణ పంపడానికి Send నొక్కండి.','no_data':'పైన అంచనా లెక్కించి, తరువాత విచారణ వివరాలు పూర్తి చేయండి.','how':'ఇది ఎలా పనిచేస్తుంది','step1':'రుణాన్ని ఎంచుకోండి','step2':'అంచనా లెక్కించండి','step3':'విచారణ పంపండి','home_desc':'బంగారు, వెండి, వ్యక్తిగత, గృహ మరియు ఆస్తి తనఖా రుణాలు — అన్నీ ఒకేచోట.','contact_desc':'మీకు సరిపోయే రుణం గురించి మా బృందాన్ని సంప్రదించండి.','contact_phone':'వ్యాపార ఫోన్','contact_address':'శాఖ చిరునామా','home_cta':'రుణాలను చూడండి','gold_desc':'అర్హత గల బంగారు ఆభరణాలపై రుణ అంచనా తెలుసుకోండి.','silver_desc':'అర్హత గల వెండి తాకట్టుపై రుణ అంచనా తెలుసుకోండి.','personal_desc':'సులభమైన నెలవారీ EMI అంచనాతో వ్యక్తిగత రుణాన్ని ప్లాన్ చేసుకోండి.','housing_desc':'మీ సొంత ఇంటి కోసం నెలవారీ EMI అంచనా చూడండి.','mortgage_desc':'ఆస్తి విలువ ఆధారంగా తనఖా రుణ అంచనా తెలుసుకోండి.','loan_info':'రుణ వివరాలు','disclaimer':'రుణ ఆమోదానికి హామీ లేదు. షరతులను మ్యాట్రిక్స్ ఫైనాన్స్‌తో నిర్ధారించుకోండి.'}}

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Telugu:wght@400;500;600;700&display=swap');
html,body,[class*="css"],.stApp{font-family:Inter,'Noto Sans Telugu',sans-serif!important}.stApp{background:#f7f9fc;color:#102d52}.block-container{max-width:1450px;padding-top:1rem;padding-bottom:4rem}header[data-testid="stHeader"]{background:transparent}
.brand{display:flex;gap:12px;align-items:center}.mark{font-size:40px;font-weight:900;background:linear-gradient(140deg,#fbe3a0,#b8790b);color:transparent;background-clip:text}.brandname{font-size:22px;font-weight:800;color:#08274e}.tagline{font-size:12px;color:#5b6c80}
.hero{padding:48px 42px;border-radius:22px;color:white;margin:22px 0 28px;min-height:200px;background:linear-gradient(110deg,#061d3b,#164b7c)}.hero h1{font-size:clamp(32px,4.2vw,53px);line-height:1.2;margin:0 0 12px;color:#f0c66c}.hero p{font-size:17px;max-width:700px;color:#e7edf6}.goldhero{background:linear-gradient(110deg,#071e3d,#164573 72%,#9a6b24)}.silverhero{background:linear-gradient(110deg,#112d48,#456782 72%,#8294a9)}.personalhero{background:linear-gradient(110deg,#08274e,#236c90)}.housinghero{background:linear-gradient(110deg,#08274e,#245a76 75%,#397b68)}.mortgagehero{background:linear-gradient(110deg,#08274e,#37446f 75%,#655c85)}
.tile{background:white;border:1px solid #e2e9f2;border-radius:17px;padding:24px;min-height:175px;box-shadow:0 7px 25px #08274e0a}.tile h3{font-size:20px;color:#08274e;margin:7px 0}.tile p{color:#64748b;font-size:14px}.tile .emoji{font-size:32px}.section{font-size:23px;font-weight:800;color:#08274e;margin:20px 0 14px}.result{border:1px solid #e8c476;border-radius:18px;padding:25px;background:linear-gradient(135deg,#fff8e8,#fff);margin:12px 0}.result h2{font-size:40px;color:#08274e;margin:6px 0}.result small{color:#64748b}.footer{margin-top:40px;padding:24px;border-radius:15px;background:#08274e;color:#e4eaf2;font-size:13px}
[data-testid="stForm"]{border:1px solid #e3e9f2;background:white;border-radius:18px;padding:18px;box-shadow:0 8px 28px #102d5210}
.stButton button[kind="primary"],div[data-testid="stFormSubmitButton"] button{background:linear-gradient(110deg,#08274e,#15538a);border:none;border-radius:11px;color:white;font-weight:700;min-height:47px}.stButton button[kind="secondary"]{background:#fff;border:1px solid #c79630;color:#08274e;border-radius:11px;min-height:45px;font-weight:700}
a[data-testid="stPageLink-NavLink"]{border-radius:10px;padding:7px 10px!important;font-weight:600}a[data-testid="stPageLink-NavLink"]:hover{background:#fff5dd}
@media(max-width:750px){.block-container{padding:1rem}.hero{padding:30px 22px;min-height:165px}.hero h1{font-size:30px}.hero p{font-size:14px}.brandname{font-size:18px}.mark{font-size:32px}.tile{min-height:135px;padding:16px}}
.float-hero{position:relative;overflow:hidden;min-height:270px;background:radial-gradient(circle at 75% 40%,#2c5b87,#08274e 65%);border-radius:22px;padding:45px 40px;margin:22px 0;color:white}.float-hero h1{font-size:clamp(30px,4vw,48px);max-width:580px;line-height:1.15;color:#f4c660}.float-hero p{max-width:500px;color:#e9eef6}.float-item{position:absolute;filter:drop-shadow(0 10px 12px #0006);animation:floaty 4s ease-in-out infinite}.float-item.one{right:20%;top:8%;font-size:90px}.float-item.two{right:4%;top:32%;font-size:90px;animation-delay:-1.3s}.float-item.three{right:33%;bottom:3%;font-size:70px;animation-delay:-2s}@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}@media(max-width:750px){.float-hero{padding:26px 20px 130px;min-height:340px}.float-item.one{right:55%;top:auto;bottom:5%;font-size:55px}.float-item.two{right:8%;top:auto;bottom:5%;font-size:65px}.float-item.three{right:35%;font-size:48px}}
.premium-hero{background:linear-gradient(115deg,#061c3a,#0b3262 60%,#1b4a77);border-radius:20px;min-height:315px;margin:22px 0 10px;padding:38px 36px;display:flex;align-items:center;position:relative;overflow:hidden;box-shadow:0 15px 45px #071e3b24}.premium-copy{width:53%;position:relative;z-index:2}.premium-copy h1{font-size:clamp(29px,3.6vw,52px);color:#fff;line-height:1.16;margin:12px 0}.premium-copy p{color:#e7eef8;font-size:14px}.eyebrow{color:#ffd46e;font-size:12px;font-weight:800;letter-spacing:2px}.hero-pill{display:inline-block;border:1px solid #f2c96e75;background:#ffffff13;border-radius:24px;color:#f9e2aa;padding:10px 14px;font-size:12px;margin-top:16px}.hero-visual{width:47%;position:relative;z-index:1;animation:heroFloat 5s ease-in-out infinite}.hero-visual img{width:100%;border-radius:22px;mix-blend-mode:screen;filter:drop-shadow(0 18px 25px #0006)}@keyframes heroFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}.benefits{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:20px 12px;background:#fff;border:1px solid #e5ebf2;border-radius:15px;margin:22px 0}.benefits span{color:#0a2a50;font-size:13px;font-weight:700}.centered{text-align:center}.product-card{background:white;border:1px solid #dce5ef;border-radius:17px;padding:12px;min-height:230px;text-align:center;box-shadow:0 5px 15px #061d3b0b}.product-card img{width:100%;height:110px;object-fit:contain;border-radius:12px}.product-card h3{color:#08274e;font-size:17px;margin:7px 0}.product-card p{color:#63748a;font-size:12px;min-height:44px}.value-card{border:1px solid #e3eaf3;border-radius:17px;background:white;padding:22px;min-height:165px}.value-card span{font-size:27px}.value-card h3{color:#08274e;margin:10px 0 6px;font-size:17px}.value-card p{color:#66758b;font-size:13px}.steps{display:flex;gap:12px;flex-wrap:wrap}.steps>div{flex:1;min-width:145px;border-radius:14px;background:#fff8e9;border:1px solid #efdcb0;padding:17px}.steps b{font-size:25px;color:#c18c19}.steps p{font-weight:600;color:#12335c;font-size:13px}.stPageLink a{border:1px solid #d3a44c!important;border-radius:10px!important;background:#fffaf0!important}.stPageLink a:hover{background:#ffe7a9!important}@media(max-width:850px){.premium-hero{display:block;padding:25px 22px}.premium-copy{width:100%}.hero-visual{width:100%;max-width:460px;margin:auto}.product-card{min-height:190px}.product-card img{height:80px}.premium-copy h1{font-size:32px}}@media(prefers-reduced-motion:reduce){.hero-visual,.float-item{animation:none!important}}
</style>''',unsafe_allow_html=True)

if 'lang' not in st.session_state:st.session_state.lang='en'
def t(key):return WORDS[st.session_state.lang][key]
def currency(n):return '₹'+format(round(n),',')
def top():
    a,b=st.columns([4,1.3],vertical_alignment='center')
    with a:st.markdown(f'<div class="brand"><div class="mark">M</div><div><div class="brandname">MATRIX FINANCE</div><div class="tagline">{t("tagline")}</div></div></div>',unsafe_allow_html=True)
    with b:st.selectbox('Language / భాష',['en','te'],format_func=lambda x:'English' if x=='en' else 'తెలుగు',key='lang',label_visibility='collapsed')
    with st.container(horizontal=True,horizontal_alignment='left'):
        for name in PAGES:st.page_link(PAGE_OBJECTS[name],label=t(name),icon={'home':'🏠','gold':'🥇','silver':'🪙','personal':'👤','housing':'🏡','mortgage':'🏢','contact':'☎️','faq':'❓'}[name])

def hero(title,desc,theme=''):
    st.markdown(f'<div class="hero {theme}"><h1>{title}</h1><p>{desc}</p></div>',unsafe_allow_html=True)

def foot():st.markdown(f'<div class="footer">© Matrix Finance · {t("tagline")}<br>{t("disclaimer")}</div>',unsafe_allow_html=True)

def asset_b64(name):
    root = Path(__file__).resolve().parent
    for path in (root / name, root / 'assets' / name):
        if path.is_file():
            return base64.b64encode(path.read_bytes()).decode('ascii')
    return None

PRODUCTS=[('gold','Gold Loan','బంగారు రుణం','Borrow against eligible gold jewellery.','అర్హత గల బంగారు ఆభరణాలపై రుణం.'),('silver','Silver Loan','వెండి రుణం','Explore loans against eligible silver.','అర్హత గల వెండిపై రుణం.'),('personal','Personal Loan','వ్యక్తిగత రుణం','Plan your needs with flexible EMIs.','సులభమైన EMIలతో మీ అవసరాలను తీర్చుకోండి.'),('housing','Home Loan','గృహ రుణం','Plan financing for your dream home.','మీ కలల ఇంటికి ఆర్థిక ప్రణాళిక.'),('mortgage','Mortgage Loan','తనఖా రుణం','Explore financing against property.','ఆస్తి ఆధారంగా రుణ అవకాశాలు.')]
FAQS=[
('What documents are generally needed for a loan?','Requirements depend on the loan product and lender. You may be asked for identity, address, income and collateral or property documents. Matrix Finance will confirm the exact list.', 'రుణం కోసం సాధారణంగా ఏ పత్రాలు అవసరం?', 'రుణ రకం మరియు రుణదాత ఆధారంగా పత్రాలు మారుతాయి. గుర్తింపు, చిరునామా, ఆదాయం, తాకట్టు లేదా ఆస్తి పత్రాలు అవసరం కావచ్చు. ఖచ్చితమైన జాబితాను మ్యాట్రిక్స్ ఫైనాన్స్ తెలియజేస్తుంది.'),
('How is gold loan eligibility estimated?','The indicative value uses entered weight, purity, an assumed metal rate and a loan-to-value percentage. The actual offer requires physical valuation and policy checks.','బంగారు రుణ అర్హతను ఎలా అంచనా వేస్తారు?','బరువు, స్వచ్ఛత, ఊహించిన లోహ ధర మరియు రుణ-విలువ నిష్పత్తి ఆధారంగా అంచనా వేస్తారు. తుది రుణానికి ప్రత్యక్ష మూల్యాంకనం అవసరం.'),
('Will applying guarantee approval?','No. Submitting an enquiry does not guarantee approval, a particular rate, or disbursement.','దరఖాస్తు చేస్తే రుణం ఖచ్చితంగా వస్తుందా?','లేదు. విచారణ పంపడం వల్ల రుణ ఆమోదం, నిర్దిష్ట వడ్డీ రేటు లేదా రుణ పంపిణీకి హామీ ఉండదు.'),
('Can I apply using WhatsApp?','Yes. After you validate your details and consent, you can open a prepared WhatsApp message to the relevant loan team. You must press Send yourself.','వాట్సాప్ ద్వారా దరఖాస్తు చేయవచ్చా?','అవును. వివరాలు ధృవీకరించి అంగీకరించిన తర్వాత సంబంధిత బృందానికి వాట్సాప్ సందేశాన్ని తెరవవచ్చు. మీరు స్వయంగా Send నొక్కాలి.'),
('Are the calculator rates live?','No. Calculator rates are editable illustrative inputs, not live market rates or binding loan offers.','కాలిక్యులేటర్ ధరలు ప్రత్యక్ష మార్కెట్ ధరలా?','కాదు. కాలిక్యులేటర్‌లోని ధరలు ఉదాహరణ కోసం మాత్రమే; ప్రత్యక్ష ధరలు లేదా ఖచ్చితమైన రుణ ఆఫర్లు కావు.'),
('How will my enquiry be used?','Your details are used to respond to your requested loan enquiry, subject to the published privacy notice and your consent. Avoid sending sensitive KYC documents through an unverified contact.','నా విచారణ వివరాలను ఎలా ఉపయోగిస్తారు?','మీ రుణ విచారణకు స్పందించేందుకు వివరాలను ఉపయోగిస్తారు. గోప్యతా ప్రకటన మరియు మీ సమ్మతి వర్తిస్తాయి. ధృవీకరించని సంప్రదింపులకు సున్నితమైన పత్రాలు పంపవద్దు.')]

def faq_section():
    te=st.session_state.lang=='te'
    st.markdown(f'<div class="section">{"తరచుగా అడిగే ప్రశ్నలు" if te else "Frequently Asked Questions"}</div>',unsafe_allow_html=True)
    for q,a,tq,ta in FAQS:
        with st.expander(tq if te else q):st.write(ta if te else a)

def home():
    top()
    te=st.session_state.lang=='te'
    heading='మీ ఆర్థిక అవసరాలకు సులభమైన రుణాలు' if te else 'Quick & Flexible Loans<br><span style="color:#f8c34e">for Your Financial Needs</span>'
    sub='బంగారు రుణం | వెండి రుణం | వ్యక్తిగత రుణం | గృహ రుణం | తనఖా రుణం' if te else 'Gold Loan | Silver Loan | Personal Loan | Home Loan | Mortgage Loan'
    heroimg=asset_b64('hero.png')
    hero_visual = (f'<div class="hero-visual"><img src="data:image/png;base64,{heroimg}" alt="Loan product illustrations"></div>' if heroimg else '')
    st.markdown(f'''<div class="premium-hero"><div class="premium-copy"><div class="eyebrow">✦ MATRIX FINANCE</div><h1>{heading}</h1><p>{sub}</p><div class="hero-pill">✦ {'మీ అవసరాలకు సరిపోయే రుణ ఎంపికలను తెలుసుకోండి' if te else 'Explore options designed around your needs'}</div></div>{hero_visual}</div>''',unsafe_allow_html=True)
    a,b=st.columns([1,1])
    with a:st.page_link(PAGE_OBJECTS['gold'],label='🧮 '+('అర్హత అంచనా చూడండి' if te else 'Check Eligibility'),use_container_width=True)
    with b:st.page_link(PAGE_OBJECTS['contact'],label='✉️ '+('ఇప్పుడే విచారించండి' if te else 'Enquire Now'),use_container_width=True)
    st.markdown('<div class="benefits"><span>🛡️ '+('గోప్యతకు ప్రాధాన్యం' if te else 'Privacy-first Enquiries')+'</span><span>⚡ '+('సులభమైన ప్రక్రియ' if te else 'Simple Application')+'</span><span>📊 '+('స్పష్టమైన అంచనాలు' if te else 'Transparent Estimates')+'</span><span>🎧 '+('బృంద సహాయం' if te else 'Team Assistance')+'</span></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section centered">{"మా రుణ ఉత్పత్తులు" if te else "Our Loan Products"}</div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for col,(key,en,tl,desc,tdesc) in zip(cols,PRODUCTS):
        with col:
            img=asset_b64(key+'.png')
            product_img = (f'<img src="data:image/png;base64,{img}" alt="{en}">' if img else '')
            st.markdown(f'<div class="product-card">{product_img}<h3>{tl if te else en}</h3><p>{tdesc if te else desc}</p></div>',unsafe_allow_html=True)
            st.page_link(PAGE_OBJECTS[key],label=('వివరాలు చూడండి →' if te else 'Explore & Apply →'),use_container_width=True)
    st.markdown(f'<div class="section centered">{"మ్యాట్రిక్స్ ఫైనాన్స్ ఎందుకు?" if te else "Why Choose Matrix Finance?"}</div>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    for col,icon,en,tl,desc,tdesc in [(a,'🧮','Easy Calculators','సులభమైన కాలిక్యులేటర్లు','Explore indicative loan values and EMIs before enquiring.','విచారణకు ముందు రుణ అంచనా, EMI తెలుసుకోండి.'),(b,'📱','Mobile Friendly','మొబైల్‌కు అనుకూలం','Browse loan products and enquire from your phone.','మీ ఫోన్ నుంచే రుణాల వివరాలు చూడండి.'),(c,'🌐','English & Telugu','ఇంగ్లీష్ & తెలుగు','Understand product information in your preferred language.','మీకు నచ్చిన భాషలో రుణ వివరాలు తెలుసుకోండి.')]:
        with col:st.markdown(f'<div class="value-card"><span>{icon}</span><h3>{tl if te else en}</h3><p>{tdesc if te else desc}</p></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section centered">{"విచారణ ఎలా చేయాలి?" if te else "How It Works"}</div>',unsafe_allow_html=True)
    steps=[('01','రుణాన్ని ఎంచుకోండి' if te else 'Choose a Loan'),('02','అంచనా లెక్కించండి' if te else 'Calculate Estimate'),('03','వివరాలు & సమ్మతి ఇవ్వండి' if te else 'Enter Details & Consent'),('04','వాట్సాప్‌లో పంపండి' if te else 'Send via WhatsApp')]
    st.markdown('<div class="steps">'+''.join(f'<div><b>{n}</b><p>{label}</p></div>' for n,label in steps)+'</div>',unsafe_allow_html=True)
    faq_section()
    foot()

@st.cache_data(ttl=3600, show_spinner=False)
def get_gold_rates():
    """Fetch INR/gram purity-specific quotes; never silently invent a live rate."""
    url = 'https://api.goldprice.dev/v1/carat?currency=INR'
    request = Request(url, headers={'Accept': 'application/json', 'User-Agent': 'MatrixFinance/1.0'})
    with urlopen(request, timeout=10) as response:
        data = json.load(response)
    if not isinstance(data, dict):
        raise ValueError('Unexpected gold-rate response')
    # API quotes are already purity-adjusted: do not multiply by purity again.
    keys = {'22K (91.6%)': 'price_gram_22k', '18K (75%)': 'price_gram_18k', '24K (99.9%)': 'price_gram_24k'}
    rates = {}
    for label, field in keys.items():
        rate = float(data[field])
        if not 0 < rate < 1000000:
            raise ValueError('Invalid gold rate returned')
        rates[label] = rate
    return rates, data.get('timestamp'), datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

def calculator(kind):
    st.markdown(f'<div class="section">🧮 {t("calc_heading")}</div>',unsafe_allow_html=True)
    with st.form(f'calc_{kind}'):
        if kind in ('gold','silver'):
            rates = None
            updated_at = None
            fetched_at = None
            if kind == 'gold':
                try:
                    rates, updated_at, fetched_at = get_gold_rates()
                except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
                    pass
            c1,c2=st.columns(2)
            with c1:
                weight=st.number_input(t('weight'),min_value=0.1,max_value=100000.0,value=50.0,step=1.0)
                if kind=='gold':
                    opts={'22K (91.6%)':.916,'18K (75%)':.75,'24K (99.9%)':.999}
                else:
                    opts={'999 (99.9%)':.999,'925 (92.5%)':.925,'800 (80%)':.8}
                purity=st.selectbox(t('purity'),list(opts))
            with c2:
                if kind == 'gold' and rates:
                    rate = rates[purity]
                    st.metric('Gold rate (INR/gram)' if st.session_state.lang=='en' else 'బంగారం ధర (₹/గ్రాము)', f'₹{rate:,.2f}')
                    st.caption(('Source timestamp: ' + str(updated_at)) if updated_at else ('Retrieved: ' + fetched_at))
                    st.caption('Indicative market quote, not a lender valuation.' if st.session_state.lang=='en' else 'ఇది మార్కెట్ సూచన ధర మాత్రమే; రుణదాత తుది మూల్యాంకనం కాదు.')
                elif kind == 'gold':
                    st.warning('Live gold rates unavailable. Enter a reference rate manually; it is NOT a live quote.' if st.session_state.lang=='en' else 'ప్రస్తుత బంగారం ధర అందుబాటులో లేదు. సూచన ధరను మీరే నమోదు చేయండి; ఇది ప్రత్యక్ష ధర కాదు.')
                    rate=st.number_input('Manual 24K reference rate (₹/gram)' if st.session_state.lang=='en' else '24K సూచన ధర (₹/గ్రాము)',min_value=1.0,value=7100.0,step=10.0)
                else:
                    rate=st.number_input(t('rate'),min_value=1.0,value=90.0,step=10.0)
                ltv=st.slider(t('ltv'),min_value=10,max_value=80,value=75,step=5)
            # API quotes already include purity; manual gold and silver rates are pure-metal reference rates.
            collateral=weight*(rate if kind=='gold' and rates else opts[purity]*rate)
            amount=collateral*ltv/100
            extras={'weight':weight,'purity':purity,'rate':rate,'ltv':ltv,
                    'rate_source':'goldprice.dev' if kind=='gold' and rates else 'manual illustrative input',
                    'rate_timestamp':updated_at or fetched_at if kind=='gold' and rates else None}
        else:
            c1,c2=st.columns(2)
            with c1:
                if kind=='mortgage':
                    prop=st.number_input(t('property'),min_value=100000,value=5000000,step=100000)
                    ltv=st.slider(t('ltv'),10,70,50,5)
                    amount=prop*ltv/100
                else:amount=float(st.number_input(t('requested'),min_value=10000,max_value=100000000,value=500000,step=10000))
            with c2:
                annual=st.number_input(t('annual'),min_value=0.0,max_value=50.0,value=12.0,step=.5)
                months=st.number_input(t('tenure'),min_value=1,max_value=360,value=36 if kind=='personal' else 180,step=1)
            monthly=annual/1200
            emi=amount/months if monthly==0 else amount*monthly*(1+monthly)**months/((1+monthly)**months-1)
            interest=emi*months-amount
            extras={'annual_rate':annual,'months':months}
            if kind=='mortgage':extras.update({'property_value':prop,'ltv':ltv})
        submitted=st.form_submit_button('🧮 '+t('calculate'),use_container_width=True,type='primary')
    if submitted:st.session_state[f'estimate_{kind}']={'amount':amount,'collateral':collateral if kind in ('gold','silver') else None,'emi':emi if kind not in ('gold','silver') else None,'interest':interest if kind not in ('gold','silver') else None,'extras':extras}
    estimate=st.session_state.get(f'estimate_{kind}')
    if estimate:
        st.markdown(f'<div class="result"><strong>{t("estimate")}</strong><h2>{currency(estimate["amount"])}</h2><small>{t("note")}</small></div>',unsafe_allow_html=True)
        if kind in ('gold','silver'):st.metric(t('collateral'),currency(estimate['collateral']))
        else:
            a,b=st.columns(2);a.metric(t('emi'),currency(estimate['emi']));b.metric(t('interest'),currency(estimate['interest']))
    else:st.info(t('no_data'))
    return estimate

def setting(name, default=''):
    value = os.getenv(name)
    if value:
        return value
    try:
        return str(st.secrets.get(name, default))
    except (FileNotFoundError, KeyError, AttributeError):
        return default

def enquiry(kind,estimate):
    st.markdown(f'<div class="section">✉️ {t("apply_heading")}</div>',unsafe_allow_html=True)
    with st.form(f'enquiry_{kind}'):
        a,b=st.columns(2)
        with a:
            name=st.text_input(t('full_name'),key=f'name_{kind}')
            phone=st.text_input(t('phone'),key=f'phone_{kind}',placeholder='10-digit mobile number')
            city=st.text_input(t('city'),key=f'city_{kind}')
        with b:
            email=st.text_input(t('email'),key=f'email_{kind}')
            state=st.selectbox(t('state'),['Telangana','Andhra Pradesh','Karnataka','Tamil Nadu','Maharashtra','Other'],key=f'state_{kind}')
        consent=st.checkbox(t('consent'),key=f'consent_{kind}')
        submit=st.form_submit_button(t('apply'),type='primary',use_container_width=True)
    if submit:
        errors=[]
        if len(name.strip())<2: errors.append('పూర్తి పేరును నమోదు చేయండి (కనీసం 2 అక్షరాలు).' if st.session_state.lang=='te' else 'Enter a valid full name (at least 2 characters).')
        if not re.fullmatch(r'[6-9]\d{9}',phone.strip()): errors.append('చెల్లని ఫోన్ నంబర్: 6, 7, 8 లేదా 9తో ప్రారంభమయ్యే 10 అంకెల నంబర్ ఇవ్వండి.' if st.session_state.lang=='te' else 'Invalid phone number: enter exactly 10 digits starting with 6, 7, 8 or 9.')
        if len(city.strip())<2: errors.append('సరైన నగరం పేరును నమోదు చేయండి.' if st.session_state.lang=='te' else 'Enter a valid city.')
        if email.strip() and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email.strip()): errors.append('చెల్లని ఇమెయిల్ చిరునామా.' if st.session_state.lang=='te' else 'Invalid email address.')
        if errors:
            for error in errors: st.error(error)
            return
        if not consent: st.warning(t('consent'));return
        number=re.sub(r'\D','',setting(f'MATRIX_{kind.upper()}_WHATSAPP_NUMBER') or setting('MATRIX_WHATSAPP_NUMBER'))
        if not number: st.warning(t('missing'));return
        if len(number)==10: number='91'+number
        if not re.fullmatch(r'91[6-9]\d{9}',number): st.error('Invalid business WhatsApp configuration.');return
        lines=['Matrix Finance loan enquiry',f'Loan: {WORDS["en"][kind]}',f'Name: {name}',f'Phone: +91 {phone}',f'City: {city}',f'State: {state}']
        if email:lines.append(f'Email: {email}')
        if estimate:lines.append(f'Indicative estimate: {currency(estimate["amount"])}')
        link=f'https://wa.me/{number}?text={quote(chr(10).join(lines))}'
        st.info('Message prepared for the relevant loan team. Press Send in WhatsApp to deliver it.')
        st.success(t('submitted'))
        st.link_button('💬 '+t('open_whatsapp'),link,use_container_width=True)

def loan_page(kind):
    top();hero(t(kind),t(kind+'_desc'),kind+'hero')
    if kind=='gold':st.info('💍 '+ ('Gold ornaments are valued according to weight, purity and an assumed pure-metal rate.' if st.session_state.lang=='en' else 'బంగారు ఆభరణాల బరువు, స్వచ్ఛత, ఊహించిన ధర ఆధారంగా అంచనా లెక్కించబడుతుంది.'))
    elif kind=='silver':st.info('🪙 '+('Silver collateral eligibility is subject to business policy and verification.' if st.session_state.lang=='en' else 'వెండి తాకట్టు అర్హత వ్యాపార విధానం మరియు ధృవీకరణపై ఆధారపడుతుంది.'))
    elif kind=='personal':st.info('💳 '+('Compare monthly EMI across loan amounts and tenures.' if st.session_state.lang=='en' else 'రుణ మొత్తం, కాలవ్యవధి ఆధారంగా నెలవారీ EMIని పోల్చండి.'))
    elif kind=='housing':st.info('🏡 '+('Plan long-term repayments for a home purchase.' if st.session_state.lang=='en' else 'ఇంటి కొనుగోలు కోసం దీర్ఘకాలిక EMIలను ప్లాన్ చేసుకోండి.'))
    else:st.info('🏢 '+('Explore indicative borrowing against property value.' if st.session_state.lang=='en' else 'ఆస్తి విలువ ఆధారంగా రుణ అంచనా తెలుసుకోండి.'))
    estimate=calculator(kind);enquiry(kind,estimate);foot()

def contact():
    top();hero(t('contact'),t('contact_desc'))
    st.markdown(f'<div class="section">{t("contact_phone")}</div>',unsafe_allow_html=True)
    number=setting('MATRIX_PUBLIC_PHONE','Not configured')
    st.write(number)
    st.markdown(f'<div class="section">{t("contact_address")}</div>',unsafe_allow_html=True)
    st.write(setting('MATRIX_BRANCH_ADDRESS','Not configured'))
    loan_type = st.selectbox('రుణ రకం' if st.session_state.lang=='te' else 'Loan type', ['gold','silver','personal','housing','mortgage'], format_func=lambda x: t(x))
    enquiry(loan_type,None)
    st.info(t('disclaimer'));foot()

PAGE_OBJECTS={'home':st.Page(home,title='Home',url_path='home',default=True)}
for key in ('gold','silver','personal','housing','mortgage'):
    PAGE_OBJECTS[key]=st.Page(lambda k=key:loan_page(k),title=key.title(),url_path=key)
PAGE_OBJECTS['contact']=st.Page(contact,title='Contact',url_path='contact')
def faq_page():
    top();hero('తరచుగా అడిగే ప్రశ్నలు' if st.session_state.lang=='te' else 'Frequently Asked Questions','మీ ప్రశ్నలకు సమాధానాలు' if st.session_state.lang=='te' else 'Answers to common questions about loan enquiries.');faq_section();foot()
PAGE_OBJECTS['faq']=st.Page(faq_page,title='FAQs',url_path='faq')
pg=st.navigation(list(PAGE_OBJECTS.values()),position='hidden')
pg.run()
